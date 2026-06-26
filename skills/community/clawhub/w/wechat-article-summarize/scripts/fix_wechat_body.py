#!/usr/bin/env python3
import argparse, html, re
from pathlib import Path

def normalize_text(s:str)->str:
    s=re.sub(r'<script.*?</script>','',s,flags=re.I|re.S)
    s=re.sub(r'<style.*?</style>','',s,flags=re.I|re.S)
    s=re.sub(r'<br\s*/?>','\n',s,flags=re.I)
    s=re.sub(r'</p\s*>','\n\n',s,flags=re.I)
    s=re.sub(r'</section\s*>','\n',s,flags=re.I)
    s=re.sub(r'<[^>]+>','',s)
    s=html.unescape(s).replace('\xa0',' ')
    s=re.sub(r'\n{3,}','\n\n',s)
    return s.strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('raw_html')
    ap.add_argument('--out', required=True)
    args=ap.parse_args()
    raw=Path(args.raw_html).read_text(encoding='utf-8', errors='replace')
    m=re.search(r"content_noencode:\s*JsDecode\('(.*?)'\),", raw, re.S)
    if not m:
        raise SystemExit('content_noencode not found')
    s=m.group(1).encode('utf-8').decode('unicode_escape')
    try:
        fixed=s.encode('latin1','ignore').decode('utf-8','ignore')
    except Exception:
        fixed=s
    text=normalize_text(fixed)
    out=Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')
    print(out)

if __name__=='__main__':
    main()
