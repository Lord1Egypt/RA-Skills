#!/usr/bin/env python3
"""Tiny durable task queue for agent work."""
from __future__ import annotations
import argparse, json, datetime
from pathlib import Path

def load(path):
    if path.exists(): return json.loads(path.read_text())
    return {'tasks':[]}
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--file', default='state/taiyi-tasks.json')
    sub=ap.add_subparsers(dest='cmd', required=True)
    a=sub.add_parser('add'); a.add_argument('title'); a.add_argument('--priority',type=int,default=3); a.add_argument('--status',default='pending')
    sub.add_parser('list')
    d=sub.add_parser('done'); d.add_argument('id',type=int)
    n=sub.add_parser('next')
    args=ap.parse_args(); path=Path(args.file); data=load(path)
    if args.cmd=='add':
        tid=(max([t['id'] for t in data['tasks']], default=0)+1)
        data['tasks'].append({'id':tid,'title':args.title,'priority':args.priority,'status':args.status,'created':datetime.datetime.now().isoformat(timespec='seconds')})
        save(path,data); print(f'added #{tid}')
    elif args.cmd=='done':
        for t in data['tasks']:
            if t['id']==args.id: t['status']='done'; t['done']=datetime.datetime.now().isoformat(timespec='seconds'); break
        save(path,data); print(f'done #{args.id}')
    elif args.cmd=='next':
        open_tasks=[t for t in data['tasks'] if t.get('status')!='done']
        open_tasks.sort(key=lambda t:(-t.get('priority',3),t.get('created','')))
        print(json.dumps(open_tasks[0] if open_tasks else None,ensure_ascii=False,indent=2))
    else:
        for t in sorted(data['tasks'], key=lambda x:(x.get('status')=='done',-x.get('priority',3),x.get('id',0))):
            print(f"#{t['id']} P{t.get('priority',3)} {t.get('status','pending')} - {t['title']}")
if __name__=='__main__': main()
