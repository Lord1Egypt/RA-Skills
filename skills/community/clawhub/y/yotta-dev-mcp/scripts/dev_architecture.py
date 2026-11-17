#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Architecture contract review for yotta-dev-mcp."""

import json
from pathlib import Path

import dev_contract
from dev_common import EVIDENCE_LIMIT, UNKNOWN_LIMIT, _read_text
from dev_model import (
    _decisive_edges, _edge_evidence, _module_layers, _risk_weight,
    system_model,
)


def _glob_literal_prefix(pattern):
    text = str(pattern or "")
    for marker in ("*", "?"):
        index = text.find(marker)
        if index >= 0:
            text = text[:index]
    return text.rstrip("/")

def _review_rules(contract, model, unknown_sink, violation_sink):
    module_layers = _module_layers(model)
    edges = sorted(_decisive_edges(model),
                   key=lambda item: (item["source"], item["line"], item["target"]))
    checked = []
    for rule in contract["rules"]:
        severity = rule.get("severity") or dev_contract.RULE_DEFAULT_SEVERITY
        source_modules = [
            item["id"] for item in model["modules"]
            if module_layers.get(item["id"]) == rule["from"]
        ]
        violations = 0
        undecided = 0
        decisive = 0
        seen_targets = set()
        for edge in edges:
            if module_layers.get(edge["source"]) != rule["from"]:
                continue
            target_layer = module_layers.get(edge["target"])
            if target_layer is None:
                if edge["kind"] == "internal" and edge["target"] not in seen_targets:
                    seen_targets.add(edge["target"])
                    undecided += 1
                    unknown_sink.append({
                        "kind": "rule-target-unassigned",
                        "id": "%s -> %s" % (rule["id"], edge["target"]),
                        "rule": rule["id"],
                        "target": edge["target"],
                        "detail": "the target module has no layer, so the rule cannot be decided",
                        "next_step": "assign the module to a layer or narrow the rule",
                    })
                continue
            decisive += 1
            if rule["type"] == "forbid-dependency":
                broke = target_layer == rule["to"]
                message = rule.get("claim") or (
                    "%s must not import %s" % (rule["from"], rule["to"]))
                code = "rule-forbid-dependency"
            else:
                broke = target_layer not in (rule["to"] or [])
                message = rule.get("claim") or (
                    "%s may only import %s" % (rule["from"], ", ".join(rule["to"] or [])))
                code = "rule-allow-dependency"
            if not broke:
                continue
            violations += 1
            violation_sink.append({
                "code": code,
                "rule": rule["id"],
                "severity": severity,
                "message": message,
                "from_layer": rule["from"],
                "to_layer": target_layer,
                "evidence": [_edge_evidence(
                    edge,
                    "imports %s (layer %s), which breaks %s"
                    % (edge["target"], target_layer, rule["id"]),
                )],
            })
        if violations and severity in dev_contract.BLOCKING_SEVERITIES:
            status = "FAIL"
        elif violations:
            status = "WARN"
        elif undecided:
            status = "UNKNOWN"
        elif decisive == 0:
            status = "UNKNOWN"
            if source_modules:
                unknown_sink.append({
                    "kind": "rule-no-evidence",
                    "id": rule["id"],
                    "rule": rule["id"],
                    "detail": "the from layer has modules but no decisive import was found",
                    "next_step": "add an import that exercises this rule or remove the rule",
                })
            else:
                unknown_sink.append({
                    "kind": "rule-no-source-modules",
                    "id": rule["id"],
                    "rule": rule["id"],
                    "detail": "the from layer has no modules to review",
                    "next_step": "add modules to the from layer or remove the rule",
                })
        else:
            status = "PASS"
        checked.append({
            "id": rule["id"],
            "type": rule["type"],
            "from": rule["from"],
            "to": rule["to"],
            "severity": severity,
            "claim": rule.get("claim"),
            "status": status,
            "source_modules": len(source_modules),
            "decided_imports": decisive,
            "violations": violations,
            "undecided_imports": undecided,
        })
    return checked

def _review_boundaries(contract, model, unknown_sink, violation_sink):
    module_layers = _module_layers(model)
    edges = sorted(_decisive_edges(model),
                   key=lambda item: (item["source"], item["line"], item["target"]))
    checked = []
    for boundary in contract["boundaries"]:
        paths = boundary["paths"] or []
        protected = sorted(item["id"] for item in model["modules"]
                           if dev_contract.match_any(item["id"], paths))
        visibility = boundary.get("visibility") or "internal"
        severity = "high" if visibility == "private" else "medium"
        violations = 0
        undecided = 0
        consumers = 0
        seen_importers = set()
        if not protected:
            unknown_sink.append({
                "kind": "boundary-no-modules",
                "id": boundary["id"],
                "detail": "no module matches the boundary globs",
                "next_step": "point the boundary at existing modules or drop it",
            })
        protected_set = set(protected)
        for edge in edges:
            if edge["target"] not in protected_set:
                continue
            consumers += 1
            importer = edge["source"]
            if dev_contract.match_any(importer, paths) or visibility == "public":
                continue
            importer_layer = module_layers.get(importer)
            if importer_layer is None:
                if importer not in seen_importers:
                    seen_importers.add(importer)
                    undecided += 1
                    unknown_sink.append({
                        "kind": "boundary-importer-unassigned",
                        "id": "%s <- %s" % (boundary["id"], importer),
                        "boundary": boundary["id"],
                        "target": importer,
                        "detail": "the importer has no layer, so boundary visibility is undecided",
                        "next_step": "assign the importer to a layer",
                    })
                continue
            if visibility == "internal" and importer_layer == boundary["layer"]:
                continue
            violations += 1
            violation_sink.append({
                "code": "boundary-visibility",
                "rule": boundary["id"],
                "severity": severity,
                "message": "module outside the %s boundary imports it (visibility %s)"
                           % (boundary["id"], visibility),
                "boundary": boundary["id"],
                "layer": boundary["layer"],
                "visibility": visibility,
                "evidence": [_edge_evidence(
                    edge,
                    "imports %s, protected by the %s boundary (%s)"
                    % (edge["target"], boundary["id"], visibility),
                )],
            })
        if violations and severity in dev_contract.BLOCKING_SEVERITIES:
            status = "FAIL"
        elif violations:
            status = "WARN"
        elif undecided or not protected:
            status = "UNKNOWN"
        else:
            status = "PASS"
        checked.append({
            "id": boundary["id"],
            "layer": boundary["layer"],
            "visibility": visibility,
            "paths": list(paths),
            "status": status,
            "protected_modules": protected,
            "imports_of_protected_modules": consumers,
            "violations": violations,
            "undecided_imports": undecided,
        })
    return checked

def _review_data_ownership(contract, model, root, violation_sink):
    module_layers = _module_layers(model)
    stores = contract["data_ownership"]
    prefixes = {}
    for store in stores:
        candidates = [_glob_literal_prefix(item) for item in store["paths"] or []]
        prefixes[store["store"]] = sorted(item for item in candidates if len(item) >= 4)
    needed = sorted({item for values in prefixes.values() for item in values})
    texts = {}
    if needed:
        for module in model["modules"]:
            if module.get("layer") is None:
                continue
            try:
                texts[module["id"]] = _read_text(root / module["id"])
            except (OSError, ValueError):
                continue
    checked = []
    for store in stores:
        owner = store["owner"]
        paths = store["paths"] or []
        violations = 0
        mismatched = sorted(item["id"] for item in model["modules"]
                            if dev_contract.match_any(item["id"], paths)
                            and item.get("layer") != owner)
        for rel in mismatched:
            violations += 1
            violation_sink.append({
                "code": "data-ownership-mismatch",
                "rule": store["store"],
                "severity": "medium",
                "message": "module inside the store paths belongs to layer %s, not the owner %s"
                           % (module_layers.get(rel), owner),
                "store": store["store"],
                "owner": owner,
                "evidence": [{"path": rel, "line": 1, "detail":
                              "matches the declared paths of store %s" % store["store"]}],
            })
        references = 0
        store_prefixes = prefixes.get(store["store"]) or []
        if store_prefixes:
            for rel in sorted(texts):
                if module_layers.get(rel) == owner:
                    continue
                for lineno, line in enumerate(texts[rel].splitlines(), 1):
                    if any(prefix in line for prefix in store_prefixes):
                        references += 1
                        violations += 1
                        violation_sink.append({
                            "code": "data-store-access-outside-owner",
                            "rule": store["store"],
                            "severity": "medium",
                            "message": "layer %s references the store owned by %s"
                                       % (module_layers.get(rel), owner),
                            "store": store["store"],
                            "owner": owner,
                            "evidence": [{
                                "path": rel,
                                "line": lineno,
                                "detail": "references the %s store path" % store["store"],
                                "snippet": line.strip()[:200],
                            }],
                        })
                        break
        owner_modules = sorted(item["id"] for item in model["modules"]
                               if item.get("layer") == owner)
        checked.append({
            "store": store["store"],
            "owner": owner,
            "kind": store.get("kind"),
            "paths": list(paths),
            "status": "WARN" if violations else "PASS",
            "owner_modules": len(owner_modules),
            "mismatched_modules": mismatched,
            "references_outside_owner": references,
        })
    return checked

def _review_invariants(contract, unverified_sink):
    checked = []
    for invariant in contract["invariants"]:
        check = invariant.get("check") or "manual"
        if check == "static":
            reason = "no built-in evaluator covers this claim yet"
        elif check == "command":
            reason = "architecture_review never executes commands"
        else:
            reason = "human review is required"
        unverified_sink.append({
            "claim": invariant["claim"],
            "level": "L1",
            "status": "UNVERIFIED",
            "reason": reason,
            "invariant": invariant["id"],
            "check": check,
            "severity": invariant.get("severity") or dev_contract.RULE_DEFAULT_SEVERITY,
            "paths": list(invariant.get("paths") or []),
        })
        checked.append({
            "id": invariant["id"],
            "claim": invariant["claim"],
            "check": check,
            "severity": invariant.get("severity") or dev_contract.RULE_DEFAULT_SEVERITY,
            "paths": list(invariant.get("paths") or []),
            "status": "UNVERIFIED",
            "reason": reason,
        })
    return checked

def _architecture_review_core(model_result, contract_result, root):
    """Shared review core: evaluate the contract against one system model."""
    contract = contract_result.get("contract") if contract_result.get("ok") else None
    violations = []
    unknowns = [dict(item) for item in model_result["unknowns"]]
    unverified = []
    evidence = []
    checked = {"rules": [], "boundaries": [], "data_stores": [], "invariants": []}
    if contract:
        checked["rules"] = _review_rules(contract, model_result["model"], unknowns, violations)
        checked["boundaries"] = _review_boundaries(
            contract, model_result["model"], unknowns, violations)
        checked["data_stores"] = _review_data_ownership(
            contract, model_result["model"], root, violations)
        checked["invariants"] = _review_invariants(contract, unverified)
    if model_result["truncated"]:
        unknowns.append({
            "kind": "model-truncated",
            "id": model_result["root"],
            "detail": "the file limit cut the scan short; some modules were not reviewed",
            "next_step": "raise max_files and rerun the review",
        })
    blocking = [item for item in violations
                if item["severity"] in dev_contract.BLOCKING_SEVERITIES]
    advisory = [item for item in violations
                if item["severity"] not in dev_contract.BLOCKING_SEVERITIES]
    contract_blocking = [item for item in model_result["contract"]["findings"]
                         if item["severity"] in dev_contract.BLOCKING_SEVERITIES]
    for item in violations:
        for entry in item["evidence"]:
            evidence.append({
                "path": entry["path"],
                "line": entry.get("line"),
                "detail": "%s: %s" % (item["code"], entry["detail"]),
            })
    for item in model_result["contract"]["findings"]:
        evidence.append({
            "path": model_result["contract"]["path"],
            "pointer": item["pointer"],
            "detail": "%s: %s" % (item["severity"], item["message"]),
        })
    evidence.sort(key=lambda item: (item["path"], item.get("line") or 0, item["detail"]))
    if len(evidence) > EVIDENCE_LIMIT:
        evidence = evidence[:EVIDENCE_LIMIT]
    if contract_blocking or blocking:
        status = "FAIL"
    elif not model_result["contract"]["present"] or unknowns:
        status = "UNKNOWN"
    else:
        status = "PASS"
    violations.sort(key=lambda item: (item["code"], item["rule"], item["evidence"][0]["path"]))
    unknowns.sort(key=lambda item: (item["kind"], item["id"]))
    return {
        "status": status,
        "checked": checked,
        "violations": violations,
        "blocking_findings": len(blocking) + len(contract_blocking),
        "advisory_findings": len(advisory),
        "unknowns": unknowns,
        "unverified_claims": unverified,
        "evidence": evidence,
    }

def architecture_review(path, max_files=2000, contract_file=None):
    """Review a repository against `.yotta/architecture.json`. Read-only."""
    root = Path(path)
    if not root.exists():
        raise ValueError("路径不存在: %s" % path)
    if not root.is_dir():
        raise ValueError("architecture_review 需要目录: %s" % path)
    model_result = system_model(str(root), max_files=max_files, contract_file=contract_file)
    contract_result = dev_contract.load_contract(root, contract_file=contract_file)
    core = _architecture_review_core(model_result, contract_result, root)
    return {
        "status": core["status"],
        "root": model_result["root"],
        "contract": model_result["contract"],
        "checked": core["checked"],
        "violations": core["violations"],
        "blocking_findings": core["blocking_findings"],
        "advisory_findings": core["advisory_findings"],
        "unknowns": core["unknowns"],
        "unverified_claims": core["unverified_claims"],
        "evidence": core["evidence"],
        "truncated": model_result["truncated"],
        "model_digest": model_result["model_digest"],
    }
