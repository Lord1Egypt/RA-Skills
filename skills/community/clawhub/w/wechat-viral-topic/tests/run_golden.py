#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wechat-viral-topic 黄金集跑分器：python tests/run_golden.py [--id W01]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import topicguard  # noqa: E402


def any_in(items, needles):
    return any(n in items for n in needles)


def check_scan(case):
    try:
        d = topicguard.scan(case["input"])
    except SystemExit:
        if case["expect"].get("expect_error") == "W004":
            return "PASS: 正确拒答为 W004"
        return "FAIL: 意外拒答"
    e = case["expect"]
    if "figures_contain_any" in e and not any_in(d["figures"], e["figures_contain_any"]):
        return "FAIL: 数字未命中（得到 %s）" % d["figures"]
    if "dates_contain_any" in e and not any_in(d["dates"], e["dates_contain_any"]):
        return "FAIL: 时间未命中（得到 %s）" % d["dates"]
    if "topics_contain_any" in e and not any_in(d["topics"], e["topics_contain_any"]):
        return "FAIL: 话题词未命中（得到 %s）" % d["topics"]
    if e.get("conflicts_min") and len(d["conflicts"]) < e["conflicts_min"]:
        return "FAIL: 冲突句 %d < %d" % (len(d["conflicts"]), e["conflicts_min"])
    if e.get("audience_nonempty") and not d["audience"]:
        return "FAIL: 未识别人群"
    return "PASS"


def check_risk(case):
    d = topicguard.riskcheck(case["input"])
    e = case["expect"]
    if d["verdict"] != e["verdict"]:
        return "FAIL: verdict=%s 期望 %s" % (d["verdict"], e["verdict"])
    groups = {"red_rules_contain": d["red"], "yellow_rules_contain": d["yellow"]}
    for key, hits in groups.items():
        for r in e.get(key, []):
            if r not in {h["rule"] for h in hits}:
                return "FAIL: 未命中规则 %s（得到 %s）" % (r, sorted({h["rule"] for h in hits}))
    return "PASS"


def check_title(case):
    d = topicguard.titlecheck(case["input"])
    e = case["expect"]
    if d["verdict"] != e["verdict"]:
        return "FAIL: verdict=%s 期望 %s（问题 %s）" % (d["verdict"], e["verdict"], d["problems"])
    if e.get("problems_min") and len(d["problems"]) < e["problems_min"]:
        return "FAIL: 问题数 %d < %d" % (len(d["problems"]), e["problems_min"])
    if "problems_contain_any" in e:
        blob = " ".join(d["problems"])
        if not any(k in blob for k in e["problems_contain_any"]):
            return "FAIL: 问题描述未含预期关键词（得到 %s）" % d["problems"]
    if "formulas_contain_any" in e and not any_in(d["formulas"], e["formulas_contain_any"]):
        return "FAIL: 公式未命中（得到 %s）" % d["formulas"]
    return "PASS"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    only = sys.argv[sys.argv.index("--id") + 1] if "--id" in sys.argv else None
    cases = json.load(open(os.path.join(HERE, "golden.json"), encoding="utf-8"))["cases"]
    fnmap = {"scan": check_scan, "riskcheck": check_risk, "titlecheck": check_title}
    npass = 0
    total = 0
    for c in cases:
        if only and c["id"] != only:
            continue
        total += 1
        r = fnmap[c["kind"]](c)
        npass += r.startswith("PASS")
        print("%-26s %s" % (c["id"], r))
    print("--- %d/%d PASS" % (npass, total))
    sys.exit(0 if npass == total else 1)


if __name__ == "__main__":
    main()
