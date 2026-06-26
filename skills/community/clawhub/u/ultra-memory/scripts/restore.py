#!/usr/bin/env python3
"""
ultra-memory: 会话恢复脚本
在新会话开始时，自动加载上次会话的上下文并注入提示
优化：自然语言总结 + 任务完成状态识别 + 继续/下阶段建议
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))


def find_latest_session(project: str):
    sessions_dir = ULTRA_MEMORY_HOME / "sessions"
    if not sessions_dir.exists():
        return None
    candidates = []
    for d in sessions_dir.iterdir():
        if not d.is_dir():
            continue
        meta_file = d / "meta.json"
        if not meta_file.exists():
            continue
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
        if meta.get("project") == project:
            candidates.append((meta, d))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0]["started_at"], reverse=True)
    return candidates[0]


def load_recent_ops(session_dir: Path, n: int = 10) -> list[dict]:
    """加载最近 n 条操作（不论是否压缩）"""
    ops_file = session_dir / "ops.jsonl"
    if not ops_file.exists():
        return []
    all_ops = []
    with open(ops_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                all_ops.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return all_ops[-n:]


def load_summary(session_dir: Path) -> str:
    summary_file = session_dir / "summary.md"
    if not summary_file.exists():
        return ""
    with open(summary_file, encoding="utf-8") as f:
        content = f.read()
    # 只取最后一个摘要块（--- 分隔）
    blocks = content.split("---")
    return blocks[-1].strip() if blocks else content.strip()


def detect_completion_status(meta: dict, session_dir: Path) -> tuple[bool, str]:
    """
    自动识别任务是否完成。
    判断依据：里程碑数量 vs 操作总数的比例。
    - 里程碑比例 > 30% 且最后操作是 milestone → 认为已完成
    - 否则认为未完成

    Returns:
        (is_complete, status_desc)
    """
    op_count = meta.get("op_count", 0)
    last_milestone = meta.get("last_milestone", "")

    # 统计里程碑数量
    milestone_count = 0
    last_op_type = ""
    ops_file = session_dir / "ops.jsonl"
    if ops_file.exists():
        with open(ops_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    op = json.loads(line)
                    if op.get("type") == "milestone" or "milestone" in op.get("tags", []):
                        milestone_count += 1
                    last_op_type = op.get("type", "")
                except json.JSONDecodeError:
                    continue

    if op_count == 0:
        return False, "未开始"

    milestone_ratio = milestone_count / max(op_count, 1)

    if milestone_ratio > 0.3 and last_op_type == "milestone":
        return True, f"已完成（{milestone_count} 个里程碑，共 {op_count} 步操作）"
    elif milestone_count > 0:
        return False, f"进行中（已达成 {milestone_count} 个里程碑，共 {op_count} 步）"
    else:
        return False, f"进行中（共 {op_count} 步操作，暂无里程碑）"


def generate_natural_language_summary(
    project: str,
    started_at: str,
    last_milestone: str,
    is_complete: bool,
    status_desc: str,
    recent_ops: list[dict],
) -> str:
    """
    生成 50 字以内的自然语言恢复提示（中文）。
    """
    date_str = started_at[:10]

    if last_milestone:
        action = last_milestone[:20]
    elif recent_ops:
        action = recent_ops[-1].get("summary", "进行相关操作")[:20]
    else:
        action = "进行操作"

    if is_complete:
        return f"上次（{date_str}）在 {project} 中完成了{action}，任务已结束。"
    else:
        return f"上次（{date_str}）在 {project} 中进行了{action}，尚未完成。"


def generate_continuation_advice(
    is_complete: bool,
    last_milestone: str,
    recent_ops: list[dict],
    summary_content: str,
) -> str:
    """
    根据完成状态生成继续建议或下阶段建议。
    """
    # 从 summary 中提取"下一步建议"
    next_step = ""
    if summary_content:
        for line in summary_content.split("\n"):
            if "下一步建议" in line or "💡" in line:
                continue
            if line.startswith("- ") and next_step == "":
                # 取"下一步建议"区块下的第一条
                pass
        # 简单提取：找到 💡 区块后的第一个 - 开头的行
        lines = summary_content.split("\n")
        in_next_section = False
        for line in lines:
            if "下一步建议" in line or "💡" in line:
                in_next_section = True
                continue
            if in_next_section and line.startswith("- "):
                next_step = line[2:].strip()
                break
            if in_next_section and line.startswith("##"):
                break

    if is_complete:
        if last_milestone:
            return f"上阶段已完成：{last_milestone[:30]}。建议开启新阶段或确认验收。"
        return "上次任务已完成，建议进行收尾验证或开启新阶段。"
    else:
        if next_step:
            return f"建议继续：{next_step[:40]}"
        if recent_ops:
            last = recent_ops[-1]
            op_type = last.get("type", "")
            summary = last.get("summary", "")[:30]
            if op_type == "error":
                return f"上次遇到错误：{summary}，建议先排查此问题。"
            elif op_type == "file_write":
                return f"上次写入了文件，建议运行测试验证结果。"
            elif op_type == "bash_exec":
                return f"上次执行了命令，建议确认结果后继续。"
            else:
                return f"建议从上次中断处继续：{summary}"
        return "建议回顾摘要后继续未完成的任务。"


def restore(project: str, verbose: bool = False):
    result = find_latest_session(project)
    if not result:
        print(f"[ultra-memory] 未找到项目 '{project}' 的历史会话，将从头开始")
        return

    meta, session_dir = result
    session_id = meta["session_id"]
    started_at = meta["started_at"][:10]
    op_count = meta.get("op_count", 0)
    last_milestone = meta.get("last_milestone", "")

    # 检测任务完成状态
    is_complete, status_desc = detect_completion_status(meta, session_dir)

    # 加载摘要和最近操作
    summary = load_summary(session_dir)
    recent_ops = load_recent_ops(session_dir, n=5)

    # 生成自然语言总结（50字内）
    nl_summary = generate_natural_language_summary(
        project, started_at, last_milestone, is_complete, status_desc, recent_ops
    )

    # 生成继续建议
    advice = generate_continuation_advice(is_complete, last_milestone, recent_ops, summary)

    # 输出恢复上下文
    print(f"\n[ULTRA-MEMORY RESTORE] 找到上次会话：")
    print(f"  会话 ID : {session_id}")
    print(f"  项目    : {project}")
    print(f"  时间    : {started_at}")
    print(f"  操作数  : {op_count} 条")
    print(f"  状态    : {status_desc}")
    if last_milestone:
        print(f"  最后里程碑: {last_milestone}")

    # 自然语言总结（供 Claude 直接注入 context）
    print(f"\n💬 {nl_summary}")

    # 展示摘要关键部分
    if summary:
        print(f"\n--- 上次会话摘要（关键部分）---")
        for line in summary.split("\n"):
            if any(kw in line for kw in ["##", "✅", "🔄", "⚠️", "🔑", "💡"]):
                print(line)
            elif line.startswith("- ") and len(line) < 100:
                print(f"  {line}")
        print("---")

    # 最近操作（verbose 模式或未完成时显示）
    if recent_ops and (verbose or not is_complete):
        print(f"\n最近 {len(recent_ops)} 条操作：")
        for op in recent_ops:
            ts = op["ts"][11:16]
            marker = "✅" if op["type"] == "milestone" else "  "
            print(f"  {marker} [{ts}] #{op['seq']} {op['type']}: {op['summary'][:60]}")

    # 继续建议
    print(f"\n📌 {advice}")

    print(f"\n[ultra-memory] ✅ 上下文恢复完成")
    print(f"[ultra-memory] SESSION_ID={session_id}")
    print(f"[ultra-memory] TASK_STATUS={'complete' if is_complete else 'in_progress'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="恢复上次会话上下文")
    parser.add_argument("--project", default="default", help="项目名称")
    parser.add_argument("--verbose", action="store_true", help="显示详细操作记录")
    args = parser.parse_args()
    restore(args.project, args.verbose)
