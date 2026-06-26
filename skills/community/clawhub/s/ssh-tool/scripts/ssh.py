#!/usr/bin/env python3
"""SSH Tool - SSH client wrapper."""
import argparse, subprocess, sys
parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('cmd', nargs='*')
args = parser.parse_args()
cmd = ['ssh', args.host] + (args.cmd or [])
subprocess.run(cmd)
