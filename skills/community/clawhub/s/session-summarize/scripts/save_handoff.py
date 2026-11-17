#!/usr/bin/env python3
"""Validate and atomically persist a task-bound summarize handoff."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

REPORT_METADATA = re.compile(r"\A<!-- summarize-handoff schema=2 (?P<json>\{.*\}) -->\r?\n")
POINTER_METADATA = re.compile(r"\A<!-- summarize-pointer schema=1 (?P<json>\{.*\}) -->\r?\n")
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b", re.I),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?im)^\s*(?:authorization\s*:\s*bearer|(?:api[_-]?key|access[_-]?token|password)\s*[:=])\s*\S+"),
    re.compile(r"(?im)^\s*(?:cookie|set-cookie)\s*:\s*\S+"),
    re.compile(r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^\s:@]+:[^\s@]+@", re.I),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
)
RAW_DIALOGUE_PATTERNS = (
    re.compile(r"<\|(?:im_start|user|assistant)\|>"),
    re.compile(r"(?m)^\s*(?:tool_call|response_item)\s*[:=]"),
)


def parse_metadata(text: str) -> tuple[dict[str, str] | None, list[str]]:
    match = REPORT_METADATA.match(text)
    if not match:
        return None, ["缺少或格式错误的 schema=2 summarize-handoff 元数据"]
    try:
        metadata = json.loads(match.group("json"))
    except json.JSONDecodeError as exc:
        return None, [f"交接元数据不是有效 JSON：{exc}"]
    required = ("created_at", "task_id", "project_root", "branch", "head", "goal_digest")
    errors = [f"交接元数据缺少 {key}" for key in required if not metadata.get(key)]
    if metadata.get("created_at") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", str(metadata["created_at"])):
        errors.append("created_at 必须是 UTC ISO-8601 时间")
    if metadata.get("task_id") and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}", str(metadata["task_id"])):
        errors.append("task_id 含有不安全字符或长度超限")
    if metadata.get("goal_digest") and not re.fullmatch(r"[a-f0-9]{12,64}", str(metadata["goal_digest"]), re.I):
        errors.append("goal_digest 必须是十六进制摘要")
    return metadata, errors


def validate_text(text: str, *, allow_legacy: bool = False) -> list[str]:
    errors: list[str] = []
    metadata, metadata_errors = parse_metadata(text)
    if metadata_errors and allow_legacy:
        if text.startswith("<!-- summarize-handoff schema=1 "):
            metadata_errors = []
    errors.extend(metadata_errors)
    if len(text.encode("utf-8")) > 128 * 1024:
        errors.append("交接报告超过 128 KiB 上限")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append("检测到疑似密钥、令牌、密码或个人信息")
            break
    if any(pattern.search(text) for pattern in RAW_DIALOGUE_PATTERNS):
        errors.append("检测到原始对话或工具转储标记；请先提炼交接内容")
    return errors


def acquire_lock(lock: Path) -> int:
    try:
        return os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise RuntimeError(f"保存锁已存在：{lock}；不要覆盖另一会话的交接报告") from exc


def reject_reparse_point(path: Path, label: str) -> None:
    is_junction = getattr(path, "is_junction", lambda: False)()
    if path.is_symlink() or is_junction:
        raise RuntimeError(f"{label} 不能是 symlink 或 junction：{path}")


def atomic_write(text: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, prefix=f".{output.name}.", delete=False) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def pointer_text(metadata: dict[str, str], report_path: str) -> str:
    pointer = {
        "task_id": metadata["task_id"],
        "report": report_path,
        "created_at": metadata["created_at"],
        "project_root": metadata["project_root"],
        "branch": metadata["branch"],
        "head": metadata["head"],
        "goal_digest": metadata["goal_digest"],
    }
    return f"<!-- summarize-pointer schema=1 {json.dumps(pointer, ensure_ascii=False, separators=(',', ':'))} -->\n\n# 最新交接\n\n报告：`.transfers/{report_path}`\n"


def atomic_save(text: str, output: Path) -> tuple[Path, Path]:
    if output.name != "latest.md" or output.parent.name != ".transfers":
        raise RuntimeError("输出必须是项目 .transfers/latest.md")
    metadata, errors = parse_metadata(text)
    if errors or metadata is None:
        raise RuntimeError("；".join(errors))
    task_id = str(metadata["task_id"])
    handoffs = output.parent / "handoffs"
    timestamp = re.sub(r"[^A-Za-z0-9]+", "", str(metadata["created_at"]))
    report_name = f"{timestamp}-{task_id}.md"
    report = handoffs / report_name
    output.parent.mkdir(parents=True, exist_ok=True)
    handoffs.mkdir(parents=True, exist_ok=True)
    expected_output = (Path(str(metadata["project_root"])) / ".transfers" / "latest.md").resolve()
    if output.resolve() != expected_output:
        raise RuntimeError("输出路径必须位于交接元数据声明的 project_root/.transfers/latest.md")
    reject_reparse_point(output.parent, "交接目录")
    reject_reparse_point(handoffs, "handoffs 目录")
    lock = output.with_name(f"{output.name}.lock")
    descriptor = acquire_lock(lock)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(f"pid={os.getpid()}\n")
        if output.exists():
            shutil.copy2(output, output.with_name(f"{output.name}.bak"))
        if report.exists() and report.read_text(encoding="utf-8") != text:
            raise RuntimeError("相同 created_at 和 task_id 已存在不同报告；请生成新的 UTC 时间")
        atomic_write(text, report)
        atomic_write(pointer_text(metadata, f"handoffs/{report_name}"), output)
    finally:
        lock.unlink(missing_ok=True)
    return output, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and atomically save a task-bound summarize handoff.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.check_only and args.output:
        parser.error("--check-only 不能与 --output 一起使用")
    try:
        text = args.input.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"无法读取输入：{exc}", file=sys.stderr)
        return 2
    errors = validate_text(text)
    if errors:
        print("；".join(errors), file=sys.stderr)
        return 3
    if args.check_only:
        print("handoff validation passed")
        return 0
    if not args.output:
        parser.error("保存时必须提供 --output")
    try:
        latest, report = atomic_save(text, args.output)
    except (OSError, RuntimeError) as exc:
        print(f"保存失败：{exc}", file=sys.stderr)
        return 4
    print(f"saved: {latest.resolve()}")
    print(f"report: {report.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
