Summary:	C/C++ debugger for GNOME
Summary(pl.UTF-8):	Debugger C/C++ dla GNOME
Name:		nemiver
Version:	0.7.3
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/nemiver/0.7/%{name}-%{version}.tar.bz2
# Source0-md5:	7159d64bd78dc55aad892077fb75dfec
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-configure.patch
Patch2:		gcc-4.5.diff
URL:		http://home.gna.org/nemiver/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	ghex-devel >= 2.22.0
BuildRequires:	glibmm-devel >= 2.16.0
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gtkmm-devel >= 2.12.0
BuildRequires:	gtksourceviewmm2-devel >= 2.2.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libglademm-devel >= 2.6.0
BuildRequires:	libgtop-devel >= 2.14.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	vte-devel >= 0.12.0
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	gdb
Obsoletes:	nemiver-libs < 0.5.3
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

%package devel
Summary:	Header files for Nemiver
Summary(pl.UTF-8):	Pliki nagłówkowe Nemivera
Group:		X11/Development/Libraries
Requires:	glibmm-devel >= 2.16.0
Requires:	libgtop-devel >= 2.14.0
Requires:	libxml2-devel >= 1:2.6.31
Obsoletes:	nemiver-static

%description devel
Header files for developing new debugging backends for Nemiver.

%description devel -l pl.UTF-8
Pliki nagłówkowe do rozwijania nowych backendów dla Nemivera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
	--disable-schemas-install \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/nemiver/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/nemiver/modules/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/nemiver/plugins/dbgperspective/*.la

%find_lang %{name} --with-gnome --with-omf

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
%attr(755,root,root) %{_libdir}/nemiver/libnemivercommon.so
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
%{_mandir}/man1/nemiver.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/nemiver
