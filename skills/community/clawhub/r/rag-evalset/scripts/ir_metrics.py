#!/usr/bin/env python3
"""计算标准 IR 排序指标：Recall@K、Precision@K、HitRate@K、MRR、NDCG@K。

输入：
  --evalset  带 gold_chunk_ids 的 evalset.jsonl（build_evalset.py 产出）
  --runs     被测检索系统的输出，每行：
             {"query_id": "q0001", "chunk_ids": ["doc-a-0003", ...]}  # 从最相关排起

纯标准库实现，适合进 CI。输出 markdown 表格，可用 --bucket 按字段分桶。
"""
import argparse
import json
import math
import sys
from pathlib import Path


def load_jsonl(path):
    rows = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"{path}:{n}: JSON 格式错误：{e}")
    return rows


def recall_at_k(gold, ranked, k):
    if not gold:
        return None
    return len(gold & set(ranked[:k])) / len(gold)


def precision_at_k(gold, ranked, k):
    return len(gold & set(ranked[:k])) / k


def hit_rate_at_k(gold, ranked, k):
    return 1.0 if gold & set(ranked[:k]) else 0.0


def mrr(gold, ranked):
    for i, cid in enumerate(ranked, 1):
        if cid in gold:
            return 1.0 / i
    return 0.0


def ndcg_at_k(gold, ranked, k):
    top = ranked[:k]
    dcg = sum(1.0 / math.log2(i + 2) for i, cid in enumerate(top) if cid in gold)
    ideal_hits = min(len(gold), k)
    if ideal_hits == 0:
        return None
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
    return dcg / idcg


METRICS = {
    "Recall": recall_at_k,
    "Precision": precision_at_k,
    "HitRate": hit_rate_at_k,
    "NDCG": ndcg_at_k,
}


def score_group(rows, ks):
    """rows: [(gold集合, 排序列表)]，返回 {指标名: 均值}，含 MRR。"""
    n = len(rows)
    out = {}
    if n == 0:
        return out
    out["MRR"] = sum(mrr(g, r) for g, r in rows) / n
    for name, fn in METRICS.items():
        for k in ks:
            vals = [fn(g, r, k) for g, r in rows]
            vals = [v for v in vals if v is not None]
            if vals:
                out[f"{name}@{k}"] = sum(vals) / len(vals)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--evalset", required=True)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--k", default="1,3,5,10", help="逗号分隔的 K 值列表")
    ap.add_argument("--bucket", default=None, help="按 evalset 字段分桶统计，如 synthesizer")
    ap.add_argument("--out", default=None, help="把聚合结果写成 JSON 到该路径")
    ap.add_argument("--out-perq", default=None, help="逐条指标 jsonl（query_id + 各指标值），供 combine_report 联合分析")
    a = ap.parse_args()
    ks = sorted({int(x) for x in a.k.split(",")})

    gold_by_q, meta_by_q = {}, {}
    for r in load_jsonl(a.evalset):
        qid = r.get("query_id")
        gold = set(r.get("gold_chunk_ids") or [])
        if qid and gold:
            gold_by_q[qid] = gold
            meta_by_q[qid] = r
    if not gold_by_q:
        sys.exit("evalset 里没有任何 gold_chunk_ids 非空的样本")

    rows_by_bucket = {"ALL": []}
    run_by_q = {}
    seen, dupes, short_runs = set(), 0, 0
    for run in load_jsonl(a.runs):
        qid = run.get("query_id")
        if qid not in gold_by_q:
            continue
        if qid in seen:
            dupes += 1
            continue
        seen.add(qid)
        dedup = []
        for cid in list(run.get("chunk_ids") or []):  # 去重保首次出现：重复项会让排名虚高、指标失真
            if cid not in dedup:
                dedup.append(cid)
        run_by_q[qid] = dedup
        if len(dedup) < max(ks):
            short_runs += 1
        pair = (gold_by_q[qid], dedup)
        rows_by_bucket.setdefault("ALL", []).append(pair)
        if a.bucket:
            b = str(meta_by_q[qid].get(a.bucket, "unknown"))
            rows_by_bucket.setdefault(b, []).append(pair)

    missing = len(gold_by_q) - len(seen)
    print(f"参评查询：{len(seen)}；runs 缺失：{missing}；重复 run 行已跳过：{dupes}")
    if short_runs:
        print(f"! {short_runs} 条 run 返回的块数少于 {max(ks)}——大 K 的 @K 指标会偏悲观，建议检索更深")
    if not seen:
        sys.exit("evalset 的 query_id 与 runs 完全没有交集")
    print()
    cols = ["MRR"] + [f"{m}@{k}" for m in METRICS for k in ks]
    print("| 分组 | " + " | ".join(cols) + " |")
    print("|" + "---|" * (1 + len(cols)))
    results = {}
    for bucket, rows in rows_by_bucket.items():
        scores = score_group(rows, ks)
        if not scores:
            continue
        results[bucket] = scores
        print(f"| {bucket} | " + " | ".join(f"{scores[c]:.4f}" for c in cols) + " |")
    if a.out_perq:
        with open(a.out_perq, "w", encoding="utf-8") as f:
            for qid in sorted(seen):
                g = gold_by_q[qid]
                row = {"query_id": qid, "MRR": round(mrr(g, run_by_q[qid]), 4)}
                for name, fn in METRICS.items():
                    for k in ks:
                        v = fn(g, run_by_q[qid], k)
                        if v is not None:
                            row[f"{name}@{k}"] = round(v, 4)
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"逐条指标 -> {a.out_perq}")
    if a.out:
        Path(a.out).write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n-> {a.out}")


if __name__ == "__main__":
    main()
