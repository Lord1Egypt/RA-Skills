#!/usr/bin/env python3
"""Find leftover placeholders. Usage: check_placeholders.py PATH. Exit 1 if any found."""
import re, sys, os, json
PAT=re.compile(r"\b(TODO|FIXME|TBD|XXX+|lorem ipsum)\b|\{\{\s*\w+\s*\}\}|\[(插入|待补|placeholder)[^\]]*\]|此处填写",re.I)
def files(p):
    if os.path.isfile(p): yield p; return
    for r,_,fs in os.walk(p):
        for f in fs:
            if f.endswith((".md",".txt",".html",".htm",".json",".yaml",".yml",".csv",".xml",".py",".js",".ts",".tsx")): yield os.path.join(r,f)
if __name__=="__main__":
    if len(sys.argv)<2: print(__doc__); sys.exit(2)
    out=[]
    for f in files(sys.argv[1]):
        for i,l in enumerate(open(f,encoding="utf-8",errors="ignore"),1):
            for m in PAT.finditer(l): out.append({"file":f,"line":i,"match":m.group(0)})
    print(json.dumps({"pass":not out,"hits":out},ensure_ascii=False,indent=1)); sys.exit(1 if out else 0)
