%define kannel_user    kannel
%define kannel_group   %{kannel_user}
%define kannel_home    %{_localstatedir}/lib/kannel
%define kannel_confdir %{_sysconfdir}/kannel
%define kannel_datadir %{_datadir}/kannel

Name:           kannel
Version:        1.5.0
Release:        1%{?dist}
Summary:        WAP and SMS gateway

Group:          System Environment/Daemons
License:        Kannel

URL:            http://www.kannel.org/
Source0:        https://redmine.kannel.org/attachments/download/198/gateway-1.5.0.tar.gz

Source1:        %{name}.init
Source2:        %{name}.config
Source3:        %{name}.logrotate

Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pcre-devel openssl-devel zlib-devel
BuildRequires: setup >= 2.5
Requires: pcre openssl zlib

%description
The Kannel Open Source WAP and SMS gateway

%prep
%setup -q -n gateway-%{version}

%build
#%ifarch %ix86 x86_64
#use_regparm="USE_REGPARM=1"
#%endif

%configure \
    --disable-docs \
    --enable-start-stop-daemon \
    --enable-ssl \
    --enable-pam
make %{?_smp_mflags}

%install
%makeinstall

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/groupadd -r %{kannel_group} 2>/dev/null || :
%{_sbindir}/useradd -g %{kannel_group} -d %{kannel_home} -s /sbin/nologin -r %{kannel_user} 2>/dev/null || :

%post
/sbin/chkconfig --add kannel

%preun
if [ "$1" -eq 0 ]; then
    /sbin/service kannel stop >/dev/null 2>&1
    /sbin/chkconfig --del kannel
fi

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service kannel condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING ChangeLog NEWS README STATUS
%doc contrib/*
%doc doc/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man?/*
