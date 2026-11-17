#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic system model for yotta-dev-mcp."""

import ast
import hashlib
import json
import os
import posixpath
import re
from pathlib import Path

import dev_contract
from dev_common import (
    CONFIG_NAMES, CONFIG_SUFFIXES, EVIDENCE_LIMIT, IGNORE_DIRS,
    IMPORT_KINDS_DECISIVE, JS_EXTS, RISK_ENUM_WEIGHTS, SOURCE_EXTS,
    STORAGE_SUFFIXES, TEST_NAME_RE,
    UNKNOWN_LIMIT, _iter_files, _language, _read_text, _rel, source_exts,
)


def _resolve_python_import(source_rel, node):
    source = Path(source_rel)
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if not isinstance(node, ast.ImportFrom):
        return []
    if node.level:
        parts = list(source.with_suffix("").parts[:-1])
        if node.level > 1:
            parts = parts[:-(node.level - 1)] if len(parts) >= node.level - 1 else []
        prefix = "/".join(parts)
        if not node.module:
            return [
                (prefix + "/" + alias.name.replace(".", "/")).strip("/")
                for alias in node.names
            ]
        module = node.module or ""
        target = (prefix + "/" + module.replace(".", "/")).strip("/")
        return [target] if target else [source_rel]
    if node.module:
        return [node.module]
    return []

def _repo_map_python(path, rel):
    text = _read_text(path)
    imports = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for target in _resolve_python_import(rel, node):
                imports.append({
                    "source": rel,
                    "target": target,
                    "line": getattr(node, "lineno", 1),
                    "relative": isinstance(node, ast.ImportFrom) and bool(node.level),
                })
    return imports

def _repo_map_js(path, rel):
    text = _read_text(path)
    imports = []
    patterns = [
        re.compile(r"""(?:from\s+|import\s*\()\s*['"]([^'"]+)['"]"""),
        re.compile(r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)"""),
    ]
    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern in patterns:
            for match in pattern.finditer(line):
                imports.append({"source": rel, "target": match.group(1), "line": lineno})
    return imports

def _resolve_relative_module(raw_target, source_rel, module_set, root=None):
    base = posixpath.normpath(posixpath.join(posixpath.dirname(source_rel), raw_target))
    if base.startswith("..") or base.startswith("/"):
        return None, None
    candidates = [base + ext for ext in JS_EXTS]
    candidates.extend(base + "/index" + ext for ext in JS_EXTS)
    candidates.append(base)
    for candidate in candidates:
        if candidate in module_set:
            return candidate, "module"
    if root is not None and (Path(root) / base).is_file():
        return base, "file"
    return None, None

def _classify_python_import(raw_target, source_rel, module_set, relative=False):
    if raw_target.endswith(".py"):
        if raw_target in module_set:
            return "internal", raw_target
        return "unresolved", raw_target
    dotted = raw_target.replace(".", "/")
    source_dir = posixpath.dirname(source_rel)
    bases = [dotted]
    if source_dir:
        bases.insert(0, posixpath.join(source_dir, dotted))
    for base in bases:
        for candidate in (base + ".py", base + "/__init__.py"):
            if candidate in module_set:
                return "internal", candidate
    return ("unresolved" if relative else "external"), raw_target

def _classify_js_import(raw_target, source_rel, module_set, root=None):
    if raw_target.startswith("."):
        resolved, kind = _resolve_relative_module(raw_target, source_rel, module_set, root)
        if kind == "module":
            return "internal", resolved
        if kind == "file":
            return "internal-file", resolved
        return "unresolved", raw_target
    return "external", raw_target

def _is_test_file(rel):
    parts = rel.split("/")
    if any(part in ("tests", "test", "__tests__", "spec") for part in parts[:-1]):
        return True
    return bool(TEST_NAME_RE.match(parts[-1]))

def _config_kind(name):
    suffix = Path(name).suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix == ".toml":
        return "toml"
    if suffix in (".yml", ".yaml"):
        return "yaml"
    if suffix in (".ini", ".cfg"):
        return "ini"
    return "text"

def _collect_files_by_suffix(root, suffixes, limit=200):
    root = Path(root)
    found = []
    for current, dirs, files in os.walk(str(root)):
        dirs[:] = sorted(d for d in dirs if d not in IGNORE_DIRS)
        for name in sorted(files):
            path = Path(current) / name
            if path.is_symlink():
                continue
            if path.suffix.lower() in suffixes:
                found.append(path)
                if len(found) >= limit:
                    return found
    return found

def _collect_configs(root, limit=200):
    root = Path(root)
    configs = []
    for current, dirs, files in os.walk(str(root)):
        dirs[:] = sorted(d for d in dirs if d not in IGNORE_DIRS)
        for name in sorted(files):
            path = Path(current) / name
            if path.is_symlink():
                continue
            if name in CONFIG_NAMES or path.suffix.lower() in CONFIG_SUFFIXES:
                configs.append({"path": _rel(root, path), "kind": _config_kind(name)})
                if len(configs) >= limit:
                    return configs
    return configs

def _collect_store_files(root, limit=200):
    root = Path(root)
    stores = []
    for path in _collect_files_by_suffix(root, set(STORAGE_SUFFIXES), limit=limit):
        stores.append({
            "path": _rel(root, path),
            "kind": STORAGE_SUFFIXES[path.suffix.lower()],
        })
    return stores

def _unverified_claims():
    return [
        {
            "claim": "architecture rules hold for this model",
            "level": "L1",
            "status": "UNVERIFIED",
            "reason": "system_model only builds the model; rule checking runs in architecture_review",
        },
        {
            "claim": "changed code still passes its tests",
            "level": "L2-L4",
            "status": "UNVERIFIED",
            "reason": "system_model executes no tests, mutations or property checks",
        },
    ]

def system_model(path, max_files=2000, contract_file=None):
    """Build the system model and attach architecture contract layer data."""
    root = Path(path)
    if not root.exists():
        raise ValueError("路径不存在: %s" % path)
    if not root.is_dir():
        raise ValueError("system_model 需要目录: %s" % path)
    if max_files < 1:
        raise ValueError("max_files 必须 >= 1")

    contract_result = dev_contract.load_contract(root, contract_file=contract_file)
    contract = contract_result["contract"]
    contract_usable = bool(
        contract_result["present"] and contract_result["ok"] and contract
    )

    unknowns = []
    evidence = []
    if not contract_result["present"]:
        unknowns.append({
            "kind": "contract-missing",
            "id": contract_result["path"],
            "detail": "no architecture contract found",
            "next_step": "add %s with layers, rules and data ownership" % contract_result["path"],
        })
    elif not contract_result["ok"]:
        blocking = [item for item in contract_result["findings"]
                    if item["severity"] in dev_contract.BLOCKING_SEVERITIES]
        unknowns.append({
            "kind": "contract-invalid",
            "id": contract_result["path"],
            "detail": "%d blocking finding(s); layer data is not applied" % len(blocking),
            "next_step": "fix the contract findings and rerun system_model",
        })
    for finding in contract_result["findings"]:
        evidence.append({
            "path": finding["path"],
            "pointer": finding["pointer"],
            "detail": "%s: %s" % (finding["severity"], finding["message"]),
        })

    files = list(_iter_files(root, source_exts(), max_files=max_files + 1))
    truncated = len(files) > max_files
    if truncated:
        files = files[:max_files]
    module_set = {_rel(root, item) for item in files}

    modules = []
    imports = []
    entrypoints = []
    tests = []
    for file_path in files:
        rel = _rel(root, file_path)
        try:
            text = _read_text(file_path)
        except (OSError, ValueError):
            continue
        language = _language(file_path)
        layer = None
        if contract_usable:
            matched = dev_contract.match_layers(rel, contract)
            if not matched:
                unknowns.append({
                    "kind": "unassigned-module",
                    "id": rel,
                    "detail": "no layer glob matches this module",
                    "next_step": "add a layer paths glob in %s" % contract_result["path"],
                })
            elif len(matched) > 1:
                layer = matched[0]
                unknowns.append({
                    "kind": "layer-overlap",
                    "id": rel,
                    "layers": matched,
                    "detail": "module matches %d layers; first declaration wins" % len(matched),
                    "next_step": "narrow the overlapping layer globs",
                })
            else:
                layer = matched[0]
        modules.append({
            "id": rel,
            "language": language,
            "lines": len(text.splitlines()),
            "layer": layer,
        })
        suffix = file_path.suffix.lower()
        if suffix == ".py":
            raw_imports = _repo_map_python(file_path, rel)
        elif suffix in JS_EXTS:
            raw_imports = _repo_map_js(file_path, rel)
        else:
            raw_imports = []
        module_imports = []
        for raw in raw_imports:
            target_raw = raw["target"]
            if target_raw == rel:
                continue
            if suffix == ".py":
                kind, target = _classify_python_import(
                    target_raw, rel, module_set, relative=raw.get("relative", False)
                )
            else:
                kind, target = _classify_js_import(target_raw, rel, module_set, root)
            entry = {
                "source": rel,
                "target": target,
                "kind": kind,
                "line": raw["line"],
                "raw": target_raw,
            }
            module_imports.append(entry)
            imports.append(entry)
            if kind == "unresolved":
                unknowns.append({
                    "kind": "unresolved-import",
                    "id": rel,
                    "line": raw["line"],
                    "detail": "relative import does not resolve: %s" % target_raw,
                    "next_step": "check the import path or add the missing module",
                })
                evidence.append({
                    "path": rel,
                    "line": raw["line"],
                    "detail": "unresolved relative import: %s" % target_raw,
                })
        if _is_test_file(rel):
            tests.append({
                "path": rel,
                "targets": sorted({item["target"] for item in module_imports
                                   if item["kind"] == "internal"}),
            })
        if (
            file_path.name in ("main.py", "cli.py", "app.py", "index.js", "index.ts")
            or "if __name__ == '__main__'" in text
            or 'if __name__ == "__main__"' in text
        ):
            entrypoints.append(rel)

    layer_summaries = []
    if contract_usable:
        for layer in contract["layers"]:
            layer_summaries.append({
                "id": layer["id"],
                "title": layer["title"],
                "risk": layer["risk"],
                "paths": layer["paths"],
                "modules": sorted(item["id"] for item in modules
                                  if item["layer"] == layer["id"]),
            })

    data_stores = []
    if contract_usable:
        for store in contract["data_ownership"]:
            data_stores.append({
                "store": store["store"],
                "owner": store["owner"],
                "kind": store["kind"] or "unknown",
                "paths": store["paths"],
                "owner_modules": sorted(item["id"] for item in modules
                                        if item["layer"] == store["owner"]),
                "detected": False,
            })
            for store_path in store["paths"]:
                evidence.append({
                    "path": store_path,
                    "detail": "declared data ownership: %s" % store["store"],
                })
    for item in _collect_store_files(root):
        matched = dev_contract.match_layers(item["path"], contract) if contract_usable else []
        owner = matched[0] if matched else None
        data_stores.append({
            "store": item["path"],
            "owner": owner,
            "kind": item["kind"],
            "paths": [item["path"]],
            "owner_modules": sorted(m["id"] for m in modules if owner and m["layer"] == owner),
            "detected": True,
        })
        evidence.append({
            "path": item["path"],
            "detail": "detected local data store file (%s)" % item["kind"],
        })
    data_stores.sort(key=lambda item: item["store"])

    model = {
        "modules": sorted(modules, key=lambda item: item["id"]),
        "layers": layer_summaries,
        "imports": sorted(imports, key=lambda item: (item["source"], item["line"], item["target"])),
        "entrypoints": sorted(set(entrypoints)),
        "tests": sorted(tests, key=lambda item: item["path"]),
        "configs": _collect_configs(root),
        "data_stores": data_stores,
    }
    digest = hashlib.sha256(
        json.dumps(model, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    unknowns.sort(key=lambda item: (item["kind"], item["id"], item.get("line", 0)))
    unknowns_truncated = len(unknowns) > UNKNOWN_LIMIT
    evidence.sort(key=lambda item: (item["path"], item.get("line", 0), item["detail"]))
    if len(evidence) > EVIDENCE_LIMIT:
        evidence = evidence[:EVIDENCE_LIMIT]
    if contract_result["present"] and not contract_result["ok"]:
        status = "FAIL"
    elif unknowns:
        status = "UNKNOWN"
    else:
        status = "PASS"
    return {
        "status": status,
        "root": str(root.resolve()),
        "contract": {
            "path": contract_result["path"],
            "present": contract_result["present"],
            "ok": contract_result["ok"],
            "version": contract_result["version"],
            "layers": contract_result["layers"],
            "rules": contract_result["rules"],
            "findings": contract_result["findings"],
        },
        "model": model,
        "unknowns": unknowns[:UNKNOWN_LIMIT],
        "unknowns_truncated": unknowns_truncated,
        "unverified_claims": _unverified_claims(),
        "evidence": evidence,
        "truncated": truncated,
        "model_digest": "sha256:" + digest,
    }

def _module_layers(model):
    return {item["id"]: item.get("layer") for item in model["modules"]}

def _risk_weight(contract, layer_id):
    """Risk weight for a layer: explicit risk_weights, else the risk enum."""
    if not layer_id:
        return 0.0
    weights = (contract or {}).get("risk_weights") or {}
    value = weights.get(layer_id)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        value = None
        for layer in (contract or {}).get("layers") or []:
            if layer.get("id") == layer_id:
                value = RISK_ENUM_WEIGHTS.get(layer.get("risk"), 1)
                break
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        value = 1
    return float(max(0, min(5, value)))

def _decisive_edges(model):
    return [edge for edge in model["imports"] if edge["kind"] in IMPORT_KINDS_DECISIVE]

def _edge_evidence(edge, detail):
    return {
        "path": edge["source"],
        "line": edge["line"],
        "detail": detail,
        "snippet": edge.get("raw"),
    }
