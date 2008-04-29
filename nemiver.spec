Summary:	C/C++ debugger for GNOME
Summary(pl.UTF-8):	Debugger C/C++ dla GNOME
Name:		nemiver
Version:	0.4.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/nemiver/0.4/%{name}-%{version}.tar.bz2
# Source0-md5:	0df4c48b0b1f09b46498a71344b4e3e8
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-configure.patch
URL:		http://home.gna.org/nemiver/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	glibmm-devel >= 2.8.2
BuildRequires:	gnome-vfs2-devel >= 2.14.0
BuildRequires:	gtkmm-devel >= 2.6.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libglademm-devel >= 2.6.0
BuildRequires:	libgtksourceviewmm-devel >= 0.3.0
BuildRequires:	libgtop-devel >= 2.14
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.22
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	vte-devel >= 0.12.0
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gdb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nemiver is an ongoing effort to write a standalone graphical debugger
that integrates well in the GNOME desktop environment. It currently
features a backend which uses the well known GNU Debugger (gdb) to
debug C/C++ programs.

%description -l pl.UTF-8
Nemiver to próba napisania samodzielnego graficznego debuggera dobrze
integrującego się ze środowiskiem graficznym GNOME. Aktualnie zawiera
backend wykorzystujący dobrze znany GNU Debugger (gdb) do śledzenia
programów w C/C++.

%package libs
Summary:	Nemiver library
Summary(pl.UTF-8):	Biblioteka Nemivera
Group:		Libraries
Requires(post,postun):	/sbin/ldconfig

%description libs
Nemiver shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona Nemivera.

%package devel
Summary:	Header files for Nemiver library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Nemivera
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glibmm-devel >= 2.8.2
Requires:	libgtop-devel >= 2.14
Requires:	libxml2-devel >= 1:2.6.22

%description devel
Header files for Nemiver library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Nemivera.

%package static
Summary:	Static Nemiver library
Summary(pl.UTF-8):	Statyczna biblioteka Nemivera
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Nemiver library.

%description static -l pl.UTF-8
Statyczna biblioteka Nemivera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-scrollkeeper \
	--disable-schemas-install
%{__make} \
	GDB_PROG='%{_bindir}/gdb'

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/nemiver/modules/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/nemiver/plugins/dbgperspective/*.{a,la}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install nemiver-dbgperspective.schemas
%gconf_schema_install nemiver-workbench.schemas
%scrollkeeper_update_post
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall nemiver-dbgperspective.schemas
%gconf_schema_uninstall nemiver-workbench.schemas

%postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/nemiver
%{_sysconfdir}/gconf/schemas/nemiver-dbgperspective.schemas
%{_sysconfdir}/gconf/schemas/nemiver-workbench.schemas
%{_datadir}/nemiver
%{_desktopdir}/nemiver.desktop
%{_iconsdir}/hicolor/*/apps/nemiver.png
%{_iconsdir}/hicolor/*/apps/nemiver.svg
%dir %{_libdir}/nemiver
%{_libdir}/nemiver/config
%dir %{_libdir}/nemiver/modules
%attr(755,root,root) %{_libdir}/nemiver/modules/*.so
%dir %{_libdir}/nemiver/plugins
%dir %{_libdir}/nemiver/plugins/dbgperspective
%{_libdir}/nemiver/plugins/dbgperspective/dbgperspective.conf
%{_libdir}/nemiver/plugins/dbgperspective/glade
%{_libdir}/nemiver/plugins/dbgperspective/icons
%attr(755,root,root) %{_libdir}/nemiver/plugins/dbgperspective/libdbgperspectiveplugin.so
%{_libdir}/nemiver/plugins/dbgperspective/menus
%{_libdir}/nemiver/plugins/dbgperspective/plugin-descriptor.xml
%{_libdir}/nemiver/plugins/dbgperspective/sqlscripts
%dir %{_omf_dest_dir}/nemiver
%{_omf_dest_dir}/nemiver/nemiver-C.omf
%lang(sv) %{_omf_dest_dir}/nemiver/nemiver-sv.omf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnemivercommon.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnemivercommon.so
%{_libdir}/libnemivercommon.la
%dir %{_includedir}/nemiver
%dir %{_includedir}/nemiver/dynmods
%{_includedir}/nemiver/dynmods/*.h
%dir %{_includedir}/nemiver/common
%{_includedir}/nemiver/common/*.h
%{_pkgconfigdir}/libnemivercommon.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnemivercommon.a
