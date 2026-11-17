#!/usr/bin/env python3
"""OR + 95%CI + p + Benjamini-Hochberg FDR, 按组分别计算。

输入: judgments jsonl, 每行 {"key":..., "group":"exp|ctrl", "lead":true/false,
                             "hits":{"R1":true,...}}
      (兼容首次产物字段名: skey/grp/j)
输出: JSON 到 stdout(或 --out 文件), 结构:
  {group: [{id, hit_lead, hit_nolead, miss_lead, miss_nolead,
            or, ci_lo, ci_hi, p, q, hit_rate}, ...(按 q 升序)]}

用法: or_fdr.py judgments.jsonl [--out results.json]
依赖: 纯标准库。OR 用 Haldane-Anscombe 校正(任一格为 0 时全表 +0.5)。
"""
import argparse
import json
import math
import sys
from collections import defaultdict


def norm_sf(z):
    """P(Z > z), 标准正态生存函数。"""
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def or_ci_p(a, b, c, d):
    """2x2 表: a=命中且留资, b=命中未留资, c=未命中留资, d=未命中未留资。"""
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    or_ = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    lo = math.exp(math.log(or_) - 1.96 * se)
    hi = math.exp(math.log(or_) + 1.96 * se)
    z = abs(math.log(or_)) / se
    p = 2 * norm_sf(z)
    return or_, lo, hi, p


def bh_fdr(pvals):
    """Benjamini-Hochberg, 返回与输入同序的 q 值。"""
    n = len(pvals)
    order = sorted(range(n), key=lambda i: pvals[i])
    q = [0.0] * n
    prev = 1.0
    for rank_from_end, idx in enumerate(reversed(order)):
        rank = n - rank_from_end  # 1-based rank of this p
        val = min(prev, pvals[idx] * n / rank)
        q[idx] = val
        prev = val
    return q


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("judgments")
    ap.add_argument("--out")
    args = ap.parse_args()

    # group -> rubric_id -> [a,b,c,d]
    tables = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0]))
    with open(args.judgments, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            g = rec.get("group") or rec["grp"]
            lead = bool(rec["lead"])
            hits = rec.get("hits") or rec["j"]
            for rid, hit in hits.items():
                t = tables[g][rid]
                if hit and lead:
                    t[0] += 1
                elif hit:
                    t[1] += 1
                elif lead:
                    t[2] += 1
                else:
                    t[3] += 1

    result = {}
    for g, rubrics in tables.items():
        ids = sorted(rubrics, key=lambda x: (len(x), x))  # R1..R9,R10..
        rows, ps = [], []
        for rid in ids:
            a, b, c, d = rubrics[rid]
            or_, lo, hi, p = or_ci_p(a, b, c, d)
            n = a + b + c + d
            rows.append({
                "id": rid, "hit_lead": a, "hit_nolead": b,
                "miss_lead": c, "miss_nolead": d,
                "or": round(or_, 3), "ci_lo": round(lo, 3),
                "ci_hi": round(hi, 3), "p": p,
                "hit_rate": round((a + b) / n, 4) if n else 0.0,
            })
            ps.append(p)
        qs = bh_fdr(ps)
        for row, q in zip(rows, qs):
            row["q"] = q
            row["p"] = round(row["p"], 6)
            row["q"] = round(q, 6)
        rows.sort(key=lambda r: r["q"])
        result[g] = rows

    out = json.dumps(result, ensure_ascii=False, indent=1)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"written: {args.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
