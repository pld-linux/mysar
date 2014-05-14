Summary:	MySQL Squid Access Report
Summary(pl.UTF-8):	Program raportujący dostęp do Squida
Name:		mysar
Version:	2.1.4
Release:	3
License:	GPL
Group:		Applications/WWW
Source0:	http://downloads.sourceforge.net/mysar/%{name}-%{version}.tar.gz
# Source0-md5:	4b570ace1b46ec3c13e0a048e9d6cf37
Patch0:		%{name}-smarty_path.patch
Patch1:		%{name}-cron.patch
Patch2:		%{name}-install.patch
Patch3:		%{name}-ip.patch
URL:		http://giannis.stoilis.gr/software/mysar/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	webapps
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Suggests:	crondaemon
Conflicts:	apache-base < 2.4.0-1
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
MySQL Squid Access Report, w skrócie mysar, to system raportujący
aktywność użytkowników na WWW logowaną poprzez proxy squid.

%package install
Summary:	Installation scripts for mysar
Summary(pl.UTF-8):	Skrypty instalacyjne dla mysar
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
AutoProv:	no
AutoReq:	no

%description install
This package provides installation scripts for mysar.

%description install -l pl.UTF-8
Pakiet ten dostarcza skryptów instalacyjnych dla mysar.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}/www
<Directory %{_appdir}/www>
	Allow from all
</Directory>
EOF

cat > httpd.conf <<'EOF'
Alias /%{name} %{_appdir}/www
<Directory %{_appdir}/www>
	Require all granted
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += ( "/mysar/" => "%{_datadir}/mysar/www/" )
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/etc,/etc/cron.d}
install -d $RPM_BUILD_ROOT{%{_sharedstatedir}/%{_webapp}/smarty-tmp,/var/log/%{_webapp}}

cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

cp -af bin inc www www-templates* $RPM_BUILD_ROOT%{_appdir}
rm -f $RPM_BUILD_ROOT%{_appdir}/etc/config,ini.example $RPM_BUILD_ROOT%{_appdir}/etc/mysar.cron
rm -rf $RPM_BUILD_ROOT%{_appdir}/bin/mysar-binary-importer

cp -p etc/mysar.cron $RPM_BUILD_ROOT/etc/cron.d

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL README TODO UPGRADE etc/config.ini.example
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) /etc/cron.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%dir %{_sharedstatedir}/%{_webapp}
%attr(770,root,http) %{_sharedstatedir}/%{_webapp}/smarty-tmp
%dir %{_appdir}/bin
%attr(750,root,root) %{_appdir}/bin/*.php
%dir %{_appdir}/etc
%{_appdir}/inc
%{_appdir}/www-templates
%{_appdir}/www-templates.pt_BR
%{_appdir}/www
%exclude %{_appdir}/www/install
%{_appdir}/www-templates.fr_FR
%{_appdir}/www-templates.ru_RU
/var/log/mysar

%files install
%defattr(644,root,root,755)
%{_appdir}/www/install
