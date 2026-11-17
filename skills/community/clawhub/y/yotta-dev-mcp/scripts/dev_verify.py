#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L0-L5 verification ledger for yotta-dev-mcp."""

import ast
import hashlib
import json
from pathlib import Path

import dev_contract
from dev_common import EVIDENCE_LIMIT, JS_EXTS, VERIFY_EXEC_LEVELS, VERIFY_LEVELS
from dev_impact import impact_analysis


def _run_checks_lazy(kind, cwd, timeout, allow_execute):
    from dev_engine import run_checks
    return run_checks(kind, cwd, timeout=timeout, allow_execute=allow_execute)


def _is_within(root, target):
    try:
        Path(target).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False

def _ledger_entry(check_id, level, claim, status, severity="info", evidence=None,
                  next_step=None, command=None, confidence="high"):
    return {
        "id": check_id,
        "level": level,
        "claim": claim,
        "status": status,
        "severity": severity,
        "check": "verify_change",
        "confidence": confidence,
        "evidence": sorted(
            list(evidence or []),
            key=lambda item: (item.get("path") or "", item.get("line") or 0,
                              item.get("detail") or ""),
        ),
        "next_step": next_step,
        "command": command,
    }

def _verify_contract_result(contract_result):
    if not contract_result["present"]:
        return "UNKNOWN", [{
            "path": contract_result["path"],
            "line": None,
            "detail": "architecture contract is missing",
        }], "add .yotta/architecture.json"
    if not contract_result["ok"]:
        evidence = []
        for item in contract_result["findings"]:
            if item["severity"] in dev_contract.BLOCKING_SEVERITIES:
                evidence.append({
                    "path": item["path"],
                    "line": None,
                    "detail": "%s: %s" % (item["code"], item["message"]),
                })
        return "FAIL", evidence, "fix the contract findings and rerun verify_change"
    return "PASS", [], None

def _verify_syntax(changed, root):
    evidence = []
    unknown = []
    for item in changed:
        rel = item["path"]
        if item.get("change") == "deleted":
            continue
        target = root / rel
        if not target.is_file():
            continue
        suffix = target.suffix.lower()
        if suffix not in (".py", ".json") and suffix not in JS_EXTS:
            continue
        if suffix in JS_EXTS:
            unknown.append({
                "path": rel,
                "line": None,
                "detail": "no zero-dependency JavaScript parser is available at L0",
            })
            continue
        try:
            text = target.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            unknown.append({
                "path": rel,
                "line": None,
                "detail": "file could not be read: %s" % exc,
            })
            continue
        try:
            if suffix == ".py":
                ast.parse(text, filename=rel)
            else:
                json.loads(text)
        except SyntaxError as exc:
            evidence.append({
                "path": rel,
                "line": exc.lineno,
                "detail": "syntax error: %s" % exc.msg,
            })
        except json.JSONDecodeError as exc:
            evidence.append({
                "path": rel,
                "line": exc.lineno,
                "detail": "JSON error: %s" % exc.msg,
            })
    if evidence:
        return "FAIL", evidence, "fix the syntax error(s) and rerun verify_change", []
    if unknown:
        return "UNKNOWN", unknown, "use an L2-L4 adapter or a language-specific parser", unknown
    return "PASS", [], None, []

def _verify_architecture(impact):
    architecture = impact["architecture"]
    blocking = [
        item for item in architecture["violations_in_scope"]
        if item["severity"] in dev_contract.BLOCKING_SEVERITIES
    ]
    if blocking:
        evidence = []
        for item in blocking:
            for entry in item["evidence"]:
                evidence.append({
                    "path": entry["path"],
                    "line": entry.get("line"),
                    "detail": "%s (%s): %s" % (
                        item["rule"], item["code"], entry.get("detail") or "",
                    ),
                })
        return "FAIL", evidence, "fix the in-scope architecture violation(s)"
    scoped = {item["path"] for item in impact["cone"]["nodes"]}
    always_relevant = {
        "contract-missing", "contract-invalid", "model-truncated", "cone-truncated",
        "change-not-found", "symbol-not-found",
    }
    unknowns = []
    for item in list(architecture.get("unknowns") or []) + list(impact.get("unknowns") or []):
        kind = item.get("kind")
        identifier = str(item.get("id") or "")
        if kind in always_relevant or not identifier:
            unknowns.append(item)
        elif identifier in scoped:
            unknowns.append(item)
        elif any(path and path in identifier for path in scoped):
            unknowns.append(item)
    if unknowns:
        evidence = [{
            "path": item.get("id") or item.get("path") or "",
            "line": None,
            "detail": "%s: %s" % (item.get("kind"), item.get("detail") or ""),
        } for item in unknowns]
        return "UNKNOWN", evidence, "resolve the unknown evidence and rerun verify_change"
    return "PASS", [], None

def _verify_policy_entries(root, policy, execution_levels, allow_execute, timeout):
    ledger = []
    unverified = []
    for level in execution_levels:
        checks = [item for item in policy["checks"] if item["level"] == level]
        if not checks:
            ledger.append(_ledger_entry(
                "%s-policy" % level, level,
                "%s verification is declared" % level,
                "UNKNOWN", severity="high",
                evidence=[{"path": policy["path"], "line": None,
                           "detail": "no %s checks are declared" % level}],
                next_step="declare a whitelisted %s check in .yotta/verification.json" % level,
            ))
            unverified.append({
                "level": level,
                "claim": "%s verification is declared and executed" % level,
                "status": "UNVERIFIED",
                "reason": "verification-level-not-declared",
                "required": True,
                "next_step": "declare a whitelisted check in .yotta/verification.json",
            })
            continue
        for check in checks:
            check_id = "%s-%s" % (level, check["id"])
            claim = check["claim"] or "%s check %s passes" % (level, check["id"])
            if not allow_execute:
                ledger.append(_ledger_entry(
                    check_id, level, claim, "UNVERIFIED",
                    severity="high" if check["required"] else "medium",
                    next_step="rerun with allow_execute=true",
                ))
                unverified.append({
                    "level": level,
                    "claim": claim,
                    "status": "UNVERIFIED",
                    "reason": "allow_execute=false",
                    "required": check["required"],
                    "next_step": "rerun with allow_execute=true",
                })
                continue
            cwd = (root / check["cwd"]).resolve()
            if not _is_within(root, cwd) or not cwd.is_dir():
                ledger.append(_ledger_entry(
                    check_id, level, claim, "FAIL", severity="high",
                    evidence=[{"path": check["cwd"], "line": None,
                               "detail": "check cwd is not a directory inside the repository"}],
                    next_step="fix the policy cwd and rerun verify_change",
                ))
                continue
            try:
                result = _run_checks_lazy(
                    check["kind"], str(cwd),
                    timeout=min(timeout, check["timeout"]),
                    allow_execute=True,
                )
            except Exception as exc:  # noqa: BLE001
                ledger.append(_ledger_entry(
                    check_id, level, claim, "FAIL", severity="high",
                    evidence=[{"path": check["cwd"], "line": None,
                               "detail": "check could not run: %s" % exc}],
                    next_step="fix the verification policy or local toolchain",
                ))
                continue
            output = result.get("output") or ""
            command = {
                "kind": result["kind"],
                "cwd": check["cwd"],
                "exit_code": result["exit_code"],
                "output_hash": hashlib.sha256(output.encode("utf-8")).hexdigest(),
                "summary": result.get("summary") or "",
                "timed_out": bool(result.get("timed_out")),
            }
            status = "PASS" if result.get("passed") else "FAIL"
            ledger.append(_ledger_entry(
                check_id, level, claim, status,
                severity="high" if check["required"] else "medium",
                evidence=[{"path": check["cwd"], "line": None,
                           "detail": result.get("summary") or "check finished"}],
                next_step=None if status == "PASS"
                          else "inspect the check output and fix the failure",
                command=command,
            ))
    return sorted(ledger, key=lambda item: (item["level"], item["id"])), unverified

def verify_change(path, changed_files=None, diff=None, symbols=None, depth=3,
                  levels=None, allow_execute=False, timeout=120,
                  max_files=2000, contract_file=None, policy_file=None):
    """Run the L0-L5 verification ladder and return a deterministic evidence ledger.

    L0/L1 always run in-process. L2-L4 run only when both a whitelisted
    .yotta/verification.json check is declared and allow_execute is true.
    L5 is always recorded as manual work and is never auto-verified.
    """
    root = Path(path)
    if not root.exists():
        raise ValueError("路径不存在: %s" % path)
    if not root.is_dir():
        raise ValueError("verify_change 需要目录: %s" % path)
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 600:
        raise ValueError("timeout 必须是 1 到 600 之间的整数")
    requested = list(levels or [])
    for level in requested:
        if level not in VERIFY_LEVELS:
            raise ValueError("level 必须是 L0-L5 之一: %s" % level)
    execution_levels = [level for level in VERIFY_EXEC_LEVELS if level in requested]

    impact = impact_analysis(
        str(root), changed_files=changed_files, diff=diff, symbols=symbols,
        depth=depth, max_files=max_files, contract_file=contract_file,
    )
    contract_result = dev_contract.load_contract(root, contract_file=contract_file)
    policy = dev_contract.load_verification_policy(root, policy_file=policy_file)

    ledger = []
    unverified = []

    contract_status, contract_evidence, contract_next = _verify_contract_result(contract_result)
    ledger.append(_ledger_entry(
        "L0-contract", "L0", "the architecture contract is valid",
        contract_status, severity="high",
        evidence=contract_evidence, next_step=contract_next,
    ))

    syntax_status, syntax_evidence, syntax_next, syntax_unknown = _verify_syntax(
        impact["changed"], root
    )
    ledger.append(_ledger_entry(
        "L0-syntax", "L0", "changed source files parse",
        syntax_status, severity="high",
        evidence=syntax_evidence, next_step=syntax_next,
    ))
    if syntax_unknown:
        unverified.append({
            "level": "L0",
            "claim": "changed JavaScript or TypeScript files parse",
            "status": "UNVERIFIED",
            "reason": "no zero-dependency JavaScript parser",
            "required": False,
            "next_step": "add a language adapter or run an explicit parser check",
        })

    architecture_status, architecture_evidence, architecture_next = _verify_architecture(impact)
    advisory = [
        item for item in impact["architecture"]["violations_in_scope"]
        if item["severity"] not in dev_contract.BLOCKING_SEVERITIES
    ]
    if architecture_status == "PASS" and advisory:
        architecture_evidence = [{
            "path": entry["path"],
            "line": entry.get("line"),
            "detail": "%s (%s): %s" % (
                item["rule"], item["code"], entry.get("detail") or "",
            ),
        } for item in advisory for entry in item["evidence"]]
    ledger.append(_ledger_entry(
        "L1-architecture", "L1", "in-scope architecture rules and boundaries hold",
        architecture_status, severity="high",
        evidence=architecture_evidence, next_step=architecture_next,
    ))

    for invariant in impact["affected_invariants"]:
        unverified.append({
            "level": "L1",
            "claim": invariant["claim"],
            "status": "UNVERIFIED",
            "reason": "invariant requires a static, command or manual check",
            "required": False,
            "next_step": "add a verification policy check or complete the manual review",
        })

    if execution_levels:
        if not policy["present"]:
            for level in execution_levels:
                ledger.append(_ledger_entry(
                    "%s-policy" % level, level,
                    "%s verification policy is present" % level,
                    "UNKNOWN", severity="high",
                    evidence=[{"path": policy["path"], "line": None,
                               "detail": "verification policy is missing"}],
                    next_step="add .yotta/verification.json with whitelisted checks",
                ))
                unverified.append({
                    "level": level,
                    "claim": "%s verification is declared and executed" % level,
                    "status": "UNVERIFIED",
                    "reason": "verification-policy-missing",
                    "required": True,
                    "next_step": "add .yotta/verification.json",
                })
        elif not policy["ok"]:
            evidence = [{
                "path": item["path"],
                "line": None,
                "detail": "%s: %s" % (item["code"], item["message"]),
            } for item in policy["findings"]
                if item["severity"] in dev_contract.BLOCKING_SEVERITIES]
            for level in execution_levels:
                ledger.append(_ledger_entry(
                    "%s-policy" % level, level,
                    "%s verification policy is valid" % level,
                    "FAIL", severity="high", evidence=evidence,
                    next_step="fix .yotta/verification.json and rerun verify_change",
                ))
        else:
            execution_ledger, execution_unverified = _verify_policy_entries(
                root, policy, execution_levels, allow_execute, timeout,
            )
            ledger.extend(execution_ledger)
            unverified.extend(execution_unverified)

    verified_levels = {
        item["level"] for item in ledger
        if item["status"] in ("PASS", "FAIL")
    }
    for level in VERIFY_EXEC_LEVELS:
        if level not in verified_levels and not any(
            item["level"] == level for item in unverified
        ):
            unverified.append({
                "level": level,
                "claim": "%s verification level is covered by evidence" % level,
                "status": "UNVERIFIED",
                "reason": "level-not-requested",
                "required": False,
                "next_step": "request this level and provide a verification policy",
            })
    if "L5" not in requested:
        unverified.append({
            "level": "L5",
            "claim": "independent review or manual architecture approval",
            "status": "UNVERIFIED",
            "reason": "manual verification required",
            "required": False,
            "next_step": "complete an independent review or manual architecture decision",
        })
    else:
        unverified.append({
            "level": "L5",
            "claim": "independent review or manual architecture approval",
            "status": "UNVERIFIED",
            "reason": "manual verification required",
            "required": True,
            "next_step": "complete an independent review or manual architecture decision",
        })

    unverified.sort(key=lambda item: (item["level"], item["claim"], item["reason"]))
    ledger.sort(key=lambda item: (item["level"], item["id"]))
    failed = any(item["status"] == "FAIL" for item in ledger)
    unknown = any(item["status"] == "UNKNOWN" for item in ledger) or any(
        item["required"] for item in unverified
    )
    if failed:
        status = "FAIL"
    elif unknown:
        status = "UNKNOWN"
    else:
        status = "PASS"
    required_levels = ["L0", "L1"]
    for item in ledger:
        if item["level"] in VERIFY_EXEC_LEVELS and item["status"] in ("PASS", "FAIL"):
            required_levels.append(item["level"])
    required_levels = sorted(set(required_levels), key=lambda item: int(item[1:]))
    evidence = []
    for item in ledger:
        evidence.extend(item["evidence"])
    if len(evidence) > EVIDENCE_LIMIT:
        evidence = evidence[:EVIDENCE_LIMIT]
    ledger_digest = hashlib.sha256(
        json.dumps(ledger, ensure_ascii=False, sort_keys=True,
                   separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "status": status,
        "root": str(root.resolve()),
        "inputs": {
            "changed_files": list(changed_files or []),
            "symbols": list(symbols or []),
            "diff_provided": bool(str(diff or "").strip()),
            "levels": requested,
            "allow_execute": bool(allow_execute),
            "depth": depth,
        },
        "required_levels": required_levels,
        "ledger": ledger,
        "unverified_claims": unverified,
        "policy": policy,
        "evidence": evidence,
        "ledger_digest": ledger_digest,
        "model_digest": impact["model_digest"],
        "impact_status": impact["status"],
    }
