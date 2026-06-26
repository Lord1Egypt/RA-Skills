#!/usr/bin/env python3
"""Taiyi workflow engine: create/list/advance workflow runs with evidence."""
from __future__ import annotations
import argparse, datetime, json, re
from pathlib import Path

def slug(s): return re.sub(r'-+','-',re.sub(r'[^\w\u4e00-\u9fff-]+','-',s.lower())).strip('-') or 'workflow'
def load_templates(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def save_run(path,data): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def load_run(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def current_step(run):
    for i,s in enumerate(run['steps']):
        if s.get('status')!='done': return i,s
    return None,None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dir',default='state/workflows')
    ap.add_argument('--templates',default=str(Path(__file__).resolve().parents[1]/'workflows'/'templates.json'))
    sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('templates')
    c=sub.add_parser('create'); c.add_argument('template'); c.add_argument('title'); c.add_argument('--mission',default='')
    l=sub.add_parser('list')
    s=sub.add_parser('show'); s.add_argument('run')
    a=sub.add_parser('advance'); a.add_argument('run'); a.add_argument('--evidence',default=''); a.add_argument('--note',default='')
    n=sub.add_parser('note'); n.add_argument('run'); n.add_argument('text')
    args=ap.parse_args(); root=Path(args.dir); root.mkdir(parents=True,exist_ok=True)
    templates=load_templates(args.templates)
    if args.cmd=='templates':
        for k,v in templates.items(): print(f"{k}: {v['name']} ({len(v['steps'])} steps)")
    elif args.cmd=='create':
        if args.template not in templates: raise SystemExit(f'unknown template: {args.template}')
        t=templates[args.template]; ts=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        path=root/f"{ts}-{slug(args.title)}.json"
        run={'title':args.title,'template':args.template,'mission':args.mission,'created':datetime.datetime.now().isoformat(timespec='seconds'),'updated':None,'notes':[], 'steps':[{'title':x,'status':'pending','evidence':[],'notes':[]} for x in t['steps']]}
        if run['steps']: run['steps'][0]['status']='active'
        save_run(path,run); print(path)
    elif args.cmd=='list':
        for p in sorted(root.glob('*.json')):
            r=load_run(p); i,st=current_step(r); print(f"{p.name}: {r['title']} -> {('complete' if st is None else st['title'])}")
    elif args.cmd=='show':
        p=Path(args.run); p=p if p.exists() else root/args.run
        r=load_run(p); print(f"# {r['title']}\nMission: {r.get('mission','')}\n")
        for idx,st in enumerate(r['steps'],1):
            mark={'done':'x','active':'>','pending':' '}[st.get('status','pending')]
            print(f"[{mark}] {idx}. {st['title']}")
            for e in st.get('evidence',[]): print(f"    evidence: {e}")
    elif args.cmd=='advance':
        p=Path(args.run); p=p if p.exists() else root/args.run
        r=load_run(p); i,st=current_step(r)
        if st is None: print('already complete'); return
        if args.evidence: st.setdefault('evidence',[]).append(args.evidence)
        if args.note: st.setdefault('notes',[]).append(args.note)
        st['status']='done'; st['done']=datetime.datetime.now().isoformat(timespec='seconds')
        if i+1 < len(r['steps']): r['steps'][i+1]['status']='active'
        r['updated']=datetime.datetime.now().isoformat(timespec='seconds')
        save_run(p,r); ni,ns=current_step(r); print('complete' if ns is None else f"next: {ns['title']}")
    elif args.cmd=='note':
        p=Path(args.run); p=p if p.exists() else root/args.run
        r=load_run(p); r.setdefault('notes',[]).append({'ts':datetime.datetime.now().isoformat(timespec='seconds'),'text':args.text}); save_run(p,r); print('noted')
if __name__=='__main__': main()
