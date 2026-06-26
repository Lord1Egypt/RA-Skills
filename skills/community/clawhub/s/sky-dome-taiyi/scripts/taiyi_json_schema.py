#!/usr/bin/env python3
"""Infer a simple JSON schema from JSON/JSONL samples."""
from __future__ import annotations
import argparse, json, sys
parser=argparse.ArgumentParser(); parser.add_argument('file',nargs='?'); args=parser.parse_args()
txt=open(args.file,encoding='utf-8').read() if args.file else sys.stdin.read()
vals=[]
try: vals=[json.loads(txt)]
except Exception:
    vals=[json.loads(x) for x in txt.splitlines() if x.strip()]
def typ(v):
    if isinstance(v,dict): return {'type':'object','properties':merge_objs([v])}
    if isinstance(v,list): return {'type':'array','items':merge([typ(x) for x in v]) if v else {}}
    if isinstance(v,bool): return {'type':'boolean'}
    if isinstance(v,int) and not isinstance(v,bool): return {'type':'integer'}
    if isinstance(v,float): return {'type':'number'}
    if v is None: return {'type':'null'}
    return {'type':'string'}
def merge(schemas):
    types=sorted(set(str(s.get('type','unknown')) for s in schemas))
    if len(types)==1:
        t=types[0]
        if t=='object':
            props={}
            keys=sorted(set().union(*(set(s.get('properties',{}).keys()) for s in schemas)))
            for k in keys:
                props[k]=merge([s['properties'][k] for s in schemas if k in s.get('properties',{})])
            return {'type':'object','properties':props}
        if t=='array':
            item_schemas=[s.get('items',{}) for s in schemas if s.get('items')]
            return {'type':'array','items':merge(item_schemas) if item_schemas else {}}
        return schemas[0]
    return {'anyOf':schemas[:8]}
def merge_objs(objs):
    keys=sorted(set().union(*(o.keys() for o in objs if isinstance(o,dict))))
    out={}
    for k in keys: out[k]=merge([typ(o[k]) for o in objs if isinstance(o,dict) and k in o])
    return out
schema=merge([typ(v) for v in vals])
print(json.dumps(schema,ensure_ascii=False,indent=2))
