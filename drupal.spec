#
# $Id$
#

%define name drupal
%define version 4.7
%define taglevel 11

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
Source0: http://ftp.osuosl.org/pub/drupal/files/projects/%{name}-%{version}.tar.gz
#Source1: drupal.conf
Source2: drupal-README.fedora
Source3: drupal-cron
Source4: drupal-README.planetlab
Patch0: drupal-6.0-scripts-noshebang.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: php, php-gd, php-mbstring, wget

%description
Equipped with a powerful blend of features, Drupal is a Content Management 
System written in PHP that can support a variety of websites ranging from
personal weblogs to large community-driven websites.  Drupal is highly
configurable, skinnable, and secure.

%prep

%setup -q

%patch0
chmod -x scripts/drupal.sh

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{drupaldir}
cp -pr * %{buildroot}%{drupaldir}
cp -pr .htaccess %{buildroot}%{drupaldir}
#mkdir -p %{buildroot}%{_sysconfdir}/httpd
#mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
#cp -pr %SOURCE1 %{buildroot}%{_sysconfdir}/httpd/conf.d
#mkdir -p %{buildroot}%{_sysconfdir}/drupal
#mv %{buildroot}%{drupaldir}/sites/* %{buildroot}%{_sysconfdir}/drupal
#rmdir %{buildroot}%{drupaldir}/sites
#ln -s ../../..%{_sysconfdir}/drupal %{buildroot}%{drupaldir}/sites
mkdir -p %{buildroot}%{_docdir}
cp -pr %SOURCE2 .
cp -pr %SOURCE4 .
install -D -p -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/cron.hourly/drupal 
#mkdir -p %{buildroot}%{_localstatedir}/lib/drupal
#ln -s ../../..%{_localstatedir}/lib/drupal %{buildroot}%{drupaldir}/files
mkdir %{buildroot}%{drupaldir}/files

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt INSTALL* LICENSE* MAINTAINERS.txt UPGRADE.txt 
%doc drupal-README.fedora drupal-README.planetlab sites/all/README.txt
%{drupaldir}
%config(noreplace) %{drupaldir}/.htaccess
%exclude %{drupaldir}/CHANGELOG.txt
%exclude %{drupaldir}/INSTALL* 
%exclude %{drupaldir}/LICENSE* 
%exclude %{drupaldir}/MAINTAINERS.txt 
%exclude %{drupaldir}/UPGRADE.txt
#%dir %{_sysconfdir}/drupal/
#%config(noreplace) %{_sysconfdir}/drupal/all
%config(noreplace) %{drupaldir}/sites/all
#%exclude %{_sysconfdir}/drupal/all/README.txt
%exclude %{drupaldir}/sites/all/README.txt
#%config(noreplace) %{_sysconfdir}/drupal/default
%config(noreplace) %{drupaldir}/sites/default
#%config(noreplace) %{_sysconfdir}/httpd/conf.d/drupal.conf
%attr(755,root,apache) %{_sysconfdir}/cron.hourly/drupal
#%dir %attr(775,root,apache) %{_localstatedir}/lib/drupal/
%dir %attr(775,root,apache) %{drupaldir}/files

%changelog
* Thu Dec 11 2008 Jon Ciesla <limb@jcomserv.net> - 6.7-1
- Upgrade to 6.7, SA-2008-073.

* Wed Oct 22 2008 Jon Ciesla <limb@jcomserv.net> - 6.6-1
- Upgrade to 6.6, SA-2008-067.

* Thu Oct 09 2008 Jon Ciesla <limb@jcomserv.net> - 6.5-1
- Upgrade to 6.5, SA-2008-060.
- Added notes to README and drupal.conf re CVE-2008-3661.

* Thu Aug 14 2008 Jon Ciesla <limb@jcomserv.net> - 6.4-1
- Upgrade to 6.4, SA-2008-047.

* Thu Jul 10 2008 Jon Ciesla <limb@jcomserv.net> - 6.3-1
- Upgrade to 6.3, upstream security fixes, SA-2008-044.

* Thu Apr 10 2008 Jon Ciesla <limb@jcomserv.net> - 6.2-1
- Upgrade to 6.2, upstream security fixes, SA-2008-026.

* Thu Feb 28 2008 Jon Ciesla <limb@jcomserv.net> - 6.1-1
- Upgrade to 6.1, upstream security fixes, SA-2008-018.

* Fri Feb 22 2008 Jon Ciesla <limb@jcomserv.net> - 6.0-1
- Upgrade to 6.0.
- Updated noshebang patch.

* Mon Feb 04 2008 Jon Ciesla <limb@jcomserv.net> - 5.7-1
- Upgrade to 5.7, several non-security bugs fixed.

* Fri Jan 11 2008 Jon Ciesla <limb@jcomserv.net> - 5.6-1
- Upgrade to 5.6, upstream security fixes.

* Mon Jan 07 2008 Jon Ciesla <limb@jcomserv.net> - 5.5-2
- Include .htaccess file, BZ 427720.

* Mon Dec 10 2007 Jon Ciesla <limb@jcomserv.net> - 5.5-1
- Upgrade to 5.5, critical fixes.

* Thu Dec 06 2007 Jon Ciesla <limb@jcomserv.net> - 5.4-2
- Fix /files -> /var/lib/drupal dir perms, BZ 414761.

* Wed Dec 05 2007 Jon Ciesla <limb@jcomserv.net> - 5.4-1
- Upgrade to 5.4, advisory ID DRUPAL-SA-2007-031.
- Augmented README regarding symlinks, BZ 254228.

* Thu Oct 18 2007 Jon Ciesla <limb@jcomserv.net> - 5.3-1
- Upgrade to 5.3, fixes:
- HTTP response splitting.
- Arbitrary code execution.
- Cross-site scripting.
- Cross-site request forgery.
- Access bypass.

* Mon Sep 24 2007 Jon Ciesla <limb@jcomserv.net> - 5.2-3
- Minor doc correction, BZ 301541.

* Thu Aug 16 2007 Jon Ciesla <limb@jcomserv.net> - 5.2-2
- License tag correction.

* Thu Jul 26 2007 Jon Ciesla <limb@jcomserv.net> - 5.2-1
- Upgrade to 5.2, Cross-site request forgery fix.

* Fri Jul 20 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-5
- Corrected buildroot.
- Moved /etc/drupal/all/README.txt to correct place.

* Wed Jul 04 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-4
- Made settings.php not readonly by default, with note in drupal-README.fedora
- Locked down initial security configuration, documented steps required.
- Description cleanup.
- Added wget requires.

* Wed Jun 06 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-3
- Fixed initial setting.php perms.
- Added files dir.

* Wed May 30 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-2
- Fixed category, duped docs, apache restart, cron job.

* Wed May 30 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-1
- Initial packaging.
