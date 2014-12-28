Summary:	Handling RFKILL events in userspace
Summary(pl.UTF-8):	Obsługa zdarzeń RFKILL w przestrzeni użytkownika
Name:		urfkill
Version:	0.3.0
Release:	1
License:	GPL v2+ (utility), LGPL v2.1+ (library)
Group:		Applications/System
Source0:	https://github.com/downloads/lcp/urfkill/%{name}-%{version}.tar.xz
# Source0-md5:	07ea786ac26a5aa6b623eb014021eb86
URL:		http://www.freedesktop.org/wiki/Software/urfkill
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	expat-devel
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.21.5
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:147
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 1.0
Requires:	polkit >= 0.97
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
urfkill is a project to handle RFKILL events in userspace and aimed to
replace the rfkill input handler in kernel, i.e. rfkill-input, and
provide a flexible policy for RFKILL keys.

%description -l pl.UTF-8
urfkill to projekt mający na celu obsługę zdarzeń RFKILL w przestrzeni
użytkownika, mający zastąpić obsługę wejścia rfkill w jądrze
(rfkill-input) oraz zapewnić elastyczną politykę dla klawiszy RFKILL.

%package libs
Summary:	GLib-based urfkill library
Summary(pl.UTF-8):	Biblioteka urfkill oparta na GLibie
License:	LGPL v2.1+
Group:		Libraries
Requires:	dbus-glib >= 0.76
Requires:	dbus-libs >= 1.0
Requires:	glib2 >= 1:2.21.5

%description libs
GLib-based urfkill library for managing killswitches.

%description libs -l pl.UTF-8
Oparta na GLibie biblioteka do zarządzania wyłącznikami urządzeń
radiowych.

%package devel
Summary:	Header files for urfkill-glib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki urfkill-glib
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 1.0
Requires:	dbus-glib-devel >= 0.76
Requires:	glib2-devel >= 1:2.21.5

%description devel
Header files for urfkill-glib library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki urfkill-glib.

%package static
Summary:	Static urfkill-glib library
Summary(pl.UTF-8):	Biblioteka statyczna urfkill-glib
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static urfkill-glib library.

%description static -l pl.UTF-8
Biblioteka statyczna urfkill-glib.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liburfkill-glib.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libexecdir}/urfkilld
%dir %{_sysconfdir}/urfkill
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/urfkill/urfkill.conf
%dir %{_sysconfdir}/urfkill/profile
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/urfkill/profile/*-settings.xml
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.URfkill.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.URfkill*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.URfkill.service
%{_datadir}/polkit-1/actions/org.freedesktop.urfkill.policy
%{_mandir}/man7/urfkill.7*
%{_mandir}/man8/urfkilld.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liburfkill-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liburfkill-glib.so.0
%{_libdir}/girepository-1.0/Urfkill-0.3.typelib
%{_includedir}/liburfkill-glib
%{_gtkdocdir}/urfkill

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liburfkill-glib.so
%{_datadir}/gir-1.0/Urfkill-0.3.gir
%{_pkgconfigdir}/urfkill-glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liburfkill-glib.a
