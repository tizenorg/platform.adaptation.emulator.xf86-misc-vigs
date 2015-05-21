Name:    xf86-misc-vigs
Summary:    X.Org X11 X server configuration files for vigs
Version:    0.1.0
Release:    1
ExclusiveArch:    %ix86
Group:      System/X11
License:    MIT
Source0:    %{name}-%{version}.tar.gz

Requires:   xserver-xorg-core
Requires:   xorg-x11-drv-evdev-multitouch

%description
Description: %{summary}

%prep
%setup -q

%install

mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}

mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/etc/X11/xorg.conf.d
mkdir -p %{buildroot}/etc/X11/arch-preinit.d
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/etc/rc.d/rc3.d
mkdir -p %{buildroot}/etc/rc.d/rc4.d
mkdir -p %{buildroot}/etc/profile.d

install -m 755 i386-common/startx %{buildroot}/usr/bin/startx
install -m 755 i386-common/scripts/setcpu %{buildroot}/usr/bin/setcpu
install -m 755 i386-common/scripts/setpoll %{buildroot}/usr/bin/setpoll
install -m 755 i386-common/xinitrc %{buildroot}/etc/X11/xinitrc
install -m 644 i386-common/xorg.conf %{buildroot}/etc/X11/xorg.conf

install -m 755 i386-common/Xorg.sh %{buildroot}/etc/profile.d/Xorg.sh
install -m 755 i386-common/xserver %{buildroot}/etc/rc.d/init.d/xserver
install -m 755 i386-common/xresources %{buildroot}/etc/rc.d/init.d/xresources

install -m 644 i386-common/Xmodmap %{buildroot}/etc/X11/Xmodmap
install -m 644 i386-common/Xresources %{buildroot}/etc/X11/Xresources
install -m 644 i386-common/Xorg.arch-options %{buildroot}/etc/X11/Xorg.arch-options
install -m 755 i386-common/xsetrc %{buildroot}/etc/X11/xsetrc

if [ -d i386-common/arch-preinit.d ]; then
    cp -a i386-common/arch-preinit.d %{buildroot}/etc/X11/
fi

ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S20xserver
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S20xserver
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc3.d/S80xresources
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc4.d/S80xresources

cp -Rd conf-i386* %{buildroot}/etc/X11/

mkdir -p %{buildroot}%{_libdir}/systemd/system/basic.target.wants
install -m 0644 i386-common/xorg.service %{buildroot}%{_libdir}/systemd/system/xorg.service
ln -s ../xorg.service %{buildroot}%{_libdir}/systemd/system/basic.target.wants/xorg.service
mkdir -p %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants
install -m 0644 i386-common/xresources.service %{buildroot}%{_libdir}/systemd/system/xresources.service
ln -s ../xresources.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/xresources.service

%post
mkdir -p /etc/X11/xorg.conf.d
for i in /etc/X11/conf-i386-vigs/*; do
    f="${i##*/}"
    d="/etc/X11/xorg.conf.d/$f"
    rm -f "$d"
    ln -s "$i" "$d"
done

%files
%manifest xf86-misc-vigs.manifest
%defattr(-,root,root,-)
/usr/share/license/%{name}
/usr/bin/startx
/usr/bin/setcpu
/usr/bin/setpoll
/etc/X11/xinitrc
/etc/profile.d/Xorg.sh
/etc/rc.d/init.d/*
/etc/X11/xorg.conf
/etc/rc.d/rc3.d/*
/etc/rc.d/rc4.d/*
/etc/X11/Xmodmap
/etc/X11/Xresources
%attr(755,root,root) /etc/X11/xsetrc
/etc/X11/Xorg.arch-options
%dir /etc/X11/arch-preinit.d
/etc/X11/arch-preinit.d/*
/etc/X11/conf-i386-vigs/*
%{_libdir}/systemd/system/xorg.service
%{_libdir}/systemd/system/basic.target.wants/xorg.service
%{_libdir}/systemd/system/xresources.service
%{_libdir}/systemd/system/multi-user.target.wants/xresources.service
