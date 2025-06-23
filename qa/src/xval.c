/*
 * Copyright (c) 1995-2001 Silicon Graphics, Inc.  All Rights Reserved.
 *
 * xval [-D] [-e] [-u] [-v] value-in-hex
 */

#include <stdio.h>
#include <math.h>
#include <pcp/pmapi.h>

static int types[] = {
    PM_TYPE_32, PM_TYPE_U32, PM_TYPE_64, PM_TYPE_U64, PM_TYPE_FLOAT, PM_TYPE_DOUBLE, PM_TYPE_STRING, PM_TYPE_AGGREGATE, PM_TYPE_EVENT, PM_TYPE_HIGHRES_EVENT };
static char *names[] = {
    "long", "ulong", "longlong", "ulonglong", "float", "double", "char *", "pmValueBlock *", "pmEventArray", "pmHighResEventArray" };

/*
 * ap may point into a vbuf[] and so is not necessarily aligned correctly
 */
static void
_y(void *ap, int type)
{
    int			i;
    int			vlen;
    char		*cp;
    pmAtomValue		av;

    memcpy((void *)&av, (void *)ap, sizeof(av));

    switch (type) {
	case PM_TYPE_32:
	    printf("%d", av.l);
	    break;
	case PM_TYPE_U32:
	    printf("%u", av.ul);
	    break;
	case PM_TYPE_64:
	    /* avoid alignment problems */
	    printf("%" FMT_INT64, av.ll);
	    break;
	case PM_TYPE_U64:
	    /* avoid alignment problems */
	    printf("%" FMT_UINT64, av.ull);
	    break;
	case PM_TYPE_FLOAT:
	    printf("%e", (double)av.f);
	    break;
	case PM_TYPE_DOUBLE:
	    printf("%e", av.d);
	    break;
	case PM_TYPE_STRING:
	    if (av.cp == (char *)0)
		printf("(char *)0");
	    else
		printf("\"%s\"", av.cp);
	    break;
	case PM_TYPE_AGGREGATE:
	    vlen = av.vbp->vlen - PM_VAL_HDR_SIZE;
	    printf("[vlen=%d]", vlen);
	    cp = (char *)av.vbp->vbuf;
	    for (i = 0; i < vlen && i < 12; i++) {
		if ((i % 4) == 0)
		    putchar(' ');
		printf("%02x", *cp & 0xff);
		cp++;
	    }
	    if (vlen > 12) printf(" ...");
	    break;
	case PM_TYPE_EVENT: {
	    pmEventArray *eap;
	    /* this seems alignment safe */
	    eap = (pmEventArray *)ap;
		printf("[%d event records]", eap->ea_nrecords);
	    break;
	}
	case PM_TYPE_HIGHRES_EVENT: {
	    pmHighResEventArray *hreap;
	    /* this seems alignment safe */
	    hreap = (pmHighResEventArray *)ap;
		printf("[%d event records]", hreap->ea_nrecords);
	    break;
	}
    }
}

static pmEventArray	ea;
static pmHighResEventArray	hrea;

int
main(int argc, char *argv[])
{
    int		e;
    int		k;
    int		i;
    int		o;
    void	*avp;
    pmValue	pv;
    pmAtomValue	av;
    pmAtomValue	bv;
    pmAtomValue	iv;
    pmAtomValue	*ap;
    pmValueBlock	*vbp;
    __int32_t	*foo;
    int		len;
    int		valfmt;
    int		vflag = 0;	/* set to 1 to show all results */
    int		sgn = 1;	/* -u to force 64 unsigned from command line value */
    __int64_t 	llv;
    char	*fmt_int64x;
    char	*p;

    ea.ea_nrecords = 1;
    ea.ea_record[0].er_nparams = 0;
    vbp = (pmValueBlock *)&ea;
    vbp->vtype = PM_TYPE_EVENT;
    vbp->vlen = sizeof(ea);	/* not quite correct, but close enough */
    hrea.ea_nrecords = 1;
    hrea.ea_record[0].er_nparams = 0;
    vbp = (pmValueBlock *)&hrea;
    vbp->vtype = PM_TYPE_HIGHRES_EVENT;
    vbp->vlen = sizeof(hrea);	/* not quite correct, but close enough */

    len = 7 * sizeof(int);
    vbp = (pmValueBlock *)malloc(sizeof(pmValueBlock) + len);
    if (vbp == NULL) {
	fprintf(stderr, "initial malloc failed!\n");
	exit(1);
    }

    while (argc > 1) {
	argc--;
	argv++;
	if (strcmp(argv[0], "-D") == 0) {
	    pmSetDebug("value");
	    continue;
	}
	if (strcmp(argv[0], "-e") == 0) {
	    goto error_cases;
	}
	if (strcmp(argv[0], "-u") == 0) {
	    sgn = 0;
	    continue;
	}
	if (strcmp(argv[0], "-v") == 0) {
	    vflag = 1;
	    continue;
	}
	/* note value is in hex! */
	fmt_int64x = strdup("%" FMT_INT64);
	for (p = fmt_int64x; *p; p++)
	    ;
	p--;
	if (*p != 'd') {
	    fprintf(stderr, "Botch: expect FMT_INT64 (%s) to end in 'd'\n", FMT_INT64);
	    exit (1);
	}
	*p = 'x';
	sscanf(argv[0], fmt_int64x, &llv);
	if (sgn) {
	    printf("\nValue: %" FMT_INT64, llv);
	    printf(" 0x");
	    printf(fmt_int64x, llv);
	    putchar('\n');
	}
	else {
	    printf("\nValue: %" FMT_UINT64, llv);
	    printf(" 0x");
	    printf(fmt_int64x, llv);
	    putchar('\n');
	}

	for (i = 0; i < sizeof(types)/sizeof(types[0]); i++) {
	    valfmt = PM_VAL_INSITU;
	    ap = (pmAtomValue *)&pv.value.lval;
	    switch (types[i]) {
		case PM_TYPE_32:
		case PM_TYPE_U32:
		    pv.value.lval = llv;
		    break;
		case PM_TYPE_64:
		    valfmt = PM_VAL_SPTR;
		    pv.value.pval = vbp;
		    vbp->vlen = PM_VAL_HDR_SIZE + sizeof(__int64_t);
		    vbp->vtype = PM_TYPE_64;
		    avp = (void *)vbp->vbuf;
		    bv.ll = llv;
		    memcpy(avp, (void *)&bv, sizeof(bv));
		    ap = &bv;
		    break;
		case PM_TYPE_U64:
		    valfmt = PM_VAL_SPTR;
		    pv.value.pval = vbp;
		    vbp->vlen = PM_VAL_HDR_SIZE + sizeof(__uint64_t);
		    vbp->vtype = PM_TYPE_U64;
		    avp = (void *)vbp->vbuf;
		    bv.ll = llv;
		    memcpy(avp, (void *)&bv, sizeof(bv));
		    ap = &bv;
		    break;
		case PM_TYPE_FLOAT:
		    valfmt = PM_VAL_SPTR;
		    pv.value.pval = vbp;
		    vbp->vlen = PM_VAL_HDR_SIZE + sizeof(float);
		    vbp->vtype = PM_TYPE_FLOAT;
		    avp = (void *)vbp->vbuf;
		    if (sgn)
			bv.f = llv;
		    else
			bv.f = (unsigned long long)llv;
		    memcpy(avp, (void *)&bv, sizeof(bv));
		    ap = &bv;
		    break;
		case PM_TYPE_DOUBLE:
		    valfmt = PM_VAL_SPTR;
		    pv.value.pval = vbp;
		    vbp->vlen = PM_VAL_HDR_SIZE + sizeof(double);
		    vbp->vtype = PM_TYPE_DOUBLE;
		    avp = (void *)vbp->vbuf;
		    if (sgn)
			bv.d = llv;
		    else
			bv.d = (unsigned long long)llv;
		    memcpy(avp, (void *)&bv, sizeof(bv));
		    ap = &bv;
		    break;
		case PM_TYPE_STRING:
		    valfmt = PM_VAL_SPTR;
		    pv.value.pval = vbp;
		    pmsprintf(vbp->vbuf, len, "%" FMT_INT64, llv);
		    vbp->vlen = PM_VAL_HDR_SIZE + strlen(vbp->vbuf) + 1;
		    vbp->vtype = PM_TYPE_STRING;
		    ap = &bv;
		    bv.cp = (char *)vbp->vbuf;
		    break;
		case PM_TYPE_AGGREGATE:
		    valfmt = PM_VAL_SPTR;
		    pv.value.pval = vbp;
		    vbp->vlen = PM_VAL_HDR_SIZE + 3 * sizeof(foo[0]);
		    vbp->vtype = PM_TYPE_AGGREGATE;
		    foo = (__int32_t *)vbp->vbuf;
		    foo[0] = foo[1] = foo[2] = llv;
		    foo[0]--;
		    foo[2]++;
		    /* remove endian diff in value dump output */
		    foo[0] = htonl(foo[0]);
		    foo[1] = htonl(foo[1]);
		    foo[2] = htonl(foo[2]);
		    ap = &bv;
		    bv.vbp = vbp;
		    break;
		case PM_TYPE_EVENT:
		    valfmt = PM_VAL_DPTR;
		    ap = (void *)&ea;
		    break;
		case PM_TYPE_HIGHRES_EVENT:
		    valfmt = PM_VAL_DPTR;
		    ap = (void *)&hrea;
		    break;
	    }
	    for (o = 0; o < sizeof(types)/sizeof(types[0]); o++) {
		if ((e = pmExtractValue(valfmt, &pv, types[i], &av, types[o])) < 0) {
		    if (vflag == 0) {
			/* silently ignore the expected failures */
			if (types[i] != types[o] &&
			    (types[i] == PM_TYPE_STRING || types[o] == PM_TYPE_STRING ||
			     types[i] == PM_TYPE_AGGREGATE || types[o] == PM_TYPE_AGGREGATE))
			    continue;
			 if (types[i] == PM_TYPE_EVENT || types[i] == PM_TYPE_HIGHRES_EVENT ||
			     types[o] == PM_TYPE_EVENT || types[o] == PM_TYPE_HIGHRES_EVENT)
			    continue;
		    }
		    printf("(%s) ", names[i]);
		    _y(ap, types[i]);
		    printf(" => (%s) ", names[o]);
		    printf(": %s\n", pmErrStr(e));
		}
		else {
		    int		match;
		    /* avoid ap-> alignment issues */
		    memcpy((void *)&iv, (void *)ap, sizeof(iv));
		    switch (types[o]) {
			case PM_TYPE_32:
			    if (types[i] == PM_TYPE_32)
				match = (pv.value.lval == av.l);
			    else if (types[i] == PM_TYPE_U32)
				match = ((unsigned)pv.value.lval == av.l);
			    else if (types[i] == PM_TYPE_FLOAT)
				match = (fabs((iv.f - av.l)/iv.f) < 0.00001);
			    else
				match = (llv == av.l);
			    break;
			case PM_TYPE_U32:
			    if (types[i] == PM_TYPE_32)
				match = (pv.value.lval == av.ul);
			    else if (types[i] == PM_TYPE_U32)
				match = ((unsigned)pv.value.lval == av.ul);
			    else if (types[i] == PM_TYPE_FLOAT)
				match = (fabs((iv.f - av.ul)/iv.f) < 0.00001);
			    else
				match = (llv == av.ul);
			    break;
			case PM_TYPE_64:
			    if (types[i] == PM_TYPE_32)
				match = (pv.value.lval == av.ll);
			    else if (types[i] == PM_TYPE_U32)
				match = ((unsigned)pv.value.lval == av.ll);
			    else if (types[i] == PM_TYPE_FLOAT)
				match = (fabs((iv.f - av.ll)/iv.f) < 0.00001);
			    else if (types[i] == PM_TYPE_DOUBLE)
				match = (fabs((iv.d - av.ll)/iv.d) < 0.00001);
			    else
				match = (llv == av.ll);
			    break;
			case PM_TYPE_U64:
			    if (types[i] == PM_TYPE_32)
				match = (pv.value.lval == av.ull);
			    else if (types[i] == PM_TYPE_U32)
				match = ((unsigned)pv.value.lval == av.ull);
			    else if (types[i] == PM_TYPE_FLOAT)
				match = (fabs((iv.f - av.ull)/iv.f) < 0.00001);
			    else if (types[i] == PM_TYPE_DOUBLE)
				match = (fabs((iv.d - av.ull)/iv.d) < 0.00001);
			    else
				match = (llv == av.ull);
			    break;
			case PM_TYPE_FLOAT:
			    if (types[i] == PM_TYPE_32)
				match = (fabs((pv.value.lval - av.f)/pv.value.lval) < 0.00001);
			    else if (types[i] == PM_TYPE_U32)
				match = (fabs(((unsigned)pv.value.lval - av.f)/(unsigned)pv.value.lval) < 0.00001);
			    else if (types[i] == PM_TYPE_64)
				match = (fabs((llv - av.f)/llv) < 0.00001);
			    else if (types[i] == PM_TYPE_U64)
				match = (fabs(((unsigned long long)llv - av.f)/(unsigned long long)llv) < 0.00001);
			    else if (types[i] == PM_TYPE_DOUBLE)
				match = (fabs((iv.d - av.f)/iv.d) < 0.00001);
			    else
				match = (iv.f == av.f);
			    break;
			case PM_TYPE_DOUBLE:
			    if (types[i] == PM_TYPE_32)
				match = (fabs((pv.value.lval - av.d)/pv.value.lval) < 0.00001);
			    else if (types[i] == PM_TYPE_U32)
				match = (fabs(((unsigned)pv.value.lval - av.d)/(unsigned)pv.value.lval) < 0.00001);
			    else if (types[i] == PM_TYPE_64)
				match = (fabs((llv - av.d)/llv) < 0.00001);
			    else if (types[i] == PM_TYPE_U64)
				match = (fabs(((unsigned long long)llv - av.d)/(unsigned long long)llv) < 0.00001);
			    else if (types[i] == PM_TYPE_FLOAT)
				match = (fabs((iv.f - av.d)/iv.f) < 0.00001);
			    else
				match = (iv.d == av.d);
			    break;
			case PM_TYPE_STRING:
			    if (types[i] == PM_TYPE_STRING)
				match = (strcmp(bv.cp, av.cp) == 0);
			    else {
				if (types[i] == PM_TYPE_32)
				    match = strtol(av.cp, NULL, 10) == iv.l;
				else if (types[i] == PM_TYPE_U32)
				    match = strtoul(av.cp, NULL, 10) == iv.ul;
				else if (types[i] == PM_TYPE_64)
				    match = strtoll(av.cp, NULL, 10) == iv.ll;
				else if (types[i] == PM_TYPE_U64)
				    match = strtoull(av.cp, NULL, 10) == iv.ull;
				else if (types[i] == PM_TYPE_FLOAT)
				    match = (float)atof(av.cp) == iv.f;
				else if (types[i] == PM_TYPE_DOUBLE)
				    match = atof(av.cp) == iv.d;
				else
				    match = 0;
			    }
			    break;
			case PM_TYPE_AGGREGATE:
			    match = 0;
			    for (k = 0; match == 0 && k < vbp->vlen - PM_VAL_HDR_SIZE; k++)
				match = (bv.cp[k] == av.cp[k]);
			    break;
			case PM_TYPE_EVENT:
			case PM_TYPE_HIGHRES_EVENT:
			default:
			    /* should never get here */
			    match = 0;
			    break;
		    }
		    if (match == 0 || vflag) {
			printf("(%s) ", names[i]);
			_y(ap, types[i]);
			printf(" => (%s) ", names[o]);
			_y(&av, types[o]);
			if (match == 0)
			    printf(" : value mismatch");
			putchar('\n');
		    }
		    if (types[o] == PM_TYPE_STRING)
			free(av.cp);
		    else if (types[o] == PM_TYPE_AGGREGATE)
			free(av.vbp);
		}
	    }
	}
    }

    exit(0);

error_cases:
    /*
     * a series of error and odd cases driven by QA coverage analysis
     */
    avp = (void *)&pv.value.lval;
    bv.f = 123.456;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.3f -> 32: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_32)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%d\n", av.l);

    bv.f = (float)0xf7777777;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.3f -> 32: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_32)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%d\n", av.l);

    bv.f = 123.456;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.3f -> U32: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_U32)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%u\n", av.ul);

    bv.f = (float)((unsigned)0xffffffff);
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.3f -> U32: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_U32)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%u\n", av.ul);

    bv.f = -123.456;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.3f -> U32: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_U32)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%u\n", av.ul);

    bv.f = 123.456;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.3f -> 64: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_64)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%" FMT_INT64 "\n", av.ll);

    bv.f = (float)0x7fffffffffffffffLL;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %22.1f -> 64: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_64)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%" FMT_INT64 "\n", av.ll);

    bv.f = 123.456;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.3f -> U64: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_U64)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%" FMT_UINT64 "\n", av.ull);

    bv.f = (float)((unsigned long long)0xffffffffffffffffLL);
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %22.1f -> U64: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_U64)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%" FMT_UINT64 "\n", av.ull);

    bv.f = -123.456;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.3f -> U64: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_U64)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%" FMT_UINT64 "\n", av.ull);

    bv.f = 123.45678;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.5f -> DOUBLE: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_DOUBLE)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%15.5f\n", av.d);

    bv.f = 123.45678;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("old FLOAT: %15.5f -> STRING: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_INSITU, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_STRING)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%s\n", av.cp);

    pv.value.pval = vbp;
    vbp->vlen = PM_VAL_HDR_SIZE + sizeof(bv.ll);
    vbp->vtype = (PM_TYPE_NOSUPPORT & 0xff);
    avp = (void *)vbp->vbuf;
    bv.ll = 12345;
    memcpy(avp, (void *)&bv.ll, sizeof(bv.ll));
    printf("bad 64: %" FMT_INT64 " -> 64: ", bv.ll);
    if ((e = pmExtractValue(PM_VAL_SPTR, &pv, PM_TYPE_64, &av, PM_TYPE_64)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%" FMT_INT64 "\n", av.ll);

    vbp->vlen = PM_VAL_HDR_SIZE + sizeof(bv.ull);
    memcpy(avp, (void *)&bv.ull, sizeof(bv.ull));
    printf("bad U64: %" FMT_UINT64 " -> U64: ", bv.ull);
    if ((e = pmExtractValue(PM_VAL_SPTR, &pv, PM_TYPE_U64, &av, PM_TYPE_U64)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%" FMT_UINT64 "\n", av.ull);

    vbp->vlen = PM_VAL_HDR_SIZE + sizeof(bv.f);
    bv.f = 123.456;
    memcpy(avp, (void *)&bv.f, sizeof(bv.f));
    printf("bad FLOAT: %15.3f -> FLOAT: ", bv.f);
    if ((e = pmExtractValue(PM_VAL_SPTR, &pv, PM_TYPE_FLOAT, &av, PM_TYPE_FLOAT)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%15.3f\n", av.f);

    vbp->vlen = PM_VAL_HDR_SIZE + sizeof(bv.d);
    bv.d = 123.456;
    memcpy(avp, (void *)&bv.d, sizeof(bv.d));
    printf("bad DOUBLE: %15.3f -> DOUBLE: ", bv.d);
    if ((e = pmExtractValue(PM_VAL_SPTR, &pv, PM_TYPE_DOUBLE, &av, PM_TYPE_DOUBLE)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%15.3f\n", av.d);

    bv.cp = "not me";
    memcpy(avp, (void *)&bv, sizeof(bv));
    vbp->vlen = PM_VAL_HDR_SIZE + strlen(bv.cp);
    printf("bad STRING: %s -> STRING: ", bv.cp);
    if ((e = pmExtractValue(PM_VAL_SPTR, &pv, PM_TYPE_STRING, &av, PM_TYPE_STRING)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("%s\n", av.cp);

    vbp->vlen = PM_VAL_HDR_SIZE;
    printf("bad AGGREGATE: len=%d -> AGGREGATE: ", vbp->vlen - PM_VAL_HDR_SIZE);
    if ((e = pmExtractValue(PM_VAL_SPTR, &pv, PM_TYPE_AGGREGATE, &av, PM_TYPE_AGGREGATE)) < 0)
	printf("%s\n", pmErrStr(e));
    else
	printf("len=%d\n", av.vbp->vlen);

    exit(0);
}

