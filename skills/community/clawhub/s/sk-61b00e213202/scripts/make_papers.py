# -*- coding: utf-8 -*-
"""make_papers.py — 构建期生成 / 校验 papers.json（固定种子，勿手改）。

每张卷 = 8 题全选 + 题序乱排 + 每题选项乱排。
随机作答基准下每道题被抽中次数完全相同（每卷都含全部 8 题）。
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = 20260917
PAPER_COUNT = 20


def build():
    questions = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
    qids = [q["id"] for q in questions["questions"]]
    rng = random.Random(SEED)
    papers = []
    for i in range(1, PAPER_COUNT + 1):
        order = qids[:]
        rng.shuffle(order)
        opt_orders = {}
        for q in questions["questions"]:
            ids = [o["id"] for o in q["options"]]
            rng.shuffle(ids)
            opt_orders[q["id"]] = ids
        papers.append({
            "paper_id": f"P{i:02d}",
            "order": order,
            "opt_orders": opt_orders,
        })
    out = {"version": questions["version"], "seed": SEED, "papers": papers}
    (DATA / "papers.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"papers.json 写入完成：{PAPER_COUNT} 张卷（seed={SEED}）")


def check():
    questions = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
    papers = json.loads((DATA / "papers.json").read_text(encoding="utf-8"))["papers"]
    qmap = {q["id"]: q for q in questions["questions"]}
    errors = []
    if len(papers) != PAPER_COUNT:
        errors.append(f"卷数 {len(papers)} != {PAPER_COUNT}")
    seen_opts = set()
    for p in papers:
        if sorted(p["order"]) != sorted(qmap):
            errors.append(f"{p['paper_id']} 题目覆盖不全")
        for qid, oids in p["opt_orders"].items():
            if sorted(oids) != sorted(o["id"] for o in qmap[qid]["options"]):
                errors.append(f"{p['paper_id']}/{qid} 选项覆盖不全")
            seen_opts.update((qid, oid) for oid in oids)
    # 逐题五行峰值 = max_weight（配平铁律）
    mw = questions["max_weight"]
    for q in questions["questions"]:
        peaks = {}
        for o in q["options"]:
            for a, w in o["weights"].items():
                peaks[a] = max(peaks.get(a, 0), w)
        for a in ["metal", "wood", "water", "fire", "earth"]:
            if peaks.get(a, 0) != mw:
                errors.append(f"{q['id']} 属性 {a} 峰值 {peaks.get(a, 0)} != {mw}")
    # 每个选项在卷库中至少出现一次
    all_pairs = {(q["id"], o["id"]) for q in questions["questions"] for o in q["options"]}
    missing = all_pairs - seen_opts
    if missing:
        errors.append(f"有选项从未在任何卷中出现过: {sorted(missing)}")
    if errors:
        print("CHECK FAILED:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"check 通过：{len(papers)} 卷 × 8 题，逐题五行峰值 = {mw}，覆盖完整。")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        build()
