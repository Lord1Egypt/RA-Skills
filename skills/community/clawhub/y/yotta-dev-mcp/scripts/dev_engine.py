#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic development tools for yotta-dev-mcp.

The engine is intentionally small and self-contained: Python 3.8+ standard
library only, offline by default, deterministic output, read-only unless a
tool explicitly documents a write.
"""

import argparse
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

import dev_contract
from dev_adapters import run_adapter as _run_adapter_impl
from dev_architecture import architecture_review as _architecture_review_impl
from dev_common import (
    ANSI_RE, ERROR_RE, MAX_FILE_BYTES, VERIFY_LEVELS, _iter_files, _json_safe,
    _language, _read_text, _rel,
    _frontmatter_name, _frontmatter_version, source_exts,
)
from dev_impact import impact_analysis as _impact_analysis_impl
from dev_mcp_doctor import (
    default_config_paths as _default_config_paths_impl,
    default_skill_dirs as _default_skill_dirs_impl,
    mcp_doctor as _mcp_doctor_impl,
)
from dev_verify import verify_change as _verify_change_impl
from dev_selftest import self_test
from dev_model import (
    _classify_python_import,
    _repo_map_js,
    _repo_map_python,
    system_model as _system_model_impl,
)
from dev_rules import REVIEW_RULES

VERSION = "0.2.8"








def repo_map(path, max_files=2000):
    root = Path(path)
    if not root.exists():
        raise ValueError("路径不存在: %s" % path)
    if not root.is_dir():
        raise ValueError("repo_map 需要目录: %s" % path)
    modules = []
    imports = []
    entrypoints = []
    truncated = False
    files = list(_iter_files(root, source_exts(), max_files=max_files + 1))
    if len(files) > max_files:
        truncated = True
        files = files[:max_files]
    module_set = {_rel(root, file_path) for file_path in files}
    for file_path in files:
        rel = _rel(root, file_path)
        try:
            text = _read_text(file_path)
        except (OSError, ValueError):
            continue
        language = _language(file_path)
        modules.append({"path": rel, "language": language, "lines": len(text.splitlines())})
        if file_path.suffix.lower() == ".py":
            for raw in _repo_map_python(file_path, rel):
                _, target = _classify_python_import(
                    raw["target"], rel, module_set, relative=raw.get("relative", False)
                )
                imports.append({"source": rel, "target": target, "line": raw["line"]})
        elif file_path.suffix.lower() in (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"):
            imports.extend(_repo_map_js(file_path, rel))
        if (
            file_path.name in ("main.py", "cli.py", "app.py", "index.js", "index.ts")
            or "if __name__ == '__main__'" in text
            or 'if __name__ == "__main__"' in text
        ):
            entrypoints.append(rel)
    modules.sort(key=lambda item: item["path"])
    imports.sort(key=lambda item: (item["source"], item["line"], item["target"]))
    entrypoints = sorted(set(entrypoints))
    return {
        "root": str(root.resolve()),
        "modules": modules,
        "imports": imports,
        "entrypoints": entrypoints,
        "truncated": truncated,
    }


def _classify_match(line, query):
    normalized = re.sub(
        r"^\s*(?:async\s+)?(?:def|class|function|export\s+function|const|let|var)\s+",
        "",
        str(query),
    ).strip()
    target = normalized or str(query)
    escaped = re.escape(target)
    if re.search(r"^\s*(?:async\s+)?def\s+%s\b" % escaped, line):
        return "definition"
    if re.search(r"^\s*class\s+%s\b" % escaped, line):
        return "definition"
    if re.search(r"^\s*(?:export\s+)?(?:async\s+)?function\s+%s\b" % escaped, line):
        return "definition"
    if re.search(r"^\s*(?:export\s+)?(?:const|let|var)\s+%s\b" % escaped, line):
        return "definition"
    return "reference"


def find_code(path, query, extensions=None, max_results=100, context_lines=0):
    root = Path(path)
    if not root.exists():
        raise ValueError("路径不存在: %s" % path)
    if not query:
        raise ValueError("find_code 需要 query")
    if max_results < 1:
        raise ValueError("max_results 必须大于 0")
    context_lines = max(0, min(int(context_lines), 5))
    matches = []
    truncated = False
    for file_path in _iter_files(root if root.is_dir() else root.parent, extensions=extensions):
        if root.is_file() and file_path.resolve() != root.resolve():
            continue
        try:
            lines = _read_text(file_path).splitlines()
        except (OSError, ValueError):
            continue
        for index, line in enumerate(lines):
            if query not in line:
                continue
            if len(matches) >= max_results:
                truncated = True
                break
            start = max(0, index - context_lines)
            end = min(len(lines), index + context_lines + 1)
            matches.append({
                "path": _rel(root if root.is_dir() else root.parent, file_path),
                "line": index + 1,
                "kind": _classify_match(line, query),
                "text": line.strip()[:240],
                "context": lines[start:end] if context_lines else [],
            })
        if truncated:
            break
    return {"query": query, "matches": matches, "truncated": truncated}


def _dedupe_lines(lines):
    output = []
    index = 0
    while index < len(lines):
        line = lines[index]
        count = 1
        while index + count < len(lines) and lines[index + count] == line:
            count += 1
        output.append(line + (" [x%d]" % count if count > 1 else ""))
        index += count
    return output


def _fit_text(lines, max_chars):
    text = "\n".join(lines)
    if len(text) <= max_chars:
        return text
    if max_chars < 20:
        return text[:max_chars]
    output = []
    for line in lines:
        candidate = "\n".join(output + [line])
        if len(candidate) > max_chars - 20:
            break
        output.append(line)
    if output and output[-1] != "... [truncated]":
        output.append("... [truncated]")
    return "\n".join(output)[:max_chars]


def compress_output(text=None, file=None, max_chars=4000, head_lines=40, tail_lines=40):
    if file and text is None:
        text = _read_text(file)
    if text is None:
        raise ValueError("compress_output 需要 text 或 file")
    text = ANSI_RE.sub("", str(text)).replace("\r\n", "\n").replace("\r", "\n")
    raw_lines = [line.rstrip() for line in text.splitlines()]
    deduped = _dedupe_lines(raw_lines)
    priority = [line for line in deduped if ERROR_RE.search(line)]
    head = deduped[:max(0, int(head_lines))]
    tail = deduped[-max(0, int(tail_lines)):] if tail_lines else []
    chosen = []
    for line in priority + head + tail:
        if line not in chosen:
            chosen.append(line)
    result_text = _fit_text(chosen, int(max_chars))
    return {
        "text": result_text,
        "original_lines": len(raw_lines),
        "kept_lines": len(result_text.splitlines()),
        "error_lines": len(priority),
        "truncated": len(result_text) < len("\n".join(deduped)),
    }


def _split_code_comment(line_text, rel):
    language = _language(rel)
    if language in ("python", "shell"):
        markers = ("#",)
    elif language in ("javascript", "typescript"):
        markers = ("//", "/*")
    else:
        markers = ("#", "//", "/*")
    stripped = line_text.lstrip()
    if stripped.startswith("*") and not stripped.startswith("*/"):
        return "", line_text
    quote = None
    escaped = False
    index = 0
    while index < len(line_text):
        char = line_text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ("'", '"', "`"):
            quote = char
        else:
            for marker in markers:
                if line_text.startswith(marker, index):
                    return line_text[:index], line_text[index:]
        index += 1
    return line_text, ""


def _mask_strings(code):
    chars = list(code)
    quote = None
    escaped = False
    for index, char in enumerate(chars):
        if quote:
            if escaped:
                escaped = False
                chars[index] = " "
            elif char == "\\":
                escaped = True
                chars[index] = " "
            elif char == quote:
                quote = None
            else:
                chars[index] = " "
        elif char in ("'", '"', "`"):
            quote = char
    return "".join(chars)


def _allowlist_candidates(root):
    current = Path(root).resolve()
    candidates = []
    for base in (current, *current.parents):
        candidates.append(base / ".yotta" / "review-allowlist.json")
        candidates.append(base / ".review-allowlist.json")
        if (base / ".git").exists():
            break
    return candidates


def _load_review_allowlist(root):
    for candidate in _allowlist_candidates(root):
        if not candidate.is_file():
            continue
        try:
            data = json.loads(_read_text(candidate))
        except Exception as exc:  # noqa: BLE001
            return {}, [{"path": str(candidate), "detail": str(exc)}]
        entries = data.get("entries") if isinstance(data, dict) else None
        if not isinstance(entries, list):
            return {}, [{"path": str(candidate), "detail": "entries must be a list"}]
        allowlist = {}
        errors = []
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append({"path": str(candidate), "detail": "entry must be an object"})
                continue
            rel = entry.get("path")
            rule = entry.get("rule")
            line = entry.get("line")
            reason = entry.get("reason")
            if not isinstance(rel, str) or not isinstance(rule, str) or not reason:
                errors.append({"path": str(candidate), "detail": "path, rule and reason are required"})
                continue
            if isinstance(line, bool) or not isinstance(line, int) or line < 1:
                errors.append({"path": str(candidate), "detail": "line must be a positive integer"})
                continue
            normalized = rel.replace("\\", "/")
            while normalized.startswith("./"):
                normalized = normalized[2:]
            allowlist[(normalized, rule, line)] = str(reason)
        return allowlist, errors
    return {}, []


def _apply_review_allowlist(findings, allowlist):
    kept = []
    suppressed = []
    for item in findings:
        key = (item["path"], item["rule"], item["line"])
        if key in allowlist:
            suppressed.append(dict(item, reason=allowlist[key]))
        else:
            kept.append(item)
    return kept, suppressed


def _review_line(rel, line_no, line_text):
    findings = []
    code, comment = _split_code_comment(line_text, rel)
    code = _mask_strings(code)
    for rule, severity, pattern, suggestion in REVIEW_RULES:
        target = comment if rule == "todo-comment" else code
        if pattern.search(target):
            findings.append({
                "path": rel,
                "line": line_no,
                "rule": rule,
                "severity": severity,
                "evidence": line_text.strip()[:240],
                "suggestion": suggestion,
            })
    return findings


def review_code(path=None, text=None, max_findings=200):
    findings = []
    allowlist = {}
    allowlist_errors = []
    if text is not None:
        for line_no, line in enumerate(str(text).splitlines(), 1):
            findings.extend(_review_line("<text>", line_no, line))
    else:
        if not path:
            raise ValueError("review_code 需要 path 或 text")
        root = Path(path)
        if not root.exists():
            raise ValueError("路径不存在: %s" % path)
        allowlist_root = root.parent if root.is_file() else root
        allowlist, allowlist_errors = _load_review_allowlist(allowlist_root)
        files = [root] if root.is_file() else list(_iter_files(root, extensions=source_exts()))
        base = root.parent if root.is_file() else root
        for file_path in files:
            try:
                lines = _read_text(file_path).splitlines()
            except (OSError, ValueError):
                continue
            rel = _rel(base, file_path)
            for line_no, line in enumerate(lines, 1):
                findings.extend(_review_line(rel, line_no, line))
    kept, suppressed = _apply_review_allowlist(findings, allowlist)
    kept.sort(key=lambda item: (item["path"], item["line"], item["rule"]))
    truncated = len(kept) > max_findings
    return {
        "findings": kept[:max_findings],
        "truncated": truncated,
        "suppressed": len(suppressed),
        "suppressed_findings": suppressed[:max_findings],
        "allowlist_errors": allowlist_errors,
    }


def _parse_added_lines(diff_text):
    current_file = None
    line_no = 0
    for raw in diff_text.splitlines():
        if raw.startswith("+++ "):
            current_file = raw[4:].strip()
            if current_file.startswith("b/"):
                current_file = current_file[2:]
            continue
        match = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
        if match:
            line_no = int(match.group(1))
            continue
        if current_file and raw.startswith("+") and not raw.startswith("+++"):
            yield current_file, line_no, raw[1:]
            line_no += 1
        elif current_file and not raw.startswith("-") and not raw.startswith("\\"):
            line_no += 1


def _resolve_git_commit(path, revision):
    value = str(revision or "").strip()
    if (
        not value
        or len(value) > 200
        or value.startswith("-")
        or any(char.isspace() for char in value)
    ):
        raise ValueError("base 不是有效 revision")
    command = [
        "git", "-C", str(path), "rev-parse", "--verify", "--quiet",
        "--end-of-options", value + "^{commit}",
    ]
    proc = subprocess.run(command, capture_output=True, text=True)
    if proc.returncode != 0:
        raise ValueError("base revision 无法解析: %s" % value)
    commit = proc.stdout.strip()
    if not re.match(r"^[0-9a-fA-F]{40,64}$", commit):
        raise ValueError("base revision 解析结果非法")
    return commit


def review_diff(diff_text=None, path=None, base=None, max_findings=200):
    allowlist = {}
    allowlist_errors = []
    if diff_text is None:
        if not path:
            raise ValueError("review_diff 需要 diff_text 或 path")
        allowlist, allowlist_errors = _load_review_allowlist(path)
        command = ["git", "-C", str(path), "diff", "--no-ext-diff",
                   "--no-textconv", "--unified=0"]
        if base:
            command.append(_resolve_git_commit(path, base))
        proc = subprocess.run(command, capture_output=True, text=True)
        if proc.returncode != 0:
            raise ValueError("git diff 失败: %s" % (proc.stderr.strip() or proc.stdout.strip()))
        diff_text = proc.stdout
    findings = []
    files = []
    for rel, line_no, line in _parse_added_lines(diff_text):
        if rel not in files:
            files.append(rel)
        findings.extend(_review_line(rel, line_no, line))
    kept, suppressed = _apply_review_allowlist(findings, allowlist)
    kept.sort(key=lambda item: (item["path"], item["line"], item["rule"]))
    truncated = len(kept) > max_findings
    return {
        "files": files,
        "findings": kept[:max_findings],
        "truncated": truncated,
        "suppressed": len(suppressed),
        "suppressed_findings": suppressed[:max_findings],
        "allowlist_errors": allowlist_errors,
    }


def _default_skill_dirs():
    return _default_skill_dirs_impl()


def _default_config_paths():
    return _default_config_paths_impl()


def mcp_doctor(skills_dirs=None, config_paths=None, include_defaults=None):
    return _mcp_doctor_impl(
        skills_dirs=skills_dirs,
        config_paths=config_paths,
        include_defaults=include_defaults,
    )


SECRET_KEY_RE = re.compile(
    r"""(?i)\b(api[_-]?key|access[_-]?key|secret|token|password|passwd|pwd)\b\s*[:=]\s*["']?([^"'\s#]{8,})"""
)
WEAK_PASSWORD_RE = re.compile(
    r"""(?i)\b(password|passwd|pwd)\b\s*[:=]\s*["']?([^"'\s#]{6,7})"""
)
AWS_KEY_RE = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
PRIVATE_KEY_RE = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
HIGH_ENTROPY_RE = re.compile(r"[A-Za-z0-9_+/=\-]{32,}")
HASH_CONTEXT_RE = re.compile(r"(?i)(sha1|sha256|sha512|hash|checksum|digest|integrity)")
HEX_TOKEN_RE = re.compile(r"^[0-9a-fA-F]+$")
PATH_HINT_RE = re.compile(r"(?i)(?:[a-z]:[\\/]|\\\\|https?://|file://)")
URL_HINT_RE = re.compile(r"(?i)(?:file|https?)://")
PERCENT_ESCAPE_RE = re.compile(r"%[0-9A-Fa-f]{2}")
HASH_PREFIX_RE = re.compile(r"(?i)^(?:sha1|sha256|sha512|md5)[=:]([0-9a-fA-F]{32,128})$")
FILE_SUFFIX_RE = re.compile(
    r"(?i)\.(exe|dll|sys|py|js|ts|tsx|json|md|txt|log|whl|tar|gz|zip|png|jpg|jpeg|svg)"
)


def _high_entropy_noise(line, token, start, end):
    """Return True for common non-secret high-entropy noise."""
    if HASH_PREFIX_RE.match(token):
        return True
    if PERCENT_ESCAPE_RE.search(token) and URL_HINT_RE.search(line):
        return True
    if start > 0 and line[start - 1] == "%":
        return True
    if HEX_TOKEN_RE.match(token) and len(token) in (32, 40, 64, 128) and HASH_CONTEXT_RE.search(line):
        return True
    window = line[max(0, start - 16):min(len(line), end + 16)]
    if PATH_HINT_RE.search(window):
        return True
    if URL_HINT_RE.search(line) and PERCENT_ESCAPE_RE.search(window):
        return True
    if FILE_SUFFIX_RE.match(line[end:end + 8]):
        return True
    return False


def _entropy(value):
    if not value:
        return 0.0
    counts = {}
    for char in value:
        counts[char] = counts.get(char, 0) + 1
    length = float(len(value))
    return -sum((count / length) * math.log(count / length, 2) for count in counts.values())


def _redact(value):
    if len(value) <= 8:
        return "[REDACTED]"
    return value[:4] + "...[REDACTED]"


def scan_secrets(path=None, text=None, max_findings=200, include_git_history=False):
    entries = []
    if text is not None:
        entries.append(("<text>", str(text)))
    else:
        if not path:
            raise ValueError("scan_secrets 需要 path 或 text")
        root = Path(path)
        if not root.exists():
            raise ValueError("路径不存在: %s" % path)
        files = [root] if root.is_file() else list(
            _iter_files(root, all_files=True, ignore_temp=False)
        )
        base = root.parent if root.is_file() else root
        for file_path in files:
            try:
                entries.append((_rel(base, file_path), _read_text(file_path)))
            except (OSError, ValueError):
                continue
        if include_git_history:
            entries.append(("git-history", _git_history_text(root)))
    findings = []
    for rel, content in entries:
        for line_no, line in enumerate(content.splitlines(), 1):
            specific_spans = []
            if PRIVATE_KEY_RE.search(line):
                findings.append({
                    "path": rel, "line": line_no, "rule": "private-key",
                    "severity": "critical", "evidence": "[REDACTED private key marker]",
                    "suggestion": "Remove the private key from source control and rotate it.",
                })
            for match in AWS_KEY_RE.finditer(line):
                findings.append({
                    "path": rel, "line": line_no, "rule": "aws-access-key",
                    "severity": "critical", "evidence": _redact(match.group(0)),
                    "suggestion": "Rotate the key and move it to a secret manager.",
                })
                specific_spans.append(match.span(0))
            for match in SECRET_KEY_RE.finditer(line):
                name = match.group(1).lower()
                rule = "api-key" if "api" in name or "access" in name else (
                    "token" if "token" in name else "credential"
                )
                findings.append({
                    "path": rel, "line": line_no, "rule": rule,
                    "severity": "high", "evidence": "%s=%s" % (match.group(1), _redact(match.group(2))),
                    "suggestion": "Remove the literal credential and load it from the environment or a secret store.",
                })
                specific_spans.append(match.span(2))
            for match in WEAK_PASSWORD_RE.finditer(line):
                findings.append({
                    "path": rel, "line": line_no, "rule": "weak-password",
                    "severity": "medium",
                    "evidence": "%s=%s" % (match.group(1), _redact(match.group(2))),
                    "suggestion": "Use a longer password and load it from the environment or a secret store.",
                })
                specific_spans.append(match.span(2))
            for match in HIGH_ENTROPY_RE.finditer(line):
                token = match.group(0)
                if (
                    _entropy(token) >= 4.0
                    and not PRIVATE_KEY_RE.search(line)
                    and not _high_entropy_noise(line, token, match.start(), match.end())
                    and not any(
                        start < match.end() and match.start() < end
                        for start, end in specific_spans
                    )
                ):
                    findings.append({
                        "path": rel, "line": line_no, "rule": "high-entropy-token",
                        "severity": "medium", "evidence": _redact(token),
                        "suggestion": "Verify whether this is a credential; if so, remove and rotate it.",
                    })
    unique = {}
    for item in findings:
        key = (item["path"], item["line"], item["rule"], item["evidence"])
        unique[key] = item
    ordered = sorted(unique.values(), key=lambda item: (item["path"], item["line"], item["rule"], item["evidence"]))
    return {"findings": ordered[:max_findings], "truncated": len(ordered) > max_findings}


def _git_history_text(root):
    """Return bounded git diff text for secret scanning; never fail the scan."""
    try:
        process = subprocess.run(
            ["git", "-C", str(root), "log", "-p", "--all", "--no-ext-diff",
             "--no-textconv", "--max-count=50"],
            capture_output=True, text=True, timeout=30,
        )
        if process.returncode != 0:
            return ""
        return process.stdout[:MAX_FILE_BYTES]
    except Exception:  # noqa: BLE001
        return ""


DEPENDENCY_LOCKFILES = {
    "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
    "bun.lock", "poetry.lock", "uv.lock", "Pipfile.lock",
}


def _dependency_spec_issue(spec):
    value = str(spec).strip()
    if value in ("", "*", "latest") or value.startswith((">=", ">", "http://", "git+http://")):
        return "unpinned-dependency"
    if value.startswith(("file:", "link:")):
        return "local-dependency"
    return None


POPULAR_PACKAGES = (
    "requests", "numpy", "pytest", "lodash", "express", "react", "vue",
    "typescript", "fastapi", "pydantic", "openai", "axios",
)


def _edit_distance_one(left, right):
    if abs(len(left) - len(right)) > 1:
        return False
    if left == right:
        return False
    if len(left) == len(right):
        return sum(1 for a, b in zip(left, right) if a != b) == 1
    short, long = (left, right) if len(left) < len(right) else (right, left)
    index = 0
    skipped = False
    for char in long:
        if index < len(short) and char == short[index]:
            index += 1
        elif skipped:
            return False
        else:
            skipped = True
    return True


def _typosquat_suspicion(name):
    low = str(name).lower()
    return any(_edit_distance_one(low, known) for known in POPULAR_PACKAGES)


def scan_dependencies(path):
    root = Path(path)
    if not root.exists():
        raise ValueError("路径不存在: %s" % path)
    if not root.is_dir():
        raise ValueError("scan_dependencies 需要目录: %s" % path)
    manifests = []
    lockfiles = []
    issues = []
    for file_path in _iter_files(root, extensions={".json", ".txt", ".toml", ".lock"}, max_files=500):
        rel = _rel(root, file_path)
        if file_path.name in DEPENDENCY_LOCKFILES:
            lockfiles.append(rel)
    package_file = root / "package.json"
    if package_file.is_file():
        manifests.append("package.json")
        try:
            package = json.loads(_read_text(package_file))
        except Exception as exc:  # noqa: BLE001
            issues.append({"code": "invalid-manifest", "severity": "high",
                           "manifest": "package.json", "message": str(exc)})
            package = {}
        groups = ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies")
        has_deps = False
        for group in groups:
            dependencies = package.get(group) if isinstance(package, dict) else None
            if not isinstance(dependencies, dict):
                continue
            has_deps = has_deps or bool(dependencies)
            for name, spec in sorted(dependencies.items()):
                code = _dependency_spec_issue(spec)
                if code:
                    issues.append({
                        "code": code, "severity": "medium", "manifest": "package.json",
                        "dependency": name, "message": "%s uses %s" % (name, spec),
                    })
                if _typosquat_suspicion(name):
                    issues.append({
                        "code": "typosquat-suspicion", "severity": "medium",
                        "manifest": "package.json", "dependency": name,
                        "message": "%s is one edit away from a popular package; verify the name" % name,
                        "requires_manual_review": True,
                    })
        if has_deps and not lockfiles:
            issues.append({
                "code": "missing-lockfile", "severity": "medium", "manifest": "package.json",
                "message": "Dependencies exist but no lockfile was found.",
            })
    for requirement in sorted(root.glob("requirements*.txt")):
        manifests.append(_rel(root, requirement))
        for line_no, line in enumerate(_read_text(requirement).splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith(("git+http://", "http://")):
                issues.append({"code": "insecure-source", "severity": "high",
                               "manifest": _rel(root, requirement), "line": line_no,
                               "message": stripped})
            elif "@" in stripped and "==" not in stripped and ">=" not in stripped:
                issues.append({"code": "unpinned-dependency", "severity": "medium",
                               "manifest": _rel(root, requirement), "line": line_no,
                               "message": stripped})
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        manifests.append("pyproject.toml")
        text = _read_text(pyproject)
        if "dependencies" in text and not (root / "poetry.lock").is_file() and not (root / "uv.lock").is_file():
            issues.append({
                "code": "missing-lockfile", "severity": "medium",
                "manifest": "pyproject.toml",
                "message": "Python dependencies exist but no poetry.lock / uv.lock was found.",
            })
    pipfile = root / "Pipfile"
    if pipfile.is_file():
        manifests.append("Pipfile")
        if not (root / "Pipfile.lock").is_file():
            issues.append({
                "code": "missing-lockfile", "severity": "medium",
                "manifest": "Pipfile",
                "message": "Pipfile exists but Pipfile.lock was not found.",
            })
    issues.sort(key=lambda item: (item.get("manifest", ""), item.get("line", 0), item["code"], item.get("dependency", "")))
    return {
        "manifests": sorted(manifests),
        "lockfiles": sorted(lockfiles),
        "issues": issues,
        "checked_manifests": len(manifests),
        "checked_lockfiles": len(lockfiles),
    }


def check_publish_readiness(path):
    root = Path(path)
    if not root.exists() or not root.is_dir():
        raise ValueError("check_publish_readiness 需要目录: %s" % path)
    required = ["package.json", "SKILL.md", "README.md", "LICENSE", "CHANGELOG.md", "VERSION"]
    files = {}
    issues = []
    for name in required:
        file_path = root / name
        files[name] = file_path.is_file()
        if not file_path.is_file():
            issues.append({"code": "missing-file", "severity": "high",
                           "message": "Missing required file: %s" % name})
    versions = {}
    package = {}
    package_path = root / "package.json"
    if package_path.is_file():
        try:
            package = json.loads(_read_text(package_path))
        except Exception as exc:  # noqa: BLE001
            issues.append({"code": "invalid-package-json", "severity": "high", "message": str(exc)})
            package = {}
        versions["package.json"] = package.get("version")
    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        versions["SKILL.md"] = _frontmatter_version(_read_text(skill_path))
    changelog_path = root / "CHANGELOG.md"
    if changelog_path.is_file():
        match = re.search(r"(?m)^##\s+v?(\d+\.\d+\.\d+)", _read_text(changelog_path))
        versions["CHANGELOG.md"] = match.group(1) if match else None
    version_path = root / "VERSION"
    if version_path.is_file():
        versions["VERSION"] = _read_text(version_path).strip() or None
    script_versions = []
    for script in sorted(root.glob("scripts/*.py")):
        try:
            match = re.search(r'(?m)^VERSION\s*=\s*["\']([^"\']+)["\']', _read_text(script))
        except (OSError, ValueError):
            continue
        if match:
            script_versions.append(match.group(1))
    if script_versions:
        versions["engine"] = script_versions[0]
    values = [value for value in versions.values() if value]
    if len(set(values)) > 1:
        issues.append({
            "code": "version-mismatch", "severity": "high",
            "message": "Version mismatch: %s" % json.dumps(versions, ensure_ascii=False, sort_keys=True),
        })
    repository = package.get("repository") if isinstance(package, dict) else None
    repository_url = repository.get("url") if isinstance(repository, dict) else repository
    if not repository_url:
        issues.append({"code": "missing-repository", "severity": "medium",
                       "message": "package.json repository.url is missing."})
    publish_config = package.get("publishConfig") if isinstance(package, dict) else None
    if not isinstance(publish_config, dict) or publish_config.get("access") != "public":
        issues.append({"code": "publish-access", "severity": "medium",
                       "message": "package.json publishConfig.access should be public."})
    issues.sort(key=lambda item: (item["code"], item.get("message", "")))
    return {
        "ok": not any(item["severity"] == "high" for item in issues),
        "root": str(root.resolve()),
        "files": files,
        "versions": versions,
        "issues": issues,
    }


CHECK_COMMANDS = {
    "python-unittest": lambda: [sys.executable, "-m", "unittest", "discover", "-v"],
    "pytest": lambda: [sys.executable, "-m", "pytest", "-q"],
    "python-compile": lambda: [sys.executable, "-m", "compileall", "-q", "."],
    "npm-test": lambda: ["npm", "test", "--silent"],
    "npm-lint": lambda: ["npm", "run", "lint", "--silent"],
}


def run_checks(kind, cwd, timeout=120, allow_execute=False):
    if kind not in CHECK_COMMANDS:
        raise ValueError("unsupported check kind: %s" % kind)
    if not allow_execute:
        raise PermissionError("run_checks is disabled by default; pass allow_execute=true explicitly")
    root = Path(cwd)
    if not root.is_dir():
        raise ValueError("cwd is not a directory: %s" % cwd)
    command = CHECK_COMMANDS[kind]()
    if os.name == "nt" and command[0] == "npm":
        command = ["cmd", "/c"] + command
    try:
        process = subprocess.run(
            command, cwd=str(root), capture_output=True, text=True, timeout=timeout
        )
        output = (process.stdout or "") + (process.stderr or "")
        result = compress_output(output, max_chars=4000)
        summary_lines = [
            line.strip() for line in output.splitlines()
            if re.search(r"(?i)(ran \d+ test|ok\b|failed\b|error\b|\d+ passed)", line)
        ]
        return {
            "kind": kind,
            "cwd": str(root.resolve()),
            "exit_code": process.returncode,
            "passed": process.returncode == 0,
            "summary": "\n".join(summary_lines[:8]) or "no summary matched",
            "output": result["text"],
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "kind": kind, "cwd": str(root.resolve()), "exit_code": 124,
            "passed": False, "summary": "timeout after %ss" % timeout,
            "output": "", "timed_out": True,
        }


def _license_text():
    return (
        "MIT License\n\nCopyright (c) 2026 YottaMeta\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE.\n"
    )


def scaffold_skill(name, output_dir, apply=False, description=None):
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", str(name)):
        raise ValueError("skill name must match ^[a-z0-9][a-z0-9-]*$")
    target = Path(output_dir) / name
    description = description or "Deterministic local helper skill."
    files = {
        "SKILL.md": (
            "---\nname: %s\ndescription: %s\nversion: 0.1.0\nlicense: MIT\n---\n\n"
            "# %s\n\n%s\n" % (name, description, name, description)
        ),
        "package.json": json.dumps({
            "name": "@yottameta/%s" % name,
            "version": "0.1.0",
            "description": description,
            "license": "MIT",
            "repository": {"type": "git", "url": "git+https://github.com/YottaMeta/%s.git" % name},
            "publishConfig": {"access": "public"},
            "files": ["SKILL.md", "README.md", "scripts", "LICENSE", "NOTICE"],
        }, ensure_ascii=False, indent=2) + "\n",
        "README.md": "# %s\n\n%s\n" % (name, description),
        "CHANGELOG.md": "# Changelog\n\n## v0.1.0 (2026-09-25)\n\n- Initial scaffold.\n",
        "NOTICE": "# NOTICE\n\nGenerated by yotta-dev-mcp scaffold_skill.\n",
        "LICENSE": _license_text(),
        "scripts/%s.py" % name: (
            "#!/usr/bin/env python3\n"
            "# -*- coding: utf-8 -*-\n"
            "\"\"\"%s.\"\"\"\n\n"
            "def main():\n"
            "    return 0\n\n"
            "if __name__ == '__main__':\n"
            "    raise SystemExit(main())\n" % description
        ),
    }
    if apply and target.exists() and any(target.iterdir()):
        raise ValueError("target already exists and is not empty: %s" % target)
    if apply:
        for rel, content in files.items():
            file_path = target / rel
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
    return {
        "name": name,
        "target": str(target),
        "applied": bool(apply),
        "files": [{"path": rel, "bytes": len(content.encode("utf-8"))}
                  for rel, content in sorted(files.items())],
    }


def _write_temp_text(path, content):
    descriptor, name = tempfile.mkstemp(
        prefix="." + path.name + ".", suffix=".tmp", dir=str(path.parent),
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
    except BaseException:
        try:
            os.unlink(name)
        except OSError:
            pass
        raise
    return Path(name)


def _write_temp_bytes(path, data):
    descriptor, name = tempfile.mkstemp(
        prefix="." + path.name + ".", suffix=".tmp", dir=str(path.parent),
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
    except BaseException:
        try:
            os.unlink(name)
        except OSError:
            pass
        raise
    return Path(name)


def _preserve_mode(source, target):
    try:
        os.chmod(str(target), os.stat(str(source)).st_mode & 0o777)
    except OSError:
        pass


def _is_link_like(path):
    try:
        info = os.lstat(str(path))
    except OSError:
        return False
    if stat.S_ISLNK(info.st_mode):
        return True
    attributes = getattr(info, "st_file_attributes", 0)
    reparse_point = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return bool(attributes & reparse_point)


def _assert_no_symlink_path(path, root):
    root = Path(root)
    current = Path(path)
    while True:
        if _is_link_like(current):
            raise ValueError("拒绝通过符号链接写入: %s" % current)
        if current == root or current.parent == current:
            break
        current = current.parent


def _atomic_write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if path.exists():
        backup = path.with_suffix(path.suffix + ".bak")
        temporary_backup = _write_temp_bytes(backup, path.read_bytes())
        _preserve_mode(path, temporary_backup)
        os.replace(str(temporary_backup), str(backup))
    temporary = _write_temp_text(path, content)
    if path.exists():
        _preserve_mode(path, temporary)
    os.replace(str(temporary), str(path))
    return str(backup) if backup else None


def workflow_state(root, action="read", date=None, text=None, file=None, apply=False):
    workflow = Path(root) / ".workflow"
    files = ["STATE.md", "TASKS.md", "DECISIONS.md", "ROADMAP.md"]
    if action == "read":
        existing = [name for name in files if (workflow / name).is_file()]
        missing = [name for name in files if name not in existing]
        excerpts = {}
        for name in existing:
            try:
                content = _read_text(workflow / name)
            except (OSError, ValueError):
                content = ""
            excerpts[name] = content[:1200]
        return {
            "ok": not missing,
            "workflow": str(workflow.resolve()),
            "files": existing,
            "missing": missing,
            "excerpts": excerpts,
            "applied": False,
        }
    if action == "append-log":
        if not date or not re.match(r"^\d{4}-\d{2}-\d{2}$", str(date)):
            raise ValueError("append-log requires date=YYYY-MM-DD")
        target = workflow / "logs" / ("%s.md" % date)
    elif action == "append-file":
        if file not in files:
            raise ValueError("append-file requires one of: %s" % ", ".join(files))
        target = workflow / file
    else:
        raise ValueError("unsupported workflow action: %s" % action)
    body = (text or "").rstrip() + "\n"
    preview = body
    if apply:
        _assert_no_symlink_path(target, Path(root))
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            existing = _read_text(target)
            if existing and not existing.endswith("\n"):
                existing += "\n"
            _atomic_write(target, existing + "\n" + body)
        else:
            header = ""
            if action == "append-log":
                header = "# 流水日志 %s\n\n" % date
            _atomic_write(target, header + body)
    return {
        "ok": True,
        "action": action,
        "target": str(target.resolve()),
        "applied": bool(apply),
        "preview": preview,
    }








































































































def system_model(path, max_files=2000, contract_file=None):
    """Build the deterministic system model through the stable engine facade."""
    return _system_model_impl(
        path, max_files=max_files, contract_file=contract_file,
    )


def architecture_review(path, max_files=2000, contract_file=None):
    """Review architecture through the stable engine facade."""
    return _architecture_review_impl(
        path, max_files=max_files, contract_file=contract_file,
    )


def impact_analysis(path, changed_files=None, diff=None, symbols=None, depth=3,
                    max_files=2000, contract_file=None):
    """Build the change impact cone through the stable engine facade."""
    return _impact_analysis_impl(
        path, changed_files=changed_files, diff=diff, symbols=symbols,
        depth=depth, max_files=max_files, contract_file=contract_file,
    )


def verify_change(path, changed_files=None, diff=None, symbols=None, depth=3,
                  levels=None, allow_execute=False, timeout=120,
                  max_files=2000, contract_file=None, policy_file=None):
    """Run the verification ladder through the stable engine facade."""
    return _verify_change_impl(
        path, changed_files=changed_files, diff=diff, symbols=symbols,
        depth=depth, levels=levels, allow_execute=allow_execute, timeout=timeout,
        max_files=max_files, contract_file=contract_file, policy_file=policy_file,
    )


def run_adapter(path, action="list", adapter=None, allow_execute=False, timeout=120,
                max_chars=120000, token_budget=None, target="."):
    """Probe or explicitly run one optional external adapter.

    The implementation lives in dev_adapters.py; this facade keeps the public
    dispatch signature and fail-closed default visible to self_test.
    """
    return _run_adapter_impl(
        path, action=action, adapter=adapter, allow_execute=allow_execute,
        timeout=timeout, max_chars=max_chars, token_budget=token_budget,
        target=target,
    )


def dispatch(name, arguments):
    handlers = {
        "repo_map": repo_map,
        "system_model": system_model,
        "architecture_review": architecture_review,
        "impact_analysis": impact_analysis,
        "verify_change": verify_change,
        "self_test": self_test,
        "run_adapter": run_adapter,
        "find_code": find_code,
        "compress_output": compress_output,
        "review_code": review_code,
        "review_diff": review_diff,
        "mcp_doctor": mcp_doctor,
        "scan_secrets": scan_secrets,
        "scan_dependencies": scan_dependencies,
        "check_publish_readiness": check_publish_readiness,
        "run_checks": run_checks,
        "scaffold_skill": scaffold_skill,
        "workflow_state": workflow_state,
    }
    if name not in handlers:
        raise ValueError("未知工具: %s" % name)
    return handlers[name](**(arguments or {}))


def main():
    parser = argparse.ArgumentParser(description="Deterministic development tools for yotta-dev-mcp")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command")
    repo = sub.add_parser("repo-map")
    repo.add_argument("path")
    model = sub.add_parser("system-model")
    model.add_argument("path")
    model.add_argument("--contract", help="contract path relative to the repository root")
    review = sub.add_parser("architecture-review")
    review.add_argument("path")
    review.add_argument("--contract", help="contract path relative to the repository root")
    impact = sub.add_parser("impact-analysis")
    impact.add_argument("path")
    impact.add_argument("--changed", action="append",
                        help="repository-relative changed file (repeatable)")
    impact.add_argument("--diff-file", help="read a unified diff from this file")
    impact.add_argument("--symbol", action="append",
                        help="target symbol whose definition site is the change (repeatable)")
    impact.add_argument("--depth", type=int, default=3,
                        help="reverse-dependency depth, 1-10 (default 3)")
    impact.add_argument("--contract", help="contract path relative to the repository root")
    verify = sub.add_parser("verify-change")
    verify.add_argument("path")
    verify.add_argument("--changed", action="append",
                       help="repository-relative changed file (repeatable)")
    verify.add_argument("--diff-file", help="read a unified diff from this file")
    verify.add_argument("--symbol", action="append",
                        help="target symbol whose definition site is the change (repeatable)")
    verify.add_argument("--level", action="append", choices=VERIFY_LEVELS,
                        help="additional verification level (repeatable)")
    verify.add_argument("--depth", type=int, default=3,
                        help="reverse-dependency depth, 1-10 (default 3)")
    verify.add_argument("--contract", help="contract path relative to the repository root")
    verify.add_argument("--policy-file", help="verification policy path relative to the root")
    verify.add_argument("--allow-execute", action="store_true",
                        help="run whitelisted L2-L4 policy checks")
    verify.add_argument("--timeout", type=int, default=120,
                        help="upper bound for each check in seconds")
    self_test_parser = sub.add_parser("self-test")
    self_test_parser.add_argument("path")
    self_test_parser.add_argument("--mode", choices=("auto", "source", "installed"),
                                  default="auto")
    self_test_parser.add_argument("--allow-execute", action="store_true",
                                  help="run the target test suite")
    self_test_parser.add_argument("--timeout", type=int, default=120,
                                  help="test timeout in seconds")
    adapter = sub.add_parser("adapter")
    adapter.add_argument("path")
    adapter.add_argument("--action", choices=("list", "run"), default="list")
    adapter.add_argument("--adapter",
                         choices=("import-linter", "dependency-cruiser", "repomix"))
    adapter.add_argument("--allow-execute", action="store_true",
                        help="run the selected adapter; required for action=run")
    adapter.add_argument("--timeout", type=int, default=120,
                        help="adapter timeout in seconds")
    adapter.add_argument("--max-chars", type=int, default=120000,
                        help="Repomix output cap")
    adapter.add_argument("--token-budget", type=int,
                        help="optional Repomix token budget")
    adapter.add_argument("--target", default=".",
                        help="repository-relative adapter target, default .")
    find = sub.add_parser("find-code")
    find.add_argument("path")
    find.add_argument("query")
    compress = sub.add_parser("compress-output")
    compress.add_argument("file")
    review = sub.add_parser("review-code")
    review.add_argument("path")
    doctor = sub.add_parser("mcp-doctor")
    doctor.add_argument("--skills-dir", action="append")
    doctor.add_argument("--config", action="append")
    doctor.add_argument("--include-defaults", action="store_true",
                        help="scan built-in host registry in addition to --config paths")
    args = parser.parse_args()
    if args.command == "repo-map":
        result = repo_map(args.path)
    elif args.command == "system-model":
        result = system_model(args.path, contract_file=args.contract)
    elif args.command == "architecture-review":
        result = architecture_review(args.path, contract_file=args.contract)
    elif args.command == "impact-analysis":
        diff_text = None
        if args.diff_file:
            diff_text = Path(args.diff_file).read_text(encoding="utf-8-sig")
        result = impact_analysis(args.path, changed_files=args.changed, diff=diff_text,
                                 symbols=args.symbol, depth=args.depth,
                                 contract_file=args.contract)
    elif args.command == "verify-change":
        diff_text = None
        if args.diff_file:
            diff_text = Path(args.diff_file).read_text(encoding="utf-8-sig")
        result = verify_change(
            args.path, changed_files=args.changed, diff=diff_text,
            symbols=args.symbol, depth=args.depth, levels=args.level,
            allow_execute=args.allow_execute, timeout=args.timeout,
            contract_file=args.contract, policy_file=args.policy_file,
        )
    elif args.command == "self-test":
        result = self_test(
            args.path, mode=args.mode, allow_execute=args.allow_execute,
            timeout=args.timeout,
        )
    elif args.command == "adapter":
        result = run_adapter(
            args.path, action=args.action, adapter=args.adapter,
            allow_execute=args.allow_execute, timeout=args.timeout,
            max_chars=args.max_chars, token_budget=args.token_budget,
            target=args.target,
        )
    elif args.command == "find-code":
        result = find_code(args.path, args.query)
    elif args.command == "compress-output":
        result = compress_output(file=args.file)
    elif args.command == "review-code":
        result = review_code(args.path)
    elif args.command == "mcp-doctor":
        result = mcp_doctor(
            skills_dirs=args.skills_dir,
            config_paths=args.config,
            include_defaults=args.include_defaults,
        )
    else:
        parser.print_help()
        return 2
    sys.stdout.write(json.dumps(_json_safe(result), ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
