#!/usr/bin/env python3
"""联合报告：按 query_id 合并 IR 层逐条指标与 ragas 层裁判分数，并做象限诊断。

输入：
  --evalset   evalset.jsonl（提供问题文本）
  --ir-perq   ir_metrics.py --out-perq 产出
  --scores    ragas_eval.py --out 产出（可为空/缺省——此时只出 IR 侧）

象限诊断（检索 × 生成 是否达标）：
  检索达标 = Recall@--recall-k >= --recall-th
  生成达标 = --judge-metric >= --judge-th（缺该分数的行不计入象限）

| 象限 | 含义 | 行动 |
|---|---|---|
| 双达标 | 健康 | — |
| 检索达标/生成不达标 | 检对了但答错/幻觉 | 查提示词、生成模型、上下文组织 |
| 检索不达标/生成达标 | 没检到但靠常识答对 | 危险区：评估集外会崩，优先修检索 |
| 双不达标 | 全链路问题 | 先看 gold 标注质量，再看索引 |
"""
import argparse
import json
import sys
from pathlib import Path


def load_jsonl(path):
    if not path or not Path(path).exists():
        return []
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--evalset", required=True)
    ap.add_argument("--ir-perq", required=True)
    ap.add_argument("--scores", default=None)
    ap.add_argument("--recall-k", type=int, default=5, help="象限判定用哪个 K 的 Recall")
    ap.add_argument("--recall-th", type=float, default=0.5)
    ap.add_argument("--judge-metric", default="faithfulness")
    ap.add_argument("--judge-th", type=float, default=0.7)
    ap.add_argument("--show", default="MRR,Recall@5,NDCG@5,faithfulness", help="表格列，逗号分隔")
    ap.add_argument("--worst", type=int, default=5, help="列出象限『双不达标』最差的 N 条")
    ap.add_argument("--out", default=None, help="合并结果 jsonl 输出")
    a = ap.parse_args()

    evalset = {r["query_id"]: r for r in load_jsonl(a.evalset)}
    ir = {r["query_id"]: r for r in load_jsonl(a.ir_perq)}
    sc = {r["query_id"]: {k: v for k, v in r.items() if k != "query_id"}
          for r in load_jsonl(a.scores)} if a.scores else {}
    if not evalset or not ir:
        sys.exit("evalset 或 ir-perq 为空")

    rows = []
    for qid in sorted(set(evalset) & set(ir)):
        merged = {"query_id": qid, **{k: v for k, v in ir[qid].items() if k != "query_id"},
                  **sc.get(qid, {})}
        rows.append(merged)

    cols = [c.strip() for c in a.show.split(",") if c.strip()]
    print(f"| {'query_id'} | " + " | ".join(cols) + " | 象限 |")
    print("|" + "---|" * (len(cols) + 2))
    quad = {"ok": 0, "gen_bad": 0, "ret_bad": 0, "both_bad": 0, "no_judge": 0}
    bad_rows = []
    for r in rows:
        rec = r.get(f"Recall@{a.recall_k}")
        judge = r.get(a.judge_metric)
        if rec is None:
            label = "-"
        elif judge is None:
            label = "检索" + ("✓" if rec >= a.recall_th else "✗") + "/无裁判分"
            quad["no_judge"] += 1
        else:
            ret_ok, gen_ok = rec >= a.recall_th, judge >= a.judge_th
            label = ("双达标" if ret_ok and gen_ok else
                     "生成问题" if ret_ok else "检索问题" if gen_ok else "双不达标")
            quad["ok" if ret_ok and gen_ok else "gen_bad" if ret_ok else "ret_bad" if gen_ok else "both_bad"] += 1
            if not (ret_ok and gen_ok):
                bad_rows.append((rec + (judge if judge else 0), r["query_id"], label,
                                 (r.get("query") or evalset[r["query_id"]]["query"])[:60]))
        vals = " | ".join(f"{r[c]:.3f}" if isinstance(r.get(c), float) else (str(r.get(c, "-"))[:40])
                          for c in cols)
        print(f"| {r['query_id']} | {vals} | {label} |")

    judged = len(rows) - quad["no_judge"]
    print(f"\n象限统计（检索=Recall@{a.recall_k}≥{a.recall_th}，生成={a.judge_metric}≥{a.judge_th}，"
          f"可判定 {judged}/{len(rows)}）：")
    print(f"  双达标 {quad['ok']} | 生成问题 {quad['gen_bad']} | 检索问题 {quad['ret_bad']} | "
          f"双不达标 {quad['both_bad']} | 无裁判分 {quad['no_judge']}")
    if bad_rows and a.worst:
        print(f"\n最差 {min(a.worst, len(bad_rows))} 条（按两分之和升序）：")
        for s, qid, label, q in sorted(bad_rows)[:a.worst]:
            print(f"  {qid} [{label}] {s:.2f}  {q}")
    if a.out:
        Path(a.out).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        print(f"\n-> {a.out}")


if __name__ == "__main__":
    main()
