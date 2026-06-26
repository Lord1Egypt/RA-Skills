#!/usr/bin/env python3
"""Tiny benchmark harness for shell commands."""
from __future__ import annotations
import argparse, statistics, subprocess, time
parser=argparse.ArgumentParser()
parser.add_argument('-n','--runs',type=int,default=3)
parser.add_argument('cmd', nargs=argparse.REMAINDER, help='command to benchmark; use -- before commands with flags')
args=parser.parse_args()
cmd=args.cmd[1:] if args.cmd and args.cmd[0]=='--' else args.cmd
if not cmd: raise SystemExit('missing command')
times=[]
for i in range(args.runs):
    t=time.perf_counter(); r=subprocess.run(cmd,capture_output=True,text=True); dt=time.perf_counter()-t; times.append(dt)
    print(f'run {i+1}: {dt:.4f}s exit={r.returncode}')
    if r.returncode!=0:
        print((r.stderr or r.stdout)[-1000:]); break
if times: print(f'mean={statistics.mean(times):.4f}s min={min(times):.4f}s max={max(times):.4f}s')
