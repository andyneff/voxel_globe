%include %{_sourcedir}/common.inc

Name:     futures
Version:  3.0.2
Release:  1%{?dist}
Summary:  Backport of the concurrent.futures package from Python 3.2
Source:   %{name}-%{version}.tar.gz
Source1:  common.inc

License:  BSD
Group:    Development/Libraries
URL:      https://pypi.python.org/pypi/futures
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python
BuildArch:  noarch

%description
Backport of the concurrent.futures package from Python 3.2

%prep
%setup -q -n %{name}-%{version}

%build
env CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --prefix=${RPM_BUILD_ROOT}%{cat_prefix} --install-data=${RPM_BUILD_ROOT}%{_datadir} --single-version-externally-managed --record=/dev/null

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/
