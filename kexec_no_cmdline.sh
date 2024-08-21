#!/bin/bash


kexec -l $1 --initrd=$2 --append="ro root=LABEL=/ biosdevname=0 net.ifnames=0 fsck.repair=yes systemd.gpt_auto=0 ipv6.autoconf=0 msr.allow_writes=on pcie_pme=nomsi netconsole=+6666@2401:db00:3021:01a3:face:0000:0065:0000/eth0,1514@2401:db00:eef0:a59::/02:90:fb:64:b5:86 swiotlb=4096 crashkernel=128M console=tty0 console=ttyS1,57600"

kexec -e
