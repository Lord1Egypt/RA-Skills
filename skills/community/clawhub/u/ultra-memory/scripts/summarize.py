#!/usr/bin/env python3
"""
ultra-memory: 会话摘要压缩脚本
将 ops.jsonl 中的操作日志压缩为结构化 summary.md
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# ── 三层记忆分级 ────────────────────────────────────────────────────────────
# core:       核心记忆，长期保留，召回优先级最高（里程碑/决策/错误/用户指令）
# working:    工作记忆，当前会话活跃，定期压缩后可降级为 peripheral
# peripheral: 外围记忆，历史细节，已压缩，召回时权重最低

TIER_CORE       = "core"
TIER_WORKING    = "working"
TIER_PERIPHERAL = "peripheral"

CORE_OP_TYPES       = {"milestone", "decision", "error", "user_instruction"}
PERIPHERAL_OP_TYPES = {"file_read", "tool_call"}


def classify_tier(op: dict) -> str:
    """根据操作类型和标签判断记忆层级"""
    op_type = op.get("type", "")
    tags    = set(op.get("tags", []))

    if op_type in CORE_OP_TYPES:
        return TIER_CORE
    # file_read / tool_call 且不含里程碑标签 → 外围
    if op_type in PERIPHERAL_OP_TYPES and "milestone" not in tags:
        return TIER_PERIPHERAL
    return TIER_WORKING


def load_ops(session_dir: Path, only_uncompressed: bool = True) -> list[dict]:
    ops_file = session_dir / "ops.jsonl"
    if not ops_file.exists():
        return []
    ops = []
    with open(ops_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            op = json.loads(line)
            if only_uncompressed and op.get("compressed"):
                continue
            ops.append(op)
    return ops


def mark_compressed(session_dir: Path, up_to_seq: int):
    """标记已压缩的操作（不删除，打标记 + 写入 tier 分层）"""
    ops_file = session_dir / "ops.jsonl"
    tmp_file = session_dir / "ops.jsonl.tmp"
    with open(ops_file, encoding="utf-8") as fin, open(tmp_file, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            op = json.loads(line)
            if op["seq"] <= up_to_seq:
                op["compressed"] = True
                # 写入 tier（若尚未分级）
                if "tier" not in op:
                    op["tier"] = classify_tier(op)
            fout.write(json.dumps(op, ensure_ascii=False) + "\n")
    tmp_file.replace(ops_file)


def group_by_tag(ops: list[dict]) -> dict[str, list]:
    groups = {}
    for op in ops:
        for tag in (op.get("tags") or ["general"]):
            groups.setdefault(tag, []).append(op)
    return groups


def extract_milestones(ops: list[dict]) -> list[dict]:
    return [op for op in ops if op["type"] == "milestone" or "milestone" in op.get("tags", [])]


def extract_errors(ops: list[dict]) -> list[dict]:
    return [op for op in ops if op["type"] == "error" or "error" in op.get("tags", [])]


def extract_decisions(ops: list[dict]) -> list[dict]:
    return [op for op in ops if op["type"] == "decision"]


def extract_file_changes(ops: list[dict]) -> list[str]:
    seen = []
    for op in ops:
        if op["type"] == "file_write":
            path = op.get("detail", {}).get("path", "")
            if path and path not in seen:
                seen.append(path)
    return seen


def infer_in_progress(ops: list[dict]) -> list[dict]:
    """
    推断"当前进行中"的任务：
    取最后 5 条非 milestone、非 error 的操作，判断是否存在未完成信号。
    """
    milestone_types = {"milestone"}
    error_types = {"error"}
    candidates = [
        op for op in ops
        if op["type"] not in milestone_types | error_types
        and "milestone" not in op.get("tags", [])
    ]
    return candidates[-5:] if candidates else []


def infer_next_step(ops: list[dict], in_progress: list[dict]) -> str:
    """
    基于最后操作推断"下一步建议"。
    规则：
    - 如果最后操作是 bash_exec → 建议验证结果
    - 如果最后操作是 file_write → 建议运行测试
    - 如果最后操作是 error → 建议排查错误
    - 如果最后操作是 reasoning/decision → 建议开始实现
    - 其他 → 建议继续当前任务
    """
    if not in_progress:
        return "继续当前任务"

    last = in_progress[-1]
    op_type = last.get("type", "")
    summary = last.get("summary", "")

    if op_type == "bash_exec":
        return f"验证上一条命令的执行结果，确认 {summary[:30]} 生效"
    elif op_type == "file_write":
        return f"为刚写入的文件编写或运行测试"
    elif op_type == "error":
        return f"排查错误：{summary[:40]}"
    elif op_type in ("reasoning", "decision"):
        return f"根据决策开始实现：{summary[:40]}"
    elif op_type == "file_read":
        return f"基于已读取的内容进行下一步修改"
    else:
        return f"继续：{summary[:40]}"


def generate_summary_md(session_id: str, ops: list[dict], meta: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    project = meta.get("project", "default")
    op_range = f"第 {ops[0]['seq']}-{ops[-1]['seq']} 条" if ops else "无"

    milestones = extract_milestones(ops)
    errors = extract_errors(ops)
    decisions = extract_decisions(ops)
    file_changes = extract_file_changes(ops)
    in_progress = infer_in_progress(ops)
    next_step = infer_next_step(ops, in_progress)

    # 统计操作类型分布
    type_counts = Counter(op["type"] for op in ops)
    tag_counts = Counter(tag for op in ops for tag in op.get("tags", []))

    lines = [
        f"# 会话摘要 — {session_id}",
        f"更新时间: {now} UTC",
        f"项目: {project}",
        "",
    ]

    # 已完成里程碑
    if milestones:
        lines.append("## ✅ 已完成里程碑")
        for m in milestones:
            ts = m["ts"][:16].replace("T", " ")
            lines.append(f"- [{ts}] {m['summary']}")
        lines.append("")

    # 当前进行中（新增，帮助跨天恢复时快速定位状态）
    if in_progress:
        lines.append("## 🔄 当前进行中")
        for op in in_progress:
            ts = op["ts"][11:16]
            lines.append(f"- [ ] [{ts}] {op['summary'][:80]}")
        lines.append("")

    # 下一步建议（新增，方便 Claude 恢复后立即行动）
    lines.append("## 💡 下一步建议")
    lines.append(f"- {next_step}")
    lines.append("")

    # 文件变更
    if file_changes:
        lines.append("## 📁 涉及文件")
        for path in file_changes[:20]:
            lines.append(f"- `{path}`")
        lines.append("")

    # 关键决策
    if decisions:
        lines.append("## 🔑 关键决策")
        for d in decisions:
            lines.append(f"- {d['summary']}")
            detail = d.get("detail", {})
            if detail.get("rationale"):
                lines.append(f"  - 依据: {detail['rationale']}")
        lines.append("")

    # 错误与处理
    if errors:
        lines.append("## ⚠️ 错误与处理")
        for e in errors:
            ts = e["ts"][:16].replace("T", " ")
            lines.append(f"- [{ts}] {e['summary']}")
        lines.append("")

    # 操作统计
    lines.append("## 📊 操作统计")
    for op_type, count in type_counts.most_common():
        lines.append(f"- {op_type}: {count} 次")
    if tag_counts:
        top_tags = [t for t, _ in tag_counts.most_common(5)]
        lines.append(f"- 主要领域: {', '.join(top_tags)}")
    lines.append("")

    # 记忆分层统计
    tier_counts: Counter = Counter(classify_tier(op) for op in ops)
    if any(tier_counts.values()):
        lines.append("## 🧠 记忆分层")
        lines.append(f"- core（核心）: {tier_counts[TIER_CORE]} 条 — 长期保留，高召回优先级")
        lines.append(f"- working（工作）: {tier_counts[TIER_WORKING]} 条 — 当前会话活跃")
        lines.append(f"- peripheral（外围）: {tier_counts[TIER_PERIPHERAL]} 条 — 历史细节，低优先级")
        lines.append("")

    # 操作日志范围（供下次恢复参考）
    lines.append("## 📋 操作日志范围")
    lines.append(f"ops.jsonl {op_range}（已压缩，原始记录保留）")
    lines.append("")

    return "\n".join(lines)


# summary.md 触发元压缩的字符阈值（约 3000 字符 ≈ 5~6 个压缩块）
META_SUMMARY_THRESHOLD = 3000

# 重要操作类型：压缩时保留原文
HIGH_IMPORTANCE_TYPES = {"milestone", "decision", "error"}


def build_meta_summary_block(blocks: list[str]) -> str:
    """
    将多个 summary 块二次压缩为一个 meta_summary 块。
    只保留：已完成里程碑、关键决策、错误、下一步建议。
    其余操作统计、文件列表等统一折叠为一行。

    meta_summary 结构比 summary 更紧凑，约 5 倍压缩比。
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    # 从各块提取关键行（以 - [ ] 、 ✅、🔑、⚠️、💡 开头的行）
    key_lines: list[str] = []
    op_counts: Counter = Counter()
    for block in blocks:
        for line in block.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            # 保留里程碑、决策、错误、建议
            if any(m in stripped for m in ["✅", "🔑", "⚠️", "💡", "- [x]", "[09", "[10", "[11",
                                            "[12", "[13", "[14", "[15", "[16", "[17", "[18", "[19",
                                            "[20", "[21", "[22", "[23"]):
                key_lines.append(f"  {stripped}")
            # 统计操作类型
            m = re.match(r"- (\w+): (\d+) 次", stripped)
            if m:
                op_counts[m.group(1)] += int(m.group(2))

    lines = [
        f"# [META] 历史摘要 — 压缩自 {len(blocks)} 个摘要块",
        f"压缩时间: {now} UTC",
        f"（此块包含多次会话的核心信息，细节见各会话 summary.md）",
        "",
    ]
    if key_lines:
        lines.append("## 历史关键事件（里程碑/决策/错误）")
        lines.extend(key_lines[:30])  # 最多保留30条关键行
        lines.append("")
    if op_counts:
        lines.append("## 历史操作总量")
        for op_type, count in op_counts.most_common():
            lines.append(f"- {op_type}: 累计 {count} 次")
        lines.append("")

    return "\n".join(lines)


def maybe_meta_compress(session_dir: Path, summary_file: Path):
    """
    检查 summary.md 是否超过阈值，超过则对历史块做元压缩。
    元压缩后将历史块替换为一个 [META] 块，最新块保持不变。

    机制（分层记忆）：
      ops.jsonl → [50ops] → summary块  （每50ops一块）
      summary块 × N → [META]块         （每N块合并一次）
      [META]块本身也可再次合并          （理论上无限深度）
    """
    if not summary_file.exists():
        return

    content = summary_file.read_text(encoding="utf-8")
    if len(content) < META_SUMMARY_THRESHOLD:
        return  # 还未达到阈值

    # 按 --- 分隔成各个块
    raw_blocks = [b.strip() for b in content.split("---") if b.strip()]
    if len(raw_blocks) < 4:
        return  # 块数太少，不压缩

    # 保留最新的 2 个块原样，对其余的块做元压缩
    blocks_to_compress = raw_blocks[:-2]
    blocks_to_keep = raw_blocks[-2:]

    meta_block = build_meta_summary_block(blocks_to_compress)

    new_content = meta_block + "\n\n---\n\n" + "\n\n---\n\n".join(blocks_to_keep)
    summary_file.write_text(new_content, encoding="utf-8")

    saved_chars = len(content) - len(new_content)
    print(f"[ultra-memory] 🗜️  元压缩完成：{len(blocks_to_compress)} 块 → 1 个 [META] 块，"
          f"节省 {saved_chars} 字符（{saved_chars*100//max(len(content),1)}%）")


import re


def summarize(session_id: str, force: bool = False):
    session_dir = ULTRA_MEMORY_HOME / "sessions" / session_id
    if not session_dir.exists():
        print(f"[ultra-memory] ❌ 会话不存在: {session_id}")
        return

    meta_file = session_dir / "meta.json"
    meta = {}
    if meta_file.exists():
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)

    ops = load_ops(session_dir, only_uncompressed=True)
    if len(ops) < 10 and not force:
        print(f"[ultra-memory] ⏭️  操作条数不足（{len(ops)} 条），跳过压缩（用 --force 强制执行）")
        return

    if not ops:
        print("[ultra-memory] 无新操作需要压缩")
        return

    summary_content = generate_summary_md(session_id, ops, meta)
    summary_file = session_dir / "summary.md"

    # 追加到现有摘要（不覆盖，保留历史压缩记录）
    mode = "a" if summary_file.exists() else "w"
    if mode == "a":
        summary_content = "\n---\n\n" + summary_content
    with open(summary_file, mode, encoding="utf-8") as f:
        f.write(summary_content)

    # 标记已压缩
    last_seq = ops[-1]["seq"]
    mark_compressed(session_dir, last_seq)

    # 更新 meta
    meta["last_summary_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    meta["last_milestone"] = ops[-1]["summary"] if ops else meta.get("last_milestone")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 同步到 Layer 3 索引
    sync_to_semantic(session_id, meta, ops)

    # 【新】检查是否需要元压缩（分层记忆核心）
    maybe_meta_compress(session_dir, summary_file)

    print(f"[ultra-memory] ✅ 摘要压缩完成，{len(ops)} 条操作 → summary.md")
    print(f"[ultra-memory] 摘要路径: {summary_file}")


def sync_to_semantic(session_id: str, meta: dict, ops: list[dict]):
    """将里程碑和关键信息同步到 Layer 3"""
    semantic_dir = ULTRA_MEMORY_HOME / "semantic"
    index_file = semantic_dir / "session_index.json"
    if not index_file.exists():
        return
    with open(index_file, encoding="utf-8") as f:
        index = json.load(f)
    for s in index.get("sessions", []):
        if s["session_id"] == session_id:
            milestones = extract_milestones(ops)
            if milestones:
                s["last_milestone"] = milestones[-1]["summary"]
            break
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def extract_milestones(ops):
    return [op for op in ops if op["type"] == "milestone" or "milestone" in op.get("tags", [])]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="触发会话摘要压缩")
    parser.add_argument("--session", required=True, help="会话 ID")
    parser.add_argument("--force", action="store_true", help="强制压缩（即使条数不足）")
    args = parser.parse_args()
    summarize(args.session, args.force)
