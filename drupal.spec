#
# $Id$
#

%define name drupal
%define version 4.7
%define taglevel 12

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

Packager: PlanetLab Central <support@planet-lab.org>

# remain compliant with former planetlab practices
%define drupaldir /var/www/html
Name: %{name}
Version:  %{version}
Release:  %{release}
Summary: An open-source content-management platform

Group: Applications/Publishing
License: GPLv2+        
URL: http://www.drupal.org
Source0: http://ftp.osuosl.org/pub/drupal/files/projects/%{name}-%{version}.%{taglevel}.tar.gz
#Source1: drupal.conf
Source2: drupal-cron
Source3: http://ftp.drupal.org/files/projects/taxonomy_block-4.7.x-1.x-dev.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: php, php-gd, php-mbstring, wget

%description
Equipped with a powerful blend of features, Drupal is a Content Management 
System written in PHP that can support a variety of websites ranging from
personal weblogs to large community-driven websites.  Drupal is highly
configurable, skinnable, and secure.

%prep
%setup -q -n %{name}-%{version}.%{taglevel} -a 3

%build
mv taxonomy_block modules

%install
rm -rf %{buildroot}
install -d %{buildroot}%{drupaldir}
cp -pr * %{buildroot}%{drupaldir}
cp -pr .htaccess %{buildroot}%{drupaldir}
mkdir -p %{buildroot}%{_docdir}
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.hourly/drupal 
mkdir %{buildroot}%{drupaldir}/files

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt INSTALL* LICENSE* MAINTAINERS.txt UPGRADE.txt 
%{drupaldir}
%config(noreplace) %{drupaldir}/.htaccess
%exclude %{drupaldir}/CHANGELOG.txt
%exclude %{drupaldir}/INSTALL* 
%exclude %{drupaldir}/LICENSE* 
%exclude %{drupaldir}/MAINTAINERS.txt 
%exclude %{drupaldir}/UPGRADE.txt
%config(noreplace) %{drupaldir}/sites/default
%attr(755,root,apache) %{_sysconfdir}/cron.hourly/drupal
%dir %attr(775,root,apache) %{drupaldir}/files

%changelog
* Wed Jun 10 2009 Stephen Soltesz <soltesz@cs.princeton.edu> - drupal-4.7-12
- add taxonomy_block to default install

* Fri Jan 09 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> -
- plain drupal 4.7.11 
