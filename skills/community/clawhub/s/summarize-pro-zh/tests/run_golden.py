#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跑黄金集：逐条断言 summarize_pro 的抽取/骨架/溯源/自检结果。

用法（任意目录）：
    python tests/run_golden.py            # 全部用例
    python tests/run_golden.py --id G01   # 只跑一条

退出码：0 全过；1 有失败。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import summarize_pro as sp  # noqa: E402


def load_cases():
    with open(os.path.join(HERE, "golden.json"), encoding="utf-8") as f:
        return json.load(f)["cases"]


def check(case):
    """返回 (ok, [失败原因])"""
    fails = []
    fmt = case.get("format", "minutes")
    exp = case.get("expect", {})

    # G10 专用于溯源校验
    if fmt == "citecheck":
        good = sp.citecheck(case["good_output"], case["source"])
        bad = sp.citecheck(case["bad_output"], case["source"])
        if good["verdict"] != exp.get("good_verdict"):
            fails.append("good 期望 %s，实际 %s" % (exp.get("good_verdict"), good["verdict"]))
        if bad["verdict"] != exp.get("bad_verdict"):
            fails.append("bad 期望 %s，实际 %s" % (exp.get("bad_verdict"), bad["verdict"]))
        if len(bad["missing"]) < exp.get("bad_missing_min", 0):
            fails.append("bad 检出 %d 处不可溯源，少于期望 %d"
                         % (len(bad["missing"]), exp.get("bad_missing_min", 0)))
        return (not fails), fails

    text = case["input"]

    # 期望业务失败（如原文过短）
    if exp.get("expect_error"):
        short = len(text.strip()) < 50
        if exp["expect_error"] == "S006" and not short:
            fails.append("期望 S006（原文过短），但样本长度 %d" % len(text.strip()))
        return (not fails), fails

    facts = sp.extract_facts(text)

    if "dates_min" in exp and len(facts["dates"]) < exp["dates_min"]:
        fails.append("日期抽取 %d 个，期望 ≥%d：%s" % (len(facts["dates"]), exp["dates_min"], facts["dates"]))
    if "todo_min" in exp and len(facts["todo_sentences"]) < exp["todo_min"]:
        fails.append("待办句 %d 条，期望 ≥%d" % (len(facts["todo_sentences"]), exp["todo_min"]))
    if "decision_min" in exp and len(facts["decision_sentences"]) < exp["decision_min"]:
        fails.append("决策句 %d 条，期望 ≥%d" % (len(facts["decision_sentences"]), exp["decision_min"]))
    if "condition_min" in exp and len(facts["condition_sentences"]) < exp["condition_min"]:
        fails.append("条件句 %d 条，期望 ≥%d" % (len(facts["condition_sentences"]), exp["condition_min"]))
    if "owners_contain" in exp:
        have = " ".join(facts["owners_hint"]) + " " + " ".join(facts["speakers"])
        for who in exp["owners_contain"]:
            if who not in have:
                fails.append("未识别到责任人 %s" % who)
    if "numbers_contain" in exp:
        joined = " ".join(facts["numbers"])
        for n in exp["numbers_contain"]:
            if n not in joined:
                fails.append("未抽到数字 %s（实得 %s）" % (n, facts["numbers"]))

    # v2.0.2 起：结论强度 / 承诺强度（语义档位）断言
    ss = facts.get("strength_summary", {})
    if "firm_min" in exp and ss.get("firm_decisions", 0) < exp["firm_min"]:
        fails.append("已定结论 %d 条，期望 ≥%d（实得分布 %s）"
                     % (ss.get("firm_decisions", 0), exp["firm_min"], ss.get("decisions")))
    if "soft_min" in exp and ss.get("soft_decisions", 0) < exp["soft_min"]:
        fails.append("暂定/提案/条件结论 %d 条，期望 ≥%d（实得分布 %s）"
                     % (ss.get("soft_decisions", 0), exp["soft_min"], ss.get("decisions")))
    if "committed_min" in exp and ss.get("committed_owners", 0) < exp["committed_min"]:
        fails.append("明确接活 %d 条，期望 ≥%d（实得分布 %s）"
                     % (ss.get("committed_owners", 0), exp["committed_min"], ss.get("commitments")))
    if "intent_min" in exp:
        got = ss.get("commitments", {}).get("intent_only", 0)
        if got < exp["intent_min"]:
            fails.append("仅表意向 %d 条，期望 ≥%d（实得分布 %s）"
                         % (got, exp["intent_min"], ss.get("commitments")))
    if "todo_max" in exp and len(facts["todo_sentences"]) > exp["todo_max"]:
        fails.append("待办句 %d 条，超过上限 %d（标题行/条件句/已定结论不应计入待办）"
                     % (len(facts["todo_sentences"]), exp["todo_max"]))

    body = sp.build_skeleton(fmt, facts)

    if exp.get("skeleton_has_numbered_lines") and not __import__("re").search(r"^\d+\.\s", body, __import__("re").M):
        fails.append("骨架缺少编号行")
    if "bullets_count_between" in exp:
        import re
        lo, hi = exp["bullets_count_between"]
        n = len(re.findall(r"^\d+\.\s", body, re.M))
        if not (lo <= n <= hi):
            fails.append("要点条数 %d 不在 [%d,%d]" % (n, lo, hi))

    if exp.get("selfcheck") == "PASS":
        sc = sp.selfcheck(body, fmt)
        if sc["verdict"] != "PASS":
            fails.append("结构自检未过：%s" % "; ".join(sc["problems"]))

    return (not fails), fails


def main():
    only = None
    if "--id" in sys.argv:
        only = sys.argv[sys.argv.index("--id") + 1]
    cases = load_cases()
    if only:
        cases = [c for c in cases if c["id"].startswith(only)]
    passed = 0
    for c in cases:
        ok, fails = check(c)
        print(("PASS " if ok else "FAIL ") + c["id"])
        for f in fails:
            print("     - " + f)
        passed += ok
    print("---- %d/%d PASS ----" % (passed, len(cases)))
    sys.exit(0 if passed == len(cases) else 1)


if __name__ == "__main__":
    main()
