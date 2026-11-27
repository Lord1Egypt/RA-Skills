#!/usr/bin/env python3
"""Rewrite fidelity: numbers / quoted strings / Latin proper nouns present in BEFORE but missing in AFTER.
Usage: claims_diff.py BEFORE AFTER. Exit 1 if anything is lost. Semantic claim changes still need a judge."""
import re, sys, json
def atoms(t):
    nums=set(re.findall(r"\d+(?:[.,]\d+)?%?",t))
    quotes=set(re.findall(r"[“\"]([^”\"]{2,40})[”\"]",t))
    names=set(re.findall(r"\b[A-Z][a-zA-Z0-9]+(?:[ -][A-Z][a-zA-Z0-9]+)*\b",t))
    return {"numbers":nums,"quotes":quotes,"names":names}
if __name__=="__main__":
    if len(sys.argv)<3: print(__doc__); sys.exit(2)
    a=atoms(open(sys.argv[1],encoding="utf-8").read()); b=atoms(open(sys.argv[2],encoding="utf-8").read())
    lost={k:sorted(a[k]-b[k]) for k in a}
    ok=not any(lost.values())
    print(json.dumps({"pass":ok,"lost":lost},ensure_ascii=False,indent=1)); sys.exit(0 if ok else 1)
