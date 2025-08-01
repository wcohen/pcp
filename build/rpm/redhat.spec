Name:    pcp
Version: 7.0.0
Release: 1%{?dist}
Summary: System-level performance monitoring and performance management
License: GPL-2.0-or-later AND LGPL-2.1-or-later AND CC-BY-3.0
URL:     https://pcp.io

Source0: https://github.com/performancecopilot/pcp/releases/pcp-%{version}.src.tar.gz
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
ExcludeArch: %{ix86}
%endif

# The additional linker flags break out-of-tree PMDAs.
# https://bugzilla.redhat.com/show_bug.cgi?id=2043092
%undefine _package_note_flags

# UsrMerge was completed in EL 7, however the latest 'hostname' package in EL 7 contains "Provides: /bin/hostname".  Likewise for /bin/ps from procps[-ng] packages.
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 17
%global _hostname_executable /usr/bin/hostname
%global _ps_executable /usr/bin/ps
%else
%global _hostname_executable /bin/hostname
%global _ps_executable /bin/ps
%endif

%global disable_perl 0

%if 0%{?fedora} || 0%{?rhel} > 5
%global disable_selinux 0
%else
%global disable_selinux 1
%endif

%global disable_snmp 0

# No libpfm devel packages for s390, armv7hl nor for some rhels, disable
%ifarch s390 s390x armv7hl
%global disable_perfevent 1
%else
%if 0%{?fedora} >= 20 || 0%{?rhel} > 6
%global disable_perfevent 0
%else
%global disable_perfevent 1
%endif
%endif

# Resource Control kernel feature is on recent Intel/AMD processors only
%ifarch x86_64
%global disable_resctrl 0
%else
%global disable_resctrl 1
%endif

# libchan, libhdr_histogram and pmdastatsd
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
%global disable_statsd 0
%else
%global disable_statsd 1
%endif

# GFS2 filesystem no longer supported here
%if 0%{?rhel} >= 10
%global disable_gfs2 1
%else
%global disable_gfs2 0
%endif

# No python3 development environment before el8
%if 0%{?rhel} == 0 || 0%{?rhel} > 7
%global disable_python3 0
# Do we wish to mandate python3 use in pcp?  (f22+ and el8+)
%if 0%{?fedora} >= 22 || 0%{?rhel} > 7
%global default_python 3
%endif
%else
%global disable_python3 1
%endif

%if 0%{?fedora} >= 24 || 0%{?rhel} > 7
%global perl_interpreter perl-interpreter
%else
%global perl_interpreter perl
%endif

# support for pmdabcc, check bcc.spec for supported architectures of bcc
%if 0%{?fedora} >= 25 || 0%{?rhel} > 6
%ifarch x86_64 %{power64} aarch64 s390x riscv64
%global disable_bcc 0
%else
%global disable_bcc 1
%endif
%else
%global disable_bcc 1
%endif

# support for pmdabpf, check bcc.spec for supported architectures of libbpf-tools
%if 0%{?fedora} >= 37 || 0%{?rhel} > 8
%ifarch x86_64 %{power64} aarch64 s390x riscv64
%global disable_bpf 0
%else
%global disable_bpf 1
%endif
%else
%global disable_bpf 1
%endif

# support for pmdabpftrace, check bpftrace.spec for supported architectures of bpftrace
%if 0%{?fedora} >= 30 || 0%{?rhel} > 7
%ifarch x86_64 %{power64} aarch64 s390x riscv64
%global disable_bpftrace 0
%else
%global disable_bpftrace 1
%endif
%else
%global disable_bpftrace 1
%endif

# support for pmdajson
%if 0%{?rhel} == 0 || 0%{?rhel} > 6
%if !%{disable_python3}
%global disable_json 0
%else
%global disable_json 1
%endif
%else
%global disable_json 1
%endif

# support for pmdamongodb
%if !%{disable_python3}
%global disable_mongodb 0
%else
%global disable_mongodb 1
%endif

# No mssql ODBC driver on non-x86 platforms
%ifarch x86_64
%if !%{disable_python3}
%global disable_mssql 0
%else
%global disable_mssql 1
%endif
%else
%global disable_mssql 1
%endif

# No mysql support on 32-bit x86 platforms from el9 and later
%ifarch %{ix86}
%if 0%{?rhel} >= 9
%global disable_mysql 1
%else
%global disable_mysql 0
%endif
%else
%global disable_mysql 0
%endif

# support for pmdanutcracker (perl deps missing on rhel)
%if 0%{?rhel} == 0
%global disable_nutcracker 0
%else
%global disable_nutcracker 1
%endif

# Qt development and runtime environment missing components before el6
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
%global disable_qt 0
%if 0%{?fedora} != 0 || 0%{?rhel} > 9
%global default_qt 6
%endif
%else
%global disable_qt 1
%endif

# systemd services and pmdasystemd
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%global disable_systemd 0
%else
%global disable_systemd 1
%endif

# static probes, missing before el6 and on some architectures
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
%global disable_sdt 0
%else
%ifnarch ppc ppc64
%global disable_sdt 0
%else
%global disable_sdt 1
%endif
%endif

# libuv async event library
%if 0%{?fedora} >= 28 || 0%{?rhel} > 7
%global disable_libuv 0
%else
%global disable_libuv 1
%endif

%global disable_openssl 0

# rpm producing "noarch" packages
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
%global disable_noarch 0
%else
%global disable_noarch 1
%endif

# build pcp2arrow (no python3-arrow on RHEL or 32-bit Fedora)
%if 0%{?fedora} >= 40
%global disable_arrow 0
%else
%global disable_arrow 1
%endif

%if 0%{?fedora} >= 24
%global disable_xlsx 0
%else
%global disable_xlsx 1
%endif

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 9
%global disable_amdgpu 0
%else
%global disable_amdgpu 1
%endif

# prevent conflicting binary and man page install for pcp(1)
Conflicts: librapi < 0.16

# KVM PMDA moved into pcp (no longer using Perl, default on)
Obsoletes: pcp-pmda-kvm < 4.1.1
Provides: pcp-pmda-kvm = %{version}-%{release}

# RPM PMDA retired completely
Obsoletes: pcp-pmda-rpm < 5.3.2
Obsoletes: pcp-pmda-rpm-debuginfo < 5.3.2

# PCP REST APIs are now provided by pmproxy
Obsoletes: pcp-webapi-debuginfo < 5.0.0
Obsoletes: pcp-webapi < 5.0.0
Provides: pcp-webapi = %{version}-%{release}

# PCP discovery service now provided by pmfind
Obsoletes: pcp-manager-debuginfo < 5.2.0
Obsoletes: pcp-manager < 5.2.0

# Some older releases did not update or replace pcp-gui-debuginfo properly
%if 0%{?fedora} < 27 && 0%{?rhel} <= 7 && "%{_vendor}" == "redhat"
Obsoletes: pcp-gui-debuginfo < 4.1.1
%endif

Obsoletes: pcp-compat < 4.2.0
Obsoletes: pcp-monitor < 4.2.0
Obsoletes: pcp-collector < 4.2.0
Obsoletes: pcp-pmda-nvidia < 3.10.5

# https://fedoraproject.org/wiki/Packaging "C and C++"
BuildRequires: make
BuildRequires: gcc gcc-c++
BuildRequires: procps autoconf bison flex
BuildRequires: avahi-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel
%if !%{disable_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: cyrus-sasl-devel
%if !%{disable_statsd}
# ragel unavailable on RHEL8
%if 0%{?rhel} == 0
BuildRequires: ragel
%endif
BuildRequires: chan-devel HdrHistogram_c-devel
%endif
%if !%{disable_perfevent}
BuildRequires: libpfm-devel >= 4
%endif
%if !%{disable_sdt}
BuildRequires: systemtap-sdt-devel
%endif
%if !%{disable_libuv}
BuildRequires: libuv-devel >= 1.0
%endif
%if !%{disable_openssl}
BuildRequires: openssl-devel >= 1.1.1
%endif
%if 0%{?rhel} == 0 || 0%{?rhel} > 7
BuildRequires: perl-generators
%endif
BuildRequires: perl-devel perl(strict)
BuildRequires: perl(ExtUtils::MakeMaker) perl(LWP::UserAgent) perl(JSON)
BuildRequires: perl(Time::HiRes) perl(Digest::MD5)
BuildRequires: perl(XML::LibXML) perl(File::Slurp)
BuildRequires: %{_hostname_executable}
BuildRequires: %{_ps_executable}
%if !%{disable_systemd}
BuildRequires: systemd-devel
%endif
%if !%{disable_qt}
BuildRequires: desktop-file-utils
%if 0%{?default_qt} == 6
BuildRequires: qt6-qtbase-devel
BuildRequires: qt6-qtsvg-devel
%else
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtsvg-devel
%endif
%endif

# Utilities used indirectly e.g. by scripts we install
Requires: bash xz gawk sed grep coreutils diffutils findutils
Requires: which %{_hostname_executable} %{_ps_executable}
Requires: pcp-libs = %{version}-%{release}

%if !%{disable_selinux}
# rpm boolean dependencies are supported since RHEL 8
%if 0%{?fedora} >= 35 || 0%{?rhel} >= 8
# This ensures that the pcp-selinux package and all its dependencies are
# not pulled into containers and other systems that do not use SELinux
Requires: (pcp-selinux = %{version}-%{release} if selinux-policy-targeted)
%else
Requires: pcp-selinux = %{version}-%{release}
%endif
%endif

%global _confdir        %{_sysconfdir}/pcp
%global _logsdir        %{_localstatedir}/log/pcp
%global _pmnsdir        %{_localstatedir}/lib/pcp/pmns
%global _pmdasdir       %{_localstatedir}/lib/pcp/pmdas
%global _pmdasexecdir   %{_libexecdir}/pcp/pmdas
%global _testsdir       %{_localstatedir}/lib/pcp/testsuite
%global _ieconfdir      %{_localstatedir}/lib/pcp/config/pmieconf
%global _selinuxdir     %{_datadir}/selinux/packages/targeted

%global _with_multilib --enable-multilib=true

%if 0%{?fedora} >= 20 || 0%{?rhel} >= 8
%global _with_doc --with-docdir=%{_docdir}/%{name}
%endif

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
%global _with_dstat --with-dstat-symlink=yes
%global disable_dstat 0
%else
%global _with_dstat --with-dstat-symlink=no
%global disable_dstat 1
%endif

%if !%{disable_systemd}
%global _initddir %{_libexecdir}/pcp/lib
%else
%global _initddir %{_sysconfdir}/rc.d/init.d
%global _with_initd --with-rcdir=%{_initddir}
%endif

# we never want Infiniband on s390 and armv7hl platforms
%ifarch s390 s390x armv7hl
%global disable_infiniband 1
%else
# we never want Infiniband on RHEL5 or earlier
%if 0%{?rhel} != 0 && 0%{?rhel} < 6
%global disable_infiniband 1
%else
%global disable_infiniband 0
%endif
%endif

%if !%{disable_infiniband}
%global _with_ib --with-infiniband=yes
%endif

%if %{disable_perfevent}
%global _with_perfevent --with-perfevent=no
%else
%global _with_perfevent --with-perfevent=yes
%endif

%if %{disable_gfs2}
%global _with_gfs2 --with-pmdagfs2=no
%else
%global _with_gfs2 --with-pmdagfs2=yes
%endif

%if %{disable_statsd}
%global _with_statsd --with-pmdastatsd=no
%else
%global _with_statsd --with-pmdastatsd=yes
%endif

%if %{disable_bcc}
%global _with_bcc --with-pmdabcc=no
%else
%global _with_bcc --with-pmdabcc=yes
%endif

%if %{disable_bpf}
%global _with_bpf --with-pmdabpf=no
%else
%global _with_bpf --with-pmdabpf=yes
%endif

%if %{disable_bpftrace}
%global _with_bpftrace --with-pmdabpftrace=no
%else
%global _with_bpftrace --with-pmdabpftrace=yes
%endif

%if %{disable_json}
%global _with_json --with-pmdajson=no
%else
%global _with_json --with-pmdajson=yes
%endif

%if %{disable_mongodb}
%global _with_mongodb --with-pmdamongodb=no
%else
%global _with_mongodb --with-pmdamongodb=yes
%endif

%if %{disable_mysql}
%global _with_mysql --with-pmdamysql=no
%else
%global _with_mysql --with-pmdamysql=yes
%endif

%if %{disable_nutcracker}
%global _with_nutcracker --with-pmdanutcracker=no
%else
%global _with_nutcracker --with-pmdanutcracker=yes
%endif

%if %{disable_snmp}
%global _with_snmp --with-pmdasnmp=no
%else
%global _with_snmp --with-pmdasnmp=yes
%endif

%global pmda_remove() %{expand:
if [ %1 -eq 0 ]
then
    PCP_PMDAS_DIR=%{_pmdasdir}
    PCP_PMCDCONF_PATH=%{_confdir}/pmcd/pmcd.conf
    if [ -f "$PCP_PMCDCONF_PATH" -a -f "$PCP_PMDAS_DIR/%2/domain.h" ]
    then
        (cd "$PCP_PMDAS_DIR/%2/" && ./Remove >/dev/null 2>&1)
    fi
fi
}

%global install_file() %{expand:
if [ -w "%1" ]
then
    (cd "%1" && touch "%2" && chmod 644 "%2")
else
    echo "WARNING: Cannot write to %1, skipping %2 creation." >&2
fi
}

%global rebuild_pmns() %{expand:
if [ -w "%1" ]
then
    (cd "%1" && ./Rebuild -s && rm -f "%2")
else
    echo "WARNING: Cannot write to %1, skipping namespace rebuild." >&2
fi
}

%description
Performance Co-Pilot (PCP) provides a framework and services to support
system-level performance monitoring and performance management.

The PCP open source release provides a unifying abstraction for all of
the interesting performance data in a system, and allows client
applications to easily retrieve and process any subset of that data.

#
# pcp-conf
#
%package conf
License: LGPL-2.1-or-later
Summary: Performance Co-Pilot run-time configuration
URL: https://pcp.io

# http://fedoraproject.org/wiki/Packaging:Conflicts "Splitting Packages"
Conflicts: pcp-libs < 3.9

%description conf
Performance Co-Pilot (PCP) run-time configuration

#
# pcp-libs
#
%package libs
License: LGPL-2.1-or-later
Summary: Performance Co-Pilot run-time libraries
URL: https://pcp.io
Requires: pcp-conf = %{version}-%{release}

# prevent conflicting library (libpcp.so.N) installation
Conflicts: postgresql-pgpool-II

%description libs
Performance Co-Pilot (PCP) run-time libraries

#
# pcp-libs-devel
#
%package libs-devel
License: GPL-2.0-or-later AND LGPL-2.1-or-later
Summary: Performance Co-Pilot (PCP) development headers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

# prevent conflicting library (libpcp.so) installation
Conflicts: postgresql-pgpool-II-devel

%description libs-devel
Performance Co-Pilot (PCP) headers for development.

#
# pcp-devel
#
%package devel
License: GPL-2.0-or-later AND LGPL-2.1-or-later
Summary: Performance Co-Pilot (PCP) development tools and documentation
URL: https://pcp.io
Requires: pcp = %{version}-%{release}
Requires: pcp-libs = %{version}-%{release}
Requires: pcp-libs-devel = %{version}-%{release}

%description devel
Performance Co-Pilot (PCP) documentation and tools for development.

#
# pcp-testsuite
#
%package testsuite
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) test suite
URL: https://pcp.io
Requires: pcp = %{version}-%{release}
Requires: pcp-libs = %{version}-%{release}
Requires: pcp-libs-devel = %{version}-%{release}
Requires: pcp-devel = %{version}-%{release}
Requires: bc gcc gzip bzip2
Requires: redhat-rpm-config
%if !%{disable_selinux}
Requires: selinux-policy-devel
Requires: selinux-policy-targeted
Requires: setools
%endif

%description testsuite
Quality assurance test suite for Performance Co-Pilot (PCP).
# end testsuite

#
# perl-PCP-PMDA. This is the PCP agent perl binding.
#
%package -n perl-PCP-PMDA
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) Perl bindings and documentation
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: %{perl_interpreter}

%description -n perl-PCP-PMDA
The PCP::PMDA Perl module contains the language bindings for
building Performance Metric Domain Agents (PMDAs) using Perl.
Each PMDA exports performance data for one specific domain, for
example the operating system kernel, Cisco routers, a database,
an application, etc.

#
# perl-PCP-MMV
#
%package -n perl-PCP-MMV
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) Perl bindings for PCP Memory Mapped Values
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: %{perl_interpreter}

%description -n perl-PCP-MMV
The PCP::MMV module contains the Perl language bindings for
building scripts instrumented with the Performance Co-Pilot
(PCP) Memory Mapped Value (MMV) mechanism.
This mechanism allows arbitrary values to be exported from an
instrumented script into the PCP infrastructure for monitoring
and analysis with pmchart, pmie, pmlogger and other PCP tools.

#
# perl-PCP-LogImport
#
%package -n perl-PCP-LogImport
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) Perl bindings for importing external data into PCP archives
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: %{perl_interpreter}

%description -n perl-PCP-LogImport
The PCP::LogImport module contains the Perl language bindings for
importing data in various 3rd party formats into PCP archives so
they can be replayed with standard PCP monitoring tools.

#
# perl-PCP-LogSummary
#
%package -n perl-PCP-LogSummary
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) Perl bindings for post-processing output of pmlogsummary
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: %{perl_interpreter}

%description -n perl-PCP-LogSummary
The PCP::LogSummary module provides a Perl module for using the
statistical summary data produced by the Performance Co-Pilot
pmlogsummary utility.  This utility produces various averages,
minima, maxima, and other calculations based on the performance
data stored in a PCP archive.  The Perl interface is ideal for
exporting this data into third-party tools (e.g. spreadsheets).

#
# pcp-import-sar2pcp
#
%package import-sar2pcp
License: LGPL-2.1-or-later
Summary: Performance Co-Pilot tools for importing sar data into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}
Requires: perl(XML::TokeParser)

%description import-sar2pcp
Performance Co-Pilot (PCP) front-end tools for importing sar data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-iostat2pcp
#
%package import-iostat2pcp
License: LGPL-2.1-or-later
Summary: Performance Co-Pilot tools for importing iostat data into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}

%description import-iostat2pcp
Performance Co-Pilot (PCP) front-end tools for importing iostat data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-mrtg2pcp
#
%package import-mrtg2pcp
License: LGPL-2.1-or-later
Summary: Performance Co-Pilot tools for importing MTRG data into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}

%description import-mrtg2pcp
Performance Co-Pilot (PCP) front-end tools for importing MTRG data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-ganglia2pcp
#
%package import-ganglia2pcp
License: LGPL-2.1-or-later
Summary: Performance Co-Pilot tools for importing ganglia data into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}

%description import-ganglia2pcp
Performance Co-Pilot (PCP) front-end tools for importing ganglia data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-collectl2pcp
#
%package import-collectl2pcp
License: LGPL-2.1-or-later
Summary: Performance Co-Pilot tools for importing collectl log files into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}

%description import-collectl2pcp
Performance Co-Pilot (PCP) front-end tools for importing collectl data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-export-zabbix-agent
#
%package export-zabbix-agent
License: GPL-2.0-or-later
Summary: Module for exporting PCP metrics to Zabbix agent
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}

%description export-zabbix-agent
Performance Co-Pilot (PCP) module for exporting metrics from PCP to
Zabbix via the Zabbix agent - see zbxpcp(3) for further details.

%if !%{disable_python3}
#
# pcp-import-pmseries
#
%package import-pmseries
License: LGPL-2.1-or-later
Summary: Performance Co-Pilot tools importing PCP archives for pmseries queries
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}

%description import-pmseries
Performance Co-Pilot (PCP) tools for importing PCP archives into Valkey
or Redis for fast, scalable time series access via pmseries(1) queries.

#
# pcp-geolocate
#
%package geolocate
License: GPL-2.0-or-later
Summary: Performance Co-Pilot geographical location metric labels
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}

%description geolocate
Performance Co-Pilot (PCP) tools that automatically apply metric labels
containing latitude and longitude, based on IP-address-based lookups.
Used with live maps to show metric values from different locations.

#
# pcp-export-pcp2elasticsearch
#
%package export-pcp2elasticsearch
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics to ElasticSearch
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}
Requires: python3-requests
BuildRequires: python3-requests

%description export-pcp2elasticsearch
Performance Co-Pilot (PCP) front-end tools for exporting metric values
to Elasticsearch - a distributed, RESTful search and analytics engine.
See https://www.elastic.co/community for further details.

#
# pcp-export-pcp2graphite
#
%package export-pcp2graphite
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics to Graphite
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}

%description export-pcp2graphite
Performance Co-Pilot (PCP) front-end tools for exporting metric values
to graphite (http://graphite.readthedocs.org).

# pcp-export-pcp2influxdb
#
%package export-pcp2influxdb
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics to InfluxDB
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}
Requires: python3-requests

%description export-pcp2influxdb
Performance Co-Pilot (PCP) front-end tools for exporting metric values
to InfluxDB (https://influxdata.com/time-series-platform/influxdb).

#
# pcp-export-pcp2json
#
%package export-pcp2json
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics in JSON format
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}

%description export-pcp2json
Performance Co-Pilot (PCP) front-end tools for exporting metric values
in JSON format.

#
# pcp-export-pcp2openmetrics
#
%package export-pcp2openmetrics
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics in OpenMetrics format
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}

%description export-pcp2openmetrics
Performance Co-Pilot (PCP) front-end tools for exporting metric values
in OpenMetrics (https://openmetrics.io/) format.

#
# pcp-export-pcp2spark
#
%package export-pcp2spark
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics to Apache Spark
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}

%description export-pcp2spark
Performance Co-Pilot (PCP) front-end tools for exporting metric values
in JSON format to Apache Spark. See https://spark.apache.org/ for
further details on Apache Spark.

#
# pcp-export-pcp2arrow
#
%if !%{disable_arrow}
%package export-pcp2arrow
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics to Apache Arrow
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}
Requires: python3-pyarrow
BuildRequires: python3-pyarrow

%description export-pcp2arrow
Performance Co-Pilot (PCP) front-end tool for exporting metric values
to Apache Arrow, which supports the columnar parquet data format.
%endif

#
# pcp-export-pcp2xlsx
#
%if !%{disable_xlsx}
%package export-pcp2xlsx
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics to Excel
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}
Requires: python3-openpyxl
BuildRequires: python3-openpyxl

%description export-pcp2xlsx
Performance Co-Pilot (PCP) front-end tools for exporting metric values
in Excel spreadsheet format.
%endif

#
# pcp-export-pcp2xml
#
%package export-pcp2xml
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics in XML format
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}

%description export-pcp2xml
Performance Co-Pilot (PCP) front-end tools for exporting metric values
in XML format.

#
# pcp-export-pcp2zabbix
#
%package export-pcp2zabbix
License: GPL-2.0-or-later
Summary: Performance Co-Pilot tools for exporting PCP metrics to Zabbix
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
Requires: python3-pcp = %{version}-%{release}

%description export-pcp2zabbix
Performance Co-Pilot (PCP) front-end tools for exporting metric values
to the Zabbix (https://www.zabbix.org/) monitoring software.
%endif

#
# pcp-pmda-podman
#
%package pmda-podman
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for podman containers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description pmda-podman
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting podman container and pod statistics via the podman REST API.

%if !%{disable_statsd}
#
# pcp-pmda-statsd
#
%package pmda-statsd
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from statsd
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: chan HdrHistogram_c

%description pmda-statsd
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting statistics from the statsd daemon.
%endif

%if !%{disable_perfevent}
#
# pcp-pmda-perfevent
#
%package pmda-perfevent
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for hardware counters
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: libpfm >= 4
BuildRequires: libpfm-devel >= 4
Obsoletes: pcp-pmda-papi < 5.0.0
Obsoletes: pcp-pmda-papi-debuginfo < 5.0.0

%description pmda-perfevent
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting hardware counters statistics through libpfm.
%endif

%if !%{disable_infiniband}
#
# pcp-pmda-infiniband
#
%package pmda-infiniband
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Infiniband HCAs and switches
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: libibmad >= 1.3.7 libibumad >= 1.3.7
BuildRequires: libibmad-devel >= 1.3.7 libibumad-devel >= 1.3.7

%description pmda-infiniband
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting Infiniband statistics.  By default, it monitors the local HCAs
but can also be configured to monitor remote GUIDs such as IB switches.
%endif

#
# pcp-pmda-activemq
#
%package pmda-activemq
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for ActiveMQ
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(LWP::UserAgent)

%description pmda-activemq
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the ActiveMQ message broker.
#end pcp-pmda-activemq

#
# pcp-pmda-bind2
#
%package pmda-bind2
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for BIND servers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(LWP::UserAgent)
Requires: perl(XML::LibXML)
Requires: perl(File::Slurp)
Requires: perl-autodie
Requires: perl-Time-HiRes

%description pmda-bind2
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from BIND (Berkeley Internet Name Domain).
#end pcp-pmda-bind2

#
# pcp-pmda-redis
#
%package pmda-redis
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Redis
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-autodie
Requires: perl-Time-HiRes
Requires: perl-Data-Dumper

%description pmda-redis
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from Redis servers (redis.io).
#end pcp-pmda-redis

%if !%{disable_nutcracker}
#
# pcp-pmda-nutcracker
#
%package pmda-nutcracker
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for NutCracker (TwemCache)
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(YAML::XS)
Requires: perl(JSON)

%description pmda-nutcracker
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from NutCracker (TwemCache).
#end pcp-pmda-nutcracker
%endif

#
# pcp-pmda-bonding
#
%package pmda-bonding
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Bonded network interfaces
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-bonding
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about bonded network interfaces.
#end pcp-pmda-bonding

#
# pcp-pmda-dbping
#
%package pmda-dbping
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Database response times and Availablility
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-DBI

%description pmda-dbping
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Database response times and Availablility.
#end pcp-pmda-dbping

#
# pcp-pmda-ds389
#
%package pmda-ds389
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for 389 Directory Servers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
%if 0%{?rhel} <= 7
Requires: perl-LDAP
%endif

%description pmda-ds389
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about a 389 Directory Server.
#end pcp-pmda-ds389

#
# pcp-pmda-ds389log
#
%package pmda-ds389log
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for 389 Directory Server Loggers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-Date-Manip

%description pmda-ds389log
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from a 389 Directory Server log.
#end pcp-pmda-ds389log


#
# pcp-pmda-gpfs
#
%package pmda-gpfs
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for GPFS Filesystem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-gpfs
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the GPFS filesystem.
#end pcp-pmda-gpfs

#
# pcp-pmda-gpsd
#
%package pmda-gpsd
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for a GPS Daemon
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-Time-HiRes
Requires: perl-JSON

%description pmda-gpsd
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about a GPS Daemon.
#end pcp-pmda-gpsd

#
# pcp-pmda-denki
#
%package pmda-denki
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics dealing with electrical power
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-denki
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics related to the electrical power consumed by and inside
the system.
# end pcp-pmda-denki

#
# pcp-pmda-docker
#
%package pmda-docker
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from the Docker daemon
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description pmda-docker
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics using the Docker daemon REST API.
#end pcp-pmda-docker

#
# pcp-pmda-lustre
#
%package pmda-lustre
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Lustre Filesytem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-lustre
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Lustre Filesystem.
#end pcp-pmda-lustre

#
# pcp-pmda-lustrecomm
#
%package pmda-lustrecomm
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Lustre Filesytem Comms
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description pmda-lustrecomm
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Lustre Filesystem Comms.
#end pcp-pmda-lustrecomm

#
# pcp-pmda-memcache
#
%package pmda-memcache
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Memcached
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-memcache
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Memcached.
#end pcp-pmda-memcache

%if !%{disable_mysql}
#
# pcp-pmda-mysql
#
%package pmda-mysql
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for MySQL
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(DBI) perl(DBD::mysql)
BuildRequires: perl(DBI) perl(DBD::mysql)

%description pmda-mysql
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the MySQL database.
#end pcp-pmda-mysql
%endif

#
# pcp-pmda-named
#
%package pmda-named
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Named
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-named
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Named nameserver.
#end pcp-pmda-named

# pcp-pmda-netfilter
#
%package pmda-netfilter
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Netfilter framework
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-netfilter
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Netfilter packet filtering framework.
#end pcp-pmda-netfilter

#
# pcp-pmda-news
#
%package pmda-news
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Usenet News
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-news
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Usenet News.
#end pcp-pmda-news

#
# pcp-pmda-nginx
#
%package pmda-nginx
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Nginx Webserver
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(LWP::UserAgent)
BuildRequires: perl(LWP::UserAgent)

%description pmda-nginx
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Nginx Webserver.
#end pcp-pmda-nginx

#
# pcp-pmda-oracle
#
%package pmda-oracle
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Oracle database
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(DBI)
BuildRequires: perl(DBI)

%description pmda-oracle
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Oracle database.
#end pcp-pmda-oracle

#
# pcp-pmda-pdns
#
%package pmda-pdns
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for PowerDNS
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-Time-HiRes

%description pmda-pdns
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the PowerDNS.
#end pcp-pmda-pdns

#
# pcp-pmda-postfix
#
%package pmda-postfix
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Postfix (MTA)
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-Time-HiRes
%if 0%{?fedora} > 16 || 0%{?rhel} > 5
Requires: postfix-perl-scripts
BuildRequires: postfix-perl-scripts
%endif
%if 0%{?rhel} <= 5
Requires: postfix
BuildRequires: postfix
%endif
%if "%{_vendor}" == "suse"
Requires: postfix-doc
BuildRequires: postfix-doc
%endif

%description pmda-postfix
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Postfix (MTA).
#end pcp-pmda-postfix

#
# pcp-pmda-rsyslog
#
%package pmda-rsyslog
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Rsyslog
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-rsyslog
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Rsyslog.
#end pcp-pmda-rsyslog

#
# pcp-pmda-samba
#
%package pmda-samba
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Samba
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-samba
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Samba.
#end pcp-pmda-samba

#
# pcp-pmda-slurm
#
%package pmda-slurm
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the SLURM Workload Manager
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-slurm
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from the SLURM Workload Manager.
#end pcp-pmda-slurm

%if !%{disable_snmp}
#
# pcp-pmda-snmp
#
%package pmda-snmp
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Simple Network Management Protocol
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
# There are no perl-Net-SNMP packages in rhel, disable unless non-rhel or epel5
%if 0%{?rhel} == 0 || 0%{?rhel} < 6
Requires: perl(Net::SNMP)
%endif

%description pmda-snmp
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about SNMP.
#end pcp-pmda-snmp
%endif

#
# pcp-pmda-zimbra
#
%package pmda-zimbra
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Zimbra
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-zimbra
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Zimbra.
#end pcp-pmda-zimbra

#
# pcp-pmda-dm
#
%package pmda-dm
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Device Mapper Cache and Thin Client
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
BuildRequires: device-mapper-devel
%description pmda-dm
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Device Mapper Cache and Thin Client.
# end pcp-pmda-dm


%if !%{disable_bcc}
#
# pcp-pmda-bcc
#
%package pmda-bcc
License: Apache-2.0 AND GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from eBPF/BCC modules
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-bcc
Requires: python3-pcp
%description pmda-bcc
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting performance metrics from eBPF/BCC Python modules.
# end pcp-pmda-bcc
%endif

%if !%{disable_bpf}
#
# pcp-pmda-bpf
#
%package pmda-bpf
License: Apache-2.0 AND GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from eBPF ELF modules
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: libbpf
BuildRequires: libbpf-devel clang llvm
%description pmda-bpf
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting performance metrics from eBPF ELF modules.
# end pcp-pmda-bpf
%endif

%if !%{disable_bpftrace}
#
# pcp-pmda-bpftrace
#
%package pmda-bpftrace
License: Apache-2.0 AND GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from bpftrace scripts
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: bpftrace >= 0.9.2
Requires: python3-pcp
Requires: python3 >= 3.6
%description pmda-bpftrace
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting performance metrics from bpftrace scripts.
# end pcp-pmda-bpftrace
%endif

%if !%{disable_python3}
#
# pcp-pmda-hdb
#
%package pmda-hdb
License: GPL-3.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for SAP HANA databases
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-hdb
This package provides a PMDA to export metric values about a SAP HANA
database (https://www.sap.com/products/data-cloud/hana.html).
#end pcp-pmda-hdb

#
# pcp-pmda-gluster
#
%package pmda-gluster
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Gluster filesystem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-gluster
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the gluster filesystem.
# end pcp-pmda-gluster

#
# pcp-pmda-nfsclient
#
%package pmda-nfsclient
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for NFS Clients
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-nfsclient
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics for NFS Clients.
#end pcp-pmda-nfsclient

#
# pcp-pmda-postgresql
#
%package pmda-postgresql
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for PostgreSQL
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
Requires: python3-psycopg2
BuildRequires: python3-psycopg2
%description pmda-postgresql
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the PostgreSQL database.
#end pcp-pmda-postgresql

#
# pcp-pmda-zswap
#
%package pmda-zswap
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for compressed swap
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-zswap
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about compressed swap.
# end pcp-pmda-zswap

#
# pcp-pmda-unbound
#
%package pmda-unbound
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Unbound DNS Resolver
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-unbound
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Unbound DNS Resolver.
# end pcp-pmda-unbound

#
# pcp-pmda-mic
#
%package pmda-mic
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Intel MIC cards
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-mic
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Intel MIC cards.
# end pcp-pmda-mic

#
# pcp-pmda-haproxy
#
%package pmda-haproxy
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for HAProxy
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-haproxy
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting performance metrics from HAProxy over the HAProxy stats socket.
# end pcp-pmda-haproxy

#
# pcp-pmda-libvirt
#
%package pmda-libvirt
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from virtual machines
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
Requires: libvirt-python3 python3-lxml
BuildRequires: libvirt-python3 python3-lxml
%description pmda-libvirt
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting virtualisation statistics from libvirt about behaviour of guest
and hypervisor machines.
# end pcp-pmda-libvirt

#
# pcp-pmda-elasticsearch
#
%package pmda-elasticsearch
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Elasticsearch
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-elasticsearch
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Elasticsearch.
#end pcp-pmda-elasticsearch

#
# pcp-pmda-openvswitch
#
%package pmda-openvswitch
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Open vSwitch
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-openvswitch
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from Open vSwitch.
#end pcp-pmda-openvswitch

#
# pcp-pmda-rabbitmq
#
%package pmda-rabbitmq
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for RabbitMQ queues
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-rabbitmq
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about RabbitMQ message queues.
#end pcp-pmda-rabbitmq

#
# pcp-pmda-uwsgi
#
%package pmda-uwsgi
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from uWSGI servers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-uwsgi
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from uWSGI servers.
#end pcp-pmda-uwsgi

#
# pcp-pmda-lio
#
%package pmda-lio
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the LIO subsystem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
Requires: python3-rtslib
BuildRequires: python3-rtslib
%description pmda-lio
This package provides a PMDA to gather performance metrics from the kernels
iSCSI target interface (LIO). The metrics are stored by LIO within the Linux
kernels configfs filesystem. The PMDA provides per LUN level stats, and a
summary instance per iSCSI target, which aggregates all LUN metrics within the
target.
#end pcp-pmda-lio

#
# pcp-pmda-openmetrics
#
%package pmda-openmetrics
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from OpenMetrics endpoints
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
Requires: python3-requests
BuildRequires: python3-requests
%description pmda-openmetrics
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting metrics from OpenMetrics (https://openmetrics.io/) endpoints.
#end pcp-pmda-openmetrics

#
# pcp-pmda-lmsensors
#
%package pmda-lmsensors
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for hardware sensors
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: lm_sensors
Requires: python3-pcp
# rewritten in python, so there is no longer a debuginfo package
Obsoletes: pcp-pmda-lmsensors-debuginfo < 4.2.0
%description pmda-lmsensors
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Linux hardware monitoring sensors.
# end pcp-pmda-lmsensors

#
# pcp-pmda-netcheck
#
%package pmda-netcheck
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for simple network checks
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-netcheck
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from simple network checks.
# end pcp-pmda-netcheck

#
# pcp-pmda-rocestat
#
%package pmda-rocestat
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for nVidia RoCE devices
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%description pmda-rocestat
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting statistics for nVidia RDMA over Converged Ethernet (RoCE) devices.
# end pcp-pmda-rocestat
%endif

%if !%{disable_mongodb}
#
# pcp-pmda-mongodb
#
%package pmda-mongodb
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for MongoDB
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%if 0%{?rhel} == 0
Requires: python3-pymongo
BuildRequires: python3-pymongo
%endif
%description pmda-mongodb
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from MongoDB.
# end pcp-pmda-mongodb
%endif

%if !%{disable_mssql}
#
# pcp-pmda-mssql
#
%package pmda-mssql
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Microsoft SQL Server
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
Requires: python3-pyodbc
BuildRequires: python3-pyodbc
%endif
%description pmda-mssql
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from Microsoft SQL Server.
# end pcp-pmda-mssql
%endif

%if !%{disable_json}
#
# pcp-pmda-json
#
%package pmda-json
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for JSON data
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-pcp
Requires: python3-jsonpointer python3-six
BuildRequires: python3-jsonpointer python3-six
%description pmda-json
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics output in JSON.
# end pcp-pmda-json
%endif

#
# C pmdas
# pcp-pmda-apache
#
%package pmda-apache
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Apache webserver
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-apache
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Apache webserver.
# end pcp-pmda-apache

#
# pcp-pmda-bash
#
%package pmda-bash
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Bash shell
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-bash
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Bash shell.
# end pcp-pmda-bash

#
# pcp-pmda-cifs
#
%package pmda-cifs
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the CIFS protocol
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-cifs
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Common Internet Filesytem.
# end pcp-pmda-cifs

#
# pcp-pmda-cisco
#
%package pmda-cisco
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Cisco routers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-cisco
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Cisco routers.
# end pcp-pmda-cisco

#
# pcp-pmda-farm
#
%package pmda-farm
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Seagate FARM Log metrics
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: smartmontools
%description pmda-farm
This package contains the PCP Performance Metric Domain Agent (PMDA) for
collecting metrics from Seagate Hard Drive vendor specific Field Accessible
Reliability Metrics (FARM) Log making use of data from the smartmontools 
package.
#end pcp-pmda-farm

%if !%{disable_gfs2}
#
# pcp-pmda-gfs2
#
%package pmda-gfs2
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the GFS2 filesystem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-gfs2
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Global Filesystem v2.
# end pcp-pmda-gfs2
%endif

#
# pcp-pmda-hacluster
#
%package pmda-hacluster
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for High Availability Clusters
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-hacluster
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about linux High Availability (HA) Clusters.
# end pcp-pmda-hacluster

#
# pcp-pmda-logger
#
%package pmda-logger
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from arbitrary log files
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-logger
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from a specified set of log files (or pipes).  The PMDA
supports both sampled and event-style metrics.
# end pcp-pmda-logger

#
# pcp-pmda-mailq
#
%package pmda-mailq
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the sendmail queue
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-mailq
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about email queues managed by sendmail.
# end pcp-pmda-mailq

#
# pcp-pmda-mounts
#
%package pmda-mounts
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for filesystem mounts
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-mounts
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about filesystem mounts.
# end pcp-pmda-mounts

#
# pcp-pmda-nvidia-gpu
#
%package pmda-nvidia-gpu
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the Nvidia GPU
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-nvidia-gpu
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Nvidia GPUs.
# end pcp-pmda-nvidia-gpu

%if !%{disable_resctrl}
#
# pcp-pmda-resctrl
#
%package pmda-resctrl
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from Linux resource control
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-resctrl
This package contains the PCP Performance Metric Domain Agent (PMDA) for
collecting metrics from the Linux kernel resource control functionality.
#end pcp-pmda-resctrl
%endif

#
# pcp-pmda-roomtemp
#
%package pmda-roomtemp
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for the room temperature
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-roomtemp
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the room temperature.
# end pcp-pmda-roomtemp

#
# pcp-pmda-sendmail
#
%package pmda-sendmail
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for Sendmail
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-sendmail
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Sendmail traffic.
# end pcp-pmda-sendmail

#
# pcp-pmda-shping
#
%package pmda-shping
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for shell command responses
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-shping
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about quality of service and response time measurements of
arbitrary shell commands.
# end pcp-pmda-shping

#
# pcp-pmda-smart
#
%package pmda-smart
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for S.M.A.R.T values
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: smartmontools
%description pmda-smart
This package contains the PCP Performance Metric Domain Agent (PMDA) for
collecting metrics of disk S.M.A.R.T values making use of data from the
smartmontools package.
#end pcp-pmda-smart

#
# pcp-pmda-sockets
#
%package pmda-sockets
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) per-socket metrics
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: iproute
%description pmda-sockets
This package contains the PCP Performance Metric Domain Agent (PMDA) for
collecting per-socket statistics, making use of utilities such as 'ss'.
#end pcp-pmda-sockets

#
# pcp-pmda-summary
#
%package pmda-summary
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) summary metrics from pmie
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-summary
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about other installed PMDAs.
# end pcp-pmda-summary

%if !%{disable_systemd}
#
# pcp-pmda-systemd
#
%package pmda-systemd
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from the Systemd journal
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-systemd
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from the Systemd journal.
# end pcp-pmda-systemd
%endif

#
# pcp-pmda-trace
#
%package pmda-trace
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics for application tracing
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-trace
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about trace performance data in applications.
# end pcp-pmda-trace

#
# pcp-pmda-weblog
#
%package pmda-weblog
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from web server logs
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-weblog
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about web server logs.
# end pcp-pmda-weblog
# end C pmdas

%if !%{disable_amdgpu}
#
# pcp-pmda-amdgpu
#
%package pmda-amdgpu
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) metrics from AMD GPU devices
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: libdrm
BuildRequires: libdrm-devel
%description pmda-amdgpu
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting performance metrics from AMDGPU devices.
# end pcp-pmda-amdgpu
%endif

%package zeroconf
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) Zeroconf Package
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: pcp-system-tools = %{version}-%{release}
Requires: pcp-doc = %{version}-%{release}
Requires: pcp-pmda-dm = %{version}-%{release}
%if !%{disable_python3}
Requires: pcp-pmda-nfsclient = %{version}-%{release}
Requires: pcp-pmda-openmetrics = %{version}-%{release}
%endif
%description zeroconf
This package contains configuration tweaks and files to increase metrics
gathering frequency, several extended pmlogger configurations, as well as
automated pmie diagnosis, alerting and self-healing for the localhost.

%if !%{disable_python3}
#
# python3-pcp. This is the PCP library bindings for python3.
#
%package -n python3-pcp
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) Python3 bindings and documentation
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3

%description -n python3-pcp
This python PCP module contains the language bindings for
Performance Metric API (PMAPI) monitor tools and Performance
Metric Domain Agent (PMDA) collector tools written in Python3.
%endif

#
# pcp-system-tools
#
%package system-tools
License: GPL-2.0-or-later
Summary: Performance Co-Pilot (PCP) System and Monitoring Tools
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
%if !%{disable_dstat}
# https://fedoraproject.org/wiki/Packaging:Guidelines "Renaming/Replacing Existing Packages"
Provides: dstat = %{version}-%{release}
Provides: /usr/bin/dstat
Obsoletes: dstat <= 0.8
%endif
%endif

%description system-tools
This PCP module contains additional system monitoring tools written
in the Python language.

%if !%{disable_qt}
#
# pcp-gui package for Qt tools
#
%package gui
License: GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH Qwt-exception-1.0
Summary: Visualization tools for the Performance Co-Pilot toolkit
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: liberation-sans-fonts
BuildRequires: hicolor-icon-theme

%description gui
Visualization tools for the Performance Co-Pilot toolkit.
The pcp-gui package primarily includes visualization tools for
monitoring systems using live and archived Performance Co-Pilot
(PCP) sources.
%endif

#
# pcp-doc package
#
%package doc
License: GPL-2.0-or-later AND CC-BY-3.0
%if !%{disable_noarch}
BuildArch: noarch
%endif
Summary: Documentation and tutorial for the Performance Co-Pilot
URL: https://pcp.io
# http://fedoraproject.org/wiki/Packaging:Conflicts "Splitting Packages"
# (all man pages migrated to pcp-doc during great package split of '15)
Conflicts: pcp-pmda-infiniband < 3.10.5

%description doc
Documentation and tutorial for the Performance Co-Pilot
Performance Co-Pilot (PCP) provides a framework and services to support
system-level performance monitoring and performance management.

The pcp-doc package provides useful information on using and
configuring the Performance Co-Pilot (PCP) toolkit for system
level performance management.  It includes tutorials, HOWTOs,
and other detailed documentation about the internals of core
PCP utilities and daemons, and the PCP graphical tools.

#
# pcp-selinux package
#
%if !%{disable_selinux}
%package selinux
License: GPL-2.0-or-later AND CC-BY-3.0
Summary: Selinux policy package
URL: https://pcp.io
BuildRequires: selinux-policy-devel
BuildRequires: selinux-policy-targeted
%if 0%{?rhel} == 5
BuildRequires: setools
%else
BuildRequires: setools-console
%endif
Requires: policycoreutils selinux-policy-targeted

%description selinux
This package contains SELinux support for PCP.  The package contains
interface rules, type enforcement and file context adjustments for an
updated policy package.
%endif


%prep
%autosetup -p1

%build
# the buildsubdir macro gets defined in %%setup and is apparently only available in the next step (i.e. the %%build step)
%global __strip %{_builddir}/%{?buildsubdir}/build/rpm/custom-strip

# fix up build version
_build=`echo %{release} | sed -e 's/\..*$//'`
sed -i "/PACKAGE_BUILD/s/=[0-9]*/=$_build/" VERSION.pcp

%configure %{?_with_multilib} %{?_with_initd} %{?_with_doc} %{?_with_dstat} %{?_with_ib} %{?_with_gfs2} %{?_with_statsd} %{?_with_perfevent} %{?_with_bcc} %{?_with_bpf} %{?_with_bpftrace} %{?_with_json} %{?_with_mongodb} %{?_with_mysql} %{?_with_snmp} %{?_with_nutcracker}
make %{?_smp_mflags} default_pcp

%install
rm -Rf $RPM_BUILD_ROOT
BACKDIR=`pwd`
NO_CHOWN=true
DIST_ROOT=$RPM_BUILD_ROOT
DIST_TMPFILES=$BACKDIR/install.tmpfiles
DIST_MANIFEST=$BACKDIR/install.manifest
export NO_CHOWN DIST_ROOT DIST_MANIFEST DIST_TMPFILES
rm -f $DIST_MANIFEST $DIST_TMPFILES
make install_pcp

### TODO: remove these by incorporating into the actual build

# Fix stuff we do/don't want to ship
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
sed -i -e '/\.a$/d' $DIST_MANIFEST

# remove sheet2pcp until BZ 830923 and BZ 754678 are resolved.
rm -f $RPM_BUILD_ROOT/%{_bindir}/sheet2pcp $RPM_BUILD_ROOT/%{_mandir}/man1/sheet2pcp.1*
sed -i -e '/sheet2pcp/d' $DIST_MANIFEST

# remove {config,platform}sz.h as these are not multilib friendly.
rm -f $RPM_BUILD_ROOT/%{_includedir}/pcp/configsz.h
sed -i -e '/configsz.h/d' $DIST_MANIFEST
rm -f $RPM_BUILD_ROOT/%{_includedir}/pcp/platformsz.h
sed -i -e '/platformsz.h/d' $DIST_MANIFEST

%if %{disable_mssql}
# remove pmdamssql on platforms lacking MSODBC driver packages.
rm -fr $RPM_BUILD_ROOT/%{_confdir}/mssql
rm -fr $RPM_BUILD_ROOT/%{_confdir}/pmieconf/mssql
rm -fr $RPM_BUILD_ROOT/%{_ieconfdir}/mssql
rm -fr $RPM_BUILD_ROOT/%{_pmdasdir}/mssql
rm -fr $RPM_BUILD_ROOT/%{_pmdasexecdir}/mssql
%endif

%if !%{disable_qt}
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/pmchart.desktop
%endif

%if 0%{?rhel} || 0%{?fedora}
# Fedora and RHEL default local only access for pmcd and pmlogger
sed -i -e '/^# .*_LOCAL=1/s/^# //' $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/{pmcd,pmlogger}
%endif

# default chkconfig off (all RPM platforms)
for f in $RPM_BUILD_ROOT/%{_initddir}/{pcp,pmcd,pmlogger,pmie,pmproxy}; do
    test -f "$f" || continue
    sed -i -e '/^# chkconfig/s/:.*$/: - 95 05/' -e '/^# Default-Start:/s/:.*$/:/' $f
done

### end TODO

PCP_GUI='pmchart|pmconfirm|pmdumptext|pmmessage|pmquery|pmsnap|pmtime'

PCP_CONF=$BACKDIR/src/include/pcp.conf
export PCP_CONF
. $BACKDIR/src/include/pcp.env
CFGFILELIST=`ls -1 $BACKDIR/debian/pcp-conf.{install,dirs}`
LIBFILELIST=`ls -1 $BACKDIR/debian/lib*.{install,dirs} | grep -F -v -- -dev.`
DEVFILELIST=`ls -1 $BACKDIR/debian/lib*-dev.{install,dirs}`

# Package split: pcp{-conf,-libs,-libs-devel,-testsuite,-import-*,-export-*}...
# The above list is ordered by file selection; files for each package are
# removed from a global set, then the base package catches all remaining.
sed -e 's/^/\//' $CFGFILELIST >pcp-conf-files
sed -e 's/^/\//' $LIBFILELIST >pcp-libs-files
sed -e 's/^/\//' $DEVFILELIST >pcp-devel-files
grep "\.h$" $DEVFILELIST | cut -f2 -d":" >pcp-libs-devel-files
grep "\.pc$" $DEVFILELIST | cut -f2 -d":" >>pcp-libs-devel-files
grep "\.so$" $DEVFILELIST | cut -f2 -d":" >>pcp-libs-devel-files
grep "\.a$" $DEVFILELIST | cut -f2 -d":" >>pcp-libs-devel-files
sed -i -e 's/^/\//' pcp-libs-devel-files
sed -i '/.h$/d' pcp-devel-files
sed -i '/.pc$/d' pcp-devel-files
sed -i '/.so$/d' pcp-devel-files
sed -i '/.a$/d' pcp-devel-files
sed -i '/\/man\//d' pcp-devel-files
sed -i '/\/include\//d' pcp-devel-files

%ifarch x86_64 ppc64 ppc64le aarch64 s390x riscv64
sed -i -e 's/usr\/lib\//usr\/lib64\//' pcp-libs-files
sed -i -e 's/usr\/lib\//usr\/lib64\//' pcp-devel-files
sed -i -e 's/usr\/lib\//usr\/lib64\//' pcp-libs-devel-files
%endif
%ifarch ia64
%if "%{_vendor}" != "suse"
sed -i -e 's/usr\/lib\//usr\/lib64\//' pcp-libs-files
sed -i -e 's/usr\/lib\//usr\/lib64\//' pcp-devel-files
sed -i -e 's/usr\/lib\//usr\/lib64\//' pcp-libs-devel-files
%endif
%endif

# some special cases for devel
awk '{print $NF}' $DIST_MANIFEST |\
grep -E 'pcp/(examples|demos)|(etc/pcp|pcp/pmdas)/(sample|simple|trivial|txmon)|bin/(pmdbg|pmclient|pmerr|genpmda)' | grep -E -v tutorials >>pcp-devel-files

# Patterns for files to be marked %%config(noreplace).
# Note: /etc/pcp.{conf,env,sh} are %%config but not noreplace
# and are treated specially below.
cat >confpath.list <<EOF
etc/zabbix/zabbix_agentd.d/
etc/sysconfig/
etc/cron.d/
etc/sasl2/
etc/pcp/
EOF

# functions to manipulate the manifest of files - keeping
# or culling given (or common) patterns from the stream.
keep() {
    grep -E $@ || return 0
}
cull() {
    grep -E -v $@ || return 0
}
total_manifest() {
    awk '{print $NF}' $DIST_MANIFEST
}
basic_manifest() {
    total_manifest | cull '/pcp-doc/|/testsuite/|/man/|pcp/examples/'
}

#
# Files for the various subpackages.  We use these subpackages
# to isolate the (somewhat exotic) dependencies for these tools.
# Likewise, for the pcp-pmda and pcp-testsuite subpackages.
#
total_manifest | keep 'tutorials|/html/|pcp-doc|man.*\.[1-9].*' | cull 'out' >pcp-doc-files
total_manifest | keep 'testsuite|pcpqa|etc/systemd/system|libpcp_fault|pcp/fault.h|pmcheck/pmda-sample' >pcp-testsuite-files

basic_manifest | keep "$PCP_GUI|pcp-gui|applications|pixmaps|hicolor" | cull 'pmtime.h' >pcp-gui-files
basic_manifest | keep 'selinux' | cull 'tmp|testsuite' >pcp-selinux-files
basic_manifest | keep 'zeroconf|daily[-_]report|/sa$' | cull 'pmcheck' >pcp-zeroconf-files
basic_manifest | grep -E -e 'pmiostat|pmrep|dstat|htop|pcp2csv' \
   -e 'pcp-atop|pcp-dmcache|pcp-dstat|pcp-free' \
   -e 'pcp-htop|pcp-ipcs|pcp-iostat|pcp-lvmcache|pcp-mpstat' \
   -e 'pcp-numastat|pcp-pidstat|pcp-shping|pcp-ss' \
   -e 'pcp-tapestat|pcp-uptime|pcp-verify|pcp-xsos' | \
   cull 'selinux|pmlogconf|pmieconf|pmrepconf' >pcp-system-tools-files
basic_manifest | keep 'geolocate' >pcp-geolocate-files
basic_manifest | keep 'pmseries_import' >pcp-import-pmseries-files
basic_manifest | keep 'sar2pcp' >pcp-import-sar2pcp-files
basic_manifest | keep 'iostat2pcp' >pcp-import-iostat2pcp-files
basic_manifest | keep 'sheet2pcp' >pcp-import-sheet2pcp-files
basic_manifest | keep 'mrtg2pcp' >pcp-import-mrtg2pcp-files
basic_manifest | keep 'ganglia2pcp' >pcp-import-ganglia2pcp-files
basic_manifest | keep 'collectl2pcp' >pcp-import-collectl2pcp-files
basic_manifest | keep 'pcp2arrow' >pcp-export-pcp2arrow-files
basic_manifest | keep 'pcp2elasticsearch' >pcp-export-pcp2elasticsearch-files
basic_manifest | keep 'pcp2influxdb' >pcp-export-pcp2influxdb-files
basic_manifest | keep 'pcp2xlsx' >pcp-export-pcp2xlsx-files
basic_manifest | keep 'pcp2graphite' >pcp-export-pcp2graphite-files
basic_manifest | keep 'pcp2json' >pcp-export-pcp2json-files
basic_manifest | keep 'pcp2openmetrics' >pcp-export-pcp2openmetrics-files
basic_manifest | keep 'pcp2spark' >pcp-export-pcp2spark-files
basic_manifest | keep 'pcp2xml' >pcp-export-pcp2xml-files
basic_manifest | keep 'pcp2zabbix' >pcp-export-pcp2zabbix-files
basic_manifest | keep 'zabbix|zbxpcp' | cull pcp2zabbix >pcp-export-zabbix-agent-files
basic_manifest | keep '(etc/pcp|pmdas)/activemq(/|$)' >pcp-pmda-activemq-files
basic_manifest | keep '(etc/pcp|pmdas)/amdgpu(/|$)' >pcp-pmda-amdgpu-files
basic_manifest | keep '(etc/pcp|pmdas)/apache(/|$)' >pcp-pmda-apache-files
basic_manifest | keep '(etc/pcp|pmdas)/bash(/|$)' >pcp-pmda-bash-files
basic_manifest | keep '(etc/pcp|pmdas)/bcc(/|$)' >pcp-pmda-bcc-files
basic_manifest | keep '(etc/pcp|pmdas)/bind2(/|$)' >pcp-pmda-bind2-files
basic_manifest | keep '(etc/pcp|pmdas)/bonding(/|$)' >pcp-pmda-bonding-files
basic_manifest | keep '(etc/pcp|pmdas)/bpf(/|$)' >pcp-pmda-bpf-files
basic_manifest | keep '(etc/pcp|pmdas)/bpftrace(/|$)' >pcp-pmda-bpftrace-files
basic_manifest | keep '(etc/pcp|pmdas)/cifs(/|$)' >pcp-pmda-cifs-files
basic_manifest | keep '(etc/pcp|pmdas)/cisco(/|$)' >pcp-pmda-cisco-files
basic_manifest | keep '(etc/pcp|pmdas)/dbping(/|$)' >pcp-pmda-dbping-files
basic_manifest | keep '(etc/pcp|pmdas|pmieconf)/dm(/|$)' >pcp-pmda-dm-files
basic_manifest | keep '(etc/pcp|pmdas)/denki(/|$)' >pcp-pmda-denki-files
basic_manifest | keep '(etc/pcp|pmdas)/docker(/|$)' >pcp-pmda-docker-files
basic_manifest | keep '(etc/pcp|pmdas)/ds389log(/|$)' >pcp-pmda-ds389log-files
basic_manifest | keep '(etc/pcp|pmdas)/ds389(/|$)' >pcp-pmda-ds389-files
basic_manifest | keep '(etc/pcp|pmdas)/elasticsearch(/|$)' >pcp-pmda-elasticsearch-files
basic_manifest | keep '(etc/pcp|pmdas)/farm(/|$)' >pcp-pmda-farm-files
basic_manifest | keep '(etc/pcp|pmdas)/gfs2(/|$)' >pcp-pmda-gfs2-files
basic_manifest | keep '(etc/pcp|pmdas)/gluster(/|$)' >pcp-pmda-gluster-files
basic_manifest | keep '(etc/pcp|pmdas)/gpfs(/|$)' >pcp-pmda-gpfs-files
basic_manifest | keep '(etc/pcp|pmdas)/gpsd(/|$)' >pcp-pmda-gpsd-files
basic_manifest | keep '(etc/pcp|pmdas)/hacluster(/|$)' >pcp-pmda-hacluster-files
basic_manifest | keep '(etc/pcp|pmdas)/haproxy(/|$)' >pcp-pmda-haproxy-files
basic_manifest | keep '(etc/pcp|pmdas)/hdb(/|$)' >pcp-pmda-hdb-files
basic_manifest | keep '(etc/pcp|pmdas)/infiniband(/|$)' >pcp-pmda-infiniband-files
basic_manifest | keep '(etc/pcp|pmdas)/json(/|$)' >pcp-pmda-json-files
basic_manifest | keep '(etc/pcp|pmdas)/libvirt(/|$)' >pcp-pmda-libvirt-files
basic_manifest | keep '(etc/pcp|pmdas)/lio(/|$)' >pcp-pmda-lio-files
basic_manifest | keep '(etc/pcp|pmdas)/lmsensors(/|$)' >pcp-pmda-lmsensors-files
basic_manifest | keep '(etc/pcp|pmdas)/logger(/|$)' >pcp-pmda-logger-files
basic_manifest | keep '(etc/pcp|pmdas)/lustre(/|$)' >pcp-pmda-lustre-files
basic_manifest | keep '(etc/pcp|pmdas)/lustrecomm(/|$)' >pcp-pmda-lustrecomm-files
basic_manifest | keep '(etc/pcp|pmdas)/memcache(/|$)' >pcp-pmda-memcache-files
basic_manifest | keep '(etc/pcp|pmdas)/mailq(/|$)' >pcp-pmda-mailq-files
basic_manifest | keep '(etc/pcp|pmdas)/mic(/|$)' >pcp-pmda-mic-files
basic_manifest | keep '(etc/pcp|pmdas)/mounts(/|$)' >pcp-pmda-mounts-files
basic_manifest | keep '(etc/pcp|pmdas)/mongodb(/|$)' >pcp-pmda-mongodb-files
basic_manifest | keep '(etc/pcp|pmdas|pmieconf)/mssql(/|$)' >pcp-pmda-mssql-files
basic_manifest | keep '(etc/pcp|pmdas)/mysql(/|$)' >pcp-pmda-mysql-files
basic_manifest | keep '(etc/pcp|pmdas)/named(/|$)' >pcp-pmda-named-files
basic_manifest | keep '(etc/pcp|pmdas)/netfilter(/|$)' >pcp-pmda-netfilter-files
basic_manifest | keep '(etc/pcp|pmdas)/netcheck(/|$)' >pcp-pmda-netcheck-files
basic_manifest | keep '(etc/pcp|pmdas)/news(/|$)' >pcp-pmda-news-files
basic_manifest | keep '(etc/pcp|pmdas)/nfsclient(/|$)' >pcp-pmda-nfsclient-files
basic_manifest | keep '(etc/pcp|pmdas)/nginx(/|$)' >pcp-pmda-nginx-files
basic_manifest | keep '(etc/pcp|pmdas)/nutcracker(/|$)' >pcp-pmda-nutcracker-files
basic_manifest | keep '(etc/pcp|pmdas)/nvidia(/|$)' >pcp-pmda-nvidia-files
basic_manifest | keep '(etc/pcp|pmdas)/openmetrics(/|$)' >pcp-pmda-openmetrics-files
basic_manifest | keep '(etc/pcp|pmdas|pmieconf)/openvswitch(/|$)' >pcp-pmda-openvswitch-files
basic_manifest | keep '(etc/pcp|pmdas)/oracle(/|$)' >pcp-pmda-oracle-files
basic_manifest | keep '(etc/pcp|pmdas)/pdns(/|$)' >pcp-pmda-pdns-files
basic_manifest | keep '(etc/pcp|pmdas)/perfevent(/|$)' >pcp-pmda-perfevent-files
basic_manifest | keep '(etc/pcp|pmdas)/podman(/|$)' >pcp-pmda-podman-files
basic_manifest | keep '(etc/pcp|pmdas)/postfix(/|$)' >pcp-pmda-postfix-files
basic_manifest | keep '(etc/pcp|pmdas)/postgresql(/|$)' >pcp-pmda-postgresql-files
basic_manifest | keep '(etc/pcp|pmdas)/rabbitmq(/|$)' >pcp-pmda-rabbitmq-files
basic_manifest | keep '(etc/pcp|pmdas)/redis(/|$)' >pcp-pmda-redis-files
basic_manifest | keep '(etc/pcp|pmdas)/resctrl(/|$)|sys-fs-resctrl' >pcp-pmda-resctrl-files
basic_manifest | keep '(etc/pcp|pmdas)/rocestat(/|$)' >pcp-pmda-rocestat-files
basic_manifest | keep '(etc/pcp|pmdas)/roomtemp(/|$)' >pcp-pmda-roomtemp-files
basic_manifest | keep '(etc/pcp|pmdas)/rpm(/|$)' >pcp-pmda-rpm-files
basic_manifest | keep '(etc/pcp|pmdas)/rsyslog(/|$)' >pcp-pmda-rsyslog-files
basic_manifest | keep '(etc/pcp|pmdas)/samba(/|$)' >pcp-pmda-samba-files
basic_manifest | keep '(etc/pcp|pmdas)/sendmail(/|$)' >pcp-pmda-sendmail-files
basic_manifest | keep '(etc/pcp|pmdas)/shping(/|$)' >pcp-pmda-shping-files
basic_manifest | keep '(etc/pcp|pmdas)/slurm(/|$)' >pcp-pmda-slurm-files
basic_manifest | keep '(etc/pcp|pmdas)/smart(/|$)' >pcp-pmda-smart-files
basic_manifest | keep '(etc/pcp|pmdas)/snmp(/|$)' >pcp-pmda-snmp-files
basic_manifest | keep '(etc/pcp|pmdas)/sockets(/|$)' >pcp-pmda-sockets-files
basic_manifest | keep '(etc/pcp|pmdas)/statsd(/|$)' >pcp-pmda-statsd-files
basic_manifest | keep '(etc/pcp|pmdas)/summary(/|$)' >pcp-pmda-summary-files
basic_manifest | keep '(etc/pcp|pmdas)/systemd(/|$)' >pcp-pmda-systemd-files
basic_manifest | keep '(etc/pcp|pmdas)/trace(/|$)' >pcp-pmda-trace-files
basic_manifest | keep '(etc/pcp|pmdas)/unbound(/|$)' >pcp-pmda-unbound-files
basic_manifest | keep '(etc/pcp|pmdas)/uwsgi(/|$)' >pcp-pmda-uwsgi-files
basic_manifest | keep '(etc/pcp|pmdas)/weblog(/|$)' >pcp-pmda-weblog-files
basic_manifest | keep '(etc/pcp|pmdas)/zimbra(/|$)' >pcp-pmda-zimbra-files
basic_manifest | keep '(etc/pcp|pmdas)/zswap(/|$)' >pcp-pmda-zswap-files

rm -f packages.list
for pmda_package in \
    activemq amdgpu apache \
    bash bcc bind2 bonding bpf bpftrace \
    cifs cisco \
    dbping denki docker dm ds389 ds389log \
    elasticsearch \
    farm \
    gfs2 gluster gpfs gpsd \
    hacluster haproxy hdb \
    infiniband \
    json \
    libvirt lio lmsensors logger lustre lustrecomm \
    mailq memcache mic mounts mongodb mssql mysql \
    named netcheck netfilter news nfsclient nginx \
    nutcracker nvidia \
    openmetrics openvswitch oracle \
    pdns perfevent podman postfix postgresql \
    rabbitmq redis resctrl rocestat roomtemp rpm rsyslog \
    samba sendmail shping slurm smart snmp \
    sockets statsd summary systemd \
    unbound uwsgi \
    trace \
    weblog \
    zimbra zswap ; \
do \
    pmda_packages="$pmda_packages pcp-pmda-$pmda_package"; \
done

for import_package in \
    pmseries \
    collectl2pcp iostat2pcp ganglia2pcp mrtg2pcp sar2pcp sheet2pcp ; \
do \
    import_packages="$import_packages pcp-import-$import_package"; \
done

for export_package in \
    pcp2arrow pcp2elasticsearch pcp2graphite pcp2influxdb pcp2json \
    pcp2openmetrics pcp2spark pcp2xlsx pcp2xml pcp2zabbix zabbix-agent ; \
do \
    export_packages="$export_packages pcp-export-$export_package"; \
done

for subpackage in \
    pcp-conf pcp-gui pcp-doc pcp-libs pcp-devel pcp-libs-devel \
    pcp-geolocate pcp-selinux pcp-system-tools pcp-testsuite pcp-zeroconf \
    $pmda_packages $import_packages $export_packages ; \
do \
    echo $subpackage >> packages.list; \
done

rm -f *-files.rpm *-tmpfiles.rpm
sort -u $DIST_MANIFEST | awk '
function loadfiles(files) {
    system ("touch " files"-files");
    filelist=files"-files";
    while (getline < filelist) {
        if (length(pkg[$0]) > 0 && pkg[$0] != files)
            print "Dup: ", $0, " package: ", pkg[$0], " and ", files;
        if (length(pkg[$0]) == 0)
            pkg[$0] = files;
    }
}
BEGIN {
    while (getline < "packages.list") loadfiles($0);
    while (getline < "confpath.list") conf[nconf++]=$0;
}
{
    if (pkg[$NF]) p=pkg[$NF];
    else p="pcp";
    f=p"-files.rpm";
}
$1 == "d" {
            if (match ($5, "'$PCP_RUN_DIR'")) {
                printf ("%%%%ghost ") >> f;
            }
            if (match ($5, "'$PCP_VAR_DIR'/testsuite")) {
                $3 = $4 = "pcpqa";
            }
            printf ("%%%%dir %%%%attr(%s,%s,%s) %s\n", $2, $3, $4, $5) >> f
          }
$1 == "f" && $6 ~ "etc/pcp\\.conf" { printf ("%%%%config ") >> f; }
$1 == "f" && $6 ~ "etc/pcp\\.env"  { printf ("%%%%config ") >> f; }
$1 == "f" && $6 ~ "etc/pcp\\.sh"   { printf ("%%%%config ") >> f; }
$1 == "f" {
            for (i=0; i < nconf; i++) {
                if ($6 ~ conf[i]) {
                    printf ("%%%%config(noreplace) ") >> f;
                    break;
                }
            }
            if (match ($6, "'$PCP_VAR_DIR'/testsuite")) {
                $3 = $4 = "pcpqa";
            }
            if (match ($6, "'$PCP_MAN_DIR'") || match ($6, "'$PCP_DOC_DIR'")) {
                printf ("%%%%doc ") >> f;
            }
            printf ("%%%%attr(%s,%s,%s) %s\n", $2, $3, $4, $6) >> f
          }
$1 == "l" {
%if !%{disable_systemd}
            if (match ($3, "'$PCP_VAR_DIR'")) {
                print $3 >> p"-tmpfiles";
                if (length(tmpfiles[p]) == 0) {
                    printf ("'$PCP_SYSTEMDTMPFILES_DIR'/%s.conf\n", p) >> f;
                    tmpfiles[p] = p;
                }
            }
%endif
            print $3 >> f;
          }'

%if !%{disable_systemd}
mkdir -p $DIST_ROOT/$PCP_SYSTEMDTMPFILES_DIR
sort -u $DIST_TMPFILES | awk '
function loadtmpfiles(files) {
    system ("touch " files"-tmpfiles");
    filelist=files"-tmpfiles";
    while (getline < filelist) {
        if (pkg[$0] && pkg[$0] != files)
            print "Dup: ", $0, " package: ", pkg[$0], " and ", files;
        pkg[$0] = files;
    }
}
BEGIN {
    while (getline < "packages.list") loadtmpfiles($0);
}
{
    if (pkg[$2]) p=pkg[$2];
    else p="pcp";
    f=p".conf";
    printf ("%s\n", $0) >> f;
}'

%if %{disable_mssql}
# TODO: integrate better into the PCP build (via autoconf)
# so that this and other mssql artifacts are not generated.
rm -f pcp-pmda-mssql.conf
%endif

for tmpfile in *.conf ; \
do \
    mv $tmpfile $DIST_ROOT/$PCP_SYSTEMDTMPFILES_DIR/$tmpfile; \
done
%endif

%pre testsuite
%if !%{disable_selinux}
%selinux_relabel_pre -s targeted
%endif
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 11
%elif 0%{?fedora} >= 32 || 0%{?rhel} >= 9
echo u pcpqa - \"PCP Quality Assurance\" %{_testsdir} /bin/bash | \
  systemd-sysusers --replace=/usr/lib/sysusers.d/pcp-testsuite.conf -
%else
getent group pcpqa >/dev/null || groupadd -r pcpqa
getent passwd pcpqa >/dev/null || \
  useradd -c "PCP Quality Assurance" -g pcpqa -d %{_testsdir} -M -r -s /bin/bash pcpqa 2>/dev/null
%endif
test -d %{_testsdir} || mkdir -p -m 755 %{_testsdir}
chown -R pcpqa:pcpqa %{_testsdir} 2>/dev/null
exit 0

%post testsuite
PCP_PMDAS_DIR=%{_pmdasdir}
PCP_PMCDCONF_PATH=%{_confdir}/pmcd/pmcd.conf
%if !%{disable_selinux}
PCP_SELINUX_DIR=%{_selinuxdir}
semodule -r pcpqa >/dev/null 2>&1 || true
%selinux_modules_install -s targeted "$PCP_SELINUX_DIR/pcp-testsuite.pp.bz2"
%selinux_relabel_post -s targeted
%endif
chown -R pcpqa:pcpqa %{_testsdir} 2>/dev/null
# auto-install important PMDAs for testing (if not present already)
needinstall='sample simple'
for PMDA in $needinstall ; do
    if ! grep -q "$PMDA/pmda$PMDA" "$PCP_PMCDCONF_PATH"
    then
	%{install_file "$PCP_PMDAS_DIR/$PMDA" .NeedInstall}
    fi
done
%if 0%{?rhel}
%if !%{disable_systemd}
    systemctl restart pcp-reboot-init pmcd pmlogger >/dev/null 2>&1
    systemctl enable pcp-reboot-init pmcd pmlogger >/dev/null 2>&1
%else
    /sbin/chkconfig --add pmcd >/dev/null 2>&1
    /sbin/chkconfig --add pmlogger >/dev/null 2>&1
    /sbin/service pmcd condrestart
    /sbin/service pmlogger condrestart
%endif
%endif
exit 0

%if !%{disable_selinux}
%postun testsuite
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s targeted pcp-testsuite
    %selinux_relabel_post -s targeted
fi
%endif

%pre
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 11
%elif 0%{?fedora} >= 32 || 0%{?rhel} >= 9
echo u pcp - \"Performance Co-Pilot\" %{_localstatedir}/lib/pcp | \
  systemd-sysusers --replace=/usr/lib/sysusers.d/pcp.conf -
%else
getent group pcp >/dev/null || groupadd -r pcp
getent passwd pcp >/dev/null || \
  useradd -c "Performance Co-Pilot" -g pcp -d %{_localstatedir}/lib/pcp -M -r -s /sbin/nologin pcp
%endif
exit 0

%if !%{disable_systemd}
%preun pmda-systemd
%{pmda_remove "$1" "systemd"}
%endif

%if !%{disable_infiniband}
%preun pmda-infiniband
%{pmda_remove "$1" "infiniband"}
%endif

%if !%{disable_perfevent}
%preun pmda-perfevent
%{pmda_remove "$1" "perfevent"}
%endif

%preun pmda-podman
%{pmda_remove "$1" "podman"}

%if !%{disable_statsd}
%preun pmda-statsd
%{pmda_remove "$1" "statsd"}
%endif

%if !%{disable_json}
%preun pmda-json
%{pmda_remove "$1" "json"}
%endif

%preun pmda-nginx
%{pmda_remove "$1" "nginx"}

%preun pmda-oracle
%{pmda_remove "$1" "oracle"}

%preun pmda-postgresql
%{pmda_remove "$1" "postgresql"}

%preun pmda-postfix
%{pmda_remove "$1" "postfix"}

%preun pmda-elasticsearch
%{pmda_remove "$1" "elasticsearch"}

%preun pmda-openvswitch
%{pmda_remove "$1" "openvswitch"}

%preun pmda-rabbitmq
%{pmda_remove "$1" "rabbitmq"}

%preun pmda-uwsgi
%{pmda_remove "$1" "uwsgi"}

%if !%{disable_snmp}
%preun pmda-snmp
%{pmda_remove "$1" "snmp"}
%endif

%if !%{disable_mysql}
%preun pmda-mysql
%{pmda_remove "$1" "mysql"}
%endif

%preun pmda-activemq
%{pmda_remove "$1" "activemq"}

%preun pmda-bind2
%{pmda_remove "$1" "bind2"}

%preun pmda-bonding
%{pmda_remove "$1" "bonding"}

%preun pmda-dbping
%{pmda_remove "$1" "dbping"}

%preun pmda-denki
%{pmda_remove "$1" "denki"}

%preun pmda-docker
%{pmda_remove "$1" "docker"}

%preun pmda-ds389
%{pmda_remove "$1" "ds389"}

%preun pmda-ds389log
%{pmda_remove "$1" "ds389log"}

%preun pmda-gpfs
%{pmda_remove "$1" "gpfs"}

%preun pmda-gpsd
%{pmda_remove "$1" "gpsd"}

%preun pmda-lio
%{pmda_remove "$1" "lio"}

%preun pmda-openmetrics
%{pmda_remove "$1" "openmetrics"}

%preun pmda-lustre
%{pmda_remove "$1" "lustre"}

%preun pmda-lustrecomm
%{pmda_remove "$1" "lustrecomm"}

%preun pmda-memcache
%{pmda_remove "$1" "memcache"}

%preun pmda-named
%{pmda_remove "$1" "named"}

%preun pmda-netfilter
%{pmda_remove "$1" "netfilter"}

%preun pmda-news
%{pmda_remove "$1" "news"}

%preun pmda-nfsclient
%{pmda_remove "$1" "nfsclient"}

%if !%{disable_nutcracker}
%preun pmda-nutcracker
%{pmda_remove "$1" "nutcracker"}
%endif

%preun pmda-pdns
%{pmda_remove "$1" "pdns"}

%preun pmda-rsyslog
%{pmda_remove "$1" "rsyslog"}

%preun pmda-redis
%{pmda_remove "$1" "redis"}

%preun pmda-samba
%{pmda_remove "$1" "samba"}

%preun pmda-zimbra
%{pmda_remove "$1" "zimbra"}

%preun pmda-dm
%{pmda_remove "$1" "dm"}

%if !%{disable_bcc}
%preun pmda-bcc
%{pmda_remove "$1" "bcc"}
%endif

%if !%{disable_bpf}
%preun pmda-bpf
%{pmda_remove "$1" "bpf"}
%endif

%if !%{disable_bpftrace}
%preun pmda-bpftrace
%{pmda_remove "$1" "bpftrace"}
%endif

%if !%{disable_python3}
%preun pmda-hdb
%{pmda_remove "$1" "hdb"}

%preun pmda-gluster
%{pmda_remove "$1" "gluster"}

%preun pmda-zswap
%{pmda_remove "$1" "zswap"}

%preun pmda-unbound
%{pmda_remove "$1" "unbound"}

%preun pmda-mic
%{pmda_remove "$1" "mic"}

%preun pmda-haproxy
%{pmda_remove "$1" "haproxy"}

%preun pmda-libvirt
%{pmda_remove "$1" "libvirt"}

%preun pmda-lmsensors
%{pmda_remove "$1" "lmsensors"}

%if !%{disable_mongodb}
%preun pmda-mongodb
%{pmda_remove "$1" "mongodb"}
%endif

%if !%{disable_mssql}
%preun pmda-mssql
%{pmda_remove "$1" "mssql"}
%endif

%preun pmda-netcheck
%{pmda_remove "$1" "netcheck"}

%preun pmda-rocestat
%{pmda_remove "$1" "rocestat"}

%endif

%preun pmda-apache
%{pmda_remove "$1" "apache"}

%preun pmda-bash
%{pmda_remove "$1" "bash"}

%preun pmda-cifs
%{pmda_remove "$1" "cifs"}

%preun pmda-cisco
%{pmda_remove "$1" "cisco"}

%preun pmda-farm
%{pmda_remove "$1" "farm"}

%if !%{disable_gfs2}
%preun pmda-gfs2
%{pmda_remove "$1" "gfs2"}
%endif

%preun pmda-hacluster
%{pmda_remove "$1" "hacluster"}

%preun pmda-logger
%{pmda_remove "$1" "logger"}

%preun pmda-mailq
%{pmda_remove "$1" "mailq"}

%preun pmda-mounts
%{pmda_remove "$1" "mounts"}

%preun pmda-nvidia-gpu
%{pmda_remove "$1" "nvidia"}

%if !%{disable_resctrl}
%preun pmda-resctrl
%{pmda_remove "$1" "resctrl"}
%endif

%preun pmda-roomtemp
%{pmda_remove "$1" "roomtemp"}

%preun pmda-sendmail
%{pmda_remove "$1" "sendmail"}

%preun pmda-shping
%{pmda_remove "$1" "shping"}

%preun pmda-smart
%{pmda_remove "$1" "smart"}

%preun pmda-sockets
%{pmda_remove "$1" "sockets"}

%preun pmda-summary
%{pmda_remove "$1" "summary"}

%preun pmda-trace
%{pmda_remove "$1" "trace"}

%preun pmda-weblog
%{pmda_remove "$1" "weblog"}

%if !%{disable_amdgpu}
%preun pmda-amdgpu
%{pmda_remove "$1" "amdgpu"}
%endif

%preun
if [ "$1" -eq 0 ]
then
    # stop daemons before erasing the package
    %if !%{disable_systemd}
       %systemd_preun pmlogger_check.timer pmlogger_daily.timer pmlogger_farm_check.timer pmlogger_farm_check.service pmlogger_farm.service pmlogger.service pmie_check.timer pmie_daily.timer pmie_farm_check.timer pmie_farm_check.service pmie_farm.service pmie.service pmproxy.service pmfind.service pmcd.service pcp-reboot-init.service

       systemctl stop pmlogger.service pmie.service pmproxy.service pmfind.service pmcd.service pcp-reboot-init.service >/dev/null 2>&1
    %else
       /sbin/service pmlogger stop >/dev/null 2>&1
       /sbin/service pmie stop >/dev/null 2>&1
       /sbin/service pmproxy stop >/dev/null 2>&1
       /sbin/service pmcd stop >/dev/null 2>&1

       /sbin/chkconfig --del pcp >/dev/null 2>&1
       /sbin/chkconfig --del pmcd >/dev/null 2>&1
       /sbin/chkconfig --del pmlogger >/dev/null 2>&1
       /sbin/chkconfig --del pmie >/dev/null 2>&1
       /sbin/chkconfig --del pmproxy >/dev/null 2>&1
    %endif
    # cleanup namespace state/flag, may still exist
    PCP_PMNS_DIR=%{_pmnsdir}
    rm -f "$PCP_PMNS_DIR/.NeedRebuild" >/dev/null 2>&1
fi

%post zeroconf
PCP_PMDAS_DIR=%{_pmdasdir}
PCP_SYSCONFIG_DIR=%{_sysconfdir}/sysconfig
PCP_PMCDCONF_PATH=%{_confdir}/pmcd/pmcd.conf
# auto-install important PMDAs for RH Support (if not present already)
for PMDA in dm nfsclient openmetrics ; do
    if ! grep -q "$PMDA/pmda$PMDA" "$PCP_PMCDCONF_PATH"
    then
        %{install_file "$PCP_PMDAS_DIR/$PMDA" .NeedInstall}
    fi
done
# managed via /usr/lib/systemd/system-preset/90-default.preset nowadays:
%if 0%{?fedora} > 40 || 0%{?rhel} > 9
    for s in pmcd pmlogger pmie; do
        systemctl --quiet is-enabled $s && systemctl restart $s >/dev/null 2>&1
    done
%else  # old-school methods follow
%if !%{disable_systemd}
    systemctl restart pmcd pmlogger pmie >/dev/null 2>&1
    systemctl enable pmcd pmlogger pmie >/dev/null 2>&1
%else
    /sbin/chkconfig --add pmcd >/dev/null 2>&1
    /sbin/chkconfig --add pmlogger >/dev/null 2>&1
    /sbin/chkconfig --add pmie >/dev/null 2>&1
    /sbin/service pmcd condrestart
    /sbin/service pmlogger condrestart
    /sbin/service pmie condrestart
%endif
%endif

%post
PCP_PMNS_DIR=%{_pmnsdir}
PCP_LOG_DIR=%{_logsdir}
%{install_file "$PCP_PMNS_DIR" .NeedRebuild}
%{install_file "$PCP_LOG_DIR/pmlogger" .NeedRewrite}
%if !%{disable_systemd}
    # clean up any stale symlinks for deprecated pm*-poll services
    rm -f %{_sysconfdir}/systemd/system/pm*.requires/pm*-poll.* >/dev/null 2>&1 || true
    systemctl restart pcp-reboot-init >/dev/null 2>&1
    systemctl enable pcp-reboot-init >/dev/null 2>&1

    %systemd_postun_with_restart pmcd.service
    %systemd_post pmcd.service
    %systemd_postun_with_restart pmlogger.service
    %systemd_post pmlogger.service
    %systemd_postun_with_restart pmie.service
    %systemd_post pmie.service
    %systemd_postun_with_restart pmproxy.service
    %systemd_post pmproxy.service
    %systemd_post pmfind.service
%else
    /sbin/chkconfig --add pmcd >/dev/null 2>&1
    /sbin/service pmcd condrestart
    /sbin/chkconfig --add pmlogger >/dev/null 2>&1
    /sbin/service pmlogger condrestart
    /sbin/chkconfig --add pmie >/dev/null 2>&1
    /sbin/service pmie condrestart
    /sbin/chkconfig --add pmproxy >/dev/null 2>&1
    /sbin/service pmproxy condrestart
%endif
%{rebuild_pmns "$PCP_PMNS_DIR" .NeedRebuild}

%if 0%{?fedora} >= 26 || 0%{?rhel} > 7
%ldconfig_scriptlets libs
%else
%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%endif

%if !%{disable_selinux}
%pre selinux
%selinux_relabel_pre -s targeted

%post selinux
PCP_SELINUX_DIR=%{_selinuxdir}
semodule -r pcpupstream-container >/dev/null 2>&1 || true
semodule -r pcpupstream-docker >/dev/null 2>&1 || true
semodule -r pcpupstream >/dev/null 2>&1 || true
%selinux_modules_install -s targeted "$PCP_SELINUX_DIR/pcp.pp.bz2"
%selinux_relabel_post -s targeted

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s targeted pcp
    %selinux_relabel_post -s targeted
fi
%endif

%files -f pcp-files.rpm
%doc CHANGELOG COPYING INSTALL.md README.md VERSION.pcp pcp.lsm
%ghost %dir %attr(0775,pcp,pcp) %{_localstatedir}/run/pcp

%files conf -f pcp-conf-files.rpm

%files libs -f pcp-libs-files.rpm

%files libs-devel -f pcp-libs-devel-files.rpm

%files devel -f pcp-devel-files.rpm

%files doc -f pcp-doc-files.rpm

%if !%{disable_selinux}
%files selinux -f pcp-selinux-files.rpm
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/targeted/active/modules/200/pcp
%endif

%if !%{disable_qt}
%files gui -f pcp-gui-files.rpm
%endif

%files testsuite -f pcp-testsuite-files.rpm

%if !%{disable_infiniband}
%files pmda-infiniband -f pcp-pmda-infiniband-files.rpm
%endif

%files pmda-podman -f pcp-pmda-podman-files.rpm

%if !%{disable_statsd}
%files pmda-statsd -f pcp-pmda-statsd-files.rpm
%endif

%if !%{disable_perfevent}
%files pmda-perfevent -f pcp-pmda-perfevent-files.rpm
%endif

%if !%{disable_perl}
%files pmda-activemq -f pcp-pmda-activemq-files.rpm
%endif

%if !%{disable_perl}
%files pmda-bind2 -f pcp-pmda-bind2-files.rpm
%endif

%if !%{disable_nutcracker}
%files pmda-nutcracker -f pcp-pmda-nutcracker-files.rpm
%endif

%if !%{disable_python3}
%files pmda-elasticsearch -f pcp-pmda-elasticsearch-files.rpm
%endif

%if !%{disable_perl}
%files pmda-redis -f pcp-pmda-redis-files.rpm

%files pmda-bonding -f pcp-pmda-bonding-files.rpm

%files pmda-dbping -f pcp-pmda-dbping-files.rpm

%files pmda-ds389log -f pcp-pmda-ds389log-files.rpm

%files pmda-ds389 -f pcp-pmda-ds389-files.rpm

%files pmda-gpfs -f pcp-pmda-gpfs-files.rpm

%files pmda-gpsd -f pcp-pmda-gpsd-files.rpm

%files pmda-lustre -f pcp-pmda-lustre-files.rpm

%files pmda-memcache -f pcp-pmda-memcache-files.rpm

%files pmda-named -f pcp-pmda-named-files.rpm

%files pmda-netfilter -f pcp-pmda-netfilter-files.rpm

%files pmda-news -f pcp-pmda-news-files.rpm

%files pmda-pdns -f pcp-pmda-pdns-files.rpm

%files pmda-rsyslog -f pcp-pmda-rsyslog-files.rpm

%files pmda-samba -f pcp-pmda-samba-files.rpm

%files pmda-slurm -f pcp-pmda-slurm-files.rpm

%files pmda-zimbra -f pcp-pmda-zimbra-files.rpm
%endif

%files pmda-denki -f pcp-pmda-denki-files.rpm

%files pmda-docker -f pcp-pmda-docker-files.rpm

%files pmda-lustrecomm -f pcp-pmda-lustrecomm-files.rpm

%if !%{disable_mysql}
%files pmda-mysql -f pcp-pmda-mysql-files.rpm
%endif

%files pmda-nginx -f pcp-pmda-nginx-files.rpm

%if !%{disable_perl}
%files pmda-postfix -f pcp-pmda-postfix-files.rpm
%endif

%if !%{disable_python3}
%files pmda-postgresql -f pcp-pmda-postgresql-files.rpm
%endif

%if !%{disable_perl}
%files pmda-oracle -f pcp-pmda-oracle-files.rpm
%endif

%if !%{disable_perl}
%files pmda-snmp -f pcp-pmda-snmp-files.rpm
%endif

%files pmda-dm -f pcp-pmda-dm-files.rpm

%if !%{disable_bcc}
%files pmda-bcc -f pcp-pmda-bcc-files.rpm
%endif

%if !%{disable_bpf}
%files pmda-bpf -f pcp-pmda-bpf-files.rpm
%endif

%if !%{disable_bpftrace}
%files pmda-bpftrace -f pcp-pmda-bpftrace-files.rpm
%endif

%if !%{disable_python3}
%files geolocate -f pcp-geolocate-files.rpm

%files pmda-gluster -f pcp-pmda-gluster-files.rpm

%files pmda-zswap -f pcp-pmda-zswap-files.rpm

%files pmda-unbound -f pcp-pmda-unbound-files.rpm

%files pmda-mic -f pcp-pmda-mic-files.rpm

%files pmda-haproxy -f pcp-pmda-haproxy-files.rpm

%files pmda-lmsensors -f pcp-pmda-lmsensors-files.rpm

%if !%{disable_mongodb}
%files pmda-mongodb -f pcp-pmda-mongodb-files.rpm
%endif

%if !%{disable_mssql}
%files pmda-mssql -f pcp-pmda-mssql-files.rpm
%endif

%files pmda-netcheck -f pcp-pmda-netcheck-files.rpm

%files pmda-nfsclient -f pcp-pmda-nfsclient-files.rpm

%files pmda-openvswitch -f pcp-pmda-openvswitch-files.rpm

%files pmda-rabbitmq -f pcp-pmda-rabbitmq-files.rpm

%files pmda-rocestat -f pcp-pmda-rocestat-files.rpm

%files pmda-uwsgi -f pcp-pmda-uwsgi-files.rpm

%files export-pcp2graphite -f pcp-export-pcp2graphite-files.rpm

%files export-pcp2json -f pcp-export-pcp2json-files.rpm

%files export-pcp2openmetrics -f pcp-export-pcp2openmetrics-files.rpm

%files export-pcp2spark -f pcp-export-pcp2spark-files.rpm

%files export-pcp2xml -f pcp-export-pcp2xml-files.rpm

%files export-pcp2zabbix -f pcp-export-pcp2zabbix-files.rpm
%endif

%if !%{disable_python3}
%files export-pcp2elasticsearch -f pcp-export-pcp2elasticsearch-files.rpm
%endif

%if !%{disable_python3}
%files export-pcp2influxdb -f pcp-export-pcp2influxdb-files.rpm
%endif

%if !%{disable_arrow}
%files export-pcp2arrow -f pcp-export-pcp2arrow-files.rpm
%endif

%if !%{disable_xlsx}
%files export-pcp2xlsx -f pcp-export-pcp2xlsx-files.rpm
%endif

%files export-zabbix-agent -f pcp-export-zabbix-agent-files.rpm

%if !%{disable_json}
%files pmda-json -f pcp-pmda-json-files.rpm
%endif

%if !%{disable_python3}
%files pmda-hdb -f pcp-pmda-hdb-files.rpm

%files pmda-libvirt -f pcp-pmda-libvirt-files.rpm

%files pmda-lio -f pcp-pmda-lio-files.rpm

%files pmda-openmetrics -f pcp-pmda-openmetrics-files.rpm
%endif

%if !%{disable_amdgpu}
%files pmda-amdgpu -f pcp-pmda-amdgpu-files.rpm
%endif

%files pmda-apache -f pcp-pmda-apache-files.rpm

%files pmda-bash -f pcp-pmda-bash-files.rpm

%files pmda-cifs -f pcp-pmda-cifs-files.rpm

%files pmda-cisco -f pcp-pmda-cisco-files.rpm

%files pmda-farm -f pcp-pmda-farm-files.rpm

%if !%{disable_gfs2}
%files pmda-gfs2 -f pcp-pmda-gfs2-files.rpm
%endif

%files pmda-hacluster -f pcp-pmda-hacluster-files.rpm

%files pmda-logger -f pcp-pmda-logger-files.rpm

%files pmda-mailq -f pcp-pmda-mailq-files.rpm

%files pmda-mounts -f pcp-pmda-mounts-files.rpm

%files pmda-nvidia-gpu -f pcp-pmda-nvidia-files.rpm

%if !%{disable_resctrl}
%files pmda-resctrl -f pcp-pmda-resctrl-files.rpm
%endif

%files pmda-roomtemp -f pcp-pmda-roomtemp-files.rpm

%files pmda-sendmail -f pcp-pmda-sendmail-files.rpm

%files pmda-shping -f pcp-pmda-shping-files.rpm

%files pmda-smart -f pcp-pmda-smart-files.rpm

%files pmda-sockets -f pcp-pmda-sockets-files.rpm

%files pmda-summary -f pcp-pmda-summary-files.rpm

%if !%{disable_systemd}
%files pmda-systemd -f pcp-pmda-systemd-files.rpm
%endif

%files pmda-trace -f pcp-pmda-trace-files.rpm

%files pmda-weblog -f pcp-pmda-weblog-files.rpm

%if !%{disable_python3}
%files import-pmseries -f pcp-import-pmseries-files.rpm
%endif

%if !%{disable_perl}
%files import-sar2pcp -f pcp-import-sar2pcp-files.rpm

%files import-iostat2pcp -f pcp-import-iostat2pcp-files.rpm

#TODO:
#%%files import-sheet2pcp -f pcp-import-sheet2pcp-files.rpm

%files import-mrtg2pcp -f pcp-import-mrtg2pcp-files.rpm

%files import-ganglia2pcp -f pcp-import-ganglia2pcp-files.rpm
%endif

%files import-collectl2pcp -f pcp-import-collectl2pcp-files.rpm

%if !%{disable_perl}
%files -n perl-PCP-PMDA -f perl-pcp-pmda.list

%files -n perl-PCP-MMV -f perl-pcp-mmv.list

%files -n perl-PCP-LogImport -f perl-pcp-logimport.list

%files -n perl-PCP-LogSummary -f perl-pcp-logsummary.list
%endif

%if !%{disable_python3}
%files -n python3-pcp -f python3-pcp.list.rpm
%endif

%files system-tools -f pcp-system-tools-files.rpm

%files zeroconf -f pcp-zeroconf-files.rpm

%changelog
* Thu Jul 31 2025 Nathan Scott <nathans@redhat.com> - 7.0.0-1
- Latest release.
