# -*- coding: utf-8 -*-
"""构建期脚本：生成 / 校验 papers.json（试卷库）。

每张卷 = 27 题全量，仅打乱：
  1) 题目顺序（题目顺序打乱）
  2) 每题选项的展示顺序（选项顺序打乱，default 项跟着搬家）

固定种子，同种子输出完全一致。
"""
import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name):
    with open(DATA / name, "r", encoding="utf-8") as f:
        return json.load(f)


def build(paper_count, seed, questions):
    rng = random.Random(seed)
    papers = []
    for no in range(1, paper_count + 1):
        order = list(range(len(questions)))
        rng.shuffle(order)
        opts = {}
        for q in questions:
            idx = list(range(len(q["options"])))
            rng.shuffle(idx)
            opts[str(q["id"])] = idx
        papers.append({"no": no, "order": order, "opts": opts})
    return papers


def check(papers, questions):
    errors = []
    n = len(questions)
    for p in papers:
        if sorted(p["order"]) != list(range(n)):
            errors.append(f"卷 {p['no']}：题目顺序不是 0..{n-1} 的排列")
        for q in questions:
            got = p["opts"].get(str(q["id"]))
            if got is None or sorted(got) != list(range(len(q["options"]))):
                errors.append(f"卷 {p['no']} 题 {q['id']}：选项顺序不是全排列")
    # 两张卷不完全相同
    sigs = {json.dumps([p["order"], p["opts"]], sort_keys=True) for p in papers}
    if len(sigs) != len(papers):
        errors.append("存在两张完全相同的卷")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=None, help="试卷数量（默认读 meta.json）")
    ap.add_argument("--seed", type=int, default=None, help="随机种子（默认读 meta.json）")
    ap.add_argument("--check", action="store_true", help="只校验现有 papers.json，不重写")
    args = ap.parse_args()

    meta = load("meta.json")
    questions = load("questions.json")["questions"]
    count = args.count if args.count is not None else meta["paper_count"]
    seed = args.seed if args.seed is not None else meta["paper_seed"]

    out = DATA / "papers.json"
    if args.check:
        if not out.exists():
            print("[缺失] papers.json 不存在，请先去掉 --check 重新生成")
            sys.exit(1)
        papers = json.loads(out.read_text(encoding="utf-8"))["papers"]
    else:
        papers = build(count, seed, questions)
        out.write_text(
            json.dumps({"version": 1, "seed": seed, "count": count, "papers": papers},
                       ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        print(f"已生成 {count} 张卷（种子 {seed}）→ {out}")

    errs = check(papers, questions)
    if errs:
        for e in errs:
            print("[卷结构错误]", e)
        sys.exit(1)
    print(f"校验通过：{len(papers)} 张卷，每张 {len(questions)} 题，结构与覆盖正常")


if __name__ == "__main__":
    main()
