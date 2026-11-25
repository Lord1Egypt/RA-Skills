#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键演示：抽取 → 结构自检 → 溯源核对，三步全跑并打印结论。

用法（在技能包根目录）：
    python demo/run_demo.py

它证明两件事：
  1. 工具能从真实转写里抽出可核验的事实线索，并生成合规骨架（自检 PASS）。
  2. 一份「人写对了」的纪要，逐句事实 token 全能在原文找到（溯源 PASS）；
     而把它里面三个数字改错，溯源立刻 FAIL —— 这就是「忠实」的可执行证明。
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import summarize_pro as sp  # noqa: E402

SRC = os.path.join(HERE, "sample_transcript.md")
EXPECTED = os.path.join(HERE, "expected_minutes.md")


def main():
    src = open(SRC, encoding="utf-8").read()
    print("原文：%d 字 / %d 行" % (len(src), len([l for l in src.splitlines() if l.strip()])))

    facts = sp.extract_facts(src)
    print("抽取：日期 %d / 数字 %d / 说话人 %d / 待办句 %d / 决策句 %d / 条件句 %d"
          % (len(facts["dates"]), len(facts["numbers"]), len(facts["speakers"]),
             len(facts["todo_sentences"]), len(facts["decision_sentences"]),
             len(facts["condition_sentences"])))
    print("  日期：%s" % "、".join(facts["dates"][:8]))
    print("  说话人：%s" % "、".join(facts["speakers"][:8]))

    body = sp.build_skeleton("minutes", facts)
    sc = sp.selfcheck(body, "minutes")
    print("结构自检（minutes 骨架）：%s" % sc["verdict"])
    for p in sc["problems"]:
        print("  ✗ %s" % p)

    outdir = tempfile.mkdtemp(prefix="sumpro_demo_")
    md = os.path.join(outdir, "sample_transcript.minutes.md")
    open(md, "w", encoding="utf-8").write(body)
    print("骨架已写入：%s" % md)

    exp_text = open(EXPECTED, encoding="utf-8").read()
    r = sp.citecheck(exp_text, src)
    print("溯源核对（人工理想纪要 → 原文）：%s  （核对 token %d 个，不可溯源 %d 个）"
          % (r["verdict"], r["checked"], len(r["missing"])))
    for m in r["missing"][:10]:
        print("  ✗ %s ← %s" % (m["token"], m["sentence"]))

    tampered = exp_text.replace("1.8%", "1.2%").replace("11 月 25 日", "11 月 23 日")
    r2 = sp.citecheck(tampered, src)
    print("溯源核对（故意改错两个数字）：%s  （检出 %d 处不可溯源）"
          % (r2["verdict"], len(r2["missing"])))
    for m in r2["missing"][:5]:
        print("  ✗ %s ← %s" % (m["token"], m["sentence"]))

    ok = (sc["verdict"] == "PASS" and r["verdict"] == "PASS" and r2["verdict"] == "FAIL")
    print("\n演示结论：%s" % ("通过（忠实性可被机器证明）" if ok else "未通过，见上方明细"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
