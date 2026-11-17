"""确定性测试：同输入重复 20 次，核心结论必须一致。

AI 文本表达允许不同，但不得改变核心结论
（四柱 / 旺衰 / 格局 / 用忌 / 大运 / 流年 / 规则ID / evidence_chain）。
"""
from __future__ import annotations

import os
import sys
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))

from main import run

DT = datetime.datetime(1990, 12, 7, 20, 0)
SEX = "男"
PLACE = "山西盂县"
THEME = "事业财运"


def _core(res):
    fp = res["four_pillars"]
    pillars = {k: v["label"] for k, v in fp.items()}
    pat = next(r for r in res["evidence_chain"] if r["step"] == "pattern")["output"]
    yj = next(r for r in res["evidence_chain"] if r["step"] == "yongji")["output"]
    dy = next(r for r in res["evidence_chain"] if r["step"] == "dayun")["output"]
    ln = next(r for r in res["evidence_chain"] if r["step"] == "liunian")["output"]
    rule_ids = "|".join(
        f"{r['step']}:" + ",".join(r["rules_used"]) + f"@{r['rule_version']}"
        for r in res["evidence_chain"]
    )
    chain_sig = "|".join(
        f"{r['step']}={r['output']}" for r in res["evidence_chain"]
    )
    return {
        "pillars": pillars,
        "branch": pat["branch"],
        "pattern": pat["pattern"],
        "yong": yj["theory_yong"],
        "ji": yj["theory_ji"],
        "dayun_steps": [s["label"] for s in dy["steps"]],
        "liunian": [it["label"] for it in ln["items"]],
        "rule_ids": rule_ids,
        "chain_sig": chain_sig,
    }


def test_determinism():
    base = _core(run(DT, SEX, PLACE, THEME))
    for i in range(1, 20):
        cur = _core(run(DT, SEX, PLACE, THEME))
        assert cur == base, f"第 {i} 次运行与首次不一致:\n{cur}\nvs\n{base}"
    print("OK: 20 次运行核心结论完全一致")
    print("四柱:", base["pillars"])
    print("格局:", base["pattern"], "| 用神:", base["yong"], "| 忌神:", base["ji"])


if __name__ == "__main__":
    test_determinism()
