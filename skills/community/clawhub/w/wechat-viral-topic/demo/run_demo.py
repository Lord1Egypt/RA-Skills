#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wechat-viral-topic 一键自证：python demo/run_demo.py

四步，全部真实执行：
  1. 从素材抽信号并生成选题卡
  2. 合规扫描：故意埋了 4 类红线的草稿必须被 BLOCK
  3. 干净草稿必须 PASS（证明不是见谁都拦）
  4. 标题体检：长标题+红线 FAIL，短标题 PASS
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import topicguard  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CLEAN = "这套方法帮编辑把选题会从 3 小时压到 40 分钟，附 12 个已发案例的阅读数据。"


def main():
    print("=== 1) 素材信号 ===")
    d = topicguard.scan(topicguard.read_text(os.path.join(HERE, "hot_topic_sample.md")))
    print("人群 :", "、".join(d["audience"]) or "未指向")
    print("数字 :", "、".join(d["figures"][:5]))
    print("时间 :", "、".join(d["dates"]))
    print("话题 :", "、".join(d["topics"]))
    print("冲突 :", (d["conflicts"][0][:40] if d["conflicts"] else "无"))
    ok1 = bool(d["figures"]) and bool(d["dates"]) and bool(d["topics"]) and bool(d["conflicts"])
    print("结论 : %s" % ("PASS 五类信号齐备，可进选题会" if ok1 else "FAIL 信号不足"))

    print("\n=== 2) 埋红线草稿 ===")
    bad = topicguard.riskcheck(topicguard.read_text(os.path.join(HERE, "risky_draft.md")))
    rules = sorted({h["rule"] for h in bad["red"]})
    print("判定 :", bad["verdict"], "| RED", len(bad["red"]), "| YELLOW", len(bad["yellow"]))
    print("命中 :", "、".join(rules))
    ok2 = bad["verdict"] == "BLOCK" and {"医疗声明", "绝对化用语", "收益承诺", "诱导分享"} <= set(rules)
    print("结论 : %s" % ("PASS 四类红线全部拦下" if ok2 else "FAIL 漏拦"))

    print("\n=== 3) 干净草稿（正控）===")
    good = topicguard.riskcheck(CLEAN)
    print("判定 :", good["verdict"], "| RED", len(good["red"]), "| YELLOW", len(good["yellow"]))
    ok3 = good["verdict"] == "PASS"
    print("结论 : %s" % ("PASS 不误杀" if ok3 else "FAIL 误杀：%s" % [h["word"] for h in good["red"]]))

    print("\n=== 4) 标题体检 ===")
    long_title = "所有人都不知道这是唯一能彻底解决公众号选题焦虑并且保证阅读量翻倍的完整方法论合集第二版"
    t1 = topicguard.titlecheck(long_title)
    t2 = topicguard.titlecheck("3 个信号，说明 AI 诊断要变天")
    print("长标题 : %s | %d 字 | %s" % (t1["verdict"], t1["length"], "；".join(t1["problems"])))
    print("短标题 : %s | %d 字 | 公式 %s" % (t2["verdict"], t2["length"], "、".join(t2["formulas"])))
    ok4 = t1["verdict"] == "FAIL" and t2["verdict"] == "PASS"

    all_ok = ok1 and ok2 and ok3 and ok4
    print("\n=== 汇总：%s ===" % ("全 PASS" if all_ok else "存在 FAIL"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
