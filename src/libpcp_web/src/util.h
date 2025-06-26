/*
 * Copyright (c) 2017-2019 Red Hat.
 * 
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published
 * by the Free Software Foundation; either version 2.1 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
 * License for more details.
 */
#ifndef SERIES_UTIL_H
#define SERIES_UTIL_H

#include "sds.h"
#include "dict.h"
#include "load.h"

extern dictType intKeyDictCallBacks;	/* integer key -> (void *) value */
extern dictType sdsKeyDictCallBacks;	/* sds string -> (void *) value */
extern dictType sdsDictCallBacks;	/* sds key -> sds string value */
extern dictType sdsOwnDictCallBacks;	/* owned sds key -> sds string value */

extern const char *timespec_str(struct timespec *, char *, int);
extern const char *timespec_stream_str(struct timespec *, char *, int);
extern const char *timestamp_str(__pmTimestamp *, char *, int);

extern int context_labels(int, pmLabelSet **);
extern int metric_labelsets(struct metric *,
		char *, int,
		int (*filter)(const pmLabel *, const char *, void *),
		void *type);
extern int instance_labelsets(struct indom *, struct instance *,
		char *, int,
		int (*filter)(const pmLabel *, const char *, void *),
		void *type);

extern pmLabelSet *pmwebapi_labelsetdup(pmLabelSet *);

extern const char *pmwebapi_indom_str(struct metric *, char *, int);
extern const char *pmwebapi_pmid_str(struct metric *, char *, int);
extern const char *pmwebapi_semantics_str(struct metric *, char *, int);
extern const char *pmwebapi_type_str(struct metric *, char *, int);
extern const char *pmwebapi_units_str(struct metric *, char *, int);

extern int pmwebapi_context_hash(struct context *);
extern void pmwebapi_metric_hash(struct metric *);
extern void pmwebapi_instance_hash(struct indom *, struct instance *);

extern sds pmwebapi_new_context(struct context *);
extern void pmwebapi_locate_context(struct context *);
extern void pmwebapi_setup_context(struct context *);
extern void pmwebapi_release_context(struct context *);
extern void pmwebapi_free_context(struct context *);
extern int pmwebapi_source_meta(struct context *, char *, int);
extern int pmwebapi_source_hash(unsigned char *, const char *, int);
extern int pmwebapi_string_hash(unsigned char *, const char *, int);
extern int pmwebapi_search_hash(unsigned char *, const char *, int);
extern sds pmwebapi_hash_sds(sds, const unsigned char *);
extern char *pmwebapi_hash_str(const unsigned char *, char *, int);

extern struct domain *pmwebapi_new_domain(struct context *, unsigned int);
extern struct domain *pmwebapi_add_domain(struct context *, unsigned int);
extern void pmwebapi_add_domain_labels(struct context *, struct domain *);
extern void pmwebapi_free_domain(struct domain *);

extern struct cluster *pmwebapi_new_cluster(struct context *,
		struct domain *, pmID);
extern struct cluster *pmwebapi_add_cluster(struct context *,
		struct domain *, pmID);
extern void pmwebapi_add_cluster_labels(struct context *, struct cluster *);
extern void pmwebapi_free_cluster(struct cluster *);

extern struct indom *pmwebapi_new_indom(struct context *,
		struct domain *, pmInDom);
extern struct indom *pmwebapi_add_indom(struct context *,
		struct domain *, pmInDom);
extern void pmwebapi_add_indom_labels(struct indom *);
extern void pmwebapi_free_indom(struct indom *);
extern void pmwebapi_indom_help(struct context *, struct indom *);

extern unsigned int pmwebapi_add_indom_instances(struct context *,
		struct indom *);
extern void pmwebapi_add_instances_labels(struct context *, struct indom *);
extern struct instance *pmwebapi_lookup_instance(struct indom *, int);

extern struct instance *pmwebapi_new_instance(struct indom *, int, sds);
extern struct instance *pmwebapi_add_instance(struct indom *, int, char *);
extern void pmwebapi_free_instance(struct instance *);

extern struct metric *pmwebapi_new_pmid(struct context *,
		const sds, pmID, pmLogInfoCallBack, void *);
extern struct metric *pmwebapi_new_metric(struct context *,
		const sds, pmDesc *, int, char **);
extern struct metric *pmwebapi_add_metric(struct context *,
		const sds, pmDesc *, int, char **);
extern void pmwebapi_add_item_labels(struct context *, struct metric *);
extern int pmwebapi_add_valueset(struct metric *, pmValueSet *);
extern void pmwebapi_free_metric(struct metric *);
extern void pmwebapi_metric_help(struct context *, struct metric *);

extern void pmwebapi_event_flags(void);
extern void pmwebapi_event_missed(void);
extern sds pmwebapi_usectimestamp(sds, struct timeval *);
extern sds pmwebapi_nsectimestamp(sds, struct timespec *);
extern sds pmwebapi_event_parameter(sds, pmValueSet *, int, int *);

extern void pmwebapi_release_value(int, pmAtomValue *);


/*
 * Generally useful sds buffer formatting and diagnostics callback macros
 */
#define infofmt(msg, fmt, ...)	\
	((msg) = sdscatprintf(sdsempty(), fmt, ##__VA_ARGS__))
#define batoninfo(baton, level, msg)	\
	((baton)->info((level), (msg), (baton)->userdata), sdsfree(msg))
#define moduleinfo(module, level, msg, data)	\
	((module)->on_info((level), (msg), (data)), sdsfree(msg))

#endif	/* SERIES_UTIL_H */
