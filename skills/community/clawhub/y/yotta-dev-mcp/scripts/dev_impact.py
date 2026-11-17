#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Change impact cone analysis for yotta-dev-mcp."""

import re
from pathlib import Path

import dev_contract
from dev_architecture import _architecture_review_core
from dev_common import (
    BLAST_LEVELS, CONE_LIMIT, EVIDENCE_LIMIT, SYMBOL_MATCH_LIMIT,
    UNKNOWN_LIMIT, _read_text,
)
from dev_model import (
    _decisive_edges, _is_test_file, _module_layers, _risk_weight, system_model,
)


HUNK_RE = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")

SYMBOL_PATTERNS = (
    ("python", r"^\s*(?:async\s+)?def\s+%s\s*\("),
    ("python", r"^\s*class\s+%s\s*[\(:]"),
    ("js", r"^\s*(?:export\s+)?(?:async\s+)?function\s+%s\s*\("),
    ("js", r"^\s*(?:export\s+)?(?:const|let|var)\s+%s\s*="),
    ("js", r"^\s*(?:export\s+)?(?:abstract\s+)?class\s+%s\b"),
    ("go", r"^\s*func\s+(?:\([^)]*\)\s*)?%s\s*\("),
)

SYMBOL_LANGUAGES = {
    "python": ("python",),
    "js": ("javascript", "typescript"),
    "go": ("go",),
}

def _strip_diff_path(raw):
    text = str(raw).strip().split("\t")[0].strip()
    if not text or text == "/dev/null":
        return None
    if text.startswith("a/") or text.startswith("b/"):
        text = text[2:]
    return text.replace("\\", "/")

def _parse_unified_diff(diff_text):
    """Parse a unified diff into changed files plus added/removed line numbers."""
    changes = []
    current = None
    old_path = None
    old_line = 0
    new_line = 0
    for line in str(diff_text).splitlines():
        if line.startswith("--- "):
            old_path = _strip_diff_path(line[4:])
            current = None
            continue
        if line.startswith("+++ "):
            new_path = _strip_diff_path(line[4:])
            if new_path is None:
                if old_path is None:
                    continue
                path, change = old_path, "deleted"
            elif old_path is None:
                path, change = new_path, "added"
            else:
                path, change = new_path, "modified"
            current = {"path": path, "change": change,
                       "changed_lines": [], "removed_lines": []}
            changes.append(current)
            continue
        match = HUNK_RE.match(line)
        if match:
            old_line = int(match.group(1))
            new_line = int(match.group(2))
            continue
        if current is None:
            continue
        if line.startswith("+") and not line.startswith("+++"):
            current["changed_lines"].append(new_line)
            new_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            current["removed_lines"].append(old_line)
            old_line += 1
        elif line.startswith(" "):
            old_line += 1
            new_line += 1
    for item in changes:
        item["changed_lines"] = sorted(set(item["changed_lines"]))
        item["removed_lines"] = sorted(set(item["removed_lines"]))
    return changes

def _symbol_locations(model, root, symbol):
    escaped = re.escape(symbol)
    hits = []
    for module in model["modules"]:
        language = module["language"]
        patterns = [
            re.compile(pattern % escaped)
            for kind, pattern in SYMBOL_PATTERNS
            if language in SYMBOL_LANGUAGES[kind]
        ]
        if not patterns:
            continue
        try:
            text = _read_text(root / module["id"])
        except (OSError, ValueError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if any(pattern.match(line) for pattern in patterns):
                hits.append({"path": module["id"], "line": lineno, "language": language})
                if len(hits) >= SYMBOL_MATCH_LIMIT:
                    return hits
    return hits

def _dependency_cone(model, changed_paths, depth):
    """Reverse-dependency breadth-first cone from the changed modules."""
    consumers = {}
    for edge in _decisive_edges(model):
        consumers.setdefault(edge["target"], []).append(edge)
    module_layers = _module_layers(model)
    test_paths = {item["path"] for item in model["tests"]}
    nodes = {}
    order = []
    for path in sorted(set(changed_paths)):
        nodes[path] = {
            "path": path, "depth": 0, "via": None, "line": None,
            "layer": module_layers.get(path), "is_test": path in test_paths,
        }
        order.append(path)
    truncated = False
    index = 0
    while index < len(order):
        current = order[index]
        index += 1
        node = nodes[current]
        if node["depth"] >= depth:
            continue
        for edge in sorted(consumers.get(current, []),
                           key=lambda item: (item["source"], item["line"])):
            consumer = edge["source"]
            if consumer in nodes:
                continue
            if len(nodes) >= CONE_LIMIT:
                truncated = True
                break
            nodes[consumer] = {
                "path": consumer,
                "depth": node["depth"] + 1,
                "via": current,
                "line": edge["line"],
                "layer": module_layers.get(consumer),
                "is_test": consumer in test_paths,
            }
            order.append(consumer)
        if truncated:
            break
    return nodes, truncated

def _relevant_tests(model, nodes):
    relevant = []
    for item in model["tests"]:
        hits = sorted({target for target in item["targets"] if target in nodes})
        in_cone = item["path"] in nodes
        if not hits and not in_cone:
            continue
        if in_cone:
            depth = nodes[item["path"]]["depth"]
        elif hits:
            depth = min(nodes[target]["depth"] for target in hits) + 1
        else:
            depth = 0
        relevant.append({"path": item["path"], "targets_hit": hits, "depth": depth})
    return sorted(relevant, key=lambda item: item["path"])

def _affected_boundaries(contract, paths):
    affected = []
    for boundary in (contract or {}).get("boundaries") or []:
        matched = sorted(path for path in paths
                         if dev_contract.match_any(path, boundary["paths"] or []))
        if matched:
            affected.append({
                "id": boundary["id"],
                "layer": boundary["layer"],
                "visibility": boundary.get("visibility") or "internal",
                "matched_paths": matched,
            })
    return sorted(affected, key=lambda item: item["id"])

def _affected_data_stores(model, affected_layers, paths):
    affected = []
    for store in model["data_stores"]:
        if store.get("detected"):
            matched = sorted(path for path in paths if path == store["store"])
            if matched:
                affected.append({
                    "store": store["store"],
                    "owner": store.get("owner"),
                    "kind": store.get("kind"),
                    "reason": "changed path is the detected store file",
                    "matched_paths": matched,
                })
            continue
        reasons = []
        matched = sorted(path for path in paths
                         if dev_contract.match_any(path, store["paths"] or []))
        if store.get("owner") in affected_layers:
            reasons.append("owner layer %s is in the impact cone" % store["owner"])
        if matched:
            reasons.append("changed path matches the declared store globs")
        if reasons:
            affected.append({
                "store": store["store"],
                "owner": store.get("owner"),
                "kind": store.get("kind"),
                "reason": "; ".join(reasons),
                "matched_paths": matched,
            })
    return sorted(affected, key=lambda item: item["store"])

def _affected_invariants(contract, paths):
    affected = []
    for invariant in (contract or {}).get("invariants") or []:
        globs = invariant.get("paths") or []
        matched = sorted(path for path in paths
                         if globs and dev_contract.match_any(path, globs))
        if globs and not matched:
            continue
        affected.append({
            "id": invariant["id"],
            "claim": invariant["claim"],
            "severity": invariant.get("severity") or dev_contract.RULE_DEFAULT_SEVERITY,
            "check": invariant.get("check") or "manual",
            "scope": "paths" if globs else "repo",
            "matched_paths": matched,
        })
    return sorted(affected, key=lambda item: item["id"])

def _blast_radius(contract, nodes, affected_layers, boundaries, stores, in_scope):
    reasons = []
    score = 0
    if affected_layers:
        base = max(_risk_weight(contract, layer) for layer in affected_layers)
        weight = int(min(5, base))
        if weight:
            score += weight
            reasons.append({
                "factor": "layer-risk",
                "weight": weight,
                "detail": "highest declared risk among affected layers is %g" % base,
            })
    if len(affected_layers) >= 5:
        score += 2
        reasons.append({"factor": "layer-count", "weight": 2,
                        "detail": "%d layers are affected" % len(affected_layers)})
    elif len(affected_layers) >= 3:
        score += 1
        reasons.append({"factor": "layer-count", "weight": 1,
                        "detail": "%d layers are affected" % len(affected_layers)})
    depth = max((node["depth"] for node in nodes.values()), default=0)
    if depth >= 2:
        score += 1
        reasons.append({"factor": "cone-depth", "weight": 1,
                        "detail": "consumer chain reaches depth %d" % depth})
    public_surface = [item["id"] for item in boundaries if item["visibility"] == "public"]
    if public_surface:
        score += 1
        reasons.append({"factor": "public-boundary", "weight": 1,
                        "detail": "public boundary in scope: %s" % ", ".join(public_surface)})
    if stores:
        weight = min(2, len(stores))
        score += weight
        reasons.append({"factor": "data-store", "weight": weight,
                        "detail": "%d data store(s) touched" % len(stores)})
    blocking = [item for item in in_scope
                if item["severity"] in dev_contract.BLOCKING_SEVERITIES]
    if blocking:
        critical = any(item["severity"] == "critical" for item in blocking)
        weight = 3 if critical else 2
        score += weight
        reasons.append({"factor": "architecture-violation", "weight": weight,
                        "detail": "%d blocking architecture violation(s) in scope"
                                  % len(blocking)})
    capped = min(10, score)
    level = "low"
    for threshold, name in BLAST_LEVELS:
        if capped >= threshold:
            level = name
            break
    return {
        "level": level,
        "score": score,
        "capped_score": capped,
        "capped": score > capped,
        "reasons": reasons,
    }

def _rollback_probes(model, nodes, stores, tests, invariants):
    probes = []
    # Test files that guard on __main__ are runnable, but they are covered by the
    # test probe below; treating them as startup surfaces only adds noise.
    entrypoints = sorted(path for path in set(model["entrypoints"]) & set(nodes)
                         if not _is_test_file(path))[:5]
    for store in stores:
        probes.append({
            "kind": "data-store",
            "target": store["store"],
            "probe": "revert the change and verify %s integrity, or restore it from backup"
                     % store["store"],
            "evidence": store["reason"],
        })
    for entry in entrypoints:
        probes.append({
            "kind": "entrypoint",
            "target": entry,
            "probe": "revert and run %s once to confirm startup still works" % entry,
            "evidence": "entrypoint in the impact cone",
        })
    if tests:
        probes.append({
            "kind": "tests",
            "target": ", ".join(item["path"] for item in tests[:5]),
            "probe": "run the mapped tests before and after revert",
            "evidence": "%d mapped test file(s)" % len(tests),
        })
    for invariant in invariants:
        if invariant["check"] != "command":
            continue
        probes.append({
            "kind": "invariant",
            "target": invariant["id"],
            "probe": "run the declared check for %s after revert" % invariant["id"],
            "evidence": invariant["claim"],
        })
    if not probes:
        probes.append({
            "kind": "model",
            "target": "L0/L1",
            "probe": "no store, entrypoint or test mapping was in scope; rerun the review after revert",
            "evidence": "impact cone produced no probe anchor",
        })
    return probes

def _impact_unverified_claims():
    return [
        {
            "claim": "the change passes its tests",
            "level": "L2-L3",
            "status": "UNVERIFIED",
            "reason": "impact_analysis executes no tests",
        },
        {
            "claim": "behaviour survives mutation and property checks",
            "level": "L4",
            "status": "UNVERIFIED",
            "reason": "impact_analysis runs no mutation or property checks",
        },
        {
            "claim": "an independent reviewer agrees with the change",
            "level": "L5",
            "status": "UNVERIFIED",
            "reason": "independent review stays a human or separate-agent step",
        },
    ]

def impact_analysis(path, changed_files=None, diff=None, symbols=None, depth=3,
                    max_files=2000, contract_file=None):
    """Build a deterministic change impact cone for local changes. Read-only."""
    root = Path(path)
    if not root.exists():
        raise ValueError("路径不存在: %s" % path)
    if not root.is_dir():
        raise ValueError("impact_analysis 需要目录: %s" % path)
    if isinstance(depth, bool) or not isinstance(depth, int) or not 1 <= depth <= 10:
        raise ValueError("depth 必须是 1 到 10 之间的整数")
    requested = [str(item).replace("\\", "/").lstrip("./") for item in (changed_files or [])
                 if str(item).strip()]
    wanted_symbols = [str(item).strip() for item in (symbols or []) if str(item).strip()]
    if not requested and not wanted_symbols and not str(diff or "").strip():
        raise ValueError("impact_analysis 需要 changed_files、diff 或 symbols 至少一项")

    model_result = system_model(str(root), max_files=max_files, contract_file=contract_file)
    model = model_result["model"]
    contract_result = dev_contract.load_contract(root, contract_file=contract_file)
    contract = contract_result["contract"] if contract_result["ok"] else None
    module_layers = _module_layers(model)
    unknowns = [dict(item) for item in model_result["unknowns"]]
    changes = {}
    evidence = []

    def register_changed(rel, change, changed_lines=None, symbols_hit=None, reason=None):
        rel = str(rel).replace("\\", "/").lstrip("./")
        layer = module_layers.get(rel)
        if layer is None and contract:
            matched = dev_contract.match_layers(rel, contract)
            layer = matched[0] if matched else None
        if layer is None and not (root / rel).exists():
            unknowns.append({
                "kind": "change-not-found",
                "id": rel,
                "detail": "the changed path is not in the repository and matches no layer",
                "next_step": "check the path spelling or add a layer glob",
            })
        entry = changes.setdefault(rel, {
            "path": rel,
            "change": change,
            "layer": layer,
            "changed_lines": [],
            "symbols": [],
        })
        if changed_lines:
            entry["changed_lines"] = sorted(set(entry["changed_lines"]) | set(changed_lines))
        if symbols_hit:
            entry["symbols"] = sorted(set(entry["symbols"]) | set(symbols_hit))
        if reason and not entry.get("reason"):
            entry["reason"] = reason
        return entry

    for item in _parse_unified_diff(diff or ""):
        entry = register_changed(item["path"], item["change"],
                                 changed_lines=item["changed_lines"],
                                 reason="unified diff")
        if item["removed_lines"]:
            entry["removed_lines"] = item["removed_lines"]
    for rel in requested:
        in_model = rel in module_layers
        layer_hit = bool(contract and dev_contract.match_layers(rel, contract))
        register_changed(rel, "modified", reason="changed_files")
        if (root / rel).exists() and not in_model and not layer_hit:
            unknowns.append({
                "kind": "change-not-in-model",
                "id": rel,
                "detail": "the file is not part of the source model and matches no layer",
                "next_step": "add a layer glob or check the file type",
            })
    for symbol in wanted_symbols:
        hits = _symbol_locations(model, root, symbol)
        if not hits:
            unknowns.append({
                "kind": "symbol-not-found",
                "id": symbol,
                "detail": "no definition of this symbol was found in the model",
                "next_step": "check the symbol spelling or add the file that defines it",
            })
            continue
        for hit in hits:
            register_changed(hit["path"], "symbol", changed_lines=[hit["line"]],
                             symbols_hit=[symbol], reason="target symbol")

    changed_paths = sorted(changes)
    nodes, cone_truncated = _dependency_cone(model, changed_paths, depth)
    if cone_truncated:
        unknowns.append({
            "kind": "cone-truncated",
            "id": model_result["root"],
            "detail": "the impact cone reached the %d node limit" % CONE_LIMIT,
            "next_step": "raise depth/targets precision and rerun impact_analysis",
        })
    scoped_paths = sorted(nodes)
    direct_consumers = sorted(node["path"] for node in nodes.values() if node["depth"] == 1)
    affected_layers = sorted({node["layer"] for node in nodes.values() if node["layer"]})
    boundaries = _affected_boundaries(contract, scoped_paths)
    stores = _affected_data_stores(model, affected_layers, scoped_paths)
    invariants = _affected_invariants(contract, scoped_paths)
    tests = _relevant_tests(model, nodes)

    core = _architecture_review_core(model_result, contract_result, root)
    scoped = set(scoped_paths)
    for violation in core["violations"]:
        violation["in_cone"] = any(item["path"] in scoped for item in violation["evidence"])
    in_scope = [item for item in core["violations"] if item["in_cone"]]
    blocking_in_scope = [item for item in in_scope
                         if item["severity"] in dev_contract.BLOCKING_SEVERITIES]
    radius = _blast_radius(contract, nodes, affected_layers, boundaries, stores, in_scope)
    probes = _rollback_probes(model, nodes, stores, tests, invariants)

    for path_ in changed_paths:
        entry = changes[path_]
        evidence.append({
            "path": path_,
            "line": (entry["changed_lines"] or [None])[0],
            "detail": "changed (%s)%s" % (
                entry["change"],
                ", layer %s" % entry["layer"] if entry["layer"] else ", no layer",
            ),
        })
    for node in sorted(nodes.values(), key=lambda item: (item["depth"], item["path"])):
        if node["depth"] == 0:
            continue
        evidence.append({
            "path": node["path"],
            "line": node["line"],
            "detail": "consumer of %s at depth %d" % (node["via"], node["depth"]),
        })
    for item in blocking_in_scope:
        for entry in item["evidence"]:
            evidence.append({
                "path": entry["path"],
                "line": entry.get("line"),
                "detail": "%s: %s" % (item["code"], entry["detail"]),
            })
    evidence.sort(key=lambda item: (item["path"], item.get("line") or 0, item["detail"]))
    if len(evidence) > EVIDENCE_LIMIT:
        evidence = evidence[:EVIDENCE_LIMIT]

    unknowns.sort(key=lambda item: (item["kind"], item["id"]))
    deduped = []
    seen_unknowns = set()
    for item in unknowns:
        key = (item["kind"], item.get("id"))
        if key in seen_unknowns:
            continue
        seen_unknowns.add(key)
        deduped.append(item)
    unknowns = deduped
    if blocking_in_scope:
        status = "FAIL"
    elif unknowns or cone_truncated:
        status = "UNKNOWN"
    else:
        status = "PASS"
    return {
        "status": status,
        "root": model_result["root"],
        "inputs": {
            "changed_files": requested,
            "symbols": wanted_symbols,
            "diff_provided": bool(str(diff or "").strip()),
            "depth": depth,
        },
        "changed": [changes[path_] for path_ in changed_paths],
        "direct_consumers": direct_consumers,
        "cone": {
            "nodes": [nodes[path_] for path_ in sorted(
                nodes, key=lambda item: (nodes[item]["depth"], item))],
            "max_depth": max((node["depth"] for node in nodes.values()), default=0),
            "limit": CONE_LIMIT,
            "truncated": cone_truncated,
        },
        "affected_layers": affected_layers,
        "affected_boundaries": boundaries,
        "affected_data_stores": stores,
        "affected_invariants": invariants,
        "relevant_tests": tests,
        "architecture": {
            "status": core["status"],
            "violations_total": len(core["violations"]),
            "violations_in_scope": in_scope,
            "unknowns": core["unknowns"],
        },
        "blast_radius": radius,
        "rollback_probes": probes,
        "unknowns": unknowns,
        "unverified_claims": _impact_unverified_claims(),
        "evidence": evidence,
        "truncated": model_result["truncated"],
        "model_digest": model_result["model_digest"],
    }
