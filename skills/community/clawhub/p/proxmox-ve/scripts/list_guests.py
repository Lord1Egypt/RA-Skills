#!/usr/bin/env python3
import argparse
import json
import sys
from pve_api import build_client

parser = argparse.ArgumentParser(description='List Proxmox guests on a node')
parser.add_argument('node')
parser.add_argument('--kind', choices=['qemu', 'lxc', 'all'], default='all')
args = parser.parse_args()

client = build_client()
out = {}
if args.kind in ('qemu', 'all'):
    out['qemu'] = client.get(f'/nodes/{args.node}/qemu')
if args.kind in ('lxc', 'all'):
    out['lxc'] = client.get(f'/nodes/{args.node}/lxc')
json.dump(out, sys.stdout, indent=2)
print()
