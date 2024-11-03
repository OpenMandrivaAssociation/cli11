%define oname	CLI11
%define name	%(echo %oname | tr [:upper:] [:lower:])

Summary:	A command line parser for C++11
Name:		%{name}
Version:	2.4.2
Release:	1
Group:		Sciences/Other
URL:		https://github.com/CLIUtils/%{oname}
Source0:	https://github.com/CLIUtils/%{oname}/archive/v%{version}/%{name}-%{version}.tar.gz
License:	BSD

BuildArch:	noarch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	cmake(catch2)
BuildRequires:	python3-devel
 
%description
CLI11 is a command line parser for C++11 and beyond that provides a
rich feature set with a simple and intuitive interface.
 
#-----------------------------------------------------------------------

%package devel
Summary:	A command line parser for C++11
#Provides:	%{name}-static = %{version}-%{release}
 
%description devel
CLI11 is a command line parser for C++11 and beyond that provides a
rich feature set with a simple and intuitive interface.
 
%files devel
%doc CHANGELOG.md README.md docs/CLI11_300.png
%license LICENSE
%{_includedir}/CLI/
%{_datadir}/cmake/CLI11/
%{_datadir}/pkgconfig/CLI11.pc

#-----------------------------------------------------------------------

%package docs
Summary:	Documentation for CLI11
 
%description docs
Documentation for CLI11.
 
%files docs
%doc %{_vpath_builddir}/docs/html
%doc docs/%{oname}_100.png
%doc docs/%{oname}.svg

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n %{oname}-%{version}
 
# alter the icon path in README.md for the installed paths
sed -i.orig 's,\./docs,.,' README.md
touch -r README.md.orig README.md
rm README.md.orig
 
%build
CXXFLAGS='%{build_cxxflags} -DCLI11_OPTIONAL -DCLI11_STD_OPTIONAL=1'
%cmake \
	-DCLI11_BUILD_DOCS:BOOL=TRUE \
	-DCLI11_BUILD_TESTS:BOOL=TRUE \
	-DCMAKE_CXX_STANDARD=17 \
	-G Ninja
%ninja_build
	
# Build the documentation
%ninja_build docs
 
%install
%ninja_install -C build
	
%check
pushd build
LD_LIBRARY_PATH=./cmake/tests:$LD_LIBRARY_PATH ctest %{?_smp_mflags} -V .
popd

