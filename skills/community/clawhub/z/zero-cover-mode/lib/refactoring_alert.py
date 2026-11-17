"""零稀泥模式 — 重构警报自动聚合 refactoring_alert.py

从 FIX_CLOSURE_LOG.ndjson 自动聚合生成 REFACTORING_ALERT.md
支持 upsert（同日期同类型更新）、截断（保留最近 MAX_ALERT_BLOCKS 块）。

Usage:
    python refactoring_alert.py generate <ndjson_path> [output_path]
    python refactoring_alert.py check <ndjson_path> <bug_type>
"""

import json, os, sys, re, logging
from datetime import datetime, timezone, timedelta

from .config import TZ, MAX_ALERT_BLOCKS

log = logging.getLogger("refactoring")


def generate_alerts(ndjson_path):
    """从 ndjson 聚合重构警报数据"""
    if not os.path.exists(ndjson_path):
        return [], {}

    with open(ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = [l.strip() for l in f if l.strip()]

    type_count = {}
    type_details = {}
    for line in lines:
        try:
            row = json.loads(line)
            bt = row.get("bug_type")
            if bt and bt != "multiple":
                type_count[bt] = type_count.get(bt, 0) + 1
                type_details.setdefault(bt, []).append(row)
        except json.JSONDecodeError:
            continue

    alerts = [(bt, cnt) for bt, cnt in sorted(type_count.items(),
               key=lambda x: -x[1]) if cnt >= 2]
    return alerts, type_details


def _infer_root_pattern(bug_type: str, sample_rc: str) -> str:
    """从 bug_type 和根因摘要推断根源模式（P1-C: 加权评分替代短路匹配）

    按权重评分，"架构设计缺失"不会被 unintentional 吞掉。
    权重规则：
    - architecture: 架构 + 设计 + 重构 (权重最高, 3分)
    - deliberate: 故意 + 设计如此 (2分)
    - documentation: 文档 + 注释 (1分)
    - unintentional: 缺失 + 没有 (0.5分, 通用词汇)
    """
    rc = (sample_rc or "").lower()

    _PATTERNS = [
        (r"架构|architec|架构层面|系统性|系统性问题", "architecture", 3),
        (r"重构|重新设计|redesign", "architecture", 3),
        (r"故意|deliberate|设计如此", "deliberate", 2),
        (r"文档|注释|docstring|document", "documentation", 1),
        (r"缺失|缺少|没有|缺|无|not|遗漏", "unintentional", 0.5),
    ]

    best_score = 0
    best_pattern = None

    for pat, label, weight in _PATTERNS:
        matches = re.findall(pat, rc)
        if matches:
            score = weight * len(matches)
            if score > best_score:
                best_score = score
                best_pattern = label

    if best_pattern:
        return best_pattern

    # fallback: 从 bug_type 映射
    m = {
        "config_error": "unintentional", "type_mismatch": "unintentional",
        "null_pointer": "unintentional", "logic_error": "unintentional",
        "resource_leak": "architecture", "performance": "architecture",
        "data_corruption": "architecture", "race_condition": "architecture",
        "dead_code": "unintentional", "syntax_error": "unintentional",
    }
    return m.get(bug_type, "architecture")


def _build_alert_block(bt, cnt, bug_ids, modules, sample_rc, date_str):
    """生成单条警报块文本"""
    pattern = _infer_root_pattern(bt, sample_rc)
    return [
        f"## {date_str} 自动检测 — {bt} 出现 {cnt} 次\n",
        f"- **{bt}**: {cnt} 次 — 涉及模块: {', '.join(modules)}\n",
        f"  - Bug IDs: {', '.join(bug_ids)}\n",
        f"  - 根因摘要: {sample_rc}\n",
        f"  - 根源模式: {pattern}\n",
        f"  - 自动检测触发\n",
        "\n",
    ]


def _parse_alert_blocks(file_lines):
    """解析现有文件中的警报块

    返回 {block_key: (start_line, end_line, content_lines)}
    block_key 格式: "YYYY-MM-DD/bug_type"

    注意: 只识别格式为 `## YYYY-MM-DD 自动检测 — <bug_type> 出现 N 次` 的标题。
    文件中其他以 `## ` 开头的普通标题行不会匹配 header_pattern，
    会被跳过（current_key 置 None，不参与 block 解析）。
    这意味着 REFACTORING_ALERT.md 中可以安全地使用其他 `## ` 标题
    而不影响警报块解析。（P1-v11.3: 加注释澄清此设计）
    """
    header_pattern = re.compile(
        r'^## (\d{4}-\d{2}-\d{2}) 自动检测 — (.+) 出现 \d+ 次$'
    )
    blocks = {}
    current_key = None
    current_start = None

    for i, line in enumerate(file_lines):
        stripped = line.strip()
        if stripped.startswith("## "):
            if current_start is not None and current_key is not None:
                blocks[current_key] = (
                    current_start, i, file_lines[current_start:i],
                )
            m = header_pattern.match(stripped)
            if m:
                current_key = f"{m.group(1)}/{m.group(2)}"
            else:
                current_key = None
                current_start = None
                continue
            current_start = i

    if current_start is not None and current_key is not None:
        blocks[current_key] = (
            current_start, len(file_lines), file_lines[current_start:],
        )
    return blocks


def write_alert_md(ndjson_path, output_path):
    """upsert 模式 — 同日期同类型则更新，否则追加"""
    alerts, type_details = generate_alerts(ndjson_path)
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M CST")
    today = now[:10]

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        header = [
            "# 重构警报日志\n",
            f"> 同一 bug_type 出现 >= 2 次时自动触发。\n",
            f"> 自动生成时间: {now}  |  数据源: {ndjson_path}\n",
            "---\n\n",
        ]
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("".join(header))

    with open(output_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    existing_blocks = _parse_alert_blocks(all_lines)

    header_end = len(all_lines)
    for i, line in enumerate(all_lines):
        if re.match(r'^## \d{4}-\d{2}-\d{2} 自动检测', line.strip()):
            header_end = i
            break

    new_blocks = {}
    for bt, cnt in alerts:
        details = type_details.get(bt, [])
        modules = list(set(r.get("module", "unknown") for r in details))
        bug_ids = [r.get("bug_id", "?") for r in details[:10]]
        sample_rc = (details[0].get("root_cause", "") or "")[:80] if details else ""
        key = f"{today}/{bt}"
        new_blocks[key] = _build_alert_block(bt, cnt, bug_ids, modules, sample_rc, today)

    if not new_blocks:
        return True

    final_lines = list(all_lines[:header_end])
    inserted_keys = set()

    for key, (start, end, content) in existing_blocks.items():
        if key in new_blocks and key.split("/")[0] == today:
            final_lines.extend(new_blocks[key])
            final_lines.append("---\n")
            inserted_keys.add(key)
        else:
            final_lines.extend(content)

    for key, content in new_blocks.items():
        if key not in inserted_keys:
            final_lines.extend(content)
            final_lines.append("---\n")

    # P0-3: 避免对空 ndjson 或已有今日时间戳的文件重复追加
    if new_blocks:
        today_str = now[:10]
        has_existing = any(
            today_str in line and "*追加时间*" in line
            for line in final_lines
        )
        if not has_existing:
            if not final_lines[-1].endswith("\n"):
                final_lines.append("\n")
            final_lines.append(f"*追加时间: {now}*\n")
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(final_lines)
    log.info("重构警报已更新 -> %s (%d 个活跃, upsert=%d)", output_path, len(alerts), len(inserted_keys))
    _trim_alert_file(output_path)
    return True


def _trim_alert_file(output_path):
    """按 bug_type 聚类截断：至少每个活跃 bug_type 保留最新一块，然后按日期裁剪

    P1-E: 聚类保留替代简单的按行号截断，避免丢失有长期趋势的 bug_type。
    """
    if not os.path.exists(output_path):
        return
    with open(output_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    # 解析业务块：{(start, end): bug_type}
    blocks = {}  # (start, end) -> bug_type
    current_start = None
    current_type = None
    for i, line in enumerate(all_lines):
        m = re.match(r'^## \d{4}-\d{2}-\d{2} 自动检测 — (.+) 出现 \d+ 次$', line.strip())
        if m:
            if current_start is not None:
                blocks[(current_start, i)] = current_type
            current_start = i
            current_type = m.group(1)
    if current_start is not None:
        blocks[(current_start, len(all_lines))] = current_type

    if not blocks or len(blocks) <= MAX_ALERT_BLOCKS:
        return

    # 聚类：每个 bug_type 保留最新一块
    type_blocks = {}
    for (start, end), bt in blocks.items():
        if bt not in type_blocks or start > type_blocks[bt][0]:
            type_blocks[bt] = (start, end)

    # 按 start line 排序
    kept = sorted(type_blocks.values(), key=lambda x: x[0])

    # 如果聚类后仍然超过 MAX_ALERT_BLOCKS，裁剪最旧的
    if len(kept) > MAX_ALERT_BLOCKS:
        kept = kept[-MAX_ALERT_BLOCKS:]

    # 重构文件
    header_end = min(s for s, _ in blocks) if blocks else 0
    new_lines = list(all_lines[:header_end])
    for start, end in kept:
        new_lines.extend(all_lines[start:end])

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    log.info("警报聚类截断: %s 从 %d 块 -> %d 块 (%d 种 bug_type)",
             output_path, len(blocks), len(kept), len(type_blocks))


def check_type(ndjson_path, bug_type):
    alerts, _ = generate_alerts(ndjson_path)
    for bt, cnt in alerts:
        if bt == bug_type:
            print(f"{bug_type}: {cnt} 次 (>= 2, 触发警报)")
            return True, cnt
    print(f"{bug_type}: 未达到警报阈值")
    return False, 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="重构警报自动聚合")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate", help="生成重构警报")
    p.add_argument("ndjson_path", nargs="?", default="FIX_CLOSURE_LOG.ndjson")
    p.add_argument("output_path", nargs="?")
    p = sub.add_parser("check", help="检查类型是否触发警报")
    p.add_argument("ndjson_path", nargs="?", default="FIX_CLOSURE_LOG.ndjson")
    p.add_argument("bug_type")
    args = parser.parse_args()
    try:
        if args.command == "generate":
            write_alert_md(args.ndjson_path, args.output_path or "REFACTORING_ALERT.md")
        elif args.command == "check":
            check_type(args.ndjson_path, args.bug_type)
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)
