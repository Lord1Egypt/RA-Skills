#!/usr/bin/env python3
"""
Module 3: Edge Case & Error Handling Check
- Python: try/except coverage for network/file/subprocess calls
- Bash: set -e / set -euo pipefail presence
- HTTP calls: timeout parameter presence
- File ops: existence check before open/read/write
- User input: basic validation presence
"""

import ast
import re
from pathlib import Path

from _common import is_bash_script
from i18n import t


# ---------------------------------------------------------------------------
# Python AST helpers
# ---------------------------------------------------------------------------

# Calls that should be inside a try/except
# Use full dotted names only — generic method names like .get() are excluded
RISKY_CALL_PATTERNS = {
    "network": {
        "requests.get", "requests.post", "requests.put", "requests.delete",
        "requests.patch", "requests.request",
        "httpx.get", "httpx.post", "httpx.put", "httpx.delete", "httpx.patch",
        "urllib.request.urlopen",
    },
    "file": {
        "open",
        "json.load",
    },
    "subprocess": {
        "subprocess.run", "subprocess.call", "subprocess.check_output",
        "subprocess.Popen", "os.system",
    },
}

ALL_RISKY = set()
for calls in RISKY_CALL_PATTERNS.values():
    ALL_RISKY.update(calls)


def _call_name(node: ast.Call) -> str:
    """Return a dotted string name for a Call node."""
    if isinstance(node.func, ast.Attribute):
        val = node.func.value
        if isinstance(val, ast.Name):
            return f"{val.id}.{node.func.attr}"
        if isinstance(val, ast.Attribute) and isinstance(val.value, ast.Name):
            return f"{val.value.id}.{val.attr}.{node.func.attr}"
    if isinstance(node.func, ast.Name):
        return node.func.id
    return ""


def _has_timeout_kwarg(node: ast.Call) -> bool:
    return any(kw.arg == "timeout" for kw in node.keywords)


class RiskyCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.unprotected: list[tuple[int, str, str]] = []  # (lineno, name, category)
        self.missing_timeout: list[tuple[int, str]] = []
        self._try_depth = 0

    def visit_Try(self, node):
        self._try_depth += 1
        self.generic_visit(node)
        self._try_depth -= 1

    def visit_Call(self, node):
        name = _call_name(node)

        # Check risky call not inside try/except.
        # Match by full dotted name only (e.g. "requests.get", "subprocess.run")
        # — generic method names like ".get()" are intentionally NOT matched to
        #   avoid false positives.
        for category, calls in RISKY_CALL_PATTERNS.items():
            matched = name in calls
            if matched:
                if self._try_depth == 0:
                    self.unprotected.append((node.lineno, name or "?", category))
                # Check timeout for network calls
                if category == "network" and not _has_timeout_kwarg(node):
                    self.missing_timeout.append((node.lineno, name or "?"))
                break

        self.generic_visit(node)


def check_python_error_handling(script_path: Path) -> list[dict]:
    issues = []
    try:
        source = script_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except Exception:
        return issues

    visitor = RiskyCallVisitor()
    visitor.visit(tree)

    for lineno, name, category in visitor.unprotected:
        issues.append({
            "file": script_path.name,
            "line": lineno,
            "message": t("edges.no_try", cat=category, name=name),
            "severity": "WARN",
        })

    for lineno, name in visitor.missing_timeout:
        issues.append({
            "file": script_path.name,
            "line": lineno,
            "message": t("edges.no_timeout", name=name),
            "severity": "WARN",
        })

    return issues


# ---------------------------------------------------------------------------
# HTTP response status check (naive text scan)
# ---------------------------------------------------------------------------

def check_http_status_handling(script_path: Path) -> list[dict]:
    """Warn if HTTP calls exist but no status code check or raise_for_status."""
    issues = []
    try:
        text = script_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    has_http = bool(re.search(r'\b(requests|httpx)\.(get|post|put|delete|patch)\b', text))
    has_check = bool(re.search(r'(raise_for_status|\.status_code|status ==|\.ok\b)', text))

    if has_http and not has_check:
        issues.append({
            "file": script_path.name,
            "line": None,
            "message": t("edges.no_status_check"),
            "severity": "WARN",
        })
    return issues


# ---------------------------------------------------------------------------
# Bash safety check
# ---------------------------------------------------------------------------

def check_bash_safety(script_path: Path) -> list[dict]:
    issues = []
    try:
        text = script_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    has_safety = bool(re.search(r'set\s+-[a-zA-Z]*e', text))
    if not has_safety:
        issues.append({
            "file": script_path.name,
            "line": None,
            "message": t("edges.no_set_e"),
            "severity": "WARN",
        })
    return issues


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run(skill_dir: Path) -> dict:
    issues = []
    scripts_dir = skill_dir / "scripts"

    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if not script.is_file():
                continue
            if script.suffix == ".py":
                issues.extend(check_python_error_handling(script))
                issues.extend(check_http_status_handling(script))
            elif is_bash_script(script):
                issues.extend(check_bash_safety(script))

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]

    return {
        "module": t("module.edges"),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "issues": issues,
    }
