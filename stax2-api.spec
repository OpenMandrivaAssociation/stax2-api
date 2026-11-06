Name:		stax2-api
Version:	4.3.2
Release:	1
Summary:	Extension of the StAX XML API
Group:		Development/Java
License:	BSD
URL:		https://github.com/FasterXML/stax2-api
Source0:	https://github.com/FasterXML/stax2-api/archive/refs/tags/stax2-api-%{version}.tar.gz#/stax2-api-%{version}.tar.gz

BuildArch:	noarch
Obsoletes:	%{name}-javadoc < 4
BuildRequires:	mvn(com.fasterxml:oss-parent:pom::)
# oss-parent pins the compiler plugin to this ASM jar.
BuildRequires:	mvn(org.ow2.asm:asm)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

%description
Stax2 extends the JDK StAX pull parser with typed access, validation,
and DTD information. 4.3 requires Java 8. 4.3.2 speeds up BigInteger
and BigDecimal decoding and fixes DOM reader text on the last segment.
Tests are skipped. The OSGi bundle descriptor is not attached.

%prep
%setup -q -n stax2-api-stax2-api-%{version}
# Bundle packaging is implemented by maven-bundle-plugin, which is not
# packaged. oss-parent also declares that plugin as a build extension.
# The copy of the parent POM is rewritten by the build; this project POM
# must not ask for the extension itself.
python - <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

def local(tag):
    return tag.rsplit("}", 1)[-1]

path = Path("pom.xml")
tree = ET.parse(path)
root = tree.getroot()
packaging = None
removed = 0
for parent in root.iter():
    for child in list(parent):
        if local(child.tag) == "packaging" and (child.text or "").strip() == "bundle":
            child.text = "jar"
            packaging = "jar"
        if local(child.tag) != "plugin":
            continue
        artifact = ""
        for item in child:
            if local(item.tag) == "artifactId":
                artifact = (item.text or "").strip()
        if artifact == "maven-bundle-plugin":
            parent.remove(child)
            removed += 1
if packaging != "jar" or removed != 1:
    raise SystemExit(f"packaging={packaging} removed={removed}")
tree.write(path, encoding="UTF-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE README.md release-notes/VERSION
