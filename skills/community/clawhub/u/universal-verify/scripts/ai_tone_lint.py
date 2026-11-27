#!/usr/bin/env python3
"""Lexical AI-tone lint (zh + en). Usage: ai_tone_lint.py FILE [--max-per-1k N]. Exit 1 if over threshold."""
import re, sys, json
ZH = {
 "不是…而是": r"不是[^。！？\n]{1,30}而是",
 "套话开头": r"在[^。\n]{1,20}的(今天|时代|背景下)",
 "过渡套话": r"值得(注意|一提)的是|需要指出的是|毋庸置疑|不可否认",
 "总结套话": r"总而言之|综上所述|总的来说|一言以蔽之",
 "营销词": r"赋能|助力|打造|闭环|抓手|颠覆|极致|全方位|深度融合",
 "空洞升华": r"(让我们|未来可期|意义深远|开启.{0,6}新篇章)",
}
EN = {
 "not X but Y": r"\bnot (just |only )?\w[^.]{0,40}, but\b",
 "stock words": r"\b(delve|tapestry|testament|pivotal|seamless(ly)?|leverage|robust|showcase|underscore|realm|landscape)\b",
 "chat leftovers": r"(I hope this helps|Great question|Certainly!|As an AI)",
 "filler": r"\b(it'?s worth noting|in today'?s|in conclusion|ultimately)\b",
}
def lint(text):
    hits=[]
    for table in (ZH,EN):
        for k,p in table.items():
            for m in re.finditer(p,text,re.I):
                hits.append({"rule":k,"match":m.group(0),"pos":m.start()})
    dash=text.count("—")//1 - text.count("——")  # "——" counts once
    bold=len(re.findall(r"\*\*[^*]+\*\*",text))
    n=max(len(text),1)/1000
    if dash/n>3: hits.append({"rule":"破折号密度/em-dash density","match":f"{dash} dashes","pos":-1})
    if bold/n>4: hits.append({"rule":"粗体密度/bold density","match":f"{bold} bold spans","pos":-1})
    return hits, round(len(hits)/n,2)
if __name__=="__main__":
    if len(sys.argv)<2: print(__doc__); sys.exit(2)
    mx=float(sys.argv[sys.argv.index("--max-per-1k")+1]) if "--max-per-1k" in sys.argv else 3
    hits,rate=lint(open(sys.argv[1],encoding="utf-8").read())
    print(json.dumps({"per_1k_chars":rate,"threshold":mx,"pass":rate<=mx,"hits":hits},ensure_ascii=False,indent=1))
    sys.exit(0 if rate<=mx else 1)
