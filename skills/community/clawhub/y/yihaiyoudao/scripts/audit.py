# -*- coding: utf-8 -*-
"""
yihaiyoudao 自动化脚本：内容审核一键跑（原创性判定 + 限流风险扫描 + 修改建议）
用法：
  python audit.py 文章.txt            # 审核一个文件
  python audit.py < 文章.txt          # 或从 stdin 读
  python audit.py 文章.txt --json     # 输出 JSON 结构化结果
规则：词库读取 references/risk-lexicon.md（安全替换表 + 高危词库速查），
原创性按 originality.md 的过关/不过关信号做启发式判定。
"""
import argparse
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEXICON_PATH = os.path.join(SCRIPT_DIR, "..", "references", "risk-lexicon.md")

AI_SIGNALS = [
    "总而言之", "综上所述", "值得注意的是", "首先", "其次", "最后",
    "赋能", "闭环", "抓手", "底层逻辑", "颗粒度", "对齐", "拉通",
    "在这个快节奏的时代", "我们需要意识到", "让我们一起", "拥抱变化",
    "深度赋能", "打造", "生态", "复盘一下", "我们需要", "众所周知",
]
PERSONAL_MARKERS = ["我", "亲历", "我记得", "有一次", "上周", "上次", "我朋友",
                    "我妈", "我爸", "我的", "亲眼", "实际", "手把手"]
DANGER_GENERIC = {
    "政治类": ["阶级", "资本家", "底层人群", "剥削", "奴隶制", "政府反应慢", "法律是笑话"],
    "医学类": ["PTSD", "抑郁", "精神病", "人格障碍", "神经病症", "杏仁核劫持"],
    "宗教类": ["灵魂等级", "业力", "神煞", "道心", "识神", "元神", "华盖", "印星", "食伤", "官杀"],
    "攻击类": ["傻逼", "你他妈", "狗屁", "舔着脸", "肉鸡", "滚出去", "巨婴", "捞女"],
    "绝对类": ["没有人", "唯一", "所有", "永远", "必须"],
    "引流类": ["进群", "课程", "私信", "粉丝群", "语音课"],
}
SAFE_REPLACE = {
    "阶级": "阶层、社会结构", "资本家": "有产者、资源提供方", "底层人群": "普通劳动者",
    "剥削": "消耗、过度使用", "灵魂等级": "内在成熟度", "宇宙": "客观规律",
    "能量场": "心理状态", "神性": "内在力量", "业力": "惯性模式",
    "抑郁": "心理困境、内在冲突", "人格障碍": "不太对劲的人", "傻逼": "硬推、低认知",
    "巨婴": "需要情绪关照的沟通对象", "捞女": "某些人", "唯一": "你可以学会",
    "PTSD": "创伤感", "道心": "自我成长", "永远": "长期来看", "必须": "尽量",
}
# 极高危（命中即整段处理）示例型信号
RED_HINT = ["排挤", "撤职", "保护伞", "就是个笑话", "政府反应", "资产阶级",
            "抢流量", "进粉丝群", "语音课里讲得更系统"]

MEMORY_DIR = os.path.join(SCRIPT_DIR, "..", "memory")
ADDITIONS_FILE = os.path.join(MEMORY_DIR, "risk-additions.md")
LOG_FILE = os.path.join(MEMORY_DIR, "learning-log.md")
LOG_HEADER = """# 学习日志（自迭代用）

每次使用后把新经验记一行；每周复盘，把出现 2 次以上的经验固化到 SKILL.md 或词库。

| 日期 | 任务类型 | 经验/记录 |
|---|---|---|
"""


def log_learn(note):
    """把一条审核经验追加到学习日志（自迭代闭环的输入）。"""
    if not note:
        return
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(LOG_HEADER)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"| 今日 | 审核记录 | {note.replace('|', '／')} |\n")
    print(f"[学习] 已记录到学习日志：{LOG_FILE}")


def load_personal_lexicon(cat_words, replace):
    """读取 memory/risk-additions.md 个人风险词库（格式：词|类别|替换建议），合并进扫描词库。"""
    if not os.path.exists(ADDITIONS_FILE):
        return
    with open(ADDITIONS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if not parts[0]:
                continue
            cat = parts[1] if len(parts) > 1 and parts[1] else "个人"
            cat_words.setdefault(cat, [])
            if parts[0] not in cat_words[cat]:
                cat_words[cat].append(parts[0])
            if len(parts) >= 3 and parts[2]:
                replace[parts[0]] = parts[2]


def remember_word(entry):
    """把新风险词追加到个人词库（格式：词|类别|替换建议），下次扫描自动加载。"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(ADDITIONS_FILE):
        with open(ADDITIONS_FILE, "w", encoding="utf-8") as f:
            f.write("# 个人风险词库（audit.py 自动加载，一行一条：词|类别|替换建议）\n")
    with open(ADDITIONS_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def load_lexicon():
    """从 references/risk-lexicon.md 解析词库（读不到则用内置兜底）。"""
    cat_words = {k: list(v) for k, v in DANGER_GENERIC.items()}
    replace = dict(SAFE_REPLACE)
    closers = []
    try:
        with open(LEXICON_PATH, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return cat_words, replace, closers
    # 高危词库速查（**政治类**：词、词）
    m = re.search(r"## 高危词库速查(.*?)## 安全替换表", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"\*\*(.*?)\*\*：(.*)", line.strip())
            if mm:
                cat = mm.group(1)
                words = [w.strip() for w in re.split(r"[、，,]", mm.group(2)) if w.strip()]
                if words:
                    cat_words[cat] = words
    # 安全替换表（| 词 | 安全替换 |）
    m = re.search(r"## 安全替换表(.*?)## 收束句式库", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0] and cells[1] and cells[0] != "高危词":
                replace[cells[0]] = cells[1]
    # 收束句式库
    m = re.search(r"## 收束句式库(.*)", text, re.S)
    if m:
        closers = [l.strip().strip('- "') for l in m.group(1).splitlines()
                   if l.strip().startswith("-") and l.strip().strip('- "')]
    return cat_words, replace, closers


def judge_originality(text):
    """按 originality.md 信号启发式判定原创性等级。"""
    hits = {s: text.count(s) for s in AI_SIGNALS if s in text}
    ai_count = sum(hits.values())
    personal_count = sum(text.count(m) for m in PERSONAL_MARKERS)
    has_numbers = bool(re.search(r"\d", text))
    has_quotes = bool(re.search(r"[“”\"'《》]", text))
    signals = []
    if ai_count >= 3:
        signals.append(f"AI套话信号命中 {ai_count} 处（{'、'.join(sorted(hits)[:4])} 等）")
    if personal_count < 3:
        signals.append(f"个人痕迹偏少（个人化标记仅 {personal_count} 处）")
    if not has_numbers:
        signals.append("全文没有具体数字/数据支撑")
    if not has_quotes:
        signals.append("缺少具体引述/案例标记")
    if personal_count >= 5 and ai_count == 0 and has_numbers:
        grade = "极高"
    elif ai_count <= 1 and personal_count >= 3 and has_numbers:
        grade = "高"
    elif ai_count <= 4:
        grade = "中"
    else:
        grade = "低"
    reasons = []
    if grade in ("极高", "高"):
        reasons.append(f"个人化标记 {personal_count} 处" + ("，有具体数字" if has_numbers else ""))
        if ai_count == 0:
            reasons.append("未见明显 AI 套话信号")
    else:
        reasons = signals[:3]
    return grade, reasons, hits, personal_count


def scan_risk(text, cat_words, replace, closers):
    found = []
    red_hits = [w for w in RED_HINT if w in text]
    for cat, words in cat_words.items():
        for w in words:
            n = text.count(w)
            if n > 0:
                repl = replace.get(w, "")
                found.append({"词": w, "类别": cat, "次数": n, "安全替换": repl})
    return found, red_hits, closers


def render_report(text, path, grade, reasons, hits, personal_count, found, red_hits, closers):
    out = []
    out.append("## 审核结果")
    out.append(f"- 原创性等级：{grade}")
    if reasons:
        out.append(f"  - 依据：{('；'.join(reasons))}")
    out.append(f"  - AI套话信号命中：{sum(hits.values())} 处；个人化标记：{personal_count} 处")
    risk_level = "低"
    if red_hits or any(f["类别"] in ("政治类", "攻击类") for f in found):
        risk_level = "高"
    elif found:
        risk_level = "中"
    out.append(f"- 限流风险：{risk_level}")
    out.append(f"  - 命中风险词 {len(found)} 个"
               + (f"，极高危信号 {len(red_hits)} 处" if red_hits else ""))
    if red_hits:
        out.append(f"  - 极高危信号：{'、'.join(red_hits)}（必须删除或整段重写）")
    out.append("")
    if found:
        out.append("## 风险词扫描（按词库）")
        out.append("| 风险词 | 类别 | 出现次数 | 建议替换 |")
        out.append("|---|---|---|---|")
        for f in found:
            out.append(f"| {f['词']} | {f['类别']} | {f['次数']} | {f['安全替换'] or '删除/重写'} |")
        out.append("")
    if hits:
        top = sorted(hits.items(), key=lambda x: -x[1])[:5]
        out.append("## AI 套话提示")
        out.append("出现次数较多的套话词：" + "、".join(f"{k}（{v}次）" for k, v in top))
        out.append("改写建议：删套话，换自己的概念/比喻；每条观点加一个具体案例或数字。")
        out.append("")
    if closers:
        out.append("## 收束句式建议（批判性内容必须正向收束）")
        out.append("可选用：" + closers[0])
    out.append("")
    out.append("## 自检结果")
    out.append(f"- [ ] 原创性达标（当前判定：{grade}，目标≥高）")
    out.append(f"- [ ] 限流风险达标（当前判定：{risk_level}，目标≤低）")
    out.append("- [ ] 逐条替换后复核全文，无遗漏")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="yihaiyoudao 内容审核自动化")
    ap.add_argument("file", nargs="?", help="待审核文本文件")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--note", help="把一条审核经验追加到学习日志（自迭代）")
    ap.add_argument("--remember", help="把新风险词加入个人词库（格式：词|类别|替换建议），下次扫描自动加载")
    args = ap.parse_args()
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    if not text.strip():
        print("错误：没有输入内容。用法：python audit.py 文章.txt 或管道输入。")
        sys.exit(1)
    cat_words, replace, closers = load_lexicon()
    load_personal_lexicon(cat_words, replace)
    grade, reasons, hits, personal_count = judge_originality(text)
    found, red_hits, _ = scan_risk(text, cat_words, replace, closers)
    if args.json:
        print(json.dumps({
            "原创性等级": grade, "依据": reasons,
            "AI套话信号": hits, "个人化标记": personal_count,
            "风险词": found, "极高危信号": red_hits,
        }, ensure_ascii=False, indent=2))
    else:
        print(render_report(text, args.file, grade, reasons, hits, personal_count,
                            found, red_hits, closers))
    if args.remember:
        remember_word(args.remember)
        print(f"[学习] 已加入个人词库：{args.remember}")
    log_learn(args.note)


if __name__ == "__main__":
    main()
