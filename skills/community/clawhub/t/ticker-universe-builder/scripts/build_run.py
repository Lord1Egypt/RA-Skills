"""Resumable local build receipts; research and network retries remain agent-owned."""

from __future__ import annotations

import hashlib
import json
import shlex
from datetime import datetime, timezone
from pathlib import Path

from universe_core import (
    PROFILES,
    UniverseError,
    build_universe,
    load_policy,
    market_guidance,
    normalize_snapshot,
    read_json,
    write_artifacts,
)


def save(path: Path, value: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def diagnostics(spec: dict, snapshot: dict, policy: dict, seed: dict | None = None) -> dict:
    """Admission checks are the core's; these counts never authorize a build."""
    try:
        normalized = normalize_snapshot(
            snapshot, coverage_first=policy.get("selection_model") == "coverage_first"
        )
        if policy.get("selection_model") == "coverage_first":
            result = {
                "selection_model": "coverage_first",
                "coverage_plan_present": bool(snapshot.get("coverage_plan")),
                "admissions": sum(bool(c.get("admission")) for c in normalized["candidates"]),
                "candidates": len(normalized["candidates"]),
                "note": "Research necessary representatives and unresolved Core decisions "
                        "first; do not pad capacity.",
            }
            if spec.get("profile") == "max" and seed and seed.get("profile") == "heavy":
                from collections import Counter

                from coverage_core import expansion_distribution, expansion_minimum

                held = {c["asset_id"] for c in seed["members"]}
                minimum = expansion_minimum(len(held), policy)
                maximum = spec.get("target_count") or snapshot["coverage_plan"]["budgets"]["max"]
                proposed = {
                    c["asset_id"] for c in normalized["candidates"]
                    if c["eligible"] and c["asset_id"] not in held
                    and (c.get("admission") or {}).get("kind") == "satellite"
                }
                mapping, counts, caps = expansion_distribution(seed, minimum - len(held))
                available = Counter(mapping.get(c["theme_code"], c["theme_code"])
                                    for c in normalized["candidates"]
                                    if c["asset_id"] in proposed)
                result["expansion"] = {
                    "heavy_entities": len(held), "min_entities": minimum,
                    "max_entities": maximum, "eligible_proposed_additions": len(proposed),
                    "minimum_candidate_gap": max(0, minimum - len(held) - len(proposed)),
                    "distribution_capacity": sum(min(n, available[k]) for k, n in caps.items()),
                    "distribution": {k: {"heavy": counts[k], "added_cap": n,
                                         "proposed": available[k]}
                                     for k, n in sorted(caps.items())},
                    "note": "Snapshot capacity only; evidence, sector, satellite and export "
                            "gates still apply.",
                }
                required_added = minimum - len(held)
                capacity = result["expansion"]["distribution_capacity"]
                cause = (
                    "candidate_supply"
                    if len(proposed) < required_added
                    else "group_distribution"
                    if capacity < required_added
                    else "other_limits_or_facts"
                )
                result["recovery"] = {
                    "cause": cause,
                    "missing_groups": [k for k in sorted(caps) if available[k] < caps[k]],
                    "strategy": [
                        "Review primary business assignments and peer gauges; "
                        "correct facts, not fit-chase.",
                        "Research candidates in deficient groups; "
                        "do not redirect their places to surplus groups.",
                        "Check broad business, named-core complementarity, "
                        "sourced market cap and liquidity; "
                        "price beta is descriptive, not an admission floor.",
                        "Resume with materially revised sourced inputs; keep previous deliveries.",
                    ],
                }
                bench = [c for c in normalized["candidates"]
                         if c["asset_id"] not in held
                         and (c.get("admission") or {}).get("kind") == "satellite"]
                result["recovery"]["price_diagnostics"] = {
                    metric: {"required": False,
                             "available": sum(c["metrics"].get(metric) is not None for c in bench),
                             "missing": sum(c["metrics"].get(metric) is None for c in bench)}
                    for metric in ("factor_r2", "beta_strength", "beta_stability")
                }
                result["recovery"]["metric_count_note"] = (
                    "Auxiliary price metrics over the researched non-Heavy satellite bench; "
                    "availability is not an admission gate or proof of business quality.")
            return result
        guide = market_guidance(spec["market"], policy, normalized["market_spec"])
        stages = {}
        for profile in PROFILES[: PROFILES.index(spec["profile"]) + 1]:
            level = policy["profiles"][profile]["coverage_level"]
            themes = {
                t["theme_code"] for t in normalized["taxonomy"] if t["coverage_level"] <= level
            }
            bench = [
                c for c in normalized["candidates"] if c["eligible"] and c["theme_code"] in themes
            ]
            target = (
                spec.get("target_count") or guide[profile]["target"]
                if profile == spec["profile"]
                else guide[profile]["target"]
            )
            count = len({c["asset_id"] for c in bench})
            stages[profile] = {
                "target": target,
                "eligible_unique_assets": count,
                "capacity_shortfall": max(0, target - count),
                "missing_themes": sorted(themes - {c["theme_code"] for c in bench}),
                "unrepresented_duties": sorted(
                    t["theme_code"] for t in normalized["taxonomy"]
                    if t["theme_code"] in themes and t.get("representative_roles") and not any(
                        c["theme_code"] == t["theme_code"] and
                        c["role"] in t["representative_roles"] for c in bench)
                ),
                "qualified_beta_candidates": sum(c["role"] == "BETA_SATELLITE" for c in bench),
            }
        return {
            "stages": stages,
            "note": (
                "Capacity describes only the supplied research snapshot, not the whole market. "
                "Research unmapped inventory before declaring a source capacity ceiling; "
                "seed and token limits still apply."
            ),
        }
    except (UniverseError, KeyError, ValueError, TypeError) as exc:
        return {"input_error": str(exc)}


def run_build(
    *,
    spec: str | None,
    snapshot: str | None,
    output: str | None,
    policy: str | None = None,
    seed: str | None = None,
    language: str | None = None,
    run_dir: str | None = None,
    resume: str | None = None,
    shortfall_action: str | None = None,
) -> tuple[dict, int]:
    if resume and run_dir:
        raise UniverseError("choose --resume or --run-dir")
    if not resume and not all((spec, snapshot, output)):
        raise UniverseError("build needs --spec, --snapshot and --output, or --resume RUN_DIR")
    root = Path(resume or run_dir or (str(output) + ".run")).resolve()
    state_path = root / "run.json"
    if resume:
        state = read_json(state_path)
        if state.get("schema_version") != 1 or state.get("kind") != "build_run":
            raise UniverseError("unsupported build run checkpoint")
        paths = dict(state["inputs"])
    else:
        if root.exists() and any(root.iterdir()):
            raise UniverseError(f"run directory is not empty; continue with --resume {root}")
        root.mkdir(parents=True, exist_ok=True)
        state = {"schema_version": 1, "kind": "build_run", "attempts": []}
        paths = {}
    for key, value in (
        ("spec", spec),
        ("snapshot", snapshot),
        ("policy", policy),
        ("seed", seed),
        ("output", output),
    ):
        if value is not None:
            paths[key] = str(Path(value).resolve())
    if language is not None:
        paths["language"] = language
    if shortfall_action is not None:
        paths["shortfall_action"] = shortfall_action
    next_command = f"python scripts/universe.py build --resume {shlex.quote(str(root))}"
    # Read before starting an attempt; a missing file can be repaired at the saved input path.
    payload = {
        "spec": read_json(paths["spec"]),
        "snapshot": read_json(paths["snapshot"]),
        "policy": load_policy(paths.get("policy")),
        "seed": read_json(paths["seed"]) if paths.get("seed") else None,
        "language": paths.get("language"),
    }
    if paths.get("shortfall_action") is not None:
        payload["spec"]["shortfall_action"] = paths["shortfall_action"]
    if payload["spec"].get("profile") == "max" and payload["snapshot"].get("coverage_plan"):
        # Archive the effective choice too; pre-handler failed runs can be reconsidered once.
        payload["spec"].setdefault("shortfall_action", "auto")
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    previous = state["attempts"][-1] if state["attempts"] else None
    changed_destination = (
        output is not None and previous and str(Path(output).resolve()) != previous["output"]
    )
    if (
        previous
        and previous["input_sha256"] == digest
        and previous["status"] != "running"
        and not changed_destination
    ):
        problems = []
        if previous["status"] in ("complete", "partial"):
            files = [p for value in previous["artifacts"].values()
                     for p in (value.values() if isinstance(value, dict) else [value])]
            for name in files:
                path = Path(name)
                expected = previous.get("artifact_sha256", {}).get(name)
                if not path.is_file():
                    problems.append({"path": name, "reason": "missing"})
                elif expected and hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    problems.append({"path": name, "reason": "changed"})
        result = {
            **previous,
            "checkpoint": str(state_path),
            "resume_command": next_command,
            "retry_skipped": "Inputs unchanged; repair or expand the saved inputs before resuming.",
        }
        if problems:
            result.update(status="needs_research", validation_passed=False,
                          artifact_problems=problems,
                          error="Saved artifacts are missing or changed. Restore exact originals "
                                "or resume with --output NEW_EMPTY_DIR.")
            return result, 2
        return result, (
            0 if previous["status"] == "complete" else 3 if previous["status"] == "partial" else 2
        )
    number = len(state["attempts"]) + 1
    attempt_dir = root / f"attempt-{number:03d}"
    attempt_dir.mkdir()
    save(attempt_dir / "inputs.json", payload)
    destination = Path(paths["output"]) if not previous or output else attempt_dir / "artifacts"
    attempt = {
        "number": number,
        "input_sha256": digest,
        "status": "running",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "output": str(destination),
        "inputs_archive": str(attempt_dir / "inputs.json"),
    }
    state.update(inputs=paths, status="running", resume_command=next_command)
    state["attempts"].append(attempt)
    save(state_path, state)
    try:
        universe, report = build_universe(
            payload["spec"], payload["snapshot"], payload["policy"], payload["seed"]
        )
        artifacts = write_artifacts(universe, report, destination, paths.get("language"))
        filled, target = len(universe["members"]), universe["limits"]["target_count"]
        coverage_model = universe.get("selection_model") == "coverage_first"
        delivery = universe.get("delivery")
        attempt.update(
            status=("partial" if delivery else "complete" if coverage_model
                    or filled >= target else "partial"),
            validation_passed=True,
            **({"qualified": report["qualified"], "delivery": delivery} if delivery else {}),
            target=target,
            filled=filled,
            shortfall=(delivery["shortfall"] if delivery else 0 if coverage_model
                       else max(0, target - filled)),
            unused_capacity=max(0, target - filled),
            version_hash=universe["version_hash"],
            warnings=report["warnings"],
            **report["stats"],
        )
        attempt["artifacts"] = {
            k: {lang: str(p) for lang, p in v.items()} if isinstance(v, dict) else str(v)
            for k, v in artifacts.items()
            if k != "directory"
        }
        attempt["artifact_sha256"] = {
            str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for value in artifacts.values()
            for p in (value.values() if isinstance(value, dict) else [value])
            if isinstance(p, Path) and p.is_file()
        }
        if payload["seed"]:
            held = {c["asset_id"] for c in payload["seed"]["members"]}
            chosen = {c["asset_id"] for c in universe["members"]}
            attempt["expansion"] = {
                "from_profile": payload["seed"]["profile"],
                "seed_members": len(held),
                "retained": len(held & chosen),
                "added": len(chosen - held),
                "removed": len(held - chosen),
            }
        code = 0 if attempt["status"] == "complete" else 3
    except (UniverseError, OSError) as exc:
        attempt.update(status="needs_research", validation_passed=False, error=str(exc))
        code = 2
    if code:
        attempt["diagnostics"] = diagnostics(
            payload["spec"], payload["snapshot"], payload["policy"], payload["seed"]
        )
        attempt["next_actions"] = [
            "Repair invalid facts or missing themes; expand the verified bench for capacity gaps.",
            "Recompute affected measurements, then resume with the corrected input paths.",
            "Keep eligibility and depth unchanged; do not spend retries on identical inputs.",
        ]
        if attempt["status"] == "partial" and attempt.get("delivery"):
            attempt["handler"] = {"action": "deliver", "reason": "small_count_gap_only",
                                  "retry_command": next_command + " --shortfall-action retry"}
            attempt["next_actions"] = [
                "Deliver all partial-labelled artifacts together; "
                "disclose actual growth and missing count.",
                "For further research, use the saved diagnostics and retry command "
                "with revised inputs.",
            ]
        elif attempt["status"] == "needs_research":
            attempt["handler"] = {"action": "retry", "reason": "large_gap_or_other_failed_checks",
                                  "retry_command": next_command}
    attempt["finished_at"] = datetime.now(timezone.utc).isoformat()
    state["status"] = attempt["status"]
    save(attempt_dir / "result.json", attempt)
    save(state_path, state)
    return {**attempt, "checkpoint": str(state_path), "resume_command": next_command}, code
