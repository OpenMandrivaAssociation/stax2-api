%{?_javapackages_macros:%_javapackages_macros}
Name:             stax2-api
Version:          3.1.1
Release:          8.1%{?dist}
Summary:          Experimental API extending basic StAX implementation
License:          BSD
# NOTE. new home http://wiki.fasterxml.com/WoodstoxStax2
URL:              https://docs.codehaus.org/display/WSTX/StAX2
# NOTE. newer release available here https://github.com/FasterXML/stax2-api/
Source0:          http://repository.codehaus.org/org/codehaus/woodstox/%{name}/%{version}/%{name}-%{version}-sources.jar
Source1:          http://repository.codehaus.org/org/codehaus/woodstox/%{name}/%{version}/%{name}-%{version}.pom

BuildArch:        noarch

BuildRequires:    maven-surefire-provider-junit
BuildRequires:    bea-stax-api
BuildRequires:    java-devel
BuildRequires:    maven-local

%description
StAX2 is an experimental API that is intended to extend
basic StAX specifications in a way that allows implementations
to experiment with features before they end up in the actual
StAX specification (if they do). As such, it is intended
to be freely implementable by all StAX implementations same way
as StAX, but without going through a formal JCP process.

%package javadoc
Summary:          API documentation for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -c %{name}
# fixing incomplete source directory structure
mkdir -p src/main/java
mv -f org src/main/java/

cp %{SOURCE1} pom.xml
%pom_remove_dep javax.xml.stream:stax-api
%pom_add_dep stax:stax-api:1.0.1

%build

%mvn_file :%{name} %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Mon Aug 12 2013 gil cattaneo <puntogil@libero.it> 3.1.1-8
- fix rhbz#993381
- update to current packaging guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.1.1-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 29 2011 Jaromir Capik <jcapik@redhat.com> - 3.1.1-2
- bea-stax has it's own depmap now -> removing the local one

* Tue Sep 13 2011 Jaromir Capik <jcapik@redhat.com> - 3.1.1-1
- Initial version
