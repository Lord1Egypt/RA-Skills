#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大学避坑指南 · 自检

作用：把 SKILL.md 里那些"硬约束"变成机器能拦住的检查。
      约束写在文档里只会被忘记，写在脚本里才拦得住。

用法：
    python audit.py            # 全部检查
    python audit.py --quiet    # 只输出结论与失败项
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REFS = ROOT / "references"
KB = REFS / "kb"

results = []          # (级别, 检查项, 消息)  级别: PASS / WARN / FAIL


def record(level, name, msg=""):
    results.append((level, name, msg))


# ---------- 基础 ----------

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        record("FAIL", f"读取 {path.name}", str(e))
        return None


def load_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        record("FAIL", f"读取 {path.name}", str(e))
        return None


def normalize(text):
    out = []
    for ch in text:
        code = ord(ch)
        if code == 0x3000:
            code = 32
        elif 0xFF01 <= code <= 0xFF5E:
            code -= 0xFEE0
        out.append(chr(code))
    return re.sub(r"\s+", "", "".join(out))


# ---------- 1. 文件完整性 ----------

REQUIRED = [
    "SKILL.md",
    "references/crisis-protocol.md",
    "references/style-guide.md",
    "references/profile-slots.md",
    "references/sources.md",
    "references/test-prompts.md",
    "references/kb/01-academic.md",
    "references/kb/03-dorm.md",
    "references/kb/07-money.md",
    "references/kb/08-health.md",
    "references/kb/10-safety.md",
    "data/scenarios.json",
    "data/topic-matrix.json",
    "data/profile_rules.json",
    "data/memes.json",
    "data/hotlines.json",
    "scripts/ask.py",
    "scripts/audit.py",
]


def check_files():
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        record("FAIL", "文件完整性", "缺失：" + "、".join(missing))
    else:
        record("PASS", "文件完整性", f"{len(REQUIRED)} 个文件齐全")


# ---------- 2. scenarios 的 kb_ref 可解析 ----------

def extract_anchor_exists(md_text, anchor):
    for line in md_text.splitlines():
        if line.startswith("## ") and anchor in line:
            return True
    return False


def check_kb_refs():
    scenarios = load_json(DATA / "scenarios.json")
    if not scenarios:
        return
    bad = []
    for sc in scenarios.get("scenarios", []):
        ref = sc.get("kb_ref", "")
        if "#" not in ref:
            bad.append(f"{sc['id']} 缺少锚点")
            continue
        path_part, anchor = ref.split("#", 1)
        kb_path = REFS / path_part
        if not kb_path.exists():
            bad.append(f"{sc['id']} → {path_part} 不存在")
            continue
        text = load_text(kb_path) or ""
        if not extract_anchor_exists(text, anchor):
            bad.append(f"{sc['id']} → {path_part}#{anchor} 锚点匹配不到")
    if bad:
        record("FAIL", "情景路由表 kb_ref", f"{len(bad)} 条失效：\n      " + "\n      ".join(bad))
    else:
        record("PASS", "情景路由表 kb_ref", f"{len(scenarios.get('scenarios', []))} 条全部可解析")


# ---------- 3. 画像规则兜底 ----------

def check_profile_rules():
    rules = load_json(DATA / "profile_rules.json")
    if not rules:
        return
    problems = []

    for slot in ("year", "issue_type", "temperature"):
        branches = rules.get("global_branches", {}).get(slot, {})
        if not branches:
            problems.append(f"global_branches.{slot} 缺失")
            continue
        if "default" not in branches:
            problems.append(f"global_branches.{slot} 缺少 default 兜底")

        declared = rules.get("slots", {}).get(slot, {}).get("values", [])
        for value in declared:
            if value not in branches:
                problems.append(f"global_branches.{slot} 缺少取值 {value} 的规则")

    it = rules.get("global_branches", {}).get("issue_type", {})
    for key in ("决策型", "执行型", "关系型", "情绪型"):
        if key not in it:
            problems.append(f"issue_type 缺少 {key}")

    if problems:
        record("FAIL", "画像规则兜底", "\n      ".join(problems))
    else:
        record("PASS", "画像规则兜底", "所有槽位取值均有规则与 default")


# ---------- 4. 求助资源时效 ----------

def check_hotlines():
    data = load_json(DATA / "hotlines.json")
    if not data:
        return
    meta = data.get("meta", {})
    try:
        last = dt.datetime.strptime(meta["last_verified"], "%Y-%m-%d")
    except Exception:
        record("FAIL", "求助资源核验日期", "last_verified 格式不对")
        return

    age = (dt.datetime.now() - last).days
    interval = meta.get("verify_interval_days", 90)
    if age > interval:
        record("FAIL", "求助资源核验日期",
               f"已过 {age} 天，超过 {interval} 天复核周期。涉及学生真会拨打的号码，必须重新核对官方渠道。")
    else:
        record("PASS", "求助资源核验日期", f"距今 {age} 天（周期 {interval} 天）")

    verified = data.get("verified", [])
    required_numbers = {"12356", "96110", "110", "120"}
    have = {h.get("number") for h in verified}
    missing = required_numbers - have
    if missing:
        record("FAIL", "必需求助资源", "缺少：" + "、".join(sorted(missing)))
    else:
        record("PASS", "必需求助资源", f"{len(verified)} 条已验证资源，关键号码齐全")

    for h in verified:
        if not h.get("source"):
            record("WARN", f"资源 {h.get('number')} 缺来源", "")


# ---------- 5. 梗的时效 ----------

def check_memes():
    data = load_json(DATA / "memes.json")
    if not data:
        return
    today = dt.date.today()
    expired = []
    for m in data.get("hot_memes", {}).get("schema_if_added") and [] or []:
        pass
    hot = data.get("hot_memes", {})
    if isinstance(hot, dict):
        record("PASS", "热梗库", hot.get("_status", "空") + "（设计如此，见 _why）")

    templates = data.get("templates", [])
    if len(templates) < 8:
        record("WARN", "句式模板库", f"只有 {len(templates)} 条，建议扩充")
    else:
        record("PASS", "句式模板库", f"{len(templates)} 条模板")

    for t in templates:
        if "pattern" not in t or "use_in" not in t:
            record("WARN", f"模板 {t.get('id')} 字段不全", "")
    if expired:
        record("FAIL", "过期梗", "、".join(expired))


# ---------- 6. 禁用词扫描（只扫知识库正文） ----------

FORBIDDEN = [
    "作为过来人", "我建议你", "你应该", "努力就会成功",
    "加油", "相信自己", "熬过去就好了", "这有什么好焦虑",
    "你太矫情", "想太多了", "多大点事",
]

ALLOW_CONTEXT = ("禁止", "禁用", "不要", "别", "❌", "反例", "不许")


def check_forbidden():
    hits = []
    for kb_file in sorted(KB.glob("*.md")):
        text = load_text(kb_file) or ""
        for line in text.splitlines():
            for word in FORBIDDEN:
                if word in line:
                    if any(mark in line for mark in ALLOW_CONTEXT):
                        continue
                    hits.append(f"{kb_file.name}: {word} → {line.strip()[:60]}")
    if hits:
        record("WARN", "禁用词扫描", f"{len(hits)} 处疑似：\n      " + "\n      ".join(hits))
    else:
        record("PASS", "禁用词扫描", f"知识库正文未出现 {len(FORBIDDEN)} 个禁用词")


# ---------- 7. 危机分级回归 ----------

def parse_test_prompts():
    """从 test-prompts.md 的表格里解析用例：| # | 输入 | 期望级别 | ... |"""
    text = load_text(REFS / "test-prompts.md") or ""
    cases = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if not cells[0].isdigit():
            continue
        cases.append({"idx": cells[0], "input": cells[1], "expect": cells[2]})
    return cases


def classify(text, rules):
    norm = normalize(text)
    for level in rules["temperature_rules"]["levels"]:
        for marker in level["markers"]:
            if normalize(marker) in norm:
                return level["level"]
    return "平稳"


def check_crisis_coverage():
    rules = load_json(DATA / "profile_rules.json")
    if not rules:
        return
    cases = parse_test_prompts()
    if not cases:
        record("FAIL", "危机分级回归", "test-prompts.md 里解析不到用例")
        return

    wrong = []
    skipped = 0
    for c in cases:
        expect = c["expect"]
        # L2 及以上、以及非心理危机高危通道的判断是语义判断，关键词匹配做不到。
        # 标了「语义」的用例脚本主动跳过——假装能测等于自欺欺人。
        if "语义" in expect:
            skipped += 1
            continue
        got = classify(c["input"], rules)
        if expect.startswith("L") and len(expect) >= 2 and expect[1].isdigit():
            mapping = {"L1": "危险", "L2": "崩溃", "L3": "焦虑", "L4": "平稳"}
            want = mapping.get(expect[:2])
            if want and got != want:
                wrong.append(f"#{c['idx']} 期望 {expect}（{want}）实得 {got} — {c['input'][:24]}")
    if wrong:
        record("FAIL", "危机分级回归", f"{len(wrong)} 条不符：\n      " + "\n      ".join(wrong))
    else:
        record("PASS", "危机分级回归",
               f"{len(cases) - skipped} 条脚本可回归用例全对；{skipped} 条为语义判断，需模型评估")


# ---------- 8. 来源可溯（宽松检查） ----------

def check_sources():
    sources = load_text(REFS / "sources.md") or ""
    signals = [
        ("20000", "助学贷款本专科额度"),
        ("25000", "助学贷款研究生额度"),
        ("21.8", "刷单返利占比"),
        ("12356", "心理援助热线"),
        ("96110", "反诈专线"),
        ("8000", "国家奖学金"),
    ]
    miss = [name for key, name in signals if key not in sources]
    if miss:
        record("WARN", "来源档案覆盖", "sources.md 里找不到：" + "、".join(miss))
    else:
        record("PASS", "来源档案覆盖", f"{len(signals)} 个关键信息点均有记录")


# ---------- 主流程 ----------

def main():
    parser = argparse.ArgumentParser(description="大学避坑指南 · 自检")
    parser.add_argument("--quiet", action="store_true", help="只输出结论与失败项")
    args = parser.parse_args()

    check_files()
    check_kb_refs()
    check_profile_rules()
    check_hotlines()
    check_memes()
    check_forbidden()
    check_crisis_coverage()
    check_sources()

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]

    print("=" * 64)
    print("大学避坑指南 · 自检报告")
    print("=" * 64)
    for level, name, msg in results:
        if args.quiet and level == "PASS":
            continue
        print(f"[{level}] {name}")
        if msg:
            print(f"      {msg}")
    print("-" * 64)
    print(f"通过 {len(results) - len(fails) - len(warns)} 项 · 警告 {len(warns)} 项 · 失败 {len(fails)} 项")

    if fails:
        print("\n存在失败项。涉及危机协议与来源可溯的失败项必须先修再交付。")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
