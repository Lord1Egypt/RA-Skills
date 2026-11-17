#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Optional external adapters for yotta-dev-mcp.

The core engine stays standard-library-only.  This module only probes and
explicitly runs mature third-party tools that the user already installed.
It never installs packages, downloads files or accepts arbitrary argv.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


ADAPTER_SPECS = {
    "import-linter": {
        "package": "import-linter",
        "license": "BSD-2-Clause",
        "kind": "architecture",
        "description": "Python import boundary and layered architecture contracts",
        "executables": ("lint-imports",),
        "config_names": (".importlinter",),
        "config_sections": (
            ("setup.cfg", "importlinter"),
            ("tox.ini", "importlinter"),
            ("pyproject.toml", "tool.importlinter"),
        ),
        "config_required": True,
    },
    "dependency-cruiser": {
        "package": "dependency-cruiser",
        "license": "MIT",
        "kind": "architecture",
        "description": "JavaScript and TypeScript dependency rules",
        "executables": ("depcruise",),
        "config_names": (
            ".dependency-cruiser.js",
            ".dependency-cruiser.cjs",
            ".dependency-cruiser.mjs",
            ".dependency-cruiser.json",
        ),
        "config_sections": (),
        "config_required": True,
    },
    "repomix": {
        "package": "repomix",
        "license": "MIT",
        "kind": "context",
        "description": "Repository packing and context budget enforcement",
        "executables": ("repomix",),
        "config_names": ("repomix.config.json",),
        "config_sections": (),
        "config_required": False,
    },
}

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
EXCERPT_LIMIT = 8000
DEFAULT_MAX_CHARS = 120000


def adapter_catalog():
    """Return stable adapter metadata without touching the filesystem."""
    items = []
    for adapter_id, spec in ADAPTER_SPECS.items():
        items.append({
            "id": adapter_id,
            "package": spec["package"],
            "license": spec["license"],
            "kind": spec["kind"],
            "description": spec["description"],
            "config_required": bool(spec["config_required"]),
        })
    return items


def _validated_root(path):
    root = Path(path)
    if not root.exists():
        raise ValueError("path does not exist: %s" % path)
    if not root.is_dir():
        raise ValueError("path must be a directory: %s" % path)
    return root.resolve()


def _validated_target(root, target):
    raw = "." if target is None else str(target)
    if not raw.strip():
        raise ValueError("target must not be empty")
    target_path = Path(raw)
    if target_path.is_absolute():
        raise ValueError("target must be repository-relative")
    if ".." in target_path.parts:
        raise ValueError("target must not escape the repository")
    resolved = (root / target_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError("target must stay inside the repository")
    if not resolved.exists():
        raise ValueError("target does not exist: %s" % raw)
    rel = target_path.as_posix()
    return resolved, rel if rel not in ("", ".") else "."


def _candidate_bin_dirs(root):
    if os.name == "nt":
        venv_dirs = (
            root / ".venv" / "Scripts",
            root / "venv" / "Scripts",
            root / "env" / "Scripts",
        )
    else:
        venv_dirs = (
            root / ".venv" / "bin",
            root / "venv" / "bin",
            root / "env" / "bin",
        )
    return (root / "node_modules" / ".bin",) + venv_dirs


def _is_within(root, path):
    try:
        Path(path).resolve().relative_to(root)
        return True
    except ValueError:
        return False


def _executable_source(root, executable):
    executable = Path(executable)
    if _is_within(root / "node_modules" / ".bin", executable):
        return "project-bin"
    if any(_is_within(directory, executable)
           for directory in _candidate_bin_dirs(root)[1:]):
        return "project-venv"
    return "path"


def _display_path(root, path):
    path = Path(path)
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.name


def _find_executable(root, names):
    for name in names:
        for directory in _candidate_bin_dirs(root):
            if not directory.is_dir():
                continue
            found = shutil.which(name, path=str(directory))
            if found:
                executable = Path(found)
                return executable, _executable_source(root, executable)
        found = shutil.which(name)
        if found:
            executable = Path(found)
            return executable, _executable_source(root, executable)
    return None, None


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        return ""


def _find_config(root, spec):
    for name in spec["config_names"]:
        if (root / name).is_file():
            return name
    for name, section in spec["config_sections"]:
        path = root / name
        if not path.is_file():
            continue
        text = _read_text(path).lower()
        if "[%s]" % section.lower() in text:
            return name
    return None


def _adapter_state(root, spec):
    executable, source = _find_executable(root, spec["executables"])
    config = _find_config(root, spec)
    available = executable is not None
    config_required = bool(spec["config_required"])
    ready = available and (not config_required or config is not None)
    reason = None
    if not available:
        reason = "adapter-not-installed"
    elif config_required and not config:
        reason = "adapter-config-missing"
    return {
        "id": next(key for key, value in ADAPTER_SPECS.items() if value is spec),
        "package": spec["package"],
        "license": spec["license"],
        "kind": spec["kind"],
        "description": spec["description"],
        "available": available,
        "ready": ready,
        "executable": _display_path(root, executable) if executable else None,
        "executable_source": source,
        "config": config,
        "config_required": config_required,
        "reason": reason,
    }


def _next_step_for_reason(reason, adapter_id):
    if reason == "adapter-not-installed":
        return "install %s in the project environment or PATH" % adapter_id
    if reason == "adapter-config-missing":
        return "add the adapter configuration file at the repository root"
    if reason == "allow-execute-false":
        return "rerun with allow_execute=true"
    if reason == "adapter-output-invalid":
        return "inspect the adapter output and configuration"
    if reason == "adapter-exit-nonzero":
        return "inspect the adapter output and rerun"
    if reason == "adapter-timeout":
        return "increase the timeout or narrow the adapter target"
    if reason == "adapter-execution-failed":
        return "verify the adapter executable and local environment"
    return None


def _list_adapters(root):
    adapters = []
    unknowns = []
    for spec in ADAPTER_SPECS.values():
        state = _adapter_state(root, spec)
        adapters.append(state)
        if not state["ready"]:
            unknowns.append({
                "adapter": state["id"],
                "kind": state["reason"],
                "detail": "%s is not ready" % state["id"],
                "next_step": _next_step_for_reason(state["reason"], state["id"]),
            })
    return {
        "status": "PASS",
        "action": "list",
        "root": str(root),
        "adapters": adapters,
        "unknowns": unknowns,
        "unverified_claims": [],
    }


def _decode(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _clean_output(value):
    return ANSI_RE.sub("", _decode(value)).replace("\r\n", "\n").replace("\r", "\n")


def _hash_output(stdout, stderr):
    payload = stdout.encode("utf-8", errors="replace") + b"\x00" + \
        stderr.encode("utf-8", errors="replace")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _bounded(text, max_chars):
    if max_chars < 1:
        raise ValueError("max_chars must be >= 1")
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars], True


def _child_env():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["NO_COLOR"] = "1"
    env["FORCE_COLOR"] = "0"
    return env


def _run_process(argv, cwd, timeout):
    """Run one fixed argv without a shell. Tests replace this boundary."""
    return subprocess.run(
        [str(item) for item in argv],
        cwd=str(cwd),
        capture_output=True,
        timeout=timeout,
        env=_child_env(),
    )


def _adapter_version(executable, root, timeout):
    try:
        completed = _run_process([str(executable), "--version"], root, min(timeout, 10))
    except Exception:  # noqa: BLE001
        return None
    if completed.returncode != 0:
        return None
    text = _clean_output(completed.stdout or completed.stderr).strip()
    if not text:
        return None
    return text.splitlines()[0].strip() or None


def _base_run_result(root, state):
    adapter = dict(state)
    adapter["version"] = None
    return {
        "status": "UNKNOWN",
        "action": "run",
        "root": str(root),
        "adapter": adapter,
        "command": None,
        "findings": [],
        "content": None,
        "output_excerpt": "",
        "truncated": False,
        "reason": None,
        "next_step": None,
        "unknowns": [],
    }


def _unknown_result(result, reason, detail=None):
    result["status"] = "UNKNOWN"
    result["reason"] = reason
    result["next_step"] = _next_step_for_reason(reason, result["adapter"]["id"])
    result["unknowns"] = [{
        "kind": reason,
        "detail": detail or result["next_step"] or reason,
    }]
    return result


def _import_linter_argv(executable, config):
    return [str(executable), "--config", config]


def _dependency_cruiser_argv(executable, config, target):
    return [
        str(executable),
        "--config", config,
        "--output-type", "json",
        "--progress", "none",
        "--exclude", "node_modules",
        target,
    ]


def _repomix_argv(executable, target, token_budget):
    argv = [
        str(executable),
        "--stdout",
        "--style", "xml",
        "--quiet",
        "--no-git-sort-by-changes",
    ]
    if token_budget is not None:
        argv.extend(["--token-budget", str(token_budget)])
    argv.append(target)
    return argv


def _import_linter_findings(output):
    findings = []
    current_rule = None
    for line in output.splitlines():
        stripped = line.strip()
        broken = re.match(r"^(?P<rule>.+?)\s+BROKEN\s*$", stripped)
        if broken:
            current_rule = broken.group("rule").strip()
            continue
        violation = re.match(
            r"^(?P<source>\S+)\s+is not allowed to import\s+(?P<target>\S+)",
            stripped,
        )
        if violation:
            source = violation.group("source").rstrip(":;, ")
            target = violation.group("target").rstrip(":;, ")
            findings.append({
                "code": "adapter-violation",
                "adapter": "import-linter",
                "rule": current_rule or "lint-imports",
                "severity": "high",
                "path": source,
                "line": None,
                "target": target,
                "message": stripped,
            })
    if not findings:
        findings.append({
            "code": "adapter-violation",
            "adapter": "import-linter",
            "rule": current_rule or "lint-imports",
            "severity": "high",
            "path": None,
            "line": None,
            "target": None,
            "message": "import-linter reported a broken contract",
        })
    return findings


def _severity_from_dependency_cruiser(value):
    normalized = str(value or "info").lower()
    if normalized in ("error", "high", "critical"):
        return "high"
    if normalized in ("warn", "warning", "medium"):
        return "medium"
    return "low"


def _dependency_cruiser_findings(payload):
    violations = ((payload.get("summary") or {}).get("violations")) or []
    findings = []
    for violation in violations:
        rule = violation.get("rule") or {}
        findings.append({
            "code": "adapter-violation",
            "adapter": "dependency-cruiser",
            "rule": rule.get("name") or violation.get("name") or "dependency-cruiser",
            "severity": _severity_from_dependency_cruiser(rule.get("severity")),
            "path": violation.get("from"),
            "line": None,
            "target": violation.get("to"),
            "message": violation.get("comment") or "dependency rule violation",
        })
    return findings


def _normalize_import_linter(result, returncode, stdout, stderr):
    result["findings"] = _import_linter_findings(stdout or stderr)
    if returncode == 0:
        result["status"] = "PASS"
        result["findings"] = []
    elif returncode == 1:
        result["status"] = "FAIL"
        result["next_step"] = "fix the broken import-linter contract"
    else:
        _unknown_result(result, "adapter-exit-nonzero")
    return result


def _normalize_dependency_cruiser(result, returncode, stdout, stderr):
    try:
        payload = json.loads(stdout)
    except (ValueError, TypeError):
        return _unknown_result(result, "adapter-output-invalid")
    result["findings"] = _dependency_cruiser_findings(payload)
    blocking = [item for item in result["findings"] if item["severity"] == "high"]
    if blocking:
        result["status"] = "FAIL"
        result["next_step"] = "fix the dependency-cruiser violations"
    elif returncode == 0:
        result["status"] = "PASS"
    else:
        _unknown_result(result, "adapter-exit-nonzero")
    return result


def _normalize_repomix(result, returncode, stdout, stderr, max_chars, token_budget):
    text, truncated = _bounded(stdout, max_chars)
    result["content"] = {
        "style": "xml",
        "chars": len(stdout),
        "estimated_tokens": max(1, (len(stdout) + 3) // 4),
        "token_budget": token_budget,
        "content_hash": "sha256:" + hashlib.sha256(
            stdout.encode("utf-8", errors="replace")
        ).hexdigest(),
        "truncated": truncated,
        "text": text,
    }
    result["truncated"] = truncated
    if returncode == 0:
        result["status"] = "PASS"
    elif token_budget is not None or "token budget" in (stderr + stdout).lower():
        result["status"] = "FAIL"
        result["findings"] = [{
            "code": "token-budget-exceeded",
            "adapter": "repomix",
            "rule": "token-budget",
            "severity": "high",
            "path": None,
            "line": None,
            "target": None,
            "message": "repomix output exceeded the configured token budget",
        }]
        result["next_step"] = "narrow the target or increase the token budget"
    else:
        _unknown_result(result, "adapter-exit-nonzero")
    return result


def _validate_timeout(timeout):
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 600:
        raise ValueError("timeout must be an integer between 1 and 600")


def _validate_max_chars(max_chars):
    if isinstance(max_chars, bool) or not isinstance(max_chars, int) or \
            not 1000 <= max_chars <= 1000000:
        raise ValueError("max_chars must be an integer between 1000 and 1000000")


def _validate_token_budget(token_budget):
    if token_budget is None:
        return
    if isinstance(token_budget, bool) or not isinstance(token_budget, int) or \
            not 1 <= token_budget <= 500000:
        raise ValueError("token_budget must be an integer between 1 and 500000")


def run_adapter(path, action="list", adapter=None, allow_execute=False, timeout=120,
                max_chars=DEFAULT_MAX_CHARS, token_budget=None, target="."):
    """Probe or explicitly run one optional external adapter."""
    root = _validated_root(path)
    if action not in ("list", "run"):
        raise ValueError("action must be list or run")
    if action == "list":
        return _list_adapters(root)
    if adapter not in ADAPTER_SPECS:
        raise ValueError("unknown adapter: %s" % adapter)
    _validate_timeout(timeout)
    _validate_max_chars(max_chars)
    _validate_token_budget(token_budget)
    target_path, target_rel = _validated_target(root, target)
    del target_path

    spec = ADAPTER_SPECS[adapter]
    state = _adapter_state(root, spec)
    result = _base_run_result(root, state)
    if not state["available"]:
        return _unknown_result(result, "adapter-not-installed")
    if spec["config_required"] and not state["config"]:
        return _unknown_result(result, "adapter-config-missing")
    if not allow_execute:
        return _unknown_result(result, "allow-execute-false")

    executable = None
    for directory in _candidate_bin_dirs(root):
        if not directory.is_dir():
            continue
        executable = shutil.which(spec["executables"][0], path=str(directory))
        if executable:
            break
    if not executable:
        executable = shutil.which(spec["executables"][0])
    if not executable:
        return _unknown_result(result, "adapter-not-installed")
    executable = Path(executable)
    result["adapter"]["version"] = _adapter_version(executable, root, timeout)

    if adapter == "import-linter":
        argv = _import_linter_argv(executable, state["config"])
    elif adapter == "dependency-cruiser":
        argv = _dependency_cruiser_argv(executable, state["config"], target_rel)
    else:
        argv = _repomix_argv(executable, target_rel, token_budget)

    try:
        completed = _run_process(argv, root, timeout)
    except subprocess.TimeoutExpired as exc:
        stdout = _clean_output(exc.stdout)
        stderr = _clean_output(exc.stderr)
        result["command"] = {
            "executable": result["adapter"]["executable"],
            "argv": argv[1:],
            "cwd": ".",
            "exit_code": None,
            "timed_out": True,
            "output_hash": _hash_output(stdout, stderr),
        }
        result["output_excerpt"] = _bounded(stdout or stderr, EXCERPT_LIMIT)[0]
        return _unknown_result(result, "adapter-timeout")
    except OSError:
        return _unknown_result(result, "adapter-execution-failed")

    stdout = _clean_output(completed.stdout)
    stderr = _clean_output(completed.stderr)
    result["command"] = {
        "executable": result["adapter"]["executable"],
        "argv": argv[1:],
        "cwd": ".",
        "exit_code": int(completed.returncode),
        "timed_out": False,
        "output_hash": _hash_output(stdout, stderr),
    }
    result["output_excerpt"], excerpt_truncated = _bounded(
        stdout or stderr, EXCERPT_LIMIT
    )
    if adapter == "repomix":
        return _normalize_repomix(
            result, int(completed.returncode), stdout, stderr, max_chars, token_budget
        )
    result["truncated"] = excerpt_truncated
    if adapter == "import-linter":
        return _normalize_import_linter(result, int(completed.returncode), stdout, stderr)
    return _normalize_dependency_cruiser(result, int(completed.returncode), stdout, stderr)
