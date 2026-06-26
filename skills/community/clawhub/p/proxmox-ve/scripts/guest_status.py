#!/usr/bin/env python3
import argparse
import json
import sys
from pve_api import build_client

parser = argparse.ArgumentParser(description='Get Proxmox guest status')
parser.add_argument('node')
parser.add_argument('kind', choices=['qemu', 'lxc'])
parser.add_argument('vmid')
args = parser.parse_args()

client = build_client()
path = f'/nodes/{args.node}/{args.kind}/{args.vmid}/status/current'
json.dump(client.get(path), sys.stdout, indent=2)
print()
