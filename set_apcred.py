#!/usr/bin/python


import os
import netifaces
import bcrypt
import binascii


IFACE = 'wlp2s0'
PREFIX = 'linuxnode'
# CONFIG_PATH = '/etc/hostapd/hostapd.conf'
CONFIG_PATH = 'hostapd.conf'


def netifaces_iface(iface):
    return netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']


def build_mac(macid):
    return macid.replace(':', '')


def build_psk(macid):
    mac_str = build_mac(macid)
    bc = bcrypt.kdf(mac_str.encode(), salt=PREFIX.encode(), desired_key_bytes=45, rounds=100)
    bc_b64 = binascii.b2a_base64(bc, newline=False)
    bc_b64 = bc_b64.replace(b'/', b'')
    bc_b64 = bc_b64.replace(b'+', b'')
    if len(bc_b64) > 61:
        bc_b64 = bc_b64[:61]
    return bc_b64.decode()


def write_config(params):
    with open(template_path, 'r') as f:
        cfg = f.read()

    for k, v in params.items():
        cfg = cfg.replace(k, v)

    with open(CONFIG_PATH, 'w') as f:
        f.write(cfg)


if __name__ == '__main__':
    template_path = CONFIG_PATH + '.in'
    if not os.path.exists(template_path):
        exit(0)

    params = {
        '[MAC]': build_mac(netifaces_iface(IFACE)),
        '[PSK]': build_psk(netifaces_iface(IFACE))
    }

    write_config(params)
