%global debug_package %{nil}

Name:          native-platform
Version:       0.14
Release:       15
Summary:       Java bindings for various native APIs
License:       ASL 2.0
URL:           https://github.com/adammurdoch/native-platform
Source0:       native-platform-%{version}.tar.gz
Source1:       native-platform-0.7-Makefile
Patch0:        0001-Load-lib-from-system.patch
Patch1:        0002-Use-library-name-without-arch.patch
BuildRequires: gcc-c++ java-devel javapackages-local ncurses-devel jopt-simple
Obsoletes:     native-platform-javadoc < %{version}-%{release}
Provides:      native-platform-javadoc = %{version}-%{release}

%description
A collection of cross-platform Java APIs for various native APIs.

%prep
%autosetup -n native-platform-%{version} -p1
find .  -name "*.jar" -delete
find .  -name "*.class" -delete
cp -p %{SOURCE1} Makefile
chmod 644 readme.md
mv src/curses/cpp/*.cpp src/main/cpp
mv src/shared/cpp/* src/main/cpp

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CPPFLAGS="${CPPFLAGS:-%optflags}" ; export CPPFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
LDFLAGS="${LDFLAGS:-%__global_ldflags}"; export LDFLAGS;
%{make_build} JAVA_HOME=%{_jvmdir}/java
%mvn_artifact net.rubygrapefruit:native-platform:%{version} build/native-platform.jar
%mvn_file : native-platform

%install
%mvn_install -J build/docs/javadoc
mkdir -p %{buildroot}%{_libdir}/native-platform
install -pm 0755 build/binaries/libnative-platform-curses.so %{buildroot}%{_libdir}/native-platform/
install -pm 0755 build/binaries/libnative-platform.so %{buildroot}%{_libdir}/native-platform/

%files
%attr(0644,root,root) %{_datadir}/maven-metadata/native-platform.xml
%attr(0644,root,root) /usr/lib/java/native-platform.jar
%{_libdir}/native-platform
%doc readme.md
%license LICENSE
%{_javadocdir}/%{name}

%changelog
* Thu Dec 7 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.14-15
- Package init
