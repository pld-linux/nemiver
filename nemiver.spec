Summary:	C/C++ debugger for GNOME
Summary(pl.UTF-8):	Debugger C/C++ dla GNOME
Name:		nemiver
Version:	0.9.6
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/nemiver/0.9/%{name}-%{version}.tar.xz
# Source0-md5:	cf33f0eef4f392268a2bdf103e930bd3
Patch0:		0001-Fix-compiliation-warnings-errors.patch
Patch1:		0001-Use-RefPtr-bool-operator-in-the-conditions.patch
Patch2:		%{name}-ac.patch
Patch3:		%{name}-pc.patch
URL:		https://wiki.gnome.org/Apps/Nemiver
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	docbook-dtd412-xml
# gdlmm for dynamic layout
BuildRequires:	gdlmm-devel >= 3.2
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	gtkhex3-devel >= 3.0.0
BuildRequires:	glib2-devel >= 1:2.14
BuildRequires:	glibmm-devel >= 2.25.1
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	gtkmm3-devel >= 3.0
BuildRequires:	gtksourceviewmm3-devel >= 3.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	itstool
BuildRequires:	libgtop-devel >= 2.14.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	vte-devel >= 0.38.0
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	gdb
Requires:	gdlmm >= 3.2
Requires:	glib2 >= 1:2.14
Requires:	glibmm >= 2.25.1
Requires:	hicolor-icon-theme
Requires:	libxml2 >= 1:2.6.31
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
Requires:	glib2-devel >= 1:2.14
Requires:	glibmm-devel >= 2.25.1
Requires:	libgtop-devel >= 2.14.0
Requires:	libxml2-devel >= 1:2.6.31
Obsoletes:	nemiver-static < 0.6.3

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
	--with-default-gdb=%{_bindir}/gdb \
	--disable-schemas-install \
	--disable-silent-rules \
	--disable-static \
	--enable-gsettings
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/nemiver/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nemiver/modules/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nemiver/plugins/dbgperspective/*.la

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/nemiver
%{_datadir}/nemiver
%{_desktopdir}/nemiver.desktop
%{_iconsdir}/hicolor/*x*/apps/nemiver.png
%{_iconsdir}/hicolor/scalable/apps/nemiver.svg
%{_iconsdir}/hicolor/symbolic/apps/nemiver-symbolic.svg
%{_datadir}/glib-2.0/schemas/org.nemiver.gschema.xml
%{_datadir}/appdata/nemiver.appdata.xml
%dir %{_libdir}/nemiver
%attr(755,root,root) %{_libdir}/nemiver/libnemivercommon.so
%{_libdir}/nemiver/config
%dir %{_libdir}/nemiver/modules
%attr(755,root,root) %{_libdir}/nemiver/modules/*.so
%dir %{_libdir}/nemiver/plugins
%dir %{_libdir}/nemiver/plugins/dbgperspective
%{_libdir}/nemiver/plugins/dbgperspective/dbgperspective.conf
%{_libdir}/nemiver/plugins/dbgperspective/icons
%attr(755,root,root) %{_libdir}/nemiver/plugins/dbgperspective/libdbgperspectiveplugin.so
%{_libdir}/nemiver/plugins/dbgperspective/menus
%{_libdir}/nemiver/plugins/dbgperspective/plugin-descriptor.xml
%{_libdir}/nemiver/plugins/dbgperspective/sqlscripts
%{_libdir}/nemiver/plugins/dbgperspective/ui
%{_mandir}/man1/nemiver.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/nemiver
