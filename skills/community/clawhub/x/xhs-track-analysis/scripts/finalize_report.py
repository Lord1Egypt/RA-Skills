#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从已完成的《赛道分析主表》生成《决策简报》并做完整性自检。

用法:
  python3 finalize_report.py <主表.md> [--out 决策简报.md] [--strict]

说明:
  1. 解析主表的「一、研究任务与三问」~「八、决策结论」八个节；
  2. 检查必填项是否已填写（三问、证据边界、决策结论、置信度），
     以及是否有采集时间 > 90 天但未标「需复核」的内容；
  3. 输出两份产物:
     - 《决策简报》: 一页纸投决摘要（GO/NO-GO + 找谁讲 + 讲什么角度 + 置信度 + 下一步验证）
     - 完整性报告: 缺失项与补充提示（打印到屏幕，同时写入 <主表名>.check.md）
  4. --strict 时若存在缺失项则不生成简报（用于交付门禁）。

退出码: 0 = 简报已生成且无缺失; 1 = 简报已生成但有缺失; 2 = 用法错误 / 主表无法解析。
"""
import argparse
import csv
import datetime
import math
import os
import re
import sys

SECTIONS = [
    "一、研究任务与三问",
    "二、关键词四分组",
    "三、采集记录",
    "四、重点笔记与达人",
    "五、评论行为归类",
    "六、关键判断与下一步",
    "七、证据边界",
    "八、决策结论",
]

# 必填节：缺失即视为分析未收敛
REQUIRED_SECTIONS = ["一、研究任务与三问", "七、证据边界", "八、决策结论"]

# 决策结论节内的必填字段标记
DECISION_MARKERS = ["投决建议", "找谁讲", "讲什么角度", "进入策略", "证据边界内置信度"]

VALID_DECISIONS = ["GO", "NO-GO", "NO-GO", "条件GO"]
VALID_CONFIDENCE = ["高", "中", "低"]

USAGE = """用法:
  python3 finalize_report.py <主表.md> [--out 决策简报.md] [--strict]
  python3 finalize_report.py --focus <采集csv> [--top N] [--out 重点笔记候选.md]

示例:
  python3 finalize_report.py 赛道分析主表.md
  python3 finalize_report.py 赛道分析主表.md --strict   # 有缺失则中止，不生成简报
  python3 finalize_report.py --focus raw_notes.csv --top 15   # 从采集产物筛选重点笔记

说明:
  模式一（默认）: 主表须为由 scripts/scaffold_table.py 生成的八节结构，且「八、决策结论」
    的四个标记行（投决建议/找谁讲/讲什么角度/证据边界内置信度）已填写。
    输出: 《决策简报》 + <主表名>.check.md 完整性报告。
  模式二 (--focus): 输入采集 CSV（collector 或 integrations 产物，含 keyword/sort/note_id/
    likes/collects/comments 等字段），按"跨关键词命中 + 互动量"评分收敛重点笔记清单，
    输出可直接作为主表「四、重点笔记与达人」草稿。"""


def die(msg):
    print(f"错误: {msg}", file=sys.stderr)
    print("提示: 运行 python3 finalize_report.py --help 查看用法。", file=sys.stderr)
    sys.exit(2)


def split_sections(text):
    """按节标题切分主表，返回 {节标题: 节内容}。"""
    lines = text.splitlines()
    result = {}
    current = None
    for line in lines:
        stripped = line.strip()
        matched = None
        if stripped.startswith("##"):
            for sec in SECTIONS:
                if sec in stripped:
                    matched = sec
                    break
        if matched:
            current = matched
            result[current] = []
        elif current is not None:
            result[current].append(line)
    return result


def field_value(section_text, marker):
    """取某标记行的值（如 '投决建议: GO' -> 'GO'）。找不到返回 ''。"""
    for line in section_text:
        if marker in line and ":" in line:
            return line.split(":", 1)[1].strip()
    return ""


def list_items(section_text):
    """取节内所有 '- ...' 列表项的值部分。"""
    items = []
    for line in section_text:
        s = line.strip()
        if s.startswith("-"):
            items.append(s.lstrip("-").strip())
    return items


def days_old(date_str):
    """把 2026-08-19 / 2026/08/19 / 2026.08.19 解析为距今天数；解析失败返回 None。"""
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y年%m月%d日"):
        try:
            d = datetime.datetime.strptime(date_str.strip(), fmt).date()
            return (datetime.date.today() - d).days
        except ValueError:
            continue
    return None


def check_staleness(text, issues, infos):
    """扫描所有日期：距今 > 90 天且全文未标「需复核」则告警；已标则仅提示。"""
    dates = re.findall(r"20\d{2}[-/.年]\d{1,2}[-/.月]\d{1,2}日?", text)
    old = [d for d in dates if (n := days_old(d)) is not None and n > 90]
    if not old:
        return
    if "需复核" in text:
        infos.append(f"发现 {len(old)} 处采集日期距今 > 90 天（如 {old[0]}），已标「需复核」，请人工确认其时效性")
    else:
        issues.append(
            f"发现 {len(old)} 处采集日期距今 > 90 天（如 {old[0]}），"
            "但全文未标「需复核」。请为过期内容标注或更新采集时间。"
        )


def extract_category(text):
    """从标题行提取品类名，取不到则返回 '未命名'。"""
    m = re.search(r"主表\s*[·・]\s*(\S+)", text)
    if m:
        return m.group(1)
    return "未命名"


def _num(value):
    """把 CSV 里的数字字符串安全转 int；空/非法返回 0。"""
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def focus_reasons(item):
    """生成重点笔记的识别理由（启发式，对应方法论中的信号）。"""
    rs = []
    if item["kw_hits"] >= 2:
        rs.append(f"枢纽内容：命中 {item['kw_hits']} 个关键词")
    if item["comments"] >= 30 or (item["likes"] > 0 and item["comments"] >= item["likes"] * 0.3):
        rs.append("高评论：争议/追问信号强")
    if item["collects"] >= item["likes"] and item["collects"] > 0:
        rs.append("高收藏：留存意愿强")
    if item["comments_saved"] > 0:
        rs.append(f"已有 {item['comments_saved']} 条评论可做四行为归类")
    if not rs:
        rs.append("互动靠前（赞/藏/评综合）")
    return "；".join(rs)


def run_focus(csv_path, top_n, out_path):
    """从采集 CSV 收敛重点笔记清单（模式二）。"""
    if not os.path.exists(csv_path):
        die(f"找不到采集 CSV: {csv_path}")
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        die(f"采集 CSV 为空或无表头: {csv_path}")

    # 按规范链接（去查询参数）聚合跨关键词命中（枢纽内容信号），保留全部出处；
    # 无 url 时退回 note_id。url 比 note_id 更稳：同一笔记跨关键词/排序 URL 稳定，note_id 可能缺失。
    notes = {}
    for r in rows:
        url = (r.get("url") or "").strip().split("?")[0]
        key = url or (r.get("note_id") or "").strip()
        if not key:
            continue
        if key not in notes:
            notes[key] = {"row": r, "keywords": set(), "sorts": set()}
        notes[key]["keywords"].add(r.get("keyword", ""))
        notes[key]["sorts"].add(r.get("sort", ""))

    scored = []
    for key, agg in notes.items():
        r = agg["row"]
        item = {
            "note_id": key,
            "title": r.get("title", ""),
            "author": r.get("author", ""),
            "url": r.get("url", ""),
            "keywords": sorted(k for k in agg["keywords"] if k),
            "kw_hits": len([k for k in agg["keywords"] if k]),
            "sort_count": len(agg["sorts"]),
            "likes": _num(r.get("likes")),
            "collects": _num(r.get("collects")),
            "comments": _num(r.get("comments")),
            "comments_saved": _num(r.get("comments_saved")),
            "field_scope": r.get("field_scope", ""),
            "completion_state": r.get("completion_state", ""),
        }
        # 评分：跨关键词命中权重最高，评论>赞/藏（赛道判断核心），已存评论加分（数据可分析）
        item["score"] = (
            5 * item["kw_hits"]
            + math.log1p(item["likes"])
            + math.log1p(item["collects"])
            + 2 * math.log1p(item["comments"])
            + item["comments_saved"]
        )
        scored.append(item)

    scored.sort(key=lambda x: x["score"], reverse=True)
    picked = scored[: max(1, top_n)]

    out_path = out_path or "重点笔记候选.md"
    today = datetime.date.today().isoformat()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# 重点笔记候选 · {today}\n\n")
        f.write("> 由 scripts/finalize_report.py --focus 从采集产物自动收敛（跨关键词命中 + 互动量评分），\n")
        f.write("> **启发式初筛，非最终判断**：请结合正文、评论四行为与商业化浓度复核后，\n")
        f.write("> 填入主表「四、重点笔记与达人」并补充来源（本人/第三方）与关键判断。\n\n")
        f.write(f"输入 {len(rows)} 条采集记录 → 去重后 {len(scored)} 篇笔记 → 收敛前 {len(picked)} 篇。\n\n")
        f.write("| 排名 | 标题 | 作者 | 命中关键词(全部) | 赞 | 藏 | 评 | 已存评论 | 范围/状态 | 识别理由 | 链接 |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for i, item in enumerate(picked, 1):
            scope_state = f"{item['field_scope']}/{item['completion_state']}"
            kws = "、".join(item["keywords"]) or "-"
            title = (item["title"] or "")[:30].replace("|", "\\|")
            f.write(
                f"| {i} | {title} | {item['author']} | {kws} | "
                f"{item['likes']} | {item['collects']} | {item['comments']} | "
                f"{item['comments_saved']} | {scope_state} | {focus_reasons(item)} | "
                f"{item['url']} |\n"
            )
    print(f"[重点] 已生成: {out_path}（{len(picked)} 篇，来自 {len(scored)} 篇去重笔记）")
    return picked


def main():
    parser = argparse.ArgumentParser(
        prog="finalize_report.py",
        description=("从《赛道分析主表》生成《决策简报》并做完整性自检（默认模式）；"
                     "或 --focus 从采集 CSV 收敛重点笔记清单（模式二）。"),
        add_help=True,
    )
    parser.add_argument("main_table", nargs="?", default=None,
                        help="赛道分析主表 Markdown 文件路径（模式一）")
    parser.add_argument("--focus", default=None,
                        help="模式二：输入采集 CSV（collector 或 integrations 产物），收敛重点笔记清单")
    parser.add_argument("--top", type=int, default=15, help="模式二：重点笔记数量（默认 15）")
    parser.add_argument("--out", default=None, help="输出路径（模式一: 决策简报；模式二: 重点笔记候选）")
    parser.add_argument("--strict", action="store_true", help="模式一：存在缺失项时中止，不生成简报")
    args = parser.parse_args()

    if args.focus:
        run_focus(args.focus, args.top, args.out)
        sys.exit(0)

    path = args.main_table
    if not path:
        die("缺少主表文件。用法: python3 finalize_report.py <主表.md>，或 --focus <采集csv>。")
    if not os.path.exists(path):
        die(f"找不到主表文件: {path}")
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        die(f"读取主表失败: {e}")

    sections = split_sections(text)
    issues = []
    infos = []

    # 1) 必填节检查
    for sec in REQUIRED_SECTIONS:
        if sec not in sections:
            issues.append(f"缺少必填节「{sec}」")

    # 2) 决策结论必填字段检查
    decision_text = sections.get("八、决策结论", [])
    for marker in DECISION_MARKERS:
        if marker not in "".join(decision_text):
            issues.append(f"「八、决策结论」缺少标记行「{marker}」")
        elif not field_value(decision_text, marker):
            issues.append(f"「八、决策结论」的「{marker}」未填写")

    # 3) 决策值合法性
    advice = field_value(decision_text, "投决建议")
    if advice and not any(v in advice.upper() for v in VALID_DECISIONS):
        issues.append(f"「投决建议」取值异常（应为 GO / NO-GO / 条件GO）: {advice}")
    confidence = field_value(decision_text, "证据边界内置信度")
    if confidence and confidence not in VALID_CONFIDENCE:
        if "/" in confidence:
            issues.append("「证据边界内置信度」仍为占位符，请改为 高 / 中 / 低 之一")
        else:
            issues.append(f"「证据边界内置信度」取值异常（应为 高/中/低）: {confidence}")

    # 4) 三问完整性
    three_questions = list_items(sections.get("一、研究任务与三问", []))
    filled = [q for q in three_questions if q and not q.endswith(":")]
    if len(filled) < 3:
        issues.append(f"「一、研究任务与三问」填写不足（当前 {len(filled)} 项，应至少 3 项）")

    # 5) 过期内容检查
    check_staleness(text, issues, infos)

    # 6) 证据边界检查
    if not list_items(sections.get("七、证据边界", [])):
        issues.append("「七、证据边界」未填写任何内容")

    # 输出完整性报告
    check_path = os.path.splitext(path)[0] + ".check.md"
    with open(check_path, "w", encoding="utf-8") as f:
        f.write(f"# 完整性自检报告 · {os.path.basename(path)}\n\n")
        if issues:
            f.write(f"共发现 {len(issues)} 项问题：\n\n")
            for i, issue in enumerate(issues, 1):
                f.write(f"{i}. {issue}\n")
        else:
            f.write("全部检查通过。\n")
        if infos:
            f.write("\n提示（不阻断交付）:\n")
            for info in infos:
                f.write(f"- {info}\n")

    for info in infos:
        print(f"[提示] {info}")
    if issues:
        print(f"[自检] 发现 {len(issues)} 项问题，详见 {check_path}")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"[自检] 全部通过。")

    if issues and args.strict:
        sys.exit("--strict 模式：存在缺失项，中止生成简报。")

    # 生成决策简报
    category = extract_category(text)
    out_path = args.out or os.path.join(os.path.dirname(os.path.abspath(path)), "决策简报.md")
    today = datetime.date.today().isoformat()

    def line_value(section_text, marker):
        v = field_value(section_text, marker)
        return v or "（未填写）"

    def list_items_joined(section_text, limit=5):
        items = list_items(section_text)
        return "\n".join(f"- {i}" for i in items[:limit]) or "- （未填写）"

    brief = f"""# 决策简报 · {category}

> 生成日期: {today}　|　由 scripts/finalize_report.py 从《{os.path.basename(path)}》生成

## 投决建议
{line_value(decision_text, "投决建议")}

## 找谁讲（达人类型与可信边界）
{line_value(decision_text, "找谁讲")}

## 讲什么角度
{line_value(decision_text, "讲什么角度")}

## 进入策略
{line_value(decision_text, "进入策略")}

## 证据边界内置信度
{line_value(decision_text, "证据边界内置信度")}

## 用户在问什么（来自三问与关键判断）
{list_items_joined(sections.get("六、关键判断与下一步", []))}

## 证据边界（结论能说到哪一步）
{list_items_joined(sections.get("七、证据边界", []))}

## 下一步建议与验证
- 下一步建议: {line_value(sections.get("六、关键判断与下一步", []), "下一步建议")}
- 需品牌自有数据验证: {line_value(sections.get("七、证据边界", []), "需品牌自有数据验证的")}

---
> 本简报由分析主表自动汇编，仅汇总投决相关字段；完整证据见主表原文。
> 由擎漫网络 | Qomob.AI旗下小红书赛道深度分析引擎 v3.0.0提供支持
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(brief)
    print(f"[简报] 已生成: {out_path}")

    sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    main()
