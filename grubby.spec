Name: grubby
Version: 8.6
Release: 1%{?dist}
Summary: Command line tool for updating bootloader configs
Group: System Environment/Base
License: GPLv2+
URL: http://git.fedorahosted.org/git/grubby.git
# we only pull git snaps at the moment
# git clone git://git.fedorahosted.org/git/grubby.git
# git archive --format=tar --prefix=grubby-%{version}/ HEAD |bzip2 > grubby-%{version}.tar.bz2
Source0: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig glib2-devel popt-devel 
BuildRequires: libblkid-devel
# for make test / getopt:
BuildRequires: util-linux-ng
%ifarch s390 s390x
Requires: s390utils-base
%endif

%description
grubby  is  a command line tool for updating and displaying information about 
the configuration files for the grub, lilo, elilo (ia64),  yaboot (powerpc)  
and zipl (s390) boot loaders. It is primarily designed to be used from scripts
which install new kernels and need to find information about the current boot 
environment.

%prep
%setup -q


%build
make %{?_smp_mflags}

%check
make test

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
/sbin/installkernel
/sbin/new-kernel-pkg
/sbin/grubby
%{_mandir}/man8/*.8*


%changelog
* Mon Dec 19 2011 Peter Jones <pjones@redhat.com> - 8.6-1
- Fix a "make test" errors introduced in 8.4-1

* Sat Dec 17 2011 Peter Jones <pjones@redhat.com> - 8.5-1
- Don't hardcode dracut path
  Resolves: #768645

* Thu Dec 08 2011 Adam Williamson <awilliam@redhat.com> - 8.4-1
- Update to 8.4:
	+ fix Loading... line for updated kernels
	+ Add new '--default-title' feature
	+ Add new '--default-index' feature
	+ add feature for testing the output of a grubby command
	+ Fix detection when comparing stage1 to MBR
	+ do not link against glib-2.0
	+ Don't crash if grubConfig not found
	+ Adding extlinux support for new-kernel-pkg
	+ Look for Debian / Ubuntu grub config files (#703260)
	+ Make grubby recognize Ubuntu's spin of Grub2 (#703260)

* Thu Sep 29 2011 Peter Jones <pjones@redhat.com> - 8.3-1
- Fix new-kernel-pkg invocation of grubby for grub (patch from Mads Kiilerich)
  Resolves: rhbz#725185

* Wed Sep 14 2011 Peter Jones <pjones@redhat.com> - 8.2-1
- Fixes for xen (from Michael Petullo)
  Resolves: rhbz#658387

* Fri Jul 22 2011 Peter Jones <pjones@redhat.com> - 8.1-1
- Update to 8.1
- Fix miss-spelled variable name in new-kernel-pkg

* Thu Jul 21 2011 Peter Jones <pjones@redhat.com> - 8.0-1
- Add support for grub2.

* Tue Jun 07 2011 Brian C. Lane <bcl@redhat.com> - 7.0.18-1
- Bump version to 7.0.18 (bcl)
- Fixup new-kernel-pkg errors (#711493) (bcl)

* Mon Jun 06 2011 Peter Jones <pjones@redhat.com> - 7.0.17-1
- Fix references to wrong program name in new-kernel-pkg.8
  Resolves: rhbz#663981

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Karsten Hopp <karsten@redhat.com> 7.0.16-2
- add BR utils-linux-ng for getopt

* Tue Jul 13 2010 Brian C. Lane <bcl@redhat.com> - 7.0.16-1
- Update to 7.0.16
- Add patch to check the return value of getuuidbydev
- Resolves: rhbz#592294

* Wed Apr 14 2010 Peter Jones <pjones@redhat.com> - 7.0.15-1
- Update to 7.0.15
- Add man pages for installkernel and new-kernel-pkg
  Resolves: rhbz#529333

* Wed Apr 14 2010 Peter Jones <pjones@redhat.com> - 7.0.14-1
- Update to 7.0.14

* Thu Feb 11 2010 Peter Jones <pjones@redhat.com> - 7.0.13-1
- Strip boot partition prefix from initrd path if present during --update.
  Related: rhbz#557922
- add host only support for local kernel compiles (airlied)

* Mon Feb 08 2010 Peter Jones <pjones@redhat.com> - 7.0.12-1
- compare rootdev using uuid instead of stat, for better btrfs support (josef)
  Resolves: rhbz#530108

* Mon Feb 08 2010 Peter Jones <pjones@redhat.com> - 7.0.11-1
- Make it possible to update the initrd without any other change.
  Related: rhbz#557922

* Fri Feb 05 2010 Peter Jones <pjones@redhat.com> - 7.0.10-1
- Make --update able to add an initramfs.
  Related: rhbz#557922

* Mon Nov 30 2009 Peter Jones <pjones@redhat.com> - 7.0.9-3
- Use s390utils-base as the s390 dep, not s390utils
  Related: rhbz#540565

* Tue Nov 24 2009 Peter Jones <pjones@redhat.com> - 7.0.9-2
- Add s390utils dep when on s390, since new-kernel-package needs it.
  Resolves: rhbz#540565

* Fri Oct 30 2009 Peter Jones <pjones@redhat.com> - 7.0.9-1
- Add support for dracut to installkernel (notting)

* Thu Oct  1 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.8-1
- Stop using nash

* Fri Sep 11 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.7-1
- Remove writing rd_plytheme=$theme to kernel args in dracut mode (hansg)
- Add a couple of test cases for extra initrds (rstrode)
- Allow tmplLine to be NULL in getInitrdVal (rstrode)

* Fri Sep 11 2009 Peter Jones <pjones@redhat.com> - 7.0.6-1
- Fix test case breakage from 7.0.5 (rstrode)

* Fri Sep 11 2009 Peter Jones <pjones@redhat.com> - 7.0.5-1
- Add support for plymouth as a second initrd. (rstrode)
  Resolves: rhbz#520515

* Wed Sep 09 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.4-1
- Add --dracut cmdline argument for %post generation of dracut initrd

* Wed Aug 26 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.3-1
- Silence error when no /etc/sysconfig/keyboard (#517187)

* Fri Aug  7 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.2-1
- Add --add-dracut-args new-kernel-pkg cmdline option

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Jeremy Katz <katzj@redhat.com> - 7.0.1-1
- Fix blkid usage (#124246)

* Wed Jun 24 2009 Jeremy Katz <katzj@redhat.com> - 7.0-1
- BR libblkid-devel now instead of e2fsprogs-devel
- Add bits to switch to using dracut for new-kernel-pkg

* Wed Jun  3 2009 Jeremy Katz <katzj@redhat.com> - 6.0.86-2
- add instructions for checking out from git

* Tue Jun  2 2009 Jeremy Katz <katzj@redhat.com> - 6.0.86-1
- initial build after splitting out from mkinitrd

