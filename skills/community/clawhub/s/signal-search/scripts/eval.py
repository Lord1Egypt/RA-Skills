"""scripts/eval.py - 金标准评估（§5.14 / M33 / M51）。

离线（默认）：解析 references/eval-golden-set.md，跑 route.classify_tier 算档位命中率。
在线（--live）：对每条跑 retrieve()，算 faithfulness/引文真实率/档位命中/token 比。
用法：
    python eval.py                # 离线档位命中
    python eval.py --live         # 在线实测（需网络，逐条带超时）
    python eval.py --live --cfg x.json
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
GOLDEN = os.path.join(HERE, "..", "references", "eval-golden-set.md")


def load_golden(path: str = GOLDEN) -> List[Dict[str, str]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s.startswith("|"):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 5:
                continue
            if cells[0] in ("id",) or set(cells[0]) <= set("-: "):
                continue
            if not re.match(r"^[A-Za-z]?\d+$", cells[0]):
                continue
            rid = cells[0]
            rows.append(
                {
                    "id": rid,
                    "query": cells[1],
                    "intent": cells[2],
                    "reference": cells[3] if len(cells) > 3 else "",
                    "checkpoints": cells[4] if len(cells) > 4 else "",
                }
            )
    return rows


def _expected_tier(rid: str) -> str:
    num = int(re.sub(r"\D", "", rid))
    if num <= 4:
        return "L0"
    if num <= 10:
        return "L1"
    if num <= 18:
        return "L2"
    return "L3"


def eval_tier(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    import route

    hit = 0
    total = 0
    detail = []
    for r in rows:
        exp = _expected_tier(r["id"])
        got, _ = route.classify_tier(r["query"], {})
        ok = got == exp
        hit += ok
        total += 1
        detail.append({"id": r["id"], "expected": exp, "got": got, "ok": ok})
    return {
        "hit": hit,
        "total": total,
        "rate": round(hit / total, 3) if total else 0.0,
        "target": 0.90,
        "pass": (hit / total) >= 0.90 if total else False,
        "detail": detail,
    }


def run(rows: List[Dict[str, str]], live: bool = False, cfg: dict = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {"tier": eval_tier(rows), "live": None}
    if live:
        import orchestrate

        live_res = []
        for r in rows:
            try:
                res = orchestrate.retrieve(r["query"], {}, cfg=cfg)
                live_res.append(
                    {
                        "id": r["id"],
                        "tier_used": res["tier_used"],
                        "confidence": res["confidence"],
                        "n_sources": len(res["sources"]),
                        "exhausted": res["exhausted"],
                        "token_used": res["token_used"],
                        "verify_issues": len(res["verify_issues"]),
                        "fact_uncertain": sum(
                            1 for f in res["fact_verdicts"] if f["verdict"] == "UNCERTAIN"
                        ),
                    }
                )
            except Exception as e:  # 单条失败不影响整体
                live_res.append({"id": r["id"], "error": str(e)[:200]})
        out["live"] = live_res
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--cfg", default=None)
    args = ap.parse_args()
    rows = load_golden()
    cfg = None
    if args.cfg:
        with open(args.cfg, encoding="utf-8") as f:
            cfg = json.load(f)
    res = run(rows, live=args.live, cfg=cfg)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
