#!/usr/bin/env python3
"""Simple HTTP API smoke test with timing and JSON preview."""
from __future__ import annotations
import argparse, json, time, urllib.request
parser=argparse.ArgumentParser(); parser.add_argument('url'); parser.add_argument('-X','--method',default='GET'); parser.add_argument('-H','--header',action='append',default=[]); parser.add_argument('-d','--data'); parser.add_argument('--timeout',type=float,default=15); args=parser.parse_args()
headers=dict(h.split(':',1) for h in args.header if ':' in h)
data=args.data.encode() if args.data is not None else None
req=urllib.request.Request(args.url,data=data,method=args.method,headers=headers)
t=time.perf_counter()
try:
    with urllib.request.urlopen(req,timeout=args.timeout) as r:
        body=r.read(4096); dt=time.perf_counter()-t
        print(json.dumps({'ok':True,'status':r.status,'elapsed_ms':round(dt*1000,2),'content_type':r.headers.get('content-type'),'preview':body.decode(errors='replace')[:1000]},ensure_ascii=False,indent=2))
except Exception as e:
    dt=time.perf_counter()-t
    print(json.dumps({'ok':False,'elapsed_ms':round(dt*1000,2),'error':str(e)},ensure_ascii=False,indent=2))
