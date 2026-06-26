#!/usr/bin/env python3
import argparse, csv, re, json
from collections import Counter

def words(text):
    return re.findall(r"[A-Za-z][A-Za-z0-9+.#-]{1,}", text.lower())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume_txt")
    ap.add_argument("job_txt")
    ap.add_argument("--out", default="resume_match.json")
    args = ap.parse_args()
    resume = open(args.resume_txt, "r", encoding="utf-8").read()
    job = open(args.job_txt, "r", encoding="utf-8").read()
    rw, jw = set(words(resume)), Counter(words(job))
    top = [w for w, c in jw.most_common(40) if len(w) > 2]
    missing = [w for w in top if w not in rw][:20]
    score = round(100 * (len(top) - len(missing)) / max(len(top), 1), 1)
    json.dump({"score": score, "missing_keywords": missing, "top_keywords": top}, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
