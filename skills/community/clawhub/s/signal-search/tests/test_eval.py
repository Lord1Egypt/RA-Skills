import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import eval as eval_mod


def test_golden_parse():
    rows = eval_mod.load_golden()
    assert len(rows) == 24, f"金标准集应 24 条，实际 {len(rows)}"
    assert all(r["id"] and r["query"] for r in rows)


def test_tier_hit_rate():
    rows = eval_mod.load_golden()
    res = eval_mod.eval_tier(rows)
    assert res["total"] == 24
    assert res["rate"] >= 0.90, f"档位命中率 {res['rate']} 低于 0.90 目标"
    assert res["pass"] is True
