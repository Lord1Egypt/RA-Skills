#!/usr/bin/env python3
"""
skill-test-generate: Helper script for agent-driven test case generation.

This script does NOT perform semantic test generation.
Instead, it provides utility subcommands for the Agent workflow:

  prepare  — Resolve skill path, list files, extract SKILL.md metadata
  validate — Validate output JSON format, check source_refs, auto-generate summary, add verified flag

Usage:
  python scripts/generate.py prepare --skill <target>
  python scripts/generate.py validate --file <json_path>
"""

import sys
import os
import json
import re
import zipfile
import tempfile
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone


# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────

SKILL_MD_FILENAME = "SKILL.md"

# Skill directories to search for installed skills
# Covers: WorkBuddy, OpenDesk, and common locations
SKILL_SEARCH_DIRS = []
_home = Path.home()
# WorkBuddy user-level skills
_wb_skills = _home / ".workbuddy" / "skills"
if _wb_skills.exists():
    SKILL_SEARCH_DIRS.append(_wb_skills)
# OpenDesk skills (Windows)
_od_skills_win = Path(os.environ.get("APPDATA", "")) / "fillipdesk" / "skills"
if _od_skills_win.exists():
    SKILL_SEARCH_DIRS.append(_od_skills_win)
# OpenDesk skills (macOS)
_od_skills_mac = _home / "Library" / "Application Support" / "fillipdesk" / "skills"
if _od_skills_mac.exists():
    SKILL_SEARCH_DIRS.append(_od_skills_mac)


# ─────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────

def parse_frontmatter(raw: str) -> dict:
    """Parse YAML frontmatter from SKILL.md content (simple parser, no external deps)."""
    if not raw or not raw.strip():
        return {}
    trimmed = raw.strip()
    if not trimmed.startswith("---"):
        return {}
    end = trimmed.find("\n---", 3)
    if end == -1:
        return {}
    fm_raw = trimmed[3:end].strip()
    result = {}
    for line in fm_raw.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r'^(\w[\w-]*)\s*:\s*(.+)$', line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            # Simple value parsing
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            elif val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.isdigit():
                val = int(val)
            result[key] = val
    return result


def list_skill_files(skill_dir: str) -> list:
    """List all files in a skill directory with relative paths and sizes."""
    files = []
    root = Path(skill_dir)
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            # Skip common non-essential files
            if rel.startswith(".") or rel.endswith(".zip"):
                continue
            files.append({
                "path": rel,
                "size": p.stat().st_size,
                "line_count": sum(1 for _ in open(p, encoding="utf-8", errors="replace")),
            })
    return files


def resolve_skill_path(target: str) -> dict:
    """Resolve a skill target to an absolute directory path.

    Supports:
      - installed:<name>  → search known skill directories
      - absolute/relative directory path
      - .zip file path (extract to temp dir)

    Returns: {"success": bool, "skill_path": str, "temp_dir": str|None, "error": str|None}
    """
    # Case 1: installed:<name>
    if target.startswith("installed:"):
        name = target[len("installed:"):]
        for search_dir in SKILL_SEARCH_DIRS:
            candidate = search_dir / name
            if candidate.is_dir() and (candidate / SKILL_MD_FILENAME).exists():
                return {
                    "success": True,
                    "skill_path": str(candidate.resolve()),
                    "temp_dir": None,
                    "error": None,
                }
        return {
            "success": False,
            "skill_path": None,
            "temp_dir": None,
            "error": f"未找到已安装的 Skill: {name}（搜索了 {len(SKILL_SEARCH_DIRS)} 个目录）",
        }

    # Case 2: zip file
    target_path = Path(target).resolve()
    if target_path.suffix.lower() == ".zip":
        if not target_path.exists():
            return {
                "success": False,
                "skill_path": None,
                "temp_dir": None,
                "error": f"zip 文件不存在: {target}",
            }
        temp_dir = tempfile.mkdtemp(prefix="skill-test-gen-")
        try:
            with zipfile.ZipFile(str(target_path), "r") as zf:
                zf.extractall(temp_dir)
            # Find SKILL.md in extracted content
            for root, dirs, files in os.walk(temp_dir):
                if SKILL_MD_FILENAME in files:
                    return {
                        "success": True,
                        "skill_path": root,
                        "temp_dir": temp_dir,
                        "error": None,
                    }
            # If SKILL.md is at the root of the zip
            if (Path(temp_dir) / SKILL_MD_FILENAME).exists():
                return {
                    "success": True,
                    "skill_path": temp_dir,
                    "temp_dir": temp_dir,
                    "error": None,
                }
            shutil.rmtree(temp_dir, ignore_errors=True)
            return {
                "success": False,
                "skill_path": None,
                "temp_dir": None,
                "error": f"zip 中未找到 {SKILL_MD_FILENAME}",
            }
        except zipfile.BadZipFile:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return {
                "success": False,
                "skill_path": None,
                "temp_dir": None,
                "error": f"无效的 zip 文件: {target}",
            }

    # Case 3: directory path
    if target_path.is_dir():
        if not (target_path / SKILL_MD_FILENAME).exists():
            return {
                "success": False,
                "skill_path": None,
                "temp_dir": None,
                "error": f"目录中未找到 {SKILL_MD_FILENAME}: {target}",
            }
        return {
            "success": True,
            "skill_path": str(target_path),
            "temp_dir": None,
            "error": None,
        }

    return {
        "success": False,
        "skill_path": None,
        "temp_dir": None,
        "error": f"目标不存在或不是有效的 Skill 路径: {target}",
    }


# ─────────────────────────────────────────────
# prepare subcommand
# ─────────────────────────────────────────────

def cmd_prepare(args):
    """Resolve skill path, list files, extract SKILL.md metadata."""
    result = resolve_skill_path(args.skill)
    if not result["success"]:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    skill_path = result["skill_path"]
    skill_md_path = Path(skill_path) / SKILL_MD_FILENAME

    # Read and parse SKILL.md
    skill_md_content = skill_md_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(skill_md_content)

    # List files (with line counts for source_refs validation)
    files = list_skill_files(skill_path)

    # Build file index for quick lookup: path → {size, line_count}
    file_index = {}
    for f in files:
        file_index[f["path"]] = f

    output = {
        "success": True,
        "skill_name": frontmatter.get("name", ""),
        "skill_path": skill_path,
        "temp_dir": result["temp_dir"],
        "frontmatter": frontmatter,
        "files": files,
        "file_count": len(files),
        "file_index": file_index,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


# ─────────────────────────────────────────────
# validate subcommand
# ─────────────────────────────────────────────

def validate_json(data: dict, skill_path: str = None) -> list:
    """Validate the output JSON structure. Returns a list of error strings.

    If skill_path is provided, also validates source_refs against actual files.
    """
    errors = []

    # ── Top-level required fields ──
    for field in ["schema_version", "generated_at", "skill", "test_suites"]:
        if field not in data:
            errors.append(f"缺少顶层必填字段: {field}")

    if errors:
        return errors  # Can't validate further without basic structure

    # ── schema_version ──
    if data.get("schema_version") != "1.0":
        errors.append(f"schema_version 必须为 '1.0'，当前为: {data.get('schema_version')}")

    # ── generated_at (basic format check) ──
    gen_at = data.get("generated_at", "")
    if not gen_at or not isinstance(gen_at, str):
        errors.append("generated_at 必须为非空字符串")
    elif not re.match(r"^\d{4}-\d{2}-\d{2}T", gen_at):
        errors.append(f"generated_at 格式应为 ISO 8601，当前为: {gen_at}")

    # ── skill object ──
    skill = data.get("skill", {})
    if not isinstance(skill, dict):
        errors.append("skill 必须为对象")
    else:
        for field in ["name", "description", "source_path", "capabilities"]:
            if field not in skill:
                errors.append(f"skill 缺少必填字段: {field}")
        caps = skill.get("capabilities", [])
        if not isinstance(caps, list) or len(caps) == 0:
            errors.append("skill.capabilities 必须为非空数组")
        for i, c in enumerate(caps):
            if not isinstance(c, str) or not c.strip():
                errors.append(f"skill.capabilities[{i}] 必须为非空字符串")

    # ── Resolve skill_path for source_refs validation ──
    # Priority: explicit skill_path arg > skill.source_path in JSON
    effective_skill_path = skill_path
    if not effective_skill_path:
        sp = data.get("skill", {}).get("source_path", "")
        if sp and Path(sp).is_dir():
            effective_skill_path = sp

    # Build file line-count map for source_refs validation
    file_line_map = {}  # {relative_path: total_line_count}
    if effective_skill_path:
        skill_root = Path(effective_skill_path)
        for p in sorted(skill_root.rglob("*")):
            if p.is_file():
                rel = p.relative_to(skill_root).as_posix()
                if rel.startswith(".") or rel.endswith(".zip"):
                    continue
                try:
                    line_count = sum(1 for _ in open(p, encoding="utf-8", errors="replace"))
                    file_line_map[rel] = line_count
                except Exception:
                    pass

    # ── test_suites array ──
    suites = data.get("test_suites", [])
    if not isinstance(suites, list):
        errors.append("test_suites 必须为数组")
    elif len(suites) == 0:
        errors.append("test_suites 不能为空数组")
    else:
        all_case_ids = set()
        for si, suite in enumerate(suites):
            suite_label = f"test_suites[{si}]"

            # Suite required fields
            for field in ["suite_id", "name", "description", "cases"]:
                if field not in suite:
                    errors.append(f"{suite_label} 缺少必填字段: {field}")

            # suite_id format
            sid = suite.get("suite_id", "")
            if not re.match(r"^TS-\d{2}$", str(sid)):
                errors.append(
                    f"{suite_label}.suite_id 格式应为 TS-XX，当前为: {sid}\n"
                    f"    → 修正方法: 使用两位数字编号，如 TS-01, TS-02"
                )

            # cases array
            cases = suite.get("cases", [])
            if not isinstance(cases, list):
                errors.append(f"{suite_label}.cases 必须为数组")
            elif len(cases) == 0:
                errors.append(f"{suite_label}.cases 不能为空数组")
            else:
                for ci, case in enumerate(cases):
                    case_label = f"{suite_label}.cases[{ci}]"
                    cid_display = case.get("case_id", f"(未设置)")

                    # Case required fields
                    for field in ["case_id", "title", "scenario", "user_input", "source_refs"]:
                        if field not in case:
                            errors.append(
                                f"{case_label} (case_id={cid_display}) 缺少必填字段: {field}\n"
                                f"    → 修正方法: 在该 case 中添加 \"{field}\" 字段"
                            )

                    # case_id format and uniqueness
                    cid = case.get("case_id", "")
                    if cid and not re.match(r"^TC-\d{2}-\d{3}$", str(cid)):
                        errors.append(
                            f"{case_label}.case_id 格式应为 TC-XX-YYY，当前为: {cid}\n"
                            f"    → 修正方法: 使用 TS 编号 + 三位序号，如 TC-01-001, TC-02-003"
                        )
                    if cid:
                        if cid in all_case_ids:
                            errors.append(
                                f"{case_label}.case_id 重复: {cid}\n"
                                f"    → 修正方法: 确保 case_id 全局唯一，检查其他 suite 中是否已使用"
                            )
                        all_case_ids.add(cid)

                    # source_refs validation
                    source_refs = case.get("source_refs")
                    if source_refs is not None:
                        if not isinstance(source_refs, list) or len(source_refs) == 0:
                            errors.append(
                                f"{case_label} (case_id={cid_display}).source_refs 必须为非空数组\n"
                                f"    → 修正方法: 添加至少一个溯源引用，如 [{{\"file\": \"SKILL.md\", \"lines\": [1, 10]}}]"
                            )
                        else:
                            for ri, ref in enumerate(source_refs):
                                ref_label = f"{case_label}.source_refs[{ri}]"

                                # file field
                                ref_file = ref.get("file", "")
                                if not isinstance(ref_file, str) or not ref_file.strip():
                                    errors.append(
                                        f"{ref_label} (case_id={cid_display}).file 必须为非空字符串\n"
                                        f"    → 修正方法: 填写目标 Skill 中的文件相对路径，如 \"SKILL.md\" 或 \"scripts/handler.py\""
                                    )
                                elif file_line_map:
                                    # Validate file existence
                                    if ref_file not in file_line_map:
                                        # Try with backslash replacement (Windows path compat)
                                        alt_file = ref_file.replace("\\", "/")
                                        if alt_file in file_line_map:
                                            pass  # Found with forward slashes
                                        else:
                                            available = sorted(file_line_map.keys())
                                            errors.append(
                                                f"{ref_label} (case_id={cid_display}).file 引用的文件不存在: \"{ref_file}\"\n"
                                                f"    → 修正方法: 文件必须在目标 Skill 目录中存在。可用文件列表:\n"
                                                f"      {', '.join(available)}"
                                            )

                                # lines field
                                ref_lines = ref.get("lines")
                                if not isinstance(ref_lines, list) or len(ref_lines) != 2:
                                    errors.append(
                                        f"{ref_label} (case_id={cid_display}).lines 必须为恰好包含 2 个整数的数组 [start, end]\n"
                                        f"    → 修正方法: 如 [10, 25] 表示第 10 到 25 行（含两端）"
                                    )
                                else:
                                    start, end = ref_lines
                                    if not isinstance(start, int) or not isinstance(end, int):
                                        errors.append(
                                            f"{ref_label} (case_id={cid_display}).lines 的元素必须为整数，当前为: [{start}, {end}]"
                                        )
                                    elif start < 1 or end < 1:
                                        errors.append(
                                            f"{ref_label} (case_id={cid_display}).lines 行号从 1 开始，当前为: [{start}, {end}]\n"
                                            f"    → 修正方法: 确保行号 ≥ 1"
                                        )
                                    elif start > end:
                                        errors.append(
                                            f"{ref_label} (case_id={cid_display}).lines start({start}) > end({end})，不合法\n"
                                            f"    → 修正方法: 确保 start ≤ end，如 [10, 25]"
                                        )
                                    elif ref_file and file_line_map and ref_file in file_line_map:
                                        max_line = file_line_map[ref_file]
                                        if end > max_line:
                                            errors.append(
                                                f"{ref_label} (case_id={cid_display}).lines end({end}) 超出文件 \"{ref_file}\" 的总行数({max_line})\n"
                                                f"    → 修正方法: end 行号不能超过文件总行数 {max_line}"
                                            )
                                    elif ref_file and file_line_map:
                                        alt_file = ref_file.replace("\\", "/")
                                        if alt_file in file_line_map:
                                            max_line = file_line_map[alt_file]
                                            if end > max_line:
                                                errors.append(
                                                    f"{ref_label} (case_id={cid_display}).lines end({end}) 超出文件 \"{ref_file}\" 的总行数({max_line})\n"
                                                    f"    → 修正方法: end 行号不能超过文件总行数 {max_line}"
                                                )

    return errors


def generate_summary(data: dict) -> dict:
    """Generate summary from test_suites data."""
    suites = data.get("test_suites", [])
    total_suites = len(suites)
    total_cases = 0

    for suite in suites:
        cases = suite.get("cases", [])
        total_cases += len(cases)

    return {
        "total_suites": total_suites,
        "total_cases": total_cases,
    }


def cmd_validate(args):
    """Validate output JSON, check source_refs, auto-generate summary, add verified flag."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    # Optional: resolve skill path for source_refs validation
    skill_path = getattr(args, "skill", None)

    errors = validate_json(data, skill_path=skill_path)

    if errors:
        print("❌ 验证失败，以下问题需要修正：", file=sys.stderr)
        print("", file=sys.stderr)
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}", file=sys.stderr)
            print("", file=sys.stderr)
        print(f"共 {len(errors)} 个错误。请根据上述提示修正 JSON 文件后重新运行验证。", file=sys.stderr)
        sys.exit(1)

    # Validation passed: generate summary and add verified flag
    summary = generate_summary(data)
    data["summary"] = summary
    data["verified"] = True

    # Write back
    file_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"✅ 验证通过！", file=sys.stderr)
    print(f"  测试套件: {summary['total_suites']}", file=sys.stderr)
    print(f"  测试用例: {summary['total_cases']}", file=sys.stderr)
    print(f"  已写入 summary 和 verified 字段", file=sys.stderr)


# ─────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="skill-test-generate 辅助脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # prepare
    prep = subparsers.add_parser("prepare", help="解析 Skill 路径、列出文件、提取 SKILL.md 元数据")
    prep.add_argument("--skill", required=True, help="目标 Skill（installed:<name> / 目录路径 / zip 文件路径）")

    # validate
    val = subparsers.add_parser("validate", help="验证输出 JSON 格式，校验 source_refs，自动生成 summary，添加 verified 标记")
    val.add_argument("--file", required=True, help="输出 JSON 文件路径")
    val.add_argument("--skill", required=False, help="（可选）目标 Skill 路径，用于校验 source_refs 中的文件和行号。如未指定则从 JSON 的 skill.source_path 推断")

    args = parser.parse_args()

    if args.command == "prepare":
        cmd_prepare(args)
    elif args.command == "validate":
        cmd_validate(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
