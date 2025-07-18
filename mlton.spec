# BIG FAT WARNING: it requires 400MB memory allocated, if you have less
# don't even try do build it (or you would kill your machine with swapping)

Summary:	An optimizing compiler for the Standard ML programming language
Summary(pl.UTF-8):	Optymalizujący kompilator dla języka programowania Standard ML
Name:		mlton
Version:	20021122
Release:	2
License:	GPL
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}-1.src.tgz
# Source0-md5:	819274ea86202f0964d4edec8ba456b9
Patch0:		%{name}-no-doc-install.patch
URL:		http://www.mlton.org/
BuildRequires:	gmp-devel >= 3.1.1
BuildRequires:	latex2html
BuildRequires:	mlton
# gmp library is needed for linking with itself
# it will _not_ be resolved by rpm requires searching automate
Requires:	gmp >= 3.1.1
Requires:	gcc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MLton is a whole-program optimizing compiler for the Standard ML
programming language. It produces very fast code, almost comparable
to gcc.

%description -l pl.UTF-8
MLton jest optimalizującym kompilatorem dla języka programowania Standard ML
kompilującym cały program na raz. MLton produkuje bardzo szybki kod, prawie
tak dobry, jak gcc.

%prep
%setup -q
%patch -P0 -p1

%build
# it will compile mlton twice: first time with installed mlton
# and second time with the just compiled one
%{__make} bootstrap \
	VERSION=%{version} \
	CC="%{__cc} -I. %{rpmcflags}" \
	CFLAGS="-DNODEBUG"

for n in hacker library style user; do
	guide="$n-guide"
	cd doc/$guide
	make main.ps main/main.html
	mv main.ps $guide.ps
	mv main $guide
	cd -
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

perl -pi -e 's/-mcpu=.*/%{optflags}/' bin/mlton

%{__make} install \
	prefix=%{_prefix} \
	TBIN=$RPM_BUILD_ROOT%{_bindir} \
	TLIB=$RPM_BUILD_ROOT%{_libdir}/mlton \
	TMAN=$RPM_BUILD_ROOT%{_mandir}/man1

cp -a doc/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/README doc/changelog
%doc doc/*-guide/*-guide.ps doc/*-guide/*-guide
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/mlton
%attr(755,root,root) %{_libdir}/mlton/mlton-compile
%{_libdir}/mlton/world.mlton
%{_libdir}/mlton/hostmap
%{_libdir}/mlton/self
%{_mandir}/man1/*
%{_examplesdir}/%{name}-%{version}
