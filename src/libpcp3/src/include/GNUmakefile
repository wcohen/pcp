#
# Copyright (c) 2022 Red Hat.
# Copyright (c) 2000,2004 Silicon Graphics, Inc.  All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 

TOPDIR = ../../../..
include $(TOPDIR)/src/include/builddefs
-include ./GNUlocaldefs

SUBDIRS = pcp

ifeq "$(KEEP_CONFIG_FILES)" ""
LDIRT = pcp.conf
else
LDIRT =
endif

default :: default_pcp

default_pcp : $(SUBDIRS)
	$(SUBDIRS_MAKERULE)

include $(BUILDRULES)

install :: default_pcp install_pcp

install_pcp : $(SUBDIRS) default_pcp
