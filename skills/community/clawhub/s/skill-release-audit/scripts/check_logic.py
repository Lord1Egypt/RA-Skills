#!/usr/bin/env python3
"""
Module 1: Logic & Syntax Check
- Python: ast.parse syntax check
- Bash: bash -n syntax check
- Internal reference path validation (files referenced in SKILL.md that don't exist)
- Internal import/require resolution
"""

import ast
import os
import re
import subprocess
from pathlib import Path

from _common import is_bash_script
from i18n import t


def check_python_syntax(script_path: Path) -> list[dict]:
    issues = []
    try:
        source = script_path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(script_path))
    except SyntaxError as e:
        issues.append({
            "file": str(script_path.name),
            "line": e.lineno,
            "message": t("logic.py_syntax", msg=e.msg),
            "severity": "ERROR",
        })
    except Exception as e:
        issues.append({
            "file": str(script_path.name),
            "line": None,
            "message": t("logic.py_unparseable", err=e),
            "severity": "WARN",
        })
    return issues


def check_bash_syntax(script_path: Path) -> list[dict]:
    issues = []
    try:
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as e:
        issues.append({
            "file": str(script_path.name),
            "line": None,
            "message": t("logic.bash_check_fail", err=e),
            "severity": "WARN",
        })
        return issues
    if result.returncode != 0:
        for line in result.stderr.strip().splitlines():
            issues.append({
                "file": str(script_path.name),
                "line": None,
                "message": t("logic.bash_syntax", line=line),
                "severity": "ERROR",
            })
    return issues


def _is_runtime_external_ref(ref: str) -> bool:
    """True if the ref points outside the skill package (runtime environment path).

    Covers:
      - ~/... / ~user/...
      - $HOME/... / ${HOME}/... / other env-var-prefixed paths
      - absolute paths (/etc/..., C:\\..., ...)
    These are resolved at runtime in the *user's* environment, not inside the
    skill package, so their existence cannot be validated here. They are
    reported as INFO (when expanded path also missing) or silently skipped.
    """
    r = ref.strip()
    if r.startswith("~"):
        return True
    if r.startswith("$"):
        # $HOME/... or ${HOME}/...
        return True
    if r.startswith("/"):
        return True
    # Windows drive letters: C:\... or C:/...
    if len(r) >= 2 and r[0].isalpha() and r[1] == ":" and (r[2:3] in ("\\", "/")):
        return True
    return False


def _resolve_runtime_ref(ref: str) -> Path | None:
    """Best-effort expanduser()/expandvars() resolution for runtime paths."""
    r = ref.strip()
    if r.startswith("$"):
        # ${HOME}/x or $HOME/x -> $HOME
        r = re.sub(r"\$\{?HOME\}?", os.path.expanduser("~"), r)
    try:
        return Path(os.path.expandvars(os.path.expanduser(r)))
    except Exception:
        return None


def check_internal_paths(skill_dir: Path) -> list[dict]:
    """Check that file paths referenced in SKILL.md actually exist.

    Ref classification:
      1. Package-internal refs (scripts/, references/, assets/, bare relative
         paths) → must exist inside the skill dir; missing → WARN.
      2. Runtime external refs (~/, $HOME/, absolute paths) → outside the
         package, resolved in the user's environment at runtime. Not a package
         completeness problem even if absent (e.g. files generated on first
         run). If expanduser() resolves to an existing path → skip silently;
         otherwise emit INFO (not WARN) so the report stays honest without
         false-positive noise.
    """
    issues = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return issues

    content = skill_md.read_text(encoding="utf-8")
    # Match markdown links like [text](path) and bare paths like scripts/foo.py
    link_pattern = re.compile(r'\[.*?\]\(([^)#]+)\)')
    code_ref_pattern = re.compile(r'`([^`]+\.(?:py|sh|md|json|yaml|yml))`')

    for pattern in [link_pattern, code_ref_pattern]:
        for match in pattern.finditer(content):
            ref = match.group(1).strip()
            # Skip URLs
            if ref.startswith(("http://", "https://", "mailto:")):
                continue
            # Skip placeholders / globs, not real file references:
            #   <name>.json, {skill}/x.md, *.py, output/{id}.html
            if any(c in ref for c in "<>{}*"):
                continue

            # --- Runtime external paths: not package refs ---
            if _is_runtime_external_ref(ref):
                resolved = _resolve_runtime_ref(ref)
                if resolved is not None and resolved.exists():
                    continue  # exists in this environment — nothing to report
                issues.append({
                    "file": "SKILL.md",
                    "line": None,
                    "message": t("logic.runtime_external_ref", ref=ref),
                    "severity": "INFO",
                })
                continue

            # --- Package-internal reference ---
            # 搜索顺序：① skill 根下原样路径；② scripts/ 下同名文件（SKILL.md 惯例
            # 常用裸文件名指代 scripts/ 里的脚本）；③ references/ 下同名文件。
            # 命中任一即视为存在——检查器是保守验证存在性，不是路径拼写裁判。
            # 另：`bash xxx.sh` 这类反引号内嵌命令的写法，取末段文件名再搜，
            # 避免把命令前缀（bash/ python3 等）误当路径段。
            ref_path = skill_dir / ref
            if not ref_path.exists():
                stem = ref.split('/')[-1]
                # 命令式引用（如 `bash sync.sh`）：末段可能仍含命令前缀，
                # 取空格分隔后的最后一个 token 作为候选文件名
                token = stem.split(' ')[-1] if ' ' in stem else stem
                for sub in ("", "scripts", "references"):
                    candidate = skill_dir / sub / token if sub else skill_dir / token
                    if candidate.exists():
                        ref_path = candidate
                        break
            if not ref_path.exists():
                issues.append({
                    "file": "SKILL.md",
                    "line": None,
                    "message": t("logic.missing_ref", ref=ref),
                    "severity": "WARN",
                })
    return issues


def check_internal_imports(skill_dir: Path) -> list[dict]:
    """Check that Python scripts importing local modules can find them."""
    issues = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return issues

    py_files = list(scripts_dir.glob("*.py"))
    local_modules = {f.stem for f in py_files}

    for py_file in py_files:
        try:
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except Exception:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom) and node.module:
                    module_name = node.module.split(".")[0]
                    # Only flag if it looks like a local relative import
                    if node.level > 0 and module_name and module_name not in local_modules:
                        issues.append({
                            "file": py_file.name,
                            "line": node.lineno,
                            "message": t("logic.import_not_found", module=module_name),
                            "severity": "WARN",
                        })
    return issues


def check_todo_leftovers(skill_dir: Path) -> list[dict]:
    """Flag TODO/FIXME/HACK/XXX leftovers in non-script files and SKILL.md.
    Skips scripts/ (checker code legitimately contains these as pattern strings)
    and references/ (docs may use them as examples).
    Only scans SKILL.md and assets/.
    """
    issues = []
    # Strict pattern: only in meaningful user-facing files
    patterns = re.compile(r'\b(TODO|FIXME|HACK|XXX)\b')
    # Only scan SKILL.md — skip scripts/ and references/ entirely
    scan_targets = [skill_dir / "SKILL.md"]
    # Also scan assets/ if present
    assets_dir = skill_dir / "assets"
    if assets_dir.exists():
        scan_targets.extend(f for f in assets_dir.rglob("*") if f.is_file())

    for f in scan_targets:
        if not f.exists() or not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            for i, line in enumerate(text.splitlines(), 1):
                if patterns.search(line):
                    issues.append({
                        "file": str(f.relative_to(skill_dir)),
                        "line": i,
                        "message": t("logic.leftover_marker", line=line.strip()[:80]),
                        "severity": "WARN",
                    })
        except Exception:
            continue
    return issues


def run(skill_dir: Path) -> dict:
    issues = []
    scripts_dir = skill_dir / "scripts"

    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if not script.is_file():
                continue
            if script.suffix == ".py":
                issues.extend(check_python_syntax(script))
            elif is_bash_script(script):
                issues.extend(check_bash_syntax(script))

    issues.extend(check_internal_paths(skill_dir))
    issues.extend(check_internal_imports(skill_dir))
    issues.extend(check_todo_leftovers(skill_dir))

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]

    return {
        "module": t("module.logic"),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "issues": issues,
    }
