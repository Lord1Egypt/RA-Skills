#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大学避坑指南 · 运行时

作用：把学生的一句话变成一张「作业单」——分级结果、命中的情景、推断出的槽位、
      该用哪个文风档位、去知识库哪一节取内容。
      本脚本不生成回复文本，生成回复是模型的事。脚本负责的是可复现的判断部分。

用法：
    python ask.py "室友半夜打游戏太吵了"
    python ask.py --json "我挂了三科"           # 输出 JSON，便于程序消费
"""

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REFS = ROOT / "references"


# ---------- 加载 ----------

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        die(f"找不到文件：{path}")
    except json.JSONDecodeError as e:
        die(f"JSON 解析失败：{path}\n  {e}")


def load_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        die(f"找不到文件：{path}")


def die(msg):
    print(f"[错误] {msg}", file=sys.stderr)
    sys.exit(1)


def normalize(text):
    """全角转半角、去多余空白，保证匹配稳定"""
    out = []
    for ch in text:
        code = ord(ch)
        if code == 0x3000:
            code = 32
        elif 0xFF01 <= code <= 0xFF5E:
            code -= 0xFEE0
        out.append(chr(code))
    return re.sub(r"\s+", "", "".join(out))


# ---------- ① 危机分级 ----------

def classify_temperature(text, rules):
    norm = normalize(text)
    for level in rules["temperature_rules"]["levels"]:
        for marker in level["markers"]:
            if normalize(marker) in norm:
                return level["level"], level["action"], marker
    return "平稳", "normal_mode", None


# ---------- ② 情景路由 ----------

def route_scenarios(text, scenarios):
    norm = normalize(text)
    hits = []
    for sc in scenarios:
        matched = [t for t in sc.get("triggers", []) if normalize(t) in norm]
        if matched:
            hits.append((sc, matched))
    # 命中触发词越多越靠前；同分按 priority 无关，保持稳定排序
    hits.sort(key=lambda item: -len(item[1]))
    return hits


# ---------- ③ 槽位推断 ----------

def infer_slots(text, rules):
    norm = normalize(text)
    slots = {}

    for key, rule in rules["issue_type_rules"].items():
        if key == "note":
            continue
        if any(normalize(m) in norm for m in rule.get("markers", [])):
            slots["issue_type"] = rule["type"]
            break

    # 情绪型优先：命中情绪标记时覆盖
    emo = rules["issue_type_rules"].get("emotional", {})
    if any(normalize(m) in norm for m in emo.get("markers", [])):
        slots["issue_type"] = "情绪型"

    years = [("大一", ["大一", "刚入学", "新生", "刚来"]),
             ("大二", ["大二"]),
             ("大三", ["大三"]),
             ("大四", ["大四", "要毕业", "毕业了"]),
             ("研究生", ["研究生", "读研", "硕士", "博士"])]
    for value, markers in years:
        if any(m in norm for m in markers):
            slots["year"] = value
            break

    tried_markers = rules["tried_extraction"]["markers"]
    if any(normalize(m) in norm for m in tried_markers):
        slots["tried_is_likely"] = True

    return slots


# ---------- ④ 知识片段定位 ----------

def extract_section(md_text, anchor):
    """按 '## 标题' 抽取小节；anchor 做模糊包含匹配"""
    lines = md_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and anchor in line:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def resolve_kb(kb_ref):
    """kb_ref 形如 'kb/03-dorm.md#作息冲突'"""
    if "#" in kb_ref:
        path_part, anchor = kb_ref.split("#", 1)
    else:
        path_part, anchor = kb_ref, ""
    path = REFS / path_part
    text = load_text(path)
    if not anchor:
        return text
    section = extract_section(text, anchor)
    return section if section else text


# ---------- 主流程 ----------

def build_worklist(text):
    rules = load_json(DATA / "profile_rules.json")
    scenarios = load_json(DATA / "scenarios.json")["scenarios"]
    hotlines = load_json(DATA / "hotlines.json")

    level, action, marker = classify_temperature(text, rules)
    hits = route_scenarios(text, scenarios)
    slots = infer_slots(text, rules)
    slots["temperature"] = level

    mode = rules["global_branches"]["temperature"].get(level, {})
    issue_type = slots.get("issue_type", "执行型")
    issue_rule = rules["global_branches"]["issue_type"].get(
        issue_type, rules["global_branches"]["issue_type"]["default"])

    result = {
        "输入": text,
        "危机分级": {"级别": level, "动作": action, "命中词": marker},
        "情景命中": [
            {"id": sc["id"], "title": sc["title"], "kb_ref": sc["kb_ref"],
             "命中触发词": matched}
            for sc, matched in hits[:3]
        ],
        "槽位": slots,
        "文风档位": {
            "模式": mode.get("mode", "松弛模式"),
            "梗位预算": mode.get("meme_budget", 2),
            "emoji 上限": mode.get("emoji_budget", 2),
        },
        "回应结构": {
            "侧重": issue_rule.get("emphasis", []),
            "压缩": issue_rule.get("compress", []),
        },
    }

    if level == "危险" or action == "HARD_STOP_CRISIS_PROTOCOL":
        result["⚠️ 硬停"] = "命中危机信号。必须加载 references/crisis-protocol.md，关闭全部幽默与 emoji。"
        result["回应结构"] = {
            "模式": "crisis-protocol L1 模板（不走五段式）",
            "说明": "按 crisis-protocol.md 第 4 节 L1 模板：承认痛苦 → 不承诺 → 给号码并解释其匿名属性 → 应急通道 → 落到一个具体的人。不评估、不追问方式、不分析、不说'你会没事的'。",
        }
        result["求助资源"] = [
            {k: item[k] for k in ("number", "name", "hours", "anonymous", "what_it_does")}
            for item in hotlines["verified"] if item["number"] in ("12356", "110", "120")
        ]
    elif action == "serious_mode":
        result["⚠️ 严肃模式"] = "加载 references/crisis-protocol.md 的 L2 模板；段落结构与措辞按该文件走。"
        result["回应结构"] = {
            "模式": "crisis-protocol L2 模板（不走五段式）",
            "说明": "不给建议清单。先说明这需要专业帮助而不是建议，再给 12356 与校心理中心路径。禁止出现梗与 emoji。",
        }

    if slots.get("tried_is_likely"):
        result["⚠️ tried"] = "文本中疑似包含已尝试过的动作。回应必须显式承认，且新建议要在其之外。"

    result["知识片段"] = [
        {"来源": sc["kb_ref"], "内容": resolve_kb(sc["kb_ref"])}
        for sc, _ in hits[:2]
    ]
    return result


def render(work):
    out = []
    out.append("=" * 64)
    out.append("大学避坑指南 · 作业单")
    out.append("=" * 64)

    crisis = work["危机分级"]
    out.append(f"\n【① 危机分级】{crisis['级别']}"
               + (f"（命中：{crisis['命中词']}）" if crisis["命中词"] else ""))
    if "⚠️ 硬停" in work:
        out.append(f"   ⚠️  {work['⚠️ 硬停']}")
        out.append("   求助资源：")
        for h in work["求助资源"]:
            anon = "匿名" if h["anonymous"] else "需实名"
            out.append(f"     · {h['number']}  {h['name']}（{h['hours']}，{anon}）")
    elif "⚠️ 严肃模式" in work:
        out.append(f"   {work['⚠️ 严肃模式']}")

    out.append(f"\n【② 情景路由】命中 {len(work['情景命中'])} 条")
    for sc in work["情景命中"]:
        out.append(f"   · {sc['title']}")
        out.append(f"     知识库：{sc['kb_ref']}")
        out.append(f"     触发词：{'、'.join(sc['命中触发词'])}")
    if not work["情景命中"]:
        out.append("   （未命中。用最近类别的通用处理，不要拒答）")

    out.append("\n【③ 槽位】")
    for k, v in work["槽位"].items():
        out.append(f"   {k} = {v}")

    style = work["文风档位"]
    out.append(f"\n【④ 文风档位】{style['模式']}")
    out.append(f"   梗位预算 {style['梗位预算']} 处 · emoji 上限 {style['emoji 上限']} 个")

    shape = work["回应结构"]
    if "模式" in shape:
        out.append(f"\n【⑤ 回应结构】{shape['模式']}")
        out.append(f"   {shape['说明']}")
    else:
        out.append(f"\n【⑤ 回应结构】{work['槽位'].get('issue_type', '执行型')}")
        if shape.get("侧重"):
            out.append(f"   侧重：{'、'.join(shape['侧重'])}")
        if shape.get("压缩"):
            out.append(f"   压缩：{'、'.join(shape['压缩'])}")

    if "⚠️ tried" in work:
        out.append(f"\n{work['⚠️ tried']}")

    out.append("\n【⑥ 知识片段】")
    for seg in work["知识片段"]:
        out.append("-" * 64)
        out.append(f"# 来自 {seg['来源']}")
        out.append(seg["内容"])

    out.append("=" * 64)
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="大学避坑指南 · 运行时作业单")
    parser.add_argument("text", nargs="*", help="学生说的话")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    if not args.text:
        parser.print_help()
        sys.exit(3)

    text = " ".join(args.text)
    work = build_worklist(text)

    if args.json:
        print(json.dumps(work, ensure_ascii=False, indent=2))
    else:
        print(render(work))


if __name__ == "__main__":
    main()
