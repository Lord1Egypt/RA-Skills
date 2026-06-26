#!/usr/bin/env python3
"""Taiyi durable memory: append/search safe, non-secret lessons in JSONL."""
from __future__ import annotations
import argparse, datetime, json, re
from pathlib import Path
SECRET=re.compile(r'(?i)(api[_-]?key|token|password|secret|bearer\s+[a-z0-9._-]{10,}|sk-[a-z0-9_-]{10,})')
SECOPS=re.compile(r'(?i)(exploit|payload|reverse shell|privilege escalation|渗透|漏洞利用|攻击细节|黑客操作)')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--file',default='state/taiyi-memory.jsonl')
    sub=ap.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('add'); a.add_argument('text'); a.add_argument('--kind',default='lesson'); a.add_argument('--tags',default='')
    s=sub.add_parser('search'); s.add_argument('query'); s.add_argument('--limit',type=int,default=10)
    sub.add_parser('list').add_argument('--limit',type=int,default=20)
    args=ap.parse_args(); path=Path(args.file); path.parent.mkdir(parents=True,exist_ok=True)
    if args.cmd=='add':
        if SECRET.search(args.text): raise SystemExit('refused: possible secret')
        if SECOPS.search(args.text): raise SystemExit('refused: possible operational security-abuse detail; store high-level defensive lesson only')
        rec={'ts':datetime.datetime.now().isoformat(timespec='seconds'),'kind':args.kind,'tags':[t for t in args.tags.split(',') if t.strip()],'text':args.text}
        with path.open('a',encoding='utf-8') as f: f.write(json.dumps(rec,ensure_ascii=False)+'\n')
        print('stored')
    else:
        rows=[]
        if path.exists():
            rows=[json.loads(x) for x in path.read_text().splitlines() if x.strip()]
        if args.cmd=='search':
            q=args.query.lower(); rows=[r for r in rows if q in r.get('text','').lower() or q in ' '.join(r.get('tags',[])).lower()]
            rows=rows[-args.limit:]
        elif args.cmd=='list': rows=rows[-args.limit:]
        for r in rows: print(f"[{r['ts']}] {r.get('kind','lesson')} {','.join(r.get('tags',[]))}: {r['text']}")
if __name__=='__main__': main()
