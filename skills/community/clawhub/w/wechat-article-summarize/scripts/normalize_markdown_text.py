#!/usr/bin/env python3
import argparse, re
from pathlib import Path

def normalize(md:str)->str:
    lines=md.splitlines()
    out=[]
    para=[]
    def flush_para():
        nonlocal para
        if para:
            text=' '.join(x.strip() for x in para if x.strip())
            text=re.sub(r'\s+',' ',text).strip()
            if text:
                out.append(text)
            para=[]
    for line in lines:
        stripped=line.rstrip()
        if not stripped.strip():
            flush_para();
            if out and out[-1] != '': out.append('')
            continue
        if re.match(r'^(#{1,6}\s|[-*]\s|\d+\.\s|>\s)', stripped):
            flush_para(); out.append(stripped); continue
        para.append(stripped)
    flush_para()
    text='\n'.join(out)
    text=re.sub(r'\n{3,}','\n\n',text).strip()+'\n'
    return text

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('input')
    ap.add_argument('--out', required=True)
    args=ap.parse_args()
    src=Path(args.input).read_text(encoding='utf-8', errors='replace')
    out=Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(normalize(src), encoding='utf-8')
    print(out)

if __name__=='__main__':
    main()
