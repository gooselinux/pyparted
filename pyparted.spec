%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Python module for GNU parted
Name:    pyparted
Version: 3.4
Release: 2%{?dist}
License: GPLv2+
Group:   System Environment/Libraries
URL:     http://fedorahosted.org/pyparted

Source0: http://fedorahosted.org/releases/p/y/%{name}/%{name}-%{version}.tar.gz

# We can safely decrement the libparted version requirement because the
# parted-2.1 package in RHEL-6 has the necessary patches from parted-2.2
# backported.
Patch0: libparted-version.patch
Patch1: pyparted-3.4-bz575749.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel
BuildRequires: parted-devel >= 2.1-7
BuildRequires: pkgconfig
BuildRequires: python-decorator
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: python-decorator

%description
Python module for the parted library.  It is used for manipulating
partition tables.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I m4
%{__libtoolize} --copy --force
%{__autoconf}
%{__autoheader}
touch config.h.in
%{__automake} --foreign --add-missing --copy
%{__rm} -rf autom4te.cache
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__rm} -rf %{buildroot}%{python_sitearch}/_pedmodule.la

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING ChangeLog NEWS README TODO
%{python_sitearch}/_pedmodule.so
%{python_sitearch}/parted

%changelog
* Wed Jul 07 2010 David Cantrell <dcantrell@redhat.com> - 3.4-2
- Return PED_EXCEPTION_NO for interactive yes/no exceptions, pass
  appropriate exception to caller
  Resolves: rhbz#575749

* Thu Apr 29 2010 David Cantrell <dcantrell@redhat.com> - 3.4-1
- Handle PED_EXCEPTION_WARNING with PED_EXCEPTION_YES_NO
  Resolves: rhbz#575749

* Wed Apr 21 2010 Chris Lumens <clumens@redhat.com> - 3.3-1
- Upgrade to pyparted-3.3.
  Resolves: rhbz#585504

* Wed Mar 31 2010 David Cantrell <dcantrell@redhat.com> - 3.2-2
- Rebuild for libparted soname change

* Thu Mar 25 2010 Chris Lumens <clumens@redhat.com> - 3.2-1
- Upgrade to pyparted-3.2 (#571940).

* Mon Mar 01 2010 David Cantrell <dcantrell@redhat.com> - 3.1-1
- Upgrade to pyparted-3.1 (#567576).

* Tue Jan 12 2010 David Cantrell <dcantrell@redhat.com> - 3.0-1
- Upgrade to pyparted-3.0.

* Mon Jan 11 2010 Hans de Goede <hdegoede@redhat.com> - 2.5-4
- Rebuild for new parted-2.1
- Remove py_disk_clobber_exclude function binding, as this function was
  removed from parted-2.1

* Thu Jan  7 2010 Hans de Goede <hdegoede@redhat.com> - 2.5-3
- Change python_sitearch macro to use %%global as the new rpm will break
  using %%define here, see:
  https://www.redhat.com/archives/fedora-devel-list/2010-January/msg00093.html

* Sat Dec 19 2009 David Cantrell <dcantrell@redhat.com> - 2.5-2
- Exclude pyparted-2.4.tar.gz from source RPM (oops)

* Sat Dec 19 2009 David Cantrell <dcantrell@redhat.com> - 2.5-1
- Update release instructions. (dcantrell)
- Remove old cylinder alignment test cases for _ped. (dcantrell)
- Add tests for max partition length / start sector (hdegoede)
- Add _pedmodule and parted functions for max partition length / start
  sector (hdegoede)
- Remove align_to_cylinders function bindings (hdegoede)
- Add tests for disk flag methods (hdegoede)
- Add _pedmodule and parted functions for per disk flags (hdegoede)
- Every tuple member requires a comma after it. (dcantrell)
- Fill out a lot of simple _ped.Disk test cases. (dcantrell)
- Disable DeviceDestroyTestCase for now. (dcantrell)
- Add RequiresLabeledDevice to tests/_ped/baseclass.py. (dcantrell)
- Attempt at fixing _ped.Device.destroy(), no dice. (dcantrell)
- Fix UnitFormatCustomTestCase and UnitFormatTestCase. (dcantrell)
- Fix UnitFormatCustomByteTestCase and UnitFormatByteTestCase. (dcantrell)
- Add DeviceStrTestCase, disable DeviceDestroyTestCase. (dcantrell)
- Add DeviceDestroyTestCase and DeviceCacheRemoveTestCase. (dcantrell)
- Implemented ConstraintIsSolutionTestCase(). (dcantrell)
- Implement ConstraintSolveMaxTestCase(). (dcantrell)
- Implement ConstraintSolveNearestTestCase(). (dcantrell)
- Correct py_ped_file_system_probe_specific() for NULL returns. (dcantrell)
- Implement FileSystemProbeSpecificTestCase(). (dcantrell)
- Implement FileSystemProbeTestCase(). (dcantrell)
- Add RequiresFileSystem to tests/_ped/baseclass.py. (dcantrell)
- Add disk alignment test cases in test_ped.py. (dcantrell)
- Fix CHSGeometryStrTestCase(). (dcantrell)
- Fix ConstraintDuplicateTestCase...finally. (dcantrell)
- Put a deprecation warning in py_ped_constraint_duplicate(). (dcantrell)
- Note that we need parted from Fedora for pyparted. (dcantrell)
- Fix UnitGetSizeTestCase in _ped test cases for _ped.UNIT_PERCENT.
  (dcantrell)
- Add testcase for new _ped disk get_partition_alignment method (hdegoede)

* Fri Nov 06 2009 David Cantrell <dcantrell@redhat.com> - 2.4-1
- Upgrade to pyparted-2.4:
      Use PedDevice length instead of DIY (#532023) (hdegoede)
      Use sectorSize not physicalSectorSize for size calculations (hdegoede)

* Tue Nov 03 2009 David Cantrell <dcantrell@redhat.com> - 2.3-1
- Upgrade to pyparted-2.3:
      Remove root user requirement in _ped
      Add testcases for new _ped device methods
      Add python wrapper for new PedDisk partition alignment info function
      Add support for new PedDisk parition alignment info function
      Add python wrappers for new PedDevice alignment info functions
      Add support for new PedDevice alignment info functions
      Fix a whole pile of test cases.
      Remove ped_disk_commit_to_dev() call from py_ped_disk_new_fresh()
      Fix error in Constraint __str__ method
      Make _ped_Device2PedDevice properly set / throw exceptions
      Fixup various errorhandling issues in pydisk.c
      Add missing _ped_Device2PedDevice() retval checks
      Use libparted commit() for parted.disk.Disk.commit() (hdegoede).
- BR parted-devel >= 1.9.0-20

* Fri Oct 02 2009 David Cantrell <dcantrell@redhat.com> - 2.2-1
- Upgrade to pyparted-2.2:
      Fixes PedDisk2_ped_Disk() and avoids losing disk label data
      in the conversion process (#526999)

* Mon Aug 17 2009 Chris Lumens <clumens@redhat.com> - 2.1.2-1
- Upgrade to pyparted-2.1.2:
      PED_DEVICE_DM is always defined in libparted these days.
      Handle parted exceptions arising from ped_device_get (#495433).

* Tue Aug 04 2009 David Cantrell <dcantrell@redhat.com> - 2.1.1-1
- Upgrade to pyparted-2.1.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 David Cantrell <dcantrell@redhat.com> - 2.1.0-1
- Upgrade to pyparted-2.1.0, requires parted-1.9.0-1 or higher

* Fri Jul 10 2009 David Cantrell <dcantrell@redhat.com> - 2.0.12-2
- Rebuild for new parted

* Tue Apr 14 2009 David Cantrell <dcantrell@redhat.com> - 2.0.12-1
- Upgrade to pyparted-2.0.12

* Mon Apr 13 2009 David Cantrell <dcantrell@redhat.com> - 2.0.11-1
- Upgrade to pyparted-2.0.11

* Fri Apr 03 2009 David Cantrell <dcantrell@redhat.com> - 2.0.10-1
- Upgrade to pyparted-2.0.10
      Fix LVM problems around parted.Disk.commit() (#491746)

* Mon Mar 23 2009 David Cantrell <dcantrell@redhat.com> - 2.0.9-1
- Upgrade to pyparted-2.0.9

* Thu Mar 20 2009 David Cantrell <dcantrell@redhat.com> - 2.0.8-1
- Upgrade to pyparted-2.0.8

* Thu Mar 19 2009 David Cantrell <dcantrell@redhat.com> - 2.0.7-1
- Upgrade to pyparted-2.0.7

* Thu Mar 12 2009 David Cantrell <dcantrell@redhat.com> - 2.0.6-1
- Upgrade to pyparted-2.0.6

* Thu Mar 05 2009 David Cantrell <dcantrell@redhat.com> - 2.0.5-1
- Upgrade to pyparted-2.0.5

* Sat Feb 28 2009 David Cantrell <dcantrell@redhat.com> - 2.0.4-1
- Upgrade to pyparted-2.0.4

* Fri Feb 27 2009 David Cantrell <dcantrell@redhat.com> - 2.0.3-1
- Upgrade to pyparted-2.0.3

* Wed Feb 25 2009 David Cantrell <dcantrell@redhat.com> - 2.0.2-1
- Upgrade to pyparted-2.0.2

* Mon Feb 16 2009 David Cantrell <dcantrell@redhat.com> - 2.0.1-1
- Upgrade to pyparted-2.0.1 (#485632)

* Thu Feb 12 2009 David Cantrell <dcantrell@redhat.com> - 2.0.0-1
- Upgrade to pyparted-2.0.0

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.8.9-6
- Rebuild for Python 2.6

* Fri Feb 08 2008 David Cantrell <dcantrell@redhat.com> - 1.8.9-5
- Rebuild for gcc-4.3

* Wed Jan 02 2008 David Cantrell <dcantrell@redhat.com> - 1.8.9-4
- Rebuild

* Mon Nov 19 2007 Jeremy Katz <katzj@redhat.com> - 1.8.9-3
- Add support for exact constraints

* Tue Aug 21 2007 David Cantrell <dcantrell@redhat.com> - 1.8.9-2
- Rebuild

* Fri Aug 10 2007 David Cantrell <dcantrell@redhat.com> - 1.8.9-1
- Update license tag to indicate GPL v2 or later
- Update URLs to point to new upstream location

* Fri Jun 15 2007 David Cantrell <dcantrell@redhat.com> - 1.8.8-1
- Clean up wording in package description (#226337)
- BR pkgconfig (#226337)

* Fri Jun 15 2007 David Cantrell <dcantrell@redhat.com> - 1.8.7-1
- Merge review (#226337)

* Mon Apr 23 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-2
- Ensure build env CFLAGS are included (#226337)

* Fri Apr 19 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-1
- Merge review (#226337)

* Tue Mar 20 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-4
- Rebuild for GNU parted-1.8.6

* Tue Mar 20 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-3
- Rebuild for GNU parted-1.8.5

* Mon Mar 19 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-2
- Rebuild for GNU parted-1.8.4

* Thu Feb 08 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-1
- Define and use python_sitearch rather than python_sitelib

* Thu Feb 08 2007 David Cantrell <dcantrell@redhat.com> - 1.8.4-1
- Use preferred BuildRoot (package review)
- Define and use python_sitelib macro (package review)

* Fri Jan 12 2007 David Cantrell <dcantrell@redhat.com> - 1.8.3-1
- Required parted-1.8.2 or higher

* Wed Jan 10 2007 Jeremy Katz <katzj@redhat.com> - 1.8.2-1
- use PyObject_DEL instead of PyMem_DEL

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.8.1-3
- rebuild for python 2.5

* Tue Dec 05 2006 David Cantrell <dcantrell@redhat.com> - 1.8.1-2
- Rebuild for GNU parted-1.8.1

* Thu Nov 30 2006 David Cantrell <dcantrell@redhat.com> - 1.8.1-1
- Determine Python version to use in %%build so the source RPM is more
  easily moved between distribution releases.

* Fri Nov 17 2006 David Cantrell <dcantrell@redhat.com> - 1.8.0-1
- Bump version to 1.8.0 and require parted >= 1.8.0
- Remove python-abi Requires line since rpm handles that automatically

* Wed Aug 30 2006 David Cantrell <dcantrell@redhat.com> - 1.7.3-1
- Include parted/constraint.h in required header files

* Wed Aug 30 2006 David Cantrell <dcantrell@redhat.com> - 1.7.2-2
- Require parted-1.7.1 or higher

* Tue Jul 25 2006 David Cantrell <dcantrell@redhat.com> - 1.7.2-1
- Add HPSERVICE, PALO, PREP, and MSFT_RESERVED to partition types list

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.7.1-1.1
- rebuild

* Sun May 28 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-1
- Bump version to 1.7.1 and require parted >= 1.7.1

* Fri May 19 2006 David Cantrell <dcantrell@redhat.com> - 1.7.0-1
- Bump version to 1.7.0 and require parted >= 1.7.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Peter Jones <pjones@redhat.com> - 1.6.10-1
- rebuild for new parted.
- add debugging options for make so debuginfo isn't useless

* Wed Nov  9 2005 Jeremy Katz <katzj@redhat.com> - 1.6.9-5
- rebuild for new parted

* Wed Aug 31 2005 Chris Lumens <clumens@redhat.com> 1.6.9-4
- Rebuilt for new parted library.

* Wed Mar 16 2005 Chris Lumens <clumens@redhat.com> 1.6.9-3
- Updated for gcc4 and python2.4.  Fixed build warnings.

* Tue Dec 14 2004 Jeremy Katz <katzj@redhat.com> - 1.6.9-2
- add support for sx8 devices

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 1.6.8-3
- rebuild for python 2.4

* Mon Oct 11 2004 Warren Togami <wtogami@redhat.com> - 1.6.8-2
- #135100 req python-abi (Robert Scheck)

* Tue Aug 17 2004 Jeremy Katz <katzj@redhat.com> - 1.6.8-1
- update for new parted ABI
  - device -> heads, sectors, cylinders now refer to the bios geometry
- require parted >= 1.6.12

* Thu Jul 22 2004 Jeremy Katz <katzj@redhat.com> - 1.6.7-3
- build on ppc64 again

* Thu May 13 2004 Jeremy Katz <katzj@redhat.com> - 1.6.7-1
- fix build for newer versions of gcc (fix from Jeff Law)

* Tue Mar 16 2004 Jeremy Katz <katzj@redhat.com> 1.6.6-2
- fix PARTITION_PROTECTED definition (#118451)

* Fri Mar 12 2004 Jeremy Katz <katzj@redhat.com>
- Initial build split out into separate source from the parted package.
- Don't build on ppc64 right now due to parted build problems (#118183)
