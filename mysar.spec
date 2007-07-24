Summary:	MySQL Squid Access Report
Summary(pl.UTF-8):Program raportujący dostęp do Squida
Name:		mysar
Version:	2.1.0
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/mysar/%{name}-%{version}.tar.gz
# Source0-md5:	c632dc1332508c7c031b3a11533d8b7e
URL:		http://giannis.stoilis.gr/software/mysar/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
%if %{with trigger}
Requires(triggerpostun):	sed >= 4.0
%endif
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}


%description
MySQL Squid Access Report, mysar for short, is a reporting system for
user web traffic activity, as logged from a squid proxy.


%description -l pl.UTF-8
MySQL Squid Access Report, w skr�cie mysar, to system raportujący
aktywność u�ytkownik�w zalogowaną poprzez squid proxy.

%prep
%setup -q -n %{name}

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
Alias.url += ( "/phpMyBackupPro" => "%{_datadir}/phpMyBackupPro/")
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/etc/cron.d}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

cp -af * $RPM_BUILD_ROOT%{_appdir}
rm -f $RPM_BUILD_ROOT%{_appdir}/etc/config,ini.example $RPM_BUILD_ROOT%{_appdir}/etc/mysar.cron

install etc/mysar.cron $RPM_BUILD_ROOT/etc/cron.d/
install etc/config.ini.example $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/config.ini.example $RPM_BUILD_ROOT%{_appdir}/etc/config,ini.example

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size)
%dir %{_appdir}
%{_appdir}/bin
%{_appdir}/inc
%{_appdir}/log
%{_appdir}/smarty-tmp
%{_appdir}/www-templates
%{_appdir}/www-templates.pt_BR
%{_appdir}/www
%{_appdir}/www-templates.fr_FR
%{_appdir}/www-templates.ru_RU
