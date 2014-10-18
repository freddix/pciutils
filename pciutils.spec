# based on PLD Linux spec git://git.pld-linux.org/packages/pciutils.git
Summary:	Linux PCI utilities
Name:		pciutils
Version:	3.2.1
Release:	4
License:	GPL v2+
Group:		Applications/System
Source0:	ftp://atrey.karlin.mff.cuni.cz/pub/linux/pci/%{name}-%{version}.tar.gz
# Source0-md5:	fdc92c4665bb169022ffe730b3c08313
Patch0:		%{name}-devel.patch
Patch1:		%{name}-nowhich.patch
URL:		http://atrey.karlin.mff.cuni.cz/~mj/pciutils.shtml
BuildRequires:	zlib-devel
Requires:	hwids
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains various utilities for inspecting and setting of
devices connected to the PCI bus. Requires kernel version 2.1.82 or
newer (supporting the /proc/bus/pci interface).

%package devel
Summary:	Linux PCI development library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel

%description devel
This package contains a library for inspecting and setting devices
connected to the PCI bus.

%package static
Summary:	Static version of PCI library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of PCI library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

ln -sf lib pci

%build
%{__make} \
	CC="%{__cc}"		\
	IDSDIR=%{_datadir}	\
	INCDIR=%{_includedir}	\
	LDFLAGS="%{rpmldflags}"	\
	LIBDIR=%{_libdir}	\
	OPT="%{rpmcflags}"	\
	PREFIX=%{_prefix}	\
	SHAREDIR=%{_datadir}/hwids  \
	ZLIB=no DNS=yes SHARED=yes

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_datadir},%{_mandir}/man8,%{_libdir},%{_includedir}/pci}

%{__make} install install-lib	\
	DESTDIR=$RPM_BUILD_ROOT	\
	LIBDIR=%{_libdir}	\
	PREFIX=%{_prefix}	\
	SBINDIR=%{_sbindir}	\
	SHAREDIR=%{_datadir}/hwids

cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libpci.so.*.*.* libpci.so
chmod 755 libpci.so.*
/sbin/ldconfig -n .

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/lspci
%attr(755,root,root) %{_sbindir}/setpci
%attr(755,root,root) %ghost %{_libdir}/libpci.so.3
%attr(755,root,root) %{_libdir}/libpci.so.*.*.*
%{_mandir}/man7/pcilib.7*
%{_mandir}/man8/lspci.8*
%{_mandir}/man8/setpci.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpci.so
%dir %{_includedir}/pci
%{_includedir}/pci/*.h
%{_pkgconfigdir}/libpci.pc

