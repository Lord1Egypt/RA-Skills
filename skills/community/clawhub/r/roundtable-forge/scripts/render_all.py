#!/usr/bin/env python3
"""roundtable-forge render-all orchestrator (v2.8.0+).

读取 Memory JSON，按 `metadata.output_formats`（plural，优先）或
`metadata.output_format`（singular，回退）或默认 `["minutes"]` 解析出输出格式列表，
再读取 `metadata.output_artifacts`，按顺序调用格式与附属产物 renderer。

用法:
    python3 render_all.py <memory.json> [--output-dir <dir>] \
      [--formats minutes,podcast] [--artifacts argument_graph]

参数:
    memory.json           Memory 事实源（必填）
    --output-dir <dir>    输出目录，默认 <memory.json 同级>
    --formats <list>      显式覆盖 output_formats，逗号分隔（如 "minutes,podcast"）
    --artifacts <list>    显式覆盖 output_artifacts，逗号分隔

退出码:
    0 全部成功
    1 任何 renderer 失败
    2 任何格式无法识别
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

FORMAT_TO_RENDERER = {
    "minutes": SCRIPT_DIR / "render_memory_to_markdown.py",
    "podcast": SCRIPT_DIR / "render_memory_to_podcast_script.py",
}

ARTIFACT_TO_RENDERER = {
    "argument_graph": SCRIPT_DIR / "render_memory_to_argument_graph.py",
}
MEMORY_LINTER = SCRIPT_DIR / "lint_memory.py"


def resolve_formats(memory: dict, override: list[str] | None) -> list[str]:
    """按优先级解析有效输出格式列表。

    优先级：override（CLI）> metadata.output_formats（plural）>
            metadata.output_format（singular）> ["minutes"]（默认）
    """
    if override:
        return override

    metadata = memory.get("metadata", {}) or {}
    plural = metadata.get("output_formats")
    if isinstance(plural, list) and plural:
        return list(plural)

    singular = metadata.get("output_format")
    if isinstance(singular, str) and singular:
        return [singular]

    return ["minutes"]


def validate_formats(formats: list[str]) -> tuple[list[str], list[str]]:
    """校验格式名，把合法的和不合法的分开。"""
    valid, invalid = [], []
    for fmt in formats:
        if fmt in FORMAT_TO_RENDERER:
            valid.append(fmt)
        else:
            invalid.append(fmt)
    return valid, invalid


def resolve_artifacts(memory: dict, override: list[str] | None) -> list[str]:
    """解析附属产物；CLI 覆盖优先，缺失字段表示不生成附属产物。"""
    if override is not None:
        return override
    metadata = memory.get("metadata", {}) or {}
    artifacts = metadata.get("output_artifacts")
    if isinstance(artifacts, list):
        return list(artifacts)
    return []


def validate_artifacts(artifacts: list[str]) -> tuple[list[str], list[str]]:
    """校验附属产物名，把合法的和不合法的分开。"""
    valid, invalid = [], []
    for artifact in artifacts:
        if artifact in ARTIFACT_TO_RENDERER:
            valid.append(artifact)
        else:
            invalid.append(artifact)
    return valid, invalid


def run_renderer(renderer: Path, memory_path: Path, output_path: Path) -> tuple[int, str]:
    """调用子 renderer，返回 (returncode, stderr)。"""
    result = subprocess.run(
        ["python3", str(renderer), str(memory_path), "--output", str(output_path)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stderr


def preflight_memory(memory_path: Path) -> tuple[int, str]:
    """附属产物渲染前执行完整 Memory lint，避免输出不完整图谱。"""
    result = subprocess.run(
        [sys.executable, str(MEMORY_LINTER), str(memory_path)],
        capture_output=True,
        text=True,
    )
    detail = "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip()
    )
    return result.returncode, detail


def main() -> int:
    parser = argparse.ArgumentParser(description="Render one Memory JSON into multiple formats.")
    parser.add_argument("memory", type=Path, help="Path to Memory JSON file.")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Output directory. Defaults to the Memory file's directory.")
    parser.add_argument("--formats", type=str, default=None,
                        help="Override output_formats, comma-separated (e.g. 'minutes,podcast').")
    parser.add_argument("--artifacts", type=str, default=None,
                        help="Override output_artifacts, comma-separated (e.g. 'argument_graph').")
    args = parser.parse_args()

    if not args.memory.exists():
        print(f"ERROR: Memory file not found: {args.memory}", file=sys.stderr)
        return 1

    try:
        memory = json.loads(args.memory.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {args.memory}: {e}", file=sys.stderr)
        return 1

    override = None
    if args.formats:
        override = [s.strip() for s in args.formats.split(",") if s.strip()]
    artifact_override = None
    if args.artifacts is not None:
        artifact_override = [
            s.strip() for s in args.artifacts.split(",") if s.strip()
        ]

    formats = resolve_formats(memory, override)
    valid, invalid = validate_formats(formats)
    if invalid:
        print(f"ERROR: unknown format(s): {invalid}. Valid: {list(FORMAT_TO_RENDERER)}",
              file=sys.stderr)
        return 2

    artifacts = resolve_artifacts(memory, artifact_override)
    valid_artifacts, invalid_artifacts = validate_artifacts(artifacts)
    if invalid_artifacts:
        print(
            f"ERROR: unknown artifact(s): {invalid_artifacts}. "
            f"Valid: {list(ARTIFACT_TO_RENDERER)}",
            file=sys.stderr,
        )
        return 2

    if valid_artifacts:
        lint_rc, lint_detail = preflight_memory(args.memory)
        if lint_rc != 0:
            print(
                "ERROR: Memory lint failed; declared artifacts were not rendered.",
                file=sys.stderr,
            )
            if lint_detail:
                print(lint_detail, file=sys.stderr)
            return 1

    output_dir = args.output_dir or args.memory.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    base = args.memory.stem
    suffix_map = {"minutes": ".md", "podcast": ".podcast.md"}
    artifact_suffix_map = {"argument_graph": ".argument-graph.md"}
    overall_ok = True

    print(f"Resolved formats: {valid}")
    for fmt in valid:
        renderer = FORMAT_TO_RENDERER[fmt]
        suffix = suffix_map.get(fmt, f".{fmt}.md")
        output_path = output_dir / f"{base}{suffix}"
        print(f"  [{fmt}] {renderer.name} -> {output_path.name} ... ", end="", flush=True)
        rc, stderr = run_renderer(renderer, args.memory, output_path)
        if rc == 0:
            print("OK")
        else:
            print(f"FAILED (rc={rc})")
            if stderr:
                print(f"    stderr: {stderr.strip()}", file=sys.stderr)
            overall_ok = False

    print(f"Resolved artifacts: {valid_artifacts}")
    for artifact in valid_artifacts:
        renderer = ARTIFACT_TO_RENDERER[artifact]
        suffix = artifact_suffix_map.get(artifact, f".{artifact}.md")
        output_path = output_dir / f"{base}{suffix}"
        print(
            f"  [{artifact}] {renderer.name} -> {output_path.name} ... ",
            end="",
            flush=True,
        )
        rc, stderr = run_renderer(renderer, args.memory, output_path)
        if rc == 0:
            print("OK")
        else:
            print(f"FAILED (rc={rc})")
            if stderr:
                print(f"    stderr: {stderr.strip()}", file=sys.stderr)
            overall_ok = False

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
