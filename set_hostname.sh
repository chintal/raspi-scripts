#!/bin/bash

IFACE=wlan0
read MAC </sys/class/net/$IFACE/address
MAC="signagenode-${MAC//:}"

echo "$MAC" > "/etc/hostname"
CURRENT_HOSTNAME=$(cat /proc/sys/kernel/hostname)
sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$MAC/g" /etc/hosts
hostname $MAC
