#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile
import re, sys, json, xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print('usage: inspect_pptx.py <pptx> [out.json]', file=sys.stderr); sys.exit(2)
p=Path(sys.argv[1])
out=Path(sys.argv[2]) if len(sys.argv)>2 else None
ns_t='{http://schemas.openxmlformats.org/drawingml/2006/main}t'
with ZipFile(p) as z:
    slides=sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)], key=lambda n:int(re.search(r'slide(\d+)',n).group(1)))
    media=[n for n in z.namelist() if n.startswith('ppt/media/')]
    result={'file':str(p),'size':p.stat().st_size,'slides':len(slides),'media':len(media),'pages':[]}
    for i,n in enumerate(slides,1):
        root=ET.fromstring(z.read(n))
        texts=[t.text.strip() for t in root.iter(ns_t) if t.text and t.text.strip()]
        result['pages'].append({'page':i,'xml':n,'text':texts})
print(json.dumps(result,ensure_ascii=False,indent=2))
if out: out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
