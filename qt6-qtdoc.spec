%define beta beta3
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}
Summary:	Qt %{major} Documentation Tools
Name:		qt6-qtdoc
Version:	6.10.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtdoc-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtdoc-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
License:	LGPLv3/GPLv3/GPLv2
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}Concurrent)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Xml)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}Sql)
BuildRequires:	cmake(Qt%{major}Test)
BuildRequires:	cmake(Qt%{major}PrintSupport)
BuildRequires:	cmake(Qt%{major}OpenGL)
BuildRequires:	cmake(Qt%{major}OpenGLWidgets)
BuildRequires:	cmake(Qt%{major}DBus)
BuildRequires:	cmake(Qt%{major}QmlIntegration)
BuildRequires:	cmake(Qt%{major}QmlModels)
BuildRequires:	cmake(Qt%{major}QmlXmlListModel)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}QuickControls2)
BuildRequires:	cmake(Qt%{major}QuickTemplates2)
BuildRequires:	cmake(Qt%{major}Multimedia)
BuildRequires:	cmake(Qt%{major}Svg)
BuildRequires:	qt%{major}-cmake
BuildRequires:	qt%{major}-qtdeclarative
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6QuickControls2)
BuildRequires:	cmake(Qt6QmlXmlListModel)
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime

%description
Qt %{major} documentation tools.

%prep
%autosetup -p1 -n qtdoc%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DBUILD_EXAMPLES:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DFEATURE_cxx2a:BOOL=ON \
	-DFEATURE_dynamicgl:BOOL=ON \
	-DFEATURE_ftp:BOOL=ON \
	-DFEATURE_opengl_dynamic:BOOL=ON \
	-DFEATURE_use_lld_linker:BOOL=ON \
	-DFEATURE_xcb_native_painting:BOOL=ON \
	-DFEATURE_openssl:BOOL=ON \
	-DFEATURE_openssl_linked:BOOL=ON \
	-DFEATURE_system_sqlite:BOOL=ON \
	-DINPUT_sqlite=system \
	-DQT_WILL_INSTALL:BOOL=ON \
	-D_OPENGL_LIB_PATH=%{_libdir} \
	-DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
	-DOPENGL_glu_LIBRARY=%{_libdir}/libGLU.so \
	-DOPENGL_glx_LIBRARY=%{_libdir}/libGLX.so \
	-DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall

%files
%{_libdir}/qt6/examples/*
%{_qtdir}/mkspecs/qtdoc_dummy_file.txt
%{_qtdir}/sbom/*
