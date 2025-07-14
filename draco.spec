#
# Conditional build:
%bcond_without	transcoder	# transcoding support

Summary:	Draco 3D graphics compression library
Summary(pl.UTF-8):	Draco - biblioteka kompresji grafiki 3D
Name:		draco
Version:	1.5.7
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/draco/releases
Source0:	https://github.com/google/draco/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b91def257264152be35c62f82f805d25
Patch0:		%{name}-system-gtest.patch
Patch1:		%{name}-c++17-filesystem.patch
Patch2:		%{name}-tinygltf.patch
Patch3:		%{name}-includes.patch
URL:		https://github.com/google/draco
BuildRequires:	cmake >= 3.12
BuildRequires:	gtest-devel
BuildRequires:	libstdc++-devel
%if %{with transcoder}
BuildRequires:	eigen3
BuildRequires:	libstdc++-devel >= 6:7
# 2.8.8 added GetFileSizeInBytes in struct FsCallbacks, tinygltf patch adjusts code for it
BuildRequires:	tinygltf-devel >= 2.8.8
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Draco is a library for compressing and decompressing 3D geometric
meshes and point clouds. It is intended to improve the storage and
transmission of 3D graphics.

Draco was designed and built for compression efficiency and speed. The
code supports compressing points, connectivity information, texture
coordinates, color information, normals, and any other generic
attributes associated with geometry. With Draco, applications using 3D
graphics can be significantly smaller without compromising visual
fidelity. For users, this means apps can now be downloaded faster, 3D
graphics in the browser can load quicker, and VR and AR scenes can now
be transmitted with a fraction of the bandwidth and rendered quickly.

Draco is released as C++ source code that can be used to compress 3D
graphics as well as C++ and Javascript decoders for the encoded data.

%description -l pl.UTF-8
Draco to biblioteka do kompresji i dekompresji trójwymiarowych siatek
geometrycznych i chmur punktów. Ma za zadanie usprawnić przechowywanie
i transmisję grafiki 3D.

Biblioteka została zaprojektowana z myślą o wydajności kompresji i
szybkości. Kod obsługuje kompresję punktów, informacji o połączeniach,
współrzędnych tekstur, informacji o kolorach, wektorów normalnych oraz
dowolnych innych atrybutów związnych z geometrią. Przy użyciu Draco
aplikacje wykorzystujące grafikę 3D mogą być znacząco mniejsze bez
poświęcania doznań wizualnych. Dla użytkowników oznacza to, że
aplikacje mogą być pobrane szybciej, grafika 3D w przeglądarce może
ładować się szybciej, a sceny VR i AR mogą być przesyłane z mniejszym
zużyciem sieci i szybko renderowane.

Draco zawiera kod C++ do kompresji grafiki 3D oraz dekodery w C++ i
Javascripcie.

%package devel
Summary:	Header files for draco library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki draco
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for draco library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki draco.

%package static
Summary:	Static draco library
Summary(pl.UTF-8):	Statyczna biblioteka draco
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static draco library.

%description static -l pl.UTF-8
Statyczna biblioteka draco.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
install -d build
cd build
%cmake .. \
%if %{with transcoder}
	-DDRACO_EIGEN_PATH=/usr/include/eigen3 \
	-DDRACO_TINYGLTF_PATH=/usr/include \
	-DDRACO_TRANSCODER_SUPPORTED=ON
# -DDRACO_SIMPLIFIER_SUPPORTED=ON? missing sources as of 1.5.7
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_bindir}/draco_decoder{-%{version},}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/draco_encoder{-%{version},}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/draco_transcoder{-%{version},}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/draco_decoder
%attr(755,root,root) %{_bindir}/draco_encoder
%if %{with transcoder}
%attr(755,root,root) %{_bindir}/draco_transcoder
%endif
%attr(755,root,root) %{_libdir}/libdraco.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdraco.so.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdraco.so
%{_includedir}/draco
%{_pkgconfigdir}/draco.pc
%{_datadir}/cmake/draco

%files static
%defattr(644,root,root,755)
%{_libdir}/libdraco.a
