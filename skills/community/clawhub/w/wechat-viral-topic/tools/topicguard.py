#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wechat-viral-topic 本地工具链（零依赖、纯标准库、不联网）。

三件事，只做机械活，选题判断仍归人：
  1. scan        从素材里抽「可证信号」：数字、时间、平台、话题词、冲突句、痛点句，并给出
                 选题卡骨架（人群/冲突/信息差/可证数据/时效窗口）。没有信号就拒答（W004）。
  2. riskcheck   扫合规红线：医疗声明、绝对化用语、收益承诺、诱导分享（RED，必须删）与
                 无出处断言（YELLOW，需补出处）。
  3. titlecheck  判标题：长度、公式类型（数字/疑问/对比/痛点/结果）、是否踩红线。

脚本许可：MIT（与 SKILL.md 的理论文本许可相互独立）。

错误码：W001 文件不存在 · W002 编码不可读 · W003 内容为空 · W004 无有效信号

用法：
  python tools/topicguard.py scan --file demo/hot_topic_sample.md
  python tools/topicguard.py riskcheck --file demo/risky_draft.md
  python tools/topicguard.py titlecheck --title "为什么你的选题总是没流量"
"""
import argparse
import json
import os
import re
import sys

NUM = re.compile(r"(\d+(?:\.\d+)?)\s*(万|亿|%|％|倍|天|年|个月|人|次|条|元)")
DATE = re.compile(r"(\d{4}-\d{2}-\d{2}|\d{4}年|\d{1,2}月\d{1,2}日|近日|本周|上周|昨天|本月)")
PLATFORM = re.compile(r"(公众号|视频号|抖音|小红书|哔哩哔哩|B站|知乎|微博|快手)")
TOPIC = re.compile(r"[#＃]([^#＃\n]{2,20})[#＃]")
QUOTE = re.compile(r"「([^」\n]{2,40})」")
CONFLICT = re.compile(r"(但却|但|却|反而|然而|争议|翻车|打脸|冲突|对立|抵制|反转|被骂|举报)")
PAIN = re.compile(r"(焦虑|困惑|踩坑|被坑|找不到|不会用|太难|太贵|被拒|吃亏|后悔|白花钱|干着急)")
AUDIENCE = re.compile(r"(用户|患者|医生|编辑|老板|家长|护士|销售|创业者|新人|同行|甲方|乙方)")

RISK_RULES = [
    ("医疗声明", "RED", re.compile(r"(治愈|根治|药到病除|替代[^\n]{0,6}药物|包治|无副作用|100%有效|百分之百有效)")),
    ("绝对化用语", "RED", re.compile(r"(最好|最佳|最强|最优|唯一|独家|顶级|极致|绝对|百分百|史无前例|前所未有|国家级|世界级)")),
    ("收益承诺", "RED", re.compile(r"(月入|日赚|年入百万|稳赚|躺赚|暴富|保证收益|稳赚不赔|零风险|包赚)")),
    ("诱导分享", "RED", re.compile(r"(转发抽奖|不转不是|集赞|裂变|分享到[^\n]{0,6}群|转发到朋友圈)")),
    ("无出处断言", "YELLOW", re.compile(r"(据研究|专家表示|数据显示|研究表明|有数据显示|权威人士|内部消息)")),
]

TITLE_FORMULAS = [
    ("数字型", re.compile(r"\d")),
    ("疑问型", re.compile(r"[?？]|为什么|怎么|吗|凭什么")),
    ("对比型", re.compile(r"(vs|VS|对比|还是|选哪个|区别|哪个更)")),
    ("痛点型", re.compile(r"(踩坑|避坑|别再|千万别|后悔|踩雷|血亏)")),
    ("结果型", re.compile(r"(搞定|拿下|省了|省下|多赚|提速|翻倍)")),
]

LEN_WARN = 34       # 微信标题超此长度在列表页会被截断
LEN_TIGHT = 34


def say(msg):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(msg)


def die(code, msg):
    say("[%s] %s" % (code, msg))
    sys.exit(1)


def read_text(path):
    if not os.path.isfile(path):
        die("W001", "文件不存在：%s" % path)
    raw = open(path, "rb").read()
    text = None
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        die("W002", "编码不可读")
    if not text.strip():
        die("W003", "内容为空")
    return text


def scan(text):
    nums = NUM.findall(text)
    dates = sorted(set(DATE.findall(text)))
    platforms = sorted(set(PLATFORM.findall(text)))
    topics = [t for t in TOPIC.findall(text) if t]
    quotes = QUOTE.findall(text)[:6]
    conflicts = [l.strip() for l in text.splitlines() if CONFLICT.search(l)][:5]
    pains = [l.strip() for l in text.splitlines() if PAIN.search(l)][:5]
    audiences = sorted(set(AUDIENCE.findall(text)))
    figures = ["%s%s" % (v, u) for v, u in nums]
    if not (figures or topics or conflicts or pains):
        die("W004", "无有效信号：既没有可证数字，也没有冲突句/痛点句/话题词，不适合做选题")
    angles = []
    if conflicts and figures:
        angles.append("用「%s」的冲突，配「%s」这种硬数字做开头" % (conflicts[0][:28], figures[0]))
    if pains:
        angles.append("从痛点切入：把「%s」写成读者第一句能对号入座的话" % pains[0][:28])
    if dates:
        angles.append("时效锚点「%s」：在窗口内发，过期就换角度" % dates[0])
    return {
        "audience": audiences,
        "platforms": platforms,
        "topics": topics[:6],
        "quotes": quotes,
        "figures": figures[:8],
        "dates": dates[:5],
        "conflicts": conflicts,
        "pains": pains,
        "angles": angles[:3],
    }


def build_card(d):
    return """# 选题卡（信号自动抽取，判断由人做）

| 字段 | 值 |
|---|---|
| 目标人群 | %s |
| 适配平台 | %s |
| 话题词 | %s |
| 读者原话 | %s |
| 可证数字 | %s |
| 时效窗口 | %s |
| 冲突点 | %s |
| 痛点句 | %s |

## 可写角度（占位，不是成稿）
%s
""" % (
        "、".join(d["audience"]) or "原文未指向具体人群（需补）",
        "、".join(d["platforms"]) or "未提平台",
        "、".join(d["topics"]) or "无",
        " / ".join(d["quotes"]) or "无",
        "、".join(d["figures"]) or "无（缺硬数字，爆款概率下降）",
        "、".join(d["dates"]) or "无时效锚点",
        " / ".join(c[:40] for c in d["conflicts"]) or "无冲突（平叙难爆）",
        " / ".join(p[:40] for p in d["pains"]) or "无痛点句",
        "\n".join("- " + a for a in d["angles"]) or "- 信号不足，先补数字与冲突再写",
    )


def riskcheck(text):
    hits = []
    for name, level, pat in RISK_RULES:
        for m in pat.finditer(text):
            ctx = text[max(0, m.start() - 12):m.end() + 12].replace("\n", " ")
            hits.append({"rule": name, "level": level, "word": m.group(0), "context": ctx})
    red = [h for h in hits if h["level"] == "RED"]
    yellow = [h for h in hits if h["level"] == "YELLOW"]
    return {"verdict": "BLOCK" if red else ("WARN" if yellow else "PASS"),
            "red": red, "yellow": yellow}


def titlecheck(title):
    length = len(title)
    formulas = [n for n, p in TITLE_FORMULAS if p.search(title)]
    risk = riskcheck(title)
    problems = []
    if length > LEN_TIGHT:
        problems.append("长度 %d 字，超过 %d 字在列表页会被截断" % (length, LEN_TIGHT))
    if not formulas:
        problems.append("没有可识别的标题公式（数字/疑问/对比/痛点/结果），点击动机弱")
    if risk["red"]:
        problems.append("踩合规红线：%s" % "、".join(sorted({h["rule"] for h in risk["red"]})))
    return {"length": length, "formulas": formulas, "problems": problems,
            "verdict": "FAIL" if problems else "PASS"}


def main():
    ap = argparse.ArgumentParser(description="wechat-viral-topic 工具链（零依赖）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="素材信号扫描 + 选题卡")
    s.add_argument("--file", required=True)
    s.add_argument("--out", default=".")
    s.add_argument("--json", action="store_true")

    r = sub.add_parser("riskcheck", help="合规红线扫描")
    r.add_argument("--file", required=True)
    r.add_argument("--json", action="store_true")

    t = sub.add_parser("titlecheck", help="标题体检")
    t.add_argument("--title", required=True)
    t.add_argument("--json", action="store_true")

    a = ap.parse_args()
    as_json = getattr(a, "json", False)

    if a.cmd == "scan":
        d = scan(read_text(a.file))
        card = build_card(d)
        try:
            os.makedirs(a.out, exist_ok=True)
            stem = os.path.splitext(os.path.basename(a.file))[0]
            md = os.path.join(a.out, stem + ".topic.md")
            js = os.path.join(a.out, stem + ".signals.json")
            open(md, "w", encoding="utf-8").write(card)
            open(js, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
        except OSError as ex:
            die("W001", "输出目录不可写：%s" % ex)
        if as_json:
            say(json.dumps({"ok": True, "data": {"out_md": md, "signals": d}}, ensure_ascii=False))
        else:
            say(card)
            say("选题卡已写入：%s" % md)
        sys.exit(0)

    if a.cmd == "riskcheck":
        d = riskcheck(read_text(a.file))
        if as_json:
            say(json.dumps({"ok": True, "data": d}, ensure_ascii=False))
        else:
            say("合规判定：%s（RED %d 处 / YELLOW %d 处）" % (d["verdict"], len(d["red"]), len(d["yellow"])))
            for h in d["red"] + d["yellow"]:
                say("  [%s] %s ← 「%s」 … %s" % (h["level"], h["rule"], h["word"], h["context"]))
        sys.exit(0 if d["verdict"] != "BLOCK" else 1)

    d = titlecheck(a.title)
    if as_json:
        say(json.dumps({"ok": True, "data": d}, ensure_ascii=False))
    else:
        say("标题判定：%s｜%d 字｜识别公式：%s" % (d["verdict"], d["length"], "、".join(d["formulas"]) or "无"))
        for p in d["problems"]:
            say("  ✗ %s" % p)
    sys.exit(0 if d["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
