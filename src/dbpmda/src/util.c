/*
 * Copyright (c) 2013,2017,2022 Red Hat.
 * Copyright (c) 1995-2001 Silicon Graphics, Inc.  All Rights Reserved.
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * for more details.
 */

#include "./dbpmda.h"
#include "./lex.h"
#include "./gram.h"
#include <pcp/deprecated.h>
#ifdef HAVE_STRINGS_H
#include <strings.h>
#endif

/*
 * This works because ...
 * we get _another_ copy of debug_map[] from pmdbg.h, but this is a
 * static array, and the options field points back into the real
 * pmDebugOptions struct in libpcp, so we can see the internal state
 * of the debugging options.
 */
#include "../../libpcp/src/pmdbg.h"

extern pmdaInterface	dispatch;
extern int		fromPMDA;
extern int		toPMDA;

pmProfile		*profile;
int			profile_changed;
int			timer;
int			get_desc;
int			get_iname;

static pmID		*pmidlist;
static int		numpmid;
static __pmContext	*ctxp;

static char		**argv;
static int		argc;

void
reset_profile(void)
{
    if (pmDebugOptions.profile && ctxp->c_instprof != NULL) {
	fprintf(stderr, "Before reset_profile ...\n");
	__pmDumpProfile(stderr, PM_INDOM_NULL, ctxp->c_instprof);
    }
    if (ctxp->c_instprof != NULL)
	__pmFreeProfile(ctxp->c_instprof);
    if ((profile = (pmProfile *)malloc(sizeof(pmProfile))) == NULL) {
	pmNoMem("reset_profile", sizeof(pmProfile), PM_FATAL_ERR);
	exit(1);
    }
    ctxp->c_instprof = profile;
    memset(profile, 0, sizeof(pmProfile));
    profile->state = PM_PROFILE_INCLUDE;        /* default global state */
    profile_changed = 1;
    if (pmDebugOptions.profile) {
	fprintf(stderr, "After reset_profile ...\n");
	__pmDumpProfile(stderr, PM_INDOM_NULL, ctxp->c_instprof);
    }
}

void
setup_context(void)
{
    int sts;
#ifdef PM_MULTI_THREAD
    pthread_mutex_t	save_c_lock;
#endif

    /* 
     * we don't want or need any PMDAs to be loaded for this one
     * PM_CONTEXT_LOCAL context
     */
    pmSpecLocalPMDA("clear");

    if ((sts = pmNewContext(PM_CONTEXT_LOCAL, NULL)) < 0) {
	fprintf(stderr, "setup_context: creation failed: %s\n", pmErrStr(sts));
	exit(1);
    }

    ctxp = __pmHandleToPtr(sts);
    if (ctxp == NULL) {
	fprintf(stderr, "botch: setup_context: __pmHandleToPtr(%d) returns NULL!\n", sts);
	exit(1);
    }
    /*
     * Note: This application is single threaded, and once we have ctxp
     *	     the associated __pmContext will not move and will only be
     *	     accessed or modified synchronously either here or in libpcp.
     *	     We unlock the context so that it can be locked as required
     *	     within libpcp.
     */
    PM_UNLOCK(ctxp->c_lock);

#ifdef PM_MULTI_THREAD
    /* need to be careful about the initialized lock */
    save_c_lock = ctxp->c_lock;
#endif
    if (ctxp->c_instprof != NULL)
	__pmFreeProfile(ctxp->c_instprof);
    __pmFreeDerived(ctxp);
    memset(ctxp, 0, sizeof(__pmContext));
#ifdef PM_MULTI_THREAD
    ctxp->c_lock = save_c_lock;
#endif
    ctxp->c_type = PM_CONTEXT_HOST;
    reset_profile();
}

char *
strcons(char *s1, char *s2)
{
    int		i;
    char	*buf;

    i = (int)strlen(s1) + (int)strlen(s2) + 1;

    buf = (char *)malloc(i);
    if (buf == NULL) {
	fprintf(stderr, "strcons: malloc failed: %s\n", osstrerror());
	exit(1);
    }

    strcpy(buf, s1);
    strcat(buf, s2);

    return buf;
}

char *
strnum(int n)
{
    char	*buf;

#define MYBUFSZ 13

    buf = (char *)malloc(MYBUFSZ);
    if (buf == NULL) {
	fprintf(stderr, "strnum: malloc failed: %s\n", osstrerror());
	exit(1);
    }
    pmsprintf(buf, MYBUFSZ, "%d", n);
    return buf;
}

char *
strcluster(pmID pmid)
{
    static char buffer[32];
    char *p;

    pmIDStr_r(pmid, buffer, sizeof(buffer));
    p = rindex(buffer, '.');
    *p = '\0';
    return buffer;
}

void
initmetriclist(void)
{
    param.numpmid = 0;
    param.pmidlist = NULL;
}

void
addmetriclist(pmID pmid)
{
    param.numpmid++;

    if (param.numpmid >= numpmid) {
        numpmid = param.numpmid;
	pmidlist = (pmID *)realloc(pmidlist, numpmid * sizeof(pmidlist[0]));
	if (pmidlist == NULL) {
	    fprintf(stderr, "addmetriclist: realloc failed: %s\n", osstrerror());
	    exit(1);
	}
    }

    pmidlist[param.numpmid-1] = pmid;
    param.pmidlist = pmidlist;
}

void
initarglist(void)
{
    int		i;

    for (i = 0; i < param.argc; i++)
	if (param.argv[i] != NULL)
	    free(param.argv[i]);
    param.argc = 0;
    param.argv = NULL;
    addarglist("");
}

void
addarglist(char *arg)
{
    param.argc++;

    if (param.argc >= argc) {
        argc = param.argc;
	argv = (char **)realloc(argv, argc * sizeof(char *));
	if (argv == NULL) {
	    fprintf(stderr, "addarglist: realloc failed: %s\n", osstrerror());
	    exit(1);
	}
    }

    if (arg != NULL)
	argv[param.argc-1] = strdup(arg);
    else
	argv[param.argc-1] = arg;
    param.argv = argv;
}

#define MYCMDSZ 200

void
watch(char *fname)
{
    char	cmd[MYCMDSZ];

    pmsprintf(cmd, MYCMDSZ, "xterm -hold -title \"dbpmda watch %s\" -geom 80x16 -bg dodgerblue4 -e tail -f %s &",
	fname, fname);
    
    if (system(cmd) != 0)
	fprintf(stderr, "watch cmd: %s failed: %s\n", cmd, pmErrStr(-oserror()));
}

void
printindom(FILE *f, pmInResult *irp)
{
    int		i;

    if (irp->numinst == 0) {
	fprintf(f, "Instance domain is empty\n");
	return;
    }

    for (i = 0; i < irp->numinst; i++) {
	fprintf(f, "[%3d]", i);
	if (irp->instlist != NULL)
	    fprintf(f, " inst: %d", irp->instlist[i]);
	if (irp->namelist != NULL)
	    fprintf(f, " name: \"%s\"", irp->namelist[i]);
	fputc('\n', f);
    }
}

void
dohelp(int command, int full)
{
    if (command < 0) {
	puts("help [ command ]\n");
	dohelp(ATTR, HELP_USAGE);
	dohelp(PMNS_CHILDREN, HELP_USAGE);
	dohelp(CLOSE, HELP_USAGE);
	dohelp(DBG, HELP_USAGE);
	dohelp(DESC, HELP_USAGE);
	dohelp(FETCH, HELP_USAGE);
	dohelp(GETDESC, HELP_USAGE);
	dohelp(GETINAME, HELP_USAGE);
	dohelp(INSTANCE, HELP_USAGE);
	dohelp(LABEL, HELP_USAGE);
	dohelp(PMNS_NAME, HELP_USAGE);
	dohelp(NAMESPACE, HELP_USAGE);
	dohelp(OPEN, HELP_USAGE);
	dohelp(PMNS_PMID, HELP_USAGE);
	dohelp(PROFILE, HELP_USAGE);
	dohelp(QUIT, HELP_USAGE);
	dohelp(STATUS, HELP_USAGE);
	dohelp(STORE, HELP_USAGE);
	dohelp(INFO, HELP_USAGE);
	dohelp(TIMER, HELP_USAGE);
	dohelp(PMNS_TRAVERSE, HELP_USAGE);
	dohelp(WAIT, HELP_USAGE);
	dohelp(WATCH, HELP_USAGE);
	putchar('\n');
    }
    else {
	if (full == HELP_FULL)
	    putchar('\n');

	switch (command) {
	case ATTR:
	    puts("attr name [value]");
	    puts("attr attr# [value]");
	    break;
	case CLOSE:
	    puts("close");
	    break;
	case DBG:
	    puts("debug all | none");
	    puts("debug [-]flag [ [-]flag ... ] (- prefix to clear)");
	    break;
	case DESC:
	    puts("desc metric");
	    break;
	case FETCH:
	    puts("fetch metric [ metric ... ]");
	    break;
	case GETDESC:
	    puts("getdesc on | off");
	    break;
	case GETINAME:
	    puts("getiname on | off");
	    break;
	case INFO:
	    puts("text metric");
	    puts("text indom indom#");
	    break;
	case INSTANCE:
	    puts("instance indom# [ number | name | \"name\" ]");
	    break;
	case LABEL:
	    puts("label context");
	    puts("label domain");
	    puts("label indom indom#");
	    puts("label cluster cluster#");
	    puts("label item metric");
	    puts("label instances indom#");
	    break;
	case NAMESPACE:
	    puts("namespace fname");
	    break;
	case OPEN:
	    puts("open dso dsoname init_routine [ domain# ]");
	    puts("open pipe execname [ arg ... ]");
	    puts("open socket unix sockname");
	    puts("open socket inet port#|service");
	    puts("open socket ipv6 port#|service");
	    break;
	case PMNS_CHILDREN:
	    puts("children metric-name");
	    break;
	case PMNS_NAME:
	    puts("name pmid#");
	    break;
	case PMNS_PMID:
	    puts("pmid metric-name");
	    break;
	case PMNS_TRAVERSE:
	    puts("traverse metric-name");
	    break;
	case PROFILE:
	    puts("profile indom# [ all | none ]");
	    puts("profile indom# [ add | delete ] number");
	    break;
	case QUIT:
	    puts("quit");
	    break;
	case STATUS:
	    puts("status");
	    break;
	case STORE:
	    puts("store metric \"value\"");
	    break;
	case WATCH:
	    puts("watch logfilename");
	    break;
	case TIMER:
	    puts("timer on | off");
	    break;
	case WAIT:
	    puts("wait seconds");
	    break;
	default:
	    fprintf(stderr, "Help for that command (%d) not supported!\n", command);
	}

	if (full == HELP_FULL) {
	    putchar('\n');
	    switch (command) {
	    case ATTR:
		puts(
"Set a security attribute. These set aspects of per-user authentication,\n"
"allowing a PMDA to provide different metric views for different users.\n");
		break;
	    case CLOSE:
		puts(
"Close the pipe to a daemon PMDA or dlclose(3) a DSO PMDA. dbpmda does not\n"
"exit, allowing another PMDA to be opened.\n");
		break;
	    case DBG:
		puts(
"Specify which debugging options should be active (see pmdbg(1)).  Options\n"
"may be specified by name (or number for the old bit-field options), with\n"
"multiple options separated by white space.  All options may be selected or\n"
"deselected if 'all' or 'none' is specified.  The current setting is\n"
"displayed by the status command.\n\n");
		break;
	    case DESC:
		puts(
"Print out the meta data description for the 'metric'.  The metric may be\n"
"specified by name, or as a PMID of the form N, N.N or N.N.N.\n");
		break;
	    case FETCH:
		puts(
"Fetch metrics from the PMDA.  The metrics may be specified as a list of\n"
"metric names, or PMIDs of the form N, N.N or N.N.N.\n");
		break;
	    case GETDESC:
		puts(
"Before doing a fetch, get the descriptor so that the result of a fetch\n"
"can be printed out correctly.\n");
		break;
	    case GETINAME:
		puts(
"After a fetch if the metric has an associated instance domain then lookup\n"
"the external names of any instances returned, rather than reporting the\n"
"instance name as ???.\n");
		break;
	    case INFO:
		puts(
"Retrieve the help text for the 'metric' or 'indom' from the PMDA.  The one\n"
"line message is shown between '[' and ']' with the long message on the next\n"
"line.  To get the help text for an instance domain requires the word\n"
"``indom'' before the indom number\n");
		break;
	    case INSTANCE:
		puts(
"List the instances in 'indom'.  The list may be restricted to a specific\n"
"instance 'name' or 'number'.\n");
		break;
	    case NAMESPACE:
		puts(
"Unload the current Name Space and load up the given Name Space.\n"
"If unsuccessful then will try to reload the previous Name Space.\n");
		break;
	    case OPEN:
		puts(
"Open a PMDA as either a DSO, via a network socket (unix/inet/ipv6), or as a\n"
"daemon (connected with a pipe).  The 'dsoname' and 'execname' fields are\n"
"the path to the PMDA shared object file or executable.  The first socket PMDA\n"
"field is the type - either unix (if supported), inet or ipv6.  The 'sockname'\n"
"argument for unix sockets is a path of a named pipe where a PMDA is listening\n"
"for connections.  The 'port' argument is a port number, 'serv' a service name\n"
"typically defined in /etc/services (resolved to a port via getservent(3)).\n"
"The arguments to this command are similar to a line in the pmcd.conf file.\n");
		break;
	    case PMNS_CHILDREN:
	        puts(
"Fetch and print the next name component of the direct decendents of\n"
"metric-name in the PMNS, reporting for each if it is a leaf node or a\n"
"non-leaf node.\n"
"Most useful for PMDAs that support dynamic metrics in the PMNS.\n");
		break;
	    case PMNS_NAME:
		puts(
"Print the name of the metric with PMID pmid#.  The pmid# syntax follows\n"
"the source PMNS syntax, namely 3 numbers separated by '.' to encode\n"
"the domain, cluster and item components of the PMID, e.g.\n"
"    name 29.0.1004\n"
"Most useful for PMDAs that support dynamic metrics in the PMNS.\n");
		break;
	    case PMNS_PMID:
		puts(
"Print the PMID for the named metric\n"
"Most useful for PMDAs that support dynamic metrics in the PMNS.\n");
		break;
	    case PMNS_TRAVERSE:
		puts(
"Fetch and print all of the decendent metric names below metric-name\n"
"in the PMNS.\n"
"Most useful for PMDAs that support dynamic metrics in the PMNS.\n");
		break;
	    case PROFILE:
		puts(
"For the instance domain specified, the profile may be changed to include\n"
"'all' instances, no instances, add an instance or delete an instance.\n");
		break;
	    case QUIT:
		puts("Exit dbpmda.  This also closes any open PMDAs.\n");
		break;
	    case STATUS:
		puts(
"Display the state of dbpmda, including which PMDA is connected, which\n"
"debug options are set, and the current profile.\n");
		break;
	    case STORE:
		puts(
"Store the value (int, real or string) into the 'metric'.  The metric may be\n"
"specified by name or as a PMID with the format N, N.N, N.N.N.  The value to\n"
"be stored must be enclosed in quotes.  Unlike the other commands, a store\n"
"must request a metric description and fetch the metric to determine how to\n"
"interpret the value, and to allocate the PDU for transmitting the value,\n"
"respectively.  The current profile will be used.\n");
		break;
	    case TIMER:
		puts(
"Report the response time of the PMDA when sending and receiving PDUs.\n");
		break;
	    case WATCH:
		puts(
"An xterm window is opened which tails the specified log file.  This window\n"
"must be closed by the user when no longer required.\n");
		break;
	    case WAIT:
		puts("Sleep for this number of seconds\n");
		break;
	    }
	}
    }
}

void
dostatus(void)
{
    int		i = 0;
    int		n;

    putchar('\n');
    printf("Namespace:              ");
    if (cmd_namespace != NULL)
        printf("%s\n", cmd_namespace);
    else {
        if (pmnsfile == NULL)
            printf("(default)\n");
	else
            printf("%s\n", pmnsfile);
    }

    if (myPmdaName == NULL || connmode == NO_CONN)
	printf("PMDA:                   none\n");
    else {
	printf("PMDA:                   %s\n", myPmdaName);
	printf("Connection:             ");
	switch (connmode) {
	case CONN_DSO:
	    printf("dso\n");
	    printf("DSO Interface Version:  %d\n", dispatch.comm.pmda_interface);
	    printf("PMDA PMAPI Version:     %d\n", dispatch.comm.pmapi_version);
	    break;
	case CONN_DAEMON:
	    printf("daemon (pid: %" FMT_PID ")\n", pid);
	    printf("PMDA PMAPI Version:     ");
	    i = __pmVersionIPC(fromPMDA);
	    if (i == UNKNOWN_VERSION)
		printf("unknown!\n");
	    else
		printf("%d\n", i);
	    break;
	default:
	    printf("unknown!\n");
	    break;
	}
    }

    printf("Debug options:          ");
    n = 0;
    for (i = 0; i < num_debug; i++) {
	if (*(debug_map[i].options))
	    n++;
    }
    if (n == num_debug)
	printf("(all)");
    else if (n == 0)
	printf("(none)");
    else {
	n = 0;
	for (i = 0; i < num_debug; i++) {
	    if (*(debug_map[i].options)) {
		if (n == 0)
		    n = 1;
		else
		    putchar(' ');
		printf("%s", debug_map[i].name);
	    }
	}
    }
    putchar('\n');

    printf("Timer:                  ");
    if (timer == 0)
	printf("off\n");
    else
	printf("on\n");

    printf("Getdesc:                ");
    if (get_desc == 0)
	printf("off\n");
    else
	printf("on\n");

    printf("Getiname:               ");
    if (get_iname == 0)
	printf("off\n");
    else
	printf("on\n");

    putchar('\n');
    __pmDumpProfile(stdout, PM_INDOM_NULL, profile);
    putchar('\n');
}


/*
 * Modified versions of __pmPrintResult that use a descriptor list
 * instead of calling pmLookupDesc.
 * Notes:
 *   - desc_list should not be NULL
 */

static void
_dbPrintValueset(FILE *f, int npmid, pmValueSet **vset, pmDesc *desc_list)
{
    int		i;
    int		j;
    int		n;
    char	**names;

    fprintf(f, " numpmid: %d\n", npmid);
    for (i = 0; i < npmid; i++) {
	pmValueSet	*vsp = vset[i];
	names = NULL; /* silence coverity */
	n = pmNameAll(vsp->pmid, &names);
	if (n < 0)
	    fprintf(f, "  %s (%s):", pmIDStr(vsp->pmid), "<noname>");
	else {
	    fprintf(f, "  %s (", pmIDStr(vsp->pmid));
	    __pmPrintMetricNames(f, n, names, " or ");
	    fprintf(f, "):");
	    free(names);
	}
	if (vsp->numval == 0) {
	    fprintf(f, " No values returned!\n");
	    continue;
	}
	else if (vsp->numval < 0) {
	    fprintf(f, " %s\n", pmErrStr(vsp->numval));
	    continue;
	}
	fprintf(f, " numval: %d", vsp->numval);
	fprintf(f, " valfmt: %d vlist[]:\n", vsp->valfmt);
	for (j = 0; j < vsp->numval; j++) {
	    pmValue	*vp = &vsp->vlist[j];
	    if (vsp->numval > 1 || desc_list[i].indom != PM_INDOM_NULL) {
		fprintf(f, "    inst [%d", vp->inst);
		if (get_iname) {
		    char	*iname;
		    if (connmode == CONN_DSO)
			iname = dodso_iname(desc_list[i].indom, vp->inst);
		    else
			/* safe to assume daemon as we must have an open PMDA */
			iname = dopmda_iname(desc_list[i].indom, vp->inst);
		    if (iname != NULL) {
			fprintf(f, " or \"%s\"]", iname);
			free(iname);
		    }
		    else
			fprintf(f, " or ???]");
		}
		else
		    fprintf(f, " or ???]");
		fputc(' ', f);
	    }
	    else
		fprintf(f, "   ");
	    fprintf(f, "value ");
	    pmPrintValue(f, vsp->valfmt, desc_list[i].type, vp, 1);
	    fputc('\n', f);
	}
    }
}

void
_dbDumpResult(FILE *f, pmResult_v2 *resp, pmDesc *desc_list)
{
    fprintf(f, "pmResult dump from " PRINTF_P_PFX "%p timestamp: %lld.%06d ",
        resp, (long long)resp->timestamp.tv_sec, (int)resp->timestamp.tv_usec);
    pmtimevalPrint(f, &resp->timestamp);
    _dbPrintValueset(f, resp->numpmid, resp->vset, desc_list);
}

void
_dbPrintResult(FILE *f, __pmResult *resp, pmDesc *desc_list)
{
    fprintf(f, "__pmResult dump from " PRINTF_P_PFX "%p timestamp: %lld.%09d ",
        resp, (long long)resp->timestamp.sec, (int)resp->timestamp.nsec);
    __pmPrintTimestamp(f, &resp->timestamp);
    _dbPrintValueset(f, resp->numpmid, resp->vset, desc_list);
}

static void	**gc;		/* for Garbage Collection (GC), see below */
static int	gc_len;		/* length of gc[] */
static int	gc_have;	/* elements of gc[] in use */

/*
 * accumulate garbage
 */
void
gc_add(void *p)
{
    gc_have++;
    if (gc_have >= gc_len) {
	/* need more gc space, if this fails ignore GC */
	void	**gc_tmp;
	int	need;
	if (gc_len == 0)
	    need = 4;		/* start with 4 slots */
	else
	    need = 2 * gc_len;	/* then doubling */
	if ((gc_tmp = (void **)realloc(gc, need * sizeof(void *))) != NULL) {
	    gc = gc_tmp;
	    gc_len = need;
	}
	else {
	    /*
	     * if realloc() fails, just forget about this one
	     * or the previous last one
	     */
	    gc_have--;
	}
    }
    if (gc_have < gc_len)
	gc[gc_have - 1] = p;
}

/*
 * free up all accumulated garbage
 */
void
gc_free(void)
{
    int		j;
    if (gc_have > 0) {
	for (j = 0; j < gc_have; j++) {
	    free(gc[j]);
	}
	gc_have = 0;
    }
}
