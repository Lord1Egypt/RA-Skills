#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-test and counterexample probes for yotta-dev-mcp."""

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from dev_architecture import architecture_review
from dev_common import (
    EVIDENCE_LIMIT, LEAN_INSTALL_MARKERS, VERIFY_REQUIRED_INSTALLED_ASSETS,
    VERIFY_REQUIRED_INSTALLED_FILES,
    VERIFY_REQUIRED_SOURCE_FILES, VERIFY_WRITE_GATES, _frontmatter_version,
    _read_text,
)


def _function_default(source_text, function_name, parameter_name):
    try:
        tree = ast.parse(source_text)
    except SyntaxError:
        return False, None
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name != function_name:
            continue
        positional = list(node.args.args)
        defaults = list(node.args.defaults)
        offset = len(positional) - len(defaults)
        for index, argument in enumerate(positional):
            if argument.arg != parameter_name or index < offset:
                continue
            try:
                return True, ast.literal_eval(defaults[index - offset])
            except (ValueError, SyntaxError):
                return True, "<non-literal>"
    return False, None

def _string_constant(node):
    return isinstance(node, ast.Constant) and isinstance(node.value, str)

def _is_lean_install(root):
    return any((root / marker).is_file() for marker in LEAN_INSTALL_MARKERS)

def _protocol_tool_contracts(source_text):
    tree = ast.parse(source_text)
    function = None
    for node in tree.body:
        # v0.2.2 起工具清单字面量在 _all_tools()；mcp_tools(profile) 只做分档过滤。
        if isinstance(node, ast.FunctionDef) and node.name in ("_all_tools", "mcp_tools"):
            function = node
            break
    if function is None:
        raise ValueError("tool list function not found")
    list_node = None
    for node in ast.walk(function):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.List):
            list_node = node.value
            break
    if list_node is None:
        raise ValueError("tool list function does not return a literal tool list")
    contracts = []
    for element in list_node.elts:
        if not isinstance(element, ast.Dict):
            raise ValueError("tool list contains a non-literal tool entry")
        values = {}
        for key, value in zip(element.keys, element.values):
            if _string_constant(key):
                values[key.value] = value
        name_node = values.get("name")
        if name_node is None:
            raise ValueError("tool entry is missing name")
        try:
            name = ast.literal_eval(name_node)
        except (ValueError, SyntaxError):
            raise ValueError("tool name is not a literal string")
        schema = values.get("inputSchema")
        additional = False
        if isinstance(schema, ast.Dict):
            for key, value in zip(schema.keys, schema.values):
                if _string_constant(key) and key.value == "additionalProperties":
                    try:
                        additional = ast.literal_eval(value) is False
                    except (ValueError, SyntaxError):
                        additional = False
        contracts.append({"name": name, "additional_properties": additional})
    return contracts

def _dispatch_tool_names(source_text):
    tree = ast.parse(source_text)
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name != "dispatch":
            continue
        for child in ast.walk(node):
            if not isinstance(child, ast.Assign):
                continue
            if not any(isinstance(target, ast.Name) and target.id == "handlers"
                       for target in child.targets):
                continue
            if not isinstance(child.value, ast.Dict):
                continue
            names = []
            for key in child.value.keys:
                if _string_constant(key):
                    names.append(key.value)
                else:
                    try:
                        names.append(ast.literal_eval(key))
                    except (ValueError, SyntaxError):
                        pass
            return sorted(names)
    raise ValueError("dispatch() handler map not found")

def _self_test_counterexamples():
    probes = []

    def record(kind, name, expectation, observed, passed, detail):
        probes.append({
            "kind": kind,
            "name": name,
            "expectation": expectation,
            "observed": observed,
            "passed": bool(passed),
            "detail": detail,
        })

    with tempfile.TemporaryDirectory(prefix="yotta-dev-mcp-selftest-") as tmp:
        root = Path(tmp)

        def write(rel, text):
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")

        contract = {
            "version": 1,
            "layers": [
                {"id": "core", "paths": ["core/**"]},
                {"id": "ui", "paths": ["ui/**"]},
            ],
            "rules": [{
                "id": "core-no-ui",
                "type": "forbid-dependency",
                "from": "core",
                "to": "ui",
                "severity": "high",
                "claim": "core must not import ui",
            }],
        }
        write(".yotta/architecture.json", json.dumps(contract))
        write("core/leak.py", "from ui.view import VALUE\n")
        write("ui/view.py", "VALUE = 1\n")

        try:
            observed = architecture_review(str(root))["status"]
            detail = "seeded core -> ui dependency was reviewed"
        except Exception as exc:  # noqa: BLE001
            observed = "error"
            detail = str(exc)
        record("seeded-defect", "forbidden dependency", "FAIL", observed,
               observed == "FAIL", detail)

        contract["rules"] = []
        write(".yotta/architecture.json", json.dumps(contract))
        try:
            observed = architecture_review(str(root))["status"]
            detail = "same defect with the rule removed"
        except Exception as exc:  # noqa: BLE001
            observed = "error"
            detail = str(exc)
        record("mutation-control", "remove the rule", "not FAIL", observed,
               observed != "FAIL", detail)

        contract["version"] = 3
        write(".yotta/architecture.json", json.dumps(contract))
        try:
            observed = architecture_review(str(root))["status"]
            detail = "unsupported contract version"
        except Exception as exc:  # noqa: BLE001
            observed = "error"
            detail = str(exc)
        record("invalid-contract", "unsupported version", "FAIL or UNKNOWN",
               observed, observed in ("FAIL", "UNKNOWN"), detail)

        (root / ".yotta" / "architecture.json").unlink()
        try:
            observed = architecture_review(str(root))["status"]
            detail = "missing contract"
        except Exception as exc:  # noqa: BLE001
            observed = "error"
            detail = str(exc)
        record("missing-contract", "no architecture contract", "UNKNOWN",
               observed, observed == "UNKNOWN", detail)

        write("secret.env", "TOKEN=abcdefghijklmnopqrstuvwxyz123456\n")
        try:
            from dev_engine import scan_secrets
            observed = len(scan_secrets(str(root))["findings"])
            passed = observed >= 1
            detail = "seeded token was scanned"
        except Exception as exc:  # noqa: BLE001
            observed = "error"
            passed = False
            detail = str(exc)
        record("secret-scan", "seeded credential", "at least one finding",
               observed, passed, detail)

        write("package.json", json.dumps({"name": "probe", "version": "1.0.0"}))
        write("SKILL.md", "---\nname: probe\nversion: 2.0.0\n---\n")
        write("README.md", "# probe\n")
        write("LICENSE", "MIT\n")
        write("CHANGELOG.md", "## v1.0.0\n")
        try:
            from dev_engine import check_publish_readiness
            readiness = check_publish_readiness(str(root))
            codes = {item["code"] for item in readiness["issues"]}
            observed = "FAIL" if not readiness["ok"] else "PASS"
            passed = not readiness["ok"] and "version-mismatch" in codes
            detail = "seeded package/SKILL version mismatch"
        except Exception as exc:  # noqa: BLE001
            observed = "error"
            passed = False
            detail = str(exc)
        record("publish-check", "seeded version mismatch", "FAIL",
               observed, passed, detail)
    return probes

def _self_test_version_check(root, mode):
    if mode == "installed":
        skill = root / "SKILL.md"
        version = _frontmatter_version(_read_text(skill)) if skill.is_file() else None
        if not version:
            return "FAIL", [{"code": "missing-version", "path": "SKILL.md",
                             "detail": "SKILL.md has no version field"}], \
                "restore a valid SKILL.md version"
        version_file = root / "VERSION"
        if version_file.is_file():
            file_version = _read_text(version_file).strip()
            if not file_version:
                return "FAIL", [{"code": "missing-version", "path": "VERSION",
                                 "detail": "VERSION is empty"}], \
                    "restore a valid VERSION file"
            if file_version != version:
                return "FAIL", [{
                    "code": "version-mismatch", "path": "VERSION",
                    "detail": "VERSION=%s SKILL.md=%s" % (file_version, version),
                }], "align VERSION and SKILL.md versions"
        return "PASS", [], None

    versions = {}
    try:
        package = json.loads(_read_text(root / "package.json"))
        versions["package.json"] = package.get("version")
    except Exception as exc:  # noqa: BLE001
        return "FAIL", [{"code": "invalid-package-json", "path": "package.json",
                         "detail": str(exc)}], "fix package.json"
    for rel in ("SKILL.md", "CHANGELOG.md", "server.json"):
        target = root / rel
        if not target.is_file():
            versions[rel] = None
            continue
        if rel == "server.json":
            try:
                versions[rel] = json.loads(_read_text(target)).get("version")
            except Exception:  # noqa: BLE001
                versions[rel] = None
        elif rel == "CHANGELOG.md":
            match = re.search(r"(?m)^##\s+v?(\d+\.\d+\.\d+)", _read_text(target))
            versions[rel] = match.group(1) if match else None
        else:
            versions[rel] = _frontmatter_version(_read_text(target))
    engine_path = root / "scripts" / "dev_engine.py"
    if engine_path.is_file():
        match = re.search(r'(?m)^VERSION\s*=\s*["\']([^"\']+)["\']',
                          _read_text(engine_path))
        versions["engine"] = match.group(1) if match else None
    else:
        versions["engine"] = None
    version_path = root / "VERSION"
    if version_path.is_file():
        versions["VERSION"] = _read_text(version_path).strip() or None
    missing = sorted(key for key, value in versions.items() if not value)
    if missing:
        return "FAIL", [{
            "code": "missing-version", "path": missing[0],
            "detail": "version is missing from: %s" % ", ".join(missing),
        }], "restore version alignment"
    values = {value for value in versions.values() if value}
    if len(values) != 1:
        return "FAIL", [{
            "code": "version-mismatch", "path": "package.json",
            "detail": json.dumps(versions, ensure_ascii=False, sort_keys=True),
        }], "align package, SKILL, CHANGELOG, server, VERSION and engine versions"
    return "PASS", [], None

def _self_test_skill_version_body(root):
    skill = root / "SKILL.md"
    if not skill.is_file():
        return "UNKNOWN", [{
            "code": "skill-missing", "path": "SKILL.md",
            "detail": "SKILL.md is missing",
        }], "restore SKILL.md"
    text = _read_text(skill)
    version = _frontmatter_version(text)
    if not version:
        return "FAIL", [{
            "code": "missing-version", "path": "SKILL.md",
            "detail": "SKILL.md has no version field",
        }], "restore a valid SKILL.md version"
    section = re.search(r"(?ms)^##\s+当前版本\s*$(.*?)(?=^##\s+|\Z)", text)
    if not section:
        return "UNKNOWN", [{
            "code": "version-section-missing", "path": "SKILL.md",
            "detail": "SKILL.md has no 当前版本 section",
        }], "add a 当前版本 section"
    if not re.search(r"(?m)^\s*-\s*v?%s\b" % re.escape(version), section.group(1)):
        return "FAIL", [{
            "code": "version-section-drift", "path": "SKILL.md",
            "detail": "current version %s is not listed in 当前版本" % version,
        }], "add the current version to 当前版本"
    return "PASS", [], None

def _self_test_tool_contracts(root):
    protocol_path = root / "scripts" / "yotta_dev_mcp.py"
    engine_path = root / "scripts" / "dev_engine.py"
    if not protocol_path.is_file() or not engine_path.is_file():
        return "FAIL", [{
            "code": "missing-protocol-source", "path": "scripts",
            "detail": "protocol or engine source is missing",
        }], "restore the protocol and engine sources"
    try:
        contracts = _protocol_tool_contracts(_read_text(protocol_path))
        dispatch_names = _dispatch_tool_names(_read_text(engine_path))
    except (OSError, ValueError, SyntaxError) as exc:
        return "FAIL", [{
            "code": "tool-contract-parse-error", "path": "scripts",
            "detail": str(exc),
        }], "fix the protocol or engine source"
    protocol_names = [item["name"] for item in contracts]
    evidence = []
    if len(protocol_names) != len(set(protocol_names)):
        evidence.append({"code": "tool-name-duplicate", "path": "scripts/yotta_dev_mcp.py",
                         "detail": "duplicate tool names in mcp_tools()"})
    if set(protocol_names) != set(dispatch_names):
        evidence.append({
            "code": "tool-name-drift", "path": "scripts/yotta_dev_mcp.py",
            "detail": "protocol=%s dispatch=%s" % (
                ",".join(sorted(protocol_names)), ",".join(sorted(dispatch_names)),
            ),
        })
    drifted_schema = sorted(
        item["name"] for item in contracts if not item["additional_properties"]
    )
    if drifted_schema:
        evidence.append({
            "code": "tool-schema-drift", "path": "scripts/yotta_dev_mcp.py",
            "detail": "inputSchema.additionalProperties is not false for: %s"
                      % ", ".join(drifted_schema),
        })
    if evidence:
        return "FAIL", evidence, "align the protocol schemas with the engine handlers"
    return "PASS", [], None

def _self_test_write_gates(root):
    engine_path = root / "scripts" / "dev_engine.py"
    if not engine_path.is_file():
        return "FAIL", [{"code": "missing-engine-source", "path": "scripts/dev_engine.py",
                         "detail": "engine source is missing"}], "restore the engine source"
    text = _read_text(engine_path)
    evidence = []
    for function_name, parameter in VERIFY_WRITE_GATES:
        found, value = _function_default(text, function_name, parameter)
        if not found:
            evidence.append({
                "code": "write-gate-missing",
                "path": "scripts/dev_engine.py",
                "detail": "%s(%s=...) was not found" % (function_name, parameter),
            })
        elif value is not False:
            evidence.append({
                "code": "write-gate-drift",
                "path": "scripts/dev_engine.py",
                "detail": "%s.%s default is %r, expected False"
                          % (function_name, parameter, value),
            })
    if evidence:
        return "FAIL", evidence, "restore fail-closed defaults for write and execute gates"
    return "PASS", [], None

def _self_test_detect_test_kind(root):
    package_path = root / "package.json"
    if package_path.is_file():
        try:
            package = json.loads(_read_text(package_path))
            scripts = package.get("scripts") or {}
            if isinstance(scripts, dict) and scripts.get("test"):
                return "npm-test"
        except Exception:  # noqa: BLE001
            pass
    if list(root.glob("test*.py")) or list(root.glob("tests/test*.py")):
        return "python-unittest"
    return None

def self_test(path, mode="auto", allow_execute=False, timeout=120):
    """Run deterministic integrity and counterexample checks on yotta-dev-mcp itself."""
    root = Path(path)
    if not root.exists():
        raise ValueError("路径不存在: %s" % path)
    if not root.is_dir():
        raise ValueError("self_test 需要目录: %s" % path)
    if mode not in ("auto", "source", "installed"):
        raise ValueError("mode 必须是 auto、source 或 installed")
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 600:
        raise ValueError("timeout 必须是 1 到 600 之间的整数")
    if mode == "auto":
        if ((root / "package.json").is_file()
                or (root / "scripts" / "yotta_dev_mcp.py").is_file()):
            mode = "source"
        elif (root / "SKILL.md").is_file():
            mode = "installed"
        else:
            mode = "source"

    if mode == "source":
        required = list(VERIFY_REQUIRED_SOURCE_FILES)
    else:
        required = list(VERIFY_REQUIRED_INSTALLED_FILES)
        # Lean distribution strips assets/ by platform policy; only require
        # the banner when the copy is not lean or it already ships assets/.
        if not _is_lean_install(root) or (root / "assets").is_dir():
            required.extend(VERIFY_REQUIRED_INSTALLED_ASSETS)
    missing = [rel for rel in required if not (root / rel).is_file()]
    files_check = {
        "id": "files",
        "status": "FAIL" if missing else "PASS",
        "severity": "high",
        "claim": "required %s files are present" % mode,
        "evidence": [{
            "code": "missing-file", "path": rel,
            "detail": "required file is missing",
        } for rel in missing],
        "next_step": "restore the missing files" if missing else None,
    }

    version_status, version_evidence, version_next = _self_test_version_check(root, mode)
    version_check = {
        "id": "versions" if mode == "source" else "skill-version",
        "status": version_status,
        "severity": "high",
        "claim": ("package, SKILL, CHANGELOG, server and engine versions align"
                  if mode == "source" else "SKILL.md declares a version"),
        "evidence": version_evidence,
        "next_step": version_next,
    }

    checks = [files_check, version_check]
    unverified = []
    if mode == "source":
        body_status, body_evidence, body_next = _self_test_skill_version_body(root)
        checks.append({
            "id": "skill-version-body",
            "status": body_status,
            "severity": "high",
            "claim": "SKILL.md current-version section lists the frontmatter version",
            "evidence": body_evidence,
            "next_step": body_next,
        })
        tool_status, tool_evidence, tool_next = _self_test_tool_contracts(root)
        checks.append({
            "id": "tool-contracts",
            "status": tool_status,
            "severity": "high",
            "claim": "protocol tool schemas match the engine dispatch handlers",
            "evidence": tool_evidence,
            "next_step": tool_next,
        })
        gate_status, gate_evidence, gate_next = _self_test_write_gates(root)
        checks.append({
            "id": "write-gates",
            "status": gate_status,
            "severity": "high",
            "claim": "write and execute gates default to fail-closed",
            "evidence": gate_evidence,
            "next_step": gate_next,
        })
    else:
        unverified.extend([
            {"level": "L0", "claim": "protocol tool schemas match engine handlers",
             "status": "UNVERIFIED", "reason": "installed mode has no protocol source",
             "required": False, "next_step": "run self_test on the source checkout"},
            {"level": "L0", "claim": "write and execute gates default to fail-closed",
             "status": "UNVERIFIED", "reason": "installed mode has no engine source",
             "required": False, "next_step": "run self_test on the source checkout"},
        ])

    probes = _self_test_counterexamples()
    probe_failed = [item for item in probes if not item["passed"]]
    checks.append({
        "id": "verifier-counterexamples",
        "status": "FAIL" if probe_failed else "PASS",
        "severity": "high",
        "claim": "seeded defects and mutation controls turn the verifier red or unknown",
        "evidence": probes,
        "next_step": "fix the verifier so every counterexample is detected"
                     if probe_failed else None,
    })

    if allow_execute:
        kind = _self_test_detect_test_kind(root)
        if kind is None:
            checks.append({
                "id": "tests",
                "status": "UNKNOWN",
                "severity": "medium",
                "claim": "the project test suite passes",
                "evidence": [{"code": "test-runner-missing", "path": ".",
                              "detail": "no whitelisted test runner was detected"}],
                "next_step": "declare a test script or add test_*.py files",
            })
        else:
            try:
                from dev_engine import run_checks
                result = run_checks(kind, str(root), timeout=timeout,
                                    allow_execute=True)
                output = result.get("output") or ""
                checks.append({
                    "id": "tests",
                    "status": "PASS" if result.get("passed") else "FAIL",
                    "severity": "high",
                    "claim": "the project test suite passes",
                    "evidence": [{"code": "test-run", "path": ".",
                                  "detail": result.get("summary") or "test run finished"}],
                    "next_step": None if result.get("passed")
                                else "fix the failing tests and rerun self_test",
                    "command": {
                        "kind": kind,
                        "cwd": ".",
                        "exit_code": result.get("exit_code"),
                        "output_hash": hashlib.sha256(
                            output.encode("utf-8")
                        ).hexdigest(),
                        "timed_out": bool(result.get("timed_out")),
                    },
                })
            except Exception as exc:  # noqa: BLE001
                checks.append({
                    "id": "tests",
                    "status": "FAIL",
                    "severity": "high",
                    "claim": "the project test suite passes",
                    "evidence": [{"code": "test-run-error", "path": ".",
                                  "detail": str(exc)}],
                    "next_step": "fix the local test runner",
                })
    else:
        unverified.append({
            "level": "L2",
            "claim": "the project test suite passes",
            "status": "UNVERIFIED",
            "reason": "allow_execute=false",
            "required": False,
            "next_step": "rerun self_test with allow_execute=true",
        })

    failed = any(item["status"] == "FAIL" for item in checks)
    unknown = any(item["status"] == "UNKNOWN" for item in checks)
    if failed:
        status = "FAIL"
    elif unknown:
        status = "UNKNOWN"
    else:
        status = "PASS"
    counts = {
        "passed": sum(1 for item in checks if item["status"] == "PASS"),
        "failed": sum(1 for item in checks if item["status"] == "FAIL"),
        "unknown": sum(1 for item in checks if item["status"] == "UNKNOWN"),
        "unverified": len(unverified),
    }
    evidence = []
    for item in checks:
        evidence.extend(item.get("evidence") or [])
    return {
        "status": status,
        "root": str(root.resolve()),
        "mode": mode,
        "checks": checks,
        "unverified_claims": unverified,
        "summary": counts,
        "evidence": evidence[:EVIDENCE_LIMIT],
    }
