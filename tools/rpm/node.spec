# Copyright (c) 2013, StrongLoop, Inc. <callback@strongloop.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# This is updated by rpmbuild.sh.
%define _version 4.x.y

%{?scl:%scl_package node}
%{!?scl:%global pkg_name %{name}}

Name: %{?scl_prefix}node
Version: %{_version}
Release: 2
Summary: Node.js is a platform for building fast, scalable network applications.
Group: Development/Languages
License: MIT
URL: https://nodejs.org/
Source0: http://nodejs.org/dist/v%{_version}/node-v%{_version}.tar.gz
#BuildRequires: gcc
#BuildRequires: gcc-c++
#BuildRequires: glibc-devel
#BuildRequires: make
#BuildRequires: python

%{?scl:Requires: %scl_runtime}
BuildRequires: scl-utils-build
Requires: scl-utils
BuildRequires: %{scl_prefix}gcc-c++
# full devtoolset3 is much too large (and has broken java deps)

# Conflicts with the HAM radio package.
#Conflicts: node <= 0.3.2-11

# Conflicts with the Fedora node.js package.
#Conflicts: nodejs


%description
Node.js is a platform built on Chrome's JavaScript runtime for easily
building fast, scalable network applications.

Node.js uses an event-driven, non-blocking I/O model that makes it
lightweight and efficient, perfect for data-intensive real-time
applications that run across distributed devices.


%prep
%setup -q -n %{pkg_name}-%{_version}


%build
%ifarch arm
%define _dest_cpu arm
%endif

%ifarch i386 i686
%define _dest_cpu ia32
%endif

%ifarch x86_64
%define _dest_cpu x64
%endif

./configure --prefix=%{_prefix} --dest-cpu=%{_dest_cpu}
make %{?_smp_mflags}


%check
#make test


# Use mildly hard-coded paths in the install and files targets for now.
# _libdir is /usr/lib64 on some systems but the installer always installs
# to /usr/lib.  I have commits sitting in a branch that add --libdir and
# --mandir configure switches to the configure script but it's debatable
# if it's worth the extra complexity.
%install
export DONT_STRIP=1  # Don't strip debug symbols for now.
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}/%{_prefix}/lib/dtrace/  # No systemtap support.
install -m 755 -d %{buildroot}/%{_prefix}/lib/node_modules/
install -m 755 -d %{buildroot}/%{_datadir}/%{name}

# Remove junk files from node_modules/ - we should probably take care of
# this in the installer.
for FILE in .gitmodules .gitignore .npmignore .travis.yml \*.py[co]; do
  find %{buildroot}/%{_prefix}/lib/node_modules/ -name "$FILE" -delete
done


%files
%{_bindir}/*
%{_includedir}/*
%{_prefix}/lib/node_modules/
%{_datadir}/doc/node/gdbinit
%{_datadir}/man/man1/node.1.gz
%{_datadir}/systemtap/tapset/node.stp
%{_datadir}/doc/%{pkg_name}/
%doc CHANGELOG.md LICENSE README.md


%changelog
* Tue Nov 17 2015 Craig MacGregor <craig@1stdibs.com>
- SCL-ified

* Tue Jul 7 2015 Ali Ijaz Sheikh <ofrobots@google.com>
- Added gdbinit.

* Mon Apr 13 2015 Dan Varga <danvarga@gmail.com>
- Fix paths for changelog and manpage

* Thu Dec 4 2014 Ben Noordhuis <info@bnoordhuis.nl>
- Rename to iojs.

* Fri Jul 5 2013 Ben Noordhuis <info@bnoordhuis.nl>
- Initial release.
