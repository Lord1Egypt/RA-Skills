# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Pipeline orchestrator — the main Quorum validation flow.

Flow:
1. Load config + rubric
2. Supervisor classifies artifact and runs critics
3. Aggregator synthesizes findings and assigns verdict
4. Write run directory with all outputs (JSON + Markdown report)
5. Return Verdict
"""

from __future__ import annotations

import glob as glob_mod
import hashlib
import json
import logging
import signal
import threading
from concurrent.futures import CancelledError, ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from quorum.agents.aggregator import AggregatorAgent
from quorum.agents.supervisor import SupervisorAgent
from quorum.config import QuorumConfig
from quorum.cost import BudgetExceededError, CostTracker
from quorum.learning import LearningMemory
from quorum.models import BatchVerdict, CriticResult, FileResult, FixProposal, PreScreenResult, Severity, TesterResult, Verdict, VerdictStatus
from quorum.providers.litellm_provider import LiteLLMProvider
from quorum.rubrics.loader import RubricLoader

logger = logging.getLogger(__name__)

# Output directory for all quorum runs
DEFAULT_RUNS_DIR = Path("quorum-runs")

# Max concurrent file validations in batch mode
# Keep conservative to avoid API rate limits
MAX_BATCH_WORKERS = 3


def apply_fix_proposals(
    proposals: list[FixProposal],
    artifact_text: str,
) -> tuple[str, list[FixProposal], list[FixProposal]]:
    """
    Apply fix proposals to artifact text via exact string replacement.

    Each proposal is applied in order. If a proposal's original_text is not
    present (possibly already consumed by a prior proposal), it is skipped
    with a warning.

    Args:
        proposals:     List of FixProposal objects to apply
        artifact_text: Current text of the artifact

    Returns:
        (modified_text, applied_proposals, skipped_proposals)
    """
    applied: list[FixProposal] = []
    skipped: list[FixProposal] = []
    current_text = artifact_text

    for proposal in proposals:
        if proposal.original_text and proposal.original_text in current_text:
            current_text = current_text.replace(
                proposal.original_text, proposal.replacement_text, 1
            )
            applied.append(proposal)
            logger.debug(
                "Applied fix for finding '%s': replaced %d chars",
                proposal.finding_id,
                len(proposal.original_text),
            )
        else:
            logger.warning(
                "Fix proposal for finding '%s': original_text not found in "
                "(possibly already-modified) artifact — skipping",
                proposal.finding_id,
            )
            skipped.append(proposal)

    return current_text, applied, skipped


def _revalidate_with_critics(
    modified_text: str,
    blocking_findings: list,
    provider: LiteLLMProvider,
    config: QuorumConfig,
    rubric: object,
) -> tuple[list[CriticResult], str, str]:
    """
    Re-run only the critics that produced the original blocking findings.

    Args:
        modified_text:     The artifact text after applying fixes
        blocking_findings: The CRITICAL/HIGH findings from the previous run
        provider:          Shared LLM provider instance
        config:            Quorum config (same instance as main pipeline)
        rubric:            Rubric used in Phase 1

    Returns:
        (new_critic_results, revalidation_verdict, revalidation_delta)
        revalidation_verdict: 'improved' | 'unchanged' | 'regressed'
        revalidation_delta:   Human-readable summary of what changed
    """
    from quorum.agents.supervisor import CRITIC_REGISTRY

    # Identify critics that produced the blocking findings
    blocking_critic_names = {
        f.critic
        for f in blocking_findings
        if f.severity in (Severity.CRITICAL, Severity.HIGH)
    }

    before_count = sum(
        1 for f in blocking_findings
        if f.severity in (Severity.CRITICAL, Severity.HIGH)
    )

    rerun_results: list[CriticResult] = []
    for critic_name in sorted(blocking_critic_names):  # sorted for determinism
        cls = CRITIC_REGISTRY.get(critic_name)
        if cls is None:
            logger.warning(
                "Critic '%s' not in registry, cannot re-run for revalidation",
                critic_name,
            )
            continue
        critic = cls(provider=provider, config=config)
        result = critic.evaluate(artifact_text=modified_text, rubric=rubric)
        rerun_results.append(result)

    after_count = sum(
        1
        for cr in rerun_results
        for f in cr.findings
        if f.severity in (Severity.CRITICAL, Severity.HIGH)
    )

    if after_count < before_count:
        verdict = "improved"
    elif after_count == before_count:
        verdict = "unchanged"
    else:
        verdict = "regressed"

    delta = f"CRITICAL/HIGH findings: {before_count} → {after_count} ({verdict})"

    # Note new findings introduced by the fix (flagged but not fatal)
    if verdict == "regressed":
        new_descriptions = [
            f.description[:80]
            for cr in rerun_results
            for f in cr.findings
            if f.severity in (Severity.CRITICAL, Severity.HIGH)
        ]
        if new_descriptions:
            delta += f"; new/remaining: {new_descriptions[:3]}"

    logger.info("Revalidation: %s — %s", verdict, delta)
    return rerun_results, verdict, delta


def _load_and_save_inputs(
    target: Path,
    config: QuorumConfig,
    rubric_name: str | None,
    runs_dir: Path,
    relationships_path: Path | None,
) -> tuple[str, "RubricLoader", Path]:
    """Load artifact, select rubric, create run directory, save inputs."""
    artifact_text = target.read_text(encoding="utf-8", errors="replace")
    loader = RubricLoader()
    rubric = _select_rubric(loader, rubric_name, target, artifact_text, config)
    run_dir = _create_run_dir(runs_dir or DEFAULT_RUNS_DIR, target)
    # Run manifest (per-file validation metadata — differs from batch-manifest.json)
    _write_json(run_dir / "run-manifest.json", {
        "target": str(target),
        "depth": config.depth_profile,
        "rubric": rubric.name,
        "critics": config.critics,
        "prescreen_enabled": config.enable_prescreen,
        "relationships_path": str(relationships_path) if relationships_path else None,
        "started_at": datetime.now(timezone.utc).isoformat(),
    })
    (run_dir / "artifact.txt").write_text(artifact_text, encoding="utf-8")
    _write_json(run_dir / "rubric.json", rubric.model_dump())
    return artifact_text, rubric, run_dir


def _run_prescreen(
    config: QuorumConfig,
    target: Path,
    artifact_text: str,
    run_dir: Path,
) -> "PreScreenResult | None":
    """Run deterministic pre-screen if enabled. Returns PreScreenResult or None."""
    if not config.enable_prescreen:
        return None
    try:
        from quorum.prescreen import PreScreen
        prescreener = PreScreen()
        result = prescreener.run(target, artifact_text)
        _write_json(run_dir / "prescreen.json", result.model_dump())
        logger.info(
            "Pre-screen: %d passed, %d failed, %d skipped",
            result.passed, result.failed, result.skipped,
        )
        return result
    except Exception as e:
        # V004 fix: pre-screen failure should not kill the entire validation run
        logger.warning("Pre-screen failed, continuing without: %s", e, exc_info=True)
        return None


def _run_phase2(
    config: QuorumConfig,
    provider: LiteLLMProvider,
    critic_results: list,
    relationships_path: Path,
    run_dir: Path,
) -> list:
    """Run Phase 2 cross-artifact consistency if relationships provided."""
    from quorum.relationships import load_manifest, resolve_relationships
    from quorum.critics.cross_consistency import CrossConsistencyCritic

    # Manifest paths are relative to the manifest's directory, not the target's
    manifest_base = relationships_path.parent.resolve()
    relationships = load_manifest(relationships_path)
    resolved = resolve_relationships(relationships, base_dir=manifest_base)

    # Collect Phase 1 findings (NOT verdicts) as context
    phase1_findings: list = []
    for cr in critic_results:
        if not cr.skipped:
            phase1_findings.extend(cr.findings)

    cross_critic = CrossConsistencyCritic(provider=provider, config=config)
    cross_result = cross_critic.evaluate(resolved, phase1_findings)

    _write_json(
        run_dir / "critics" / "cross_consistency-findings.json",
        cross_result.model_dump(),
    )
    critic_results.append(cross_result)

    logger.info(
        "Phase 2 complete: %d cross-artifact findings across %d relationships",
        len(cross_result.findings), len(relationships),
    )
    return critic_results


def _run_phase3(
    config: QuorumConfig,
    provider: LiteLLMProvider | None,
    critic_results: list[CriticResult],
    base_dir: Path,
    run_dir: Path,
) -> TesterResult | None:
    """Run Phase 3 Tester verification if depth permits."""
    from quorum.critics.tester import TesterCritic

    if config.depth_profile == "quick":
        return None

    l2_enabled = config.depth_profile == "thorough"

    tester = TesterCritic(
        provider=provider if l2_enabled else None,
        config=config if l2_enabled else None,
        l2_enabled=l2_enabled,
    )

    tester_result = tester.verify(critic_results, base_dir)

    # Save tester output
    _write_json(
        run_dir / "tester" / "verification-results.json",
        tester_result.model_dump(),
    )

    logger.info(
        "Phase 3 complete: %d verified, %d unverified, %d contradicted (%dms)",
        tester_result.verified_count,
        tester_result.unverified_count,
        tester_result.contradicted_count,
        tester_result.runtime_ms,
    )

    return tester_result


def _update_manifest(
    run_dir: Path,
    config: QuorumConfig,
    prescreen_result: object,
    verdict: Verdict,
    critic_results: list,
    relationships_path: Path | None,
    learning_stats: dict | None = None,
    cost_summary: dict | None = None,
    artifact_sha256: str | None = None,
    tester_result: TesterResult | None = None,
) -> None:
    """Update run manifest with final stats."""
    prescreen_stats: dict = {"prescreen_enabled": config.enable_prescreen}
    if prescreen_result is not None:
        prescreen_stats.update({
            "prescreen_checks": prescreen_result.total_checks,
            "prescreen_passed": prescreen_result.passed,
            "prescreen_failed": prescreen_result.failed,
            "prescreen_skipped": prescreen_result.skipped,
            "prescreen_runtime_ms": prescreen_result.runtime_ms,
            "prescreen_has_failures": prescreen_result.has_failures,
        })
    manifest_path = run_dir / "run-manifest.json"
    with open(manifest_path) as f:
        manifest_data = json.load(f)
    manifest_data.update(prescreen_stats)
    manifest_data["completed_at"] = datetime.now(timezone.utc).isoformat()
    manifest_data["verdict"] = verdict.status.value
    manifest_data["total_findings"] = len(verdict.report.findings) if verdict.report else 0
    # Count cross-artifact relationships evaluated (if Phase 2 ran)
    cross_result_list = [cr for cr in critic_results if cr.critic_name == "cross_consistency"]
    if cross_result_list and relationships_path is not None:
        try:
            from quorum.relationships import load_manifest
            rels = load_manifest(relationships_path)
            manifest_data["relationships_count"] = len(rels)
        except Exception as e:
            logger.warning("Could not count relationships for manifest: %s", e)
    if learning_stats:
        manifest_data["learning"] = learning_stats
    if cost_summary:
        manifest_data["cost"] = cost_summary
    if artifact_sha256:
        manifest_data["artifact_sha256"] = artifact_sha256
    if tester_result:
        manifest_data["tester"] = {
            "verified": tester_result.verified_count,
            "unverified": tester_result.unverified_count,
            "contradicted": tester_result.contradicted_count,
            "verification_rate": tester_result.verification_rate,
            "runtime_ms": tester_result.runtime_ms,
        }
    _write_json(manifest_path, manifest_data)


def run_validation(
    target_path: str | Path,
    depth: str = "quick",
    rubric_name: str | None = None,
    config: QuorumConfig | None = None,
    runs_dir: Path | None = None,
    relationships_path: Path | None = None,
    enable_learning: bool = True,
    cost_tracker: CostTracker | None = None,
    audit_report: bool = False,
) -> tuple[Verdict, Path]:
    """
    Run a full Quorum validation against a target artifact.

    Args:
        target_path:        Path to the artifact file to validate
        depth:              Depth profile: quick | standard | thorough
        rubric_name:        Rubric to use (auto-detected from domain if None)
        config:             Pre-loaded QuorumConfig (overrides depth if provided)
        runs_dir:           Where to write the run directory (default: ./quorum-runs/)
        relationships_path: Optional path to quorum-relationships.yaml for Phase 2
                            cross-artifact consistency validation
        enable_learning:    Whether to read/write learning memory (default: True)
        audit_report:       Generate audit-detail.csv and audit-summary.csv in run_dir

    Returns:
        Tuple of (Verdict, run_dir) — the final verdict and the Path to the run output directory
    """
    run_start = datetime.now(timezone.utc)
    target = Path(target_path)
    if not target.exists():
        raise FileNotFoundError(f"Target artifact not found: {target}")

    # Load config
    if config is None:
        from quorum.config import load_config
        config = load_config(depth=depth)

    artifact_text, rubric, run_dir = _load_and_save_inputs(
        target, config, rubric_name, runs_dir, relationships_path,
    )

    # Compute SHA-256 of the artifact before any fix-loop modifications
    artifact_sha256 = hashlib.sha256(artifact_text.encode("utf-8")).hexdigest()

    # Load learning memory and get mandatory context for critics
    learning_memory = None
    mandatory_context: str | None = None
    if enable_learning:
        try:
            learning_memory = LearningMemory()
            mandatory_context = learning_memory.to_critic_context() or None
            if mandatory_context:
                logger.info(
                    "Learning memory: %d mandatory pattern(s) injected into critic prompts",
                    len(learning_memory.get_mandatory()),
                )
        except Exception as e:
            logger.warning("Learning memory load failed (non-fatal): %s", e)

    # Set up cost tracking — use provided tracker (batch mode) or create own (single file)
    _own_tracker = cost_tracker is None
    if _own_tracker:
        cost_tracker = CostTracker()
    cost_tracker.set_current_file(str(target))

    provider = LiteLLMProvider(api_keys=config.api_keys, cost_tracker=cost_tracker)
    prescreen_result = _run_prescreen(config, target, artifact_text, run_dir)

    # Run supervisor → critics
    supervisor = SupervisorAgent(provider=provider, config=config)
    critic_results = supervisor.run(
        artifact_text=artifact_text,
        artifact_path=str(target),
        rubric=rubric,
        prescreen_result=prescreen_result,
        mandatory_context=mandatory_context,
    )

    # Budget check after critics complete (non-fatal for single-file runs)
    if config.max_cost is not None:
        try:
            cost_tracker.check_budget(config.max_cost)
        except BudgetExceededError as e:
            logger.warning("Budget exceeded after critics: %s", e)

    # Save Phase 1 critic results
    for result in critic_results:
        _write_json(
            run_dir / "critics" / f"{result.critic_name}-findings.json",
            result.model_dump(),
        )

    # Phase 1.5: Fix proposals and re-validation loops (if enabled)
    fix_report = None
    if config.max_fix_loops > 0:
        blocking = [
            f for cr in critic_results for f in cr.findings
            if f.severity in (Severity.CRITICAL, Severity.HIGH)
        ]
        if blocking:
            from quorum.agents.fixer import FixerAgent
            fixer = FixerAgent(provider=provider, config=config)
            current_artifact_text = artifact_text
            all_fix_reports: list = []

            for loop_num in range(1, config.max_fix_loops + 1):
                if not blocking:
                    logger.info(
                        "Fix loop %d: no blocking findings remain, stopping early",
                        loop_num,
                    )
                    break

                loop_fix_report = fixer.run(
                    findings=blocking,
                    artifact_text=current_artifact_text,
                    artifact_path=str(target),
                )
                loop_fix_report.loop_number = loop_num

                if not loop_fix_report.proposals:
                    logger.info(
                        "Fix loop %d: fixer produced no proposals, stopping early",
                        loop_num,
                    )
                    loop_fix_report.revalidation_verdict = "unchanged"
                    loop_fix_report.revalidation_delta = "Fixer produced no proposals"
                    _write_json(
                        run_dir / f"fix-proposals-loop-{loop_num}.json",
                        loop_fix_report.model_dump(),
                    )
                    all_fix_reports.append(loop_fix_report)
                    break

                # Apply proposals to the current artifact text
                modified_text, applied, _skipped_apply = apply_fix_proposals(
                    loop_fix_report.proposals, current_artifact_text
                )

                if not applied:
                    logger.info(
                        "Fix loop %d: no proposals could be applied, stopping early",
                        loop_num,
                    )
                    loop_fix_report.revalidation_verdict = "unchanged"
                    loop_fix_report.revalidation_delta = (
                        "No proposals could be applied to artifact"
                    )
                    _write_json(
                        run_dir / f"fix-proposals-loop-{loop_num}.json",
                        loop_fix_report.model_dump(),
                    )
                    all_fix_reports.append(loop_fix_report)
                    break

                current_artifact_text = modified_text

                # Re-run only the critics that produced the blocking findings
                new_critic_results, revalidation_verdict, revalidation_delta = (
                    _revalidate_with_critics(
                        modified_text=current_artifact_text,
                        blocking_findings=blocking,
                        provider=provider,
                        config=config,
                        rubric=rubric,
                    )
                )

                loop_fix_report.revalidation_verdict = revalidation_verdict
                loop_fix_report.revalidation_delta = revalidation_delta

                _write_json(
                    run_dir / f"fix-proposals-loop-{loop_num}.json",
                    loop_fix_report.model_dump(),
                )
                all_fix_reports.append(loop_fix_report)

                logger.info(
                    "Fix loop %d complete: %d/%d proposals applied, verdict=%s",
                    loop_num,
                    len(applied),
                    len(loop_fix_report.proposals),
                    revalidation_verdict,
                )

                # Update blocking findings for the next loop
                blocking = [
                    f for cr in new_critic_results for f in cr.findings
                    if f.severity in (Severity.CRITICAL, Severity.HIGH)
                ]

            # Save fixed artifact only if the text was actually modified
            if current_artifact_text != artifact_text:
                (run_dir / "artifact-fixed.txt").write_text(
                    current_artifact_text, encoding="utf-8"
                )
                logger.info(
                    "Saved fixed artifact to %s/artifact-fixed.txt", run_dir
                )

            if all_fix_reports:
                fix_report = all_fix_reports[-1]
                # Also write fix-proposals.json for backward compatibility
                _write_json(run_dir / "fix-proposals.json", fix_report.model_dump())
                logger.info(
                    "Fixer: %d loop(s) completed, final verdict=%s",
                    len(all_fix_reports),
                    fix_report.revalidation_verdict or "no revalidation",
                )

    # Phase 2: cross-artifact consistency (runs only when --relationships is provided)
    if relationships_path is not None:
        try:
            critic_results = _run_phase2(
                config, provider, critic_results, relationships_path, run_dir,
            )
        except Exception as e:
            logger.error("Phase 2 (cross-artifact) failed: %s", e, exc_info=True)
            # Non-fatal: Phase 1 results are still valid and aggregator will proceed

    # Phase 3: Tester verification (standard + thorough depth)
    tester_result = None
    try:
        tester_result = _run_phase3(
            config, provider, critic_results, target.parent.resolve(), run_dir,
        )
    except Exception as e:
        logger.error("Phase 3 (tester) failed: %s", e, exc_info=True)
        # Non-fatal: aggregator proceeds without tester data

    # Run aggregator → verdict
    # V007 fix: guard aggregator crash so partial results are still saved
    aggregator = AggregatorAgent(provider=provider, config=config)
    try:
        verdict = aggregator.run(critic_results, tester_result=tester_result)
    except Exception as e:
        logger.error("Aggregator failed: %s", e, exc_info=True)
        verdict = Verdict(
            status=VerdictStatus.REJECT,
            reasoning=f"Aggregator failed: {e}. Critic results were saved individually.",
            confidence=0.0,
            report=None,
        )

    # Save outputs and update manifest
    _write_json(run_dir / "verdict.json", verdict.model_dump())
    _write_report(run_dir / "report.md", verdict, target, rubric, config, fix_report=fix_report, tester_result=tester_result)

    # Update learning memory with findings from this run
    learning_stats: dict = {}
    if enable_learning and learning_memory is not None:
        try:
            domain = supervisor.classify_domain(artifact_text, str(target))
            all_findings = verdict.report.findings if verdict.report else []
            update_result = learning_memory.update_from_findings(all_findings, domain)
            learning_stats = {
                "new_patterns": update_result.new_patterns,
                "updated_patterns": update_result.updated_patterns,
                "promoted_patterns": update_result.promoted_patterns,
                "total_known": update_result.total_known,
            }
            logger.info(
                "Learning memory: +%d new, %d updated, %d promoted (%d total)",
                update_result.new_patterns, update_result.updated_patterns,
                update_result.promoted_patterns, update_result.total_known,
            )
        except Exception as e:
            logger.warning("Learning memory update failed (non-fatal): %s", e)

    # Build cost summary for manifest (only when we own the tracker — single file mode)
    cost_summary_dict: dict | None = None
    if _own_tracker:
        cs = cost_tracker.summary()
        cost_summary_dict = {
            "total_usd": cs.total_usd,
            "prompt_tokens": cs.prompt_tokens,
            "completion_tokens": cs.completion_tokens,
            "calls": cs.calls,
            "per_file": cs.per_file,
        }

    _update_manifest(
        run_dir, config, prescreen_result, verdict, critic_results,
        relationships_path, learning_stats, cost_summary_dict,
        artifact_sha256=artifact_sha256,
        tester_result=tester_result,
    )

    run_end = datetime.now(timezone.utc)

    # Generate CSV audit reports if requested
    if audit_report:
        try:
            from quorum.audit import generate_audit_reports
            generate_audit_reports(
                run_dir=run_dir,
                file_path=str(target),
                cost_tracker=cost_tracker,
                run_start=run_start,
                run_end=run_end,
            )
        except Exception as e:
            logger.warning("Audit report generation failed (non-fatal): %s", e)

    logger.info(
        "Run complete: verdict=%s | %d findings | run_dir=%s",
        verdict.status.value,
        len(verdict.report.findings) if verdict.report else 0,
        run_dir,
    )

    return verdict, run_dir


def _select_rubric(
    loader: RubricLoader,
    rubric_name: str | None,
    target: Path,
    artifact_text: str,
    config: QuorumConfig,
):
    """Select the best rubric for this artifact."""
    from quorum.models import Rubric

    if rubric_name:
        return loader.load(rubric_name)

    # Auto-detect from file extension / content
    ext = target.suffix.lower()
    text_lower = artifact_text.lower()

    if ext == ".py":
        try:
            return loader.load("python-code")
        except FileNotFoundError:
            pass

    if ext in (".yaml", ".yml", ".json"):
        # Likely a config file
        if any(kw in text_lower for kw in ["agent", "model", "workflow", "pipeline"]):
            try:
                return loader.load("agent-config")
            except FileNotFoundError:
                pass

    if ext in (".md", ".txt", ".rst"):
        research_signals = ["abstract", "methodology", "findings", "hypothesis", "study"]
        if sum(1 for s in research_signals if s in text_lower) >= 2:
            try:
                return loader.load("research-synthesis")
            except FileNotFoundError:
                pass

    # Default fallback: use the first built-in rubric available
    builtins = loader.list_builtin()
    if builtins:
        logger.warning(
            "No rubric specified and auto-detection failed. Falling back to: %s",
            builtins[0],
        )
        return loader.load(builtins[0])

    raise RuntimeError(
        "No rubric specified and no built-in rubrics found. "
        "Use --rubric to specify one."
    )


def _create_run_dir(runs_dir: Path, target: Path) -> Path:
    """Create a timestamped run directory."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_name = f"{timestamp}-{target.stem}"
    run_dir = runs_dir / run_name
    (run_dir / "critics").mkdir(parents=True, exist_ok=True)
    return run_dir


def _write_json(path: Path, data: dict) -> None:
    """Write a dict to a JSON file, creating parent dirs as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    except (OSError, UnicodeEncodeError) as e:
        logger.error("Failed to write %s: %s", path, e)
        raise


def _write_json_atomic(path: Path, data: dict) -> None:
    """Atomically write a dict to a JSON file using a .tmp sibling and rename.

    Prevents partial/corrupt JSON on disk if the process crashes mid-write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        tmp_path.replace(path)
    except (OSError, UnicodeEncodeError) as e:
        logger.error("Failed to atomically write %s: %s", path, e)
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


# ──────────────────────────────────────────────────────────────────────────────
# Batch / multi-file validation
# ──────────────────────────────────────────────────────────────────────────────

# Extensions we treat as validatable text artifacts
TEXT_EXTENSIONS = {
    ".md", ".txt", ".rst", ".yaml", ".yml", ".json", ".toml",
    ".py", ".ps1", ".sh", ".bat", ".cfg", ".ini", ".conf",
    ".xml", ".html", ".csv", ".tsv", ".tex", ".adoc",
}


def _validate_path(path: Path, boundary: Path | None = None) -> Path:
    """
    Validate and resolve a path, ensuring it doesn't escape the boundary.

    Args:
        path:     Path to validate
        boundary: If set, resolved path must be under this directory.

    Returns:
        Resolved (absolute) path

    Raises:
        ValueError: If the path escapes the boundary (path traversal attempt)
    """
    resolved = path.resolve()

    if boundary is not None:
        boundary_resolved = boundary.resolve()
        try:
            resolved.relative_to(boundary_resolved)
        except ValueError:
            raise ValueError(
                f"Path escapes allowed boundary: {path} "
                f"(resolves to {resolved}, boundary: {boundary_resolved})"
            )

    return resolved


def resolve_targets(
    target: str | Path,
    pattern: str | None = None,
    boundary: Path | None = None,
) -> list[Path]:
    """
    Resolve a target specification to a list of concrete file paths.

    Supports:
      - Single file path → [file]
      - Directory path → all text files (filtered by --pattern if given)
      - Glob pattern (contains * or ?) → expanded matches

    Args:
        target:   File path, directory path, or glob pattern
        pattern:  Optional glob filter when target is a directory (e.g. "*.md")
        boundary: Optional root boundary — all resolved paths must be under this
                  directory. If None when target is a directory, the target dir
                  itself becomes the boundary. Prevents path traversal via
                  patterns like "../../*".

    Returns:
        Sorted list of resolved file paths

    Raises:
        FileNotFoundError: If target doesn't exist or no files match
        ValueError: If any resolved path escapes the boundary
    """
    # Input validation
    target_str = str(target)
    if "\x00" in target_str:
        raise ValueError("Target path contains null bytes")
    if pattern is not None:
        if "\x00" in pattern:
            raise ValueError("Pattern contains null bytes")
        if ".." in pattern:
            raise ValueError(f"Pattern contains path traversal: {pattern}")
        # Reject patterns with shell-dangerous characters
        if any(c in pattern for c in ["|", ";", "&", "$", "`"]):
            raise ValueError(f"Pattern contains disallowed characters: {pattern}")

    target = Path(target)

    # Single file
    if target.is_file():
        if boundary:
            _validate_path(target, boundary)
        return [target.resolve()]

    # Directory
    if target.is_dir():
        # When target is a directory, use it as the boundary unless overridden
        effective_boundary = boundary or target.resolve()

        if pattern:
            # Reject patterns with explicit parent traversal
            if ".." in pattern:
                raise ValueError(
                    f"Pattern contains path traversal: {pattern}"
                )
            files = sorted(target.glob(pattern))
        else:
            files = sorted(
                p for p in target.rglob("*")
                if p.is_file() and p.suffix.lower() in TEXT_EXTENSIONS
            )

        # Validate every resolved file is within boundary
        validated = []
        for f in files:
            if f.is_file():
                _validate_path(f, effective_boundary)
                validated.append(f.resolve())
        return validated

    # Glob pattern (target path contains wildcards)
    target_str = str(target)
    if "*" in target_str or "?" in target_str:
        # V005 fix: reject unbounded recursive globs without a directory anchor
        if "**" in target_str:
            anchor = target_str.split("**")[0]
            if not anchor or anchor == "/" or not Path(anchor).exists():
                raise ValueError(
                    f"Unbounded recursive glob rejected: {target_str}. "
                    "Use a directory-anchored pattern like './docs/**/*.md'"
                )

        # Derive boundary from the non-glob prefix
        parts = Path(target_str.split("*")[0].split("?")[0])
        effective_boundary = boundary or (parts.resolve() if parts.exists() else Path.cwd().resolve())

        matches = sorted(Path(p) for p in glob_mod.glob(target_str, recursive=True))
        validated = []
        for m in matches:
            if m.is_file():
                _validate_path(m, effective_boundary)
                validated.append(m.resolve())
        return validated

    raise FileNotFoundError(f"Target not found: {target}")


def _validate_one_file(
    file_path: Path,
    index: int,
    total: int,
    depth: str,
    rubric_name: str | None,
    config: "QuorumConfig | None",
    runs_dir: Path,
    relationships_path: "Path | None",
    cost_tracker: "CostTracker | None" = None,
) -> "FileResult | dict":
    """Validate a single file, returning FileResult or error dict."""
    logger.info("Validating file %d/%d: %s", index, total, file_path)
    try:
        verdict, run_dir = run_validation(
            target_path=file_path,
            depth=depth,
            rubric_name=rubric_name,
            config=config,
            runs_dir=runs_dir,
            relationships_path=relationships_path,
            cost_tracker=cost_tracker,
        )
        return FileResult(
            file_path=str(file_path),
            verdict=verdict,
            run_dir=str(run_dir),
        )
    except Exception as e:
        logger.error("Failed to validate %s: %s", file_path, e)
        return {"file": str(file_path), "error": str(e)}


def run_batch_validation(
    target: str | Path,
    pattern: str | None = None,
    depth: str = "quick",
    rubric_name: str | None = None,
    config: QuorumConfig | None = None,
    runs_dir: Path | None = None,
    relationships_path: Path | None = None,
    audit_report: bool = False,
) -> tuple[BatchVerdict, Path]:
    """
    Run Quorum validation across multiple files with consolidated results.

    Writes batch-manifest.json progressively after each file completes so that
    a crash or SIGINT/SIGTERM does not lose completed work. Use
    resume_batch_validation(batch_dir) to continue an interrupted run.

    Args:
        target:             File, directory, or glob pattern
        pattern:            Optional glob filter for directories (e.g. "*.md")
        depth:              Depth profile: quick | standard | thorough
        rubric_name:        Rubric to use (auto-detected per file if None)
        config:             Pre-loaded QuorumConfig (overrides depth)
        runs_dir:           Root directory for run outputs
        relationships_path: Optional path to quorum-relationships.yaml for Phase 2

    Returns:
        (BatchVerdict, batch_run_directory) — consolidated verdict and output dir
    """
    files = resolve_targets(target, pattern)

    if not files:
        # Use relative path in error to avoid leaking absolute paths
        display_target = Path(target).name if Path(target).is_absolute() else target
        raise FileNotFoundError(
            f"No validatable files found in: {display_target}"
            + (f" (pattern: {pattern})" if pattern else "")
        )

    # Single file → delegate to standard pipeline, wrap result
    if len(files) == 1:
        verdict, run_dir = run_validation(
            target_path=files[0],
            depth=depth,
            rubric_name=rubric_name,
            config=config,
            runs_dir=runs_dir,
            relationships_path=relationships_path,
            audit_report=audit_report,
        )
        batch = BatchVerdict(
            status=verdict.status,
            file_results=[FileResult(
                file_path=str(files[0]),
                verdict=verdict,
                run_dir=str(run_dir),
            )],
            total_files=1,
            total_findings=len(verdict.report.findings) if verdict.report else 0,
            files_passed=0 if verdict.is_actionable else 1,
            files_failed=1 if verdict.is_actionable else 0,
            confidence=verdict.confidence,
            reasoning=verdict.reasoning,
        )
        return batch, run_dir

    # Multi-file batch
    base_runs_dir = runs_dir or DEFAULT_RUNS_DIR
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    batch_dir = base_runs_dir / f"batch-{timestamp}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    batch_start_dt = datetime.now(timezone.utc)
    batch_started = batch_start_dt.isoformat()

    # Shared cost tracker for the entire batch — thread-safe, uses thread-local file context
    batch_cost_tracker = CostTracker()

    # Write initial manifest immediately so a crash after this point is resumable
    # Persist config + relationships so resume can reconstruct the original run parameters
    _write_json_atomic(batch_dir / "batch-manifest.json", {
        "target": str(target),
        "pattern": pattern,
        "depth": depth,
        "rubric": rubric_name,
        "config": config.model_dump() if config else None,
        "relationships_path": str(relationships_path) if relationships_path else None,
        "total_files": len(files),
        "validated": 0,
        "errors": 0,
        "started_at": batch_started,
        "status": "running",
        "completed_files": [],
        "failed_files": [],
    })

    # Write initial batch report header
    _init_batch_report(batch_dir / "batch-report.md", target)

    # Signal handling — graceful shutdown on SIGTERM/SIGINT
    _stop_event = threading.Event()
    _old_sigterm: object = None
    _old_sigint: object = None
    _signals_registered = False

    def _handle_signal(signum: int, frame: object) -> None:
        logger.warning(
            "Signal %d received — stopping batch after in-flight tasks complete", signum
        )
        _stop_event.set()

    try:
        _old_sigterm = signal.signal(signal.SIGTERM, _handle_signal)
        _old_sigint = signal.signal(signal.SIGINT, _handle_signal)
        _signals_registered = True
    except ValueError:
        # signal.signal() raises ValueError when called outside the main thread
        logger.debug("Signal handlers not registered (not in main thread)")

    file_results: list[FileResult] = []
    errors: list[dict] = []
    completed_files: list[dict] = []
    failed_files: list[dict] = []
    _manifest_lock = threading.Lock()
    _report_lock = threading.Lock()

    try:
        max_workers = min(len(files), MAX_BATCH_WORKERS)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    _validate_one_file,
                    file_path, i, len(files),
                    depth, rubric_name, config,
                    batch_dir / "per-file", relationships_path,
                    batch_cost_tracker,
                ): file_path
                for i, file_path in enumerate(files, 1)
            }
            for future in as_completed(futures, timeout=3600):  # 1 hour max
                file_path = futures[future]
                try:
                    result = future.result()
                except CancelledError:
                    logger.debug("Future for %s was cancelled", file_path)
                    continue

                with _manifest_lock:
                    if isinstance(result, FileResult):
                        file_results.append(result)
                        completed_files.append({
                            "file": str(file_path),
                            "run_dir": result.run_dir,
                            "verdict": result.verdict.status.value,
                            "completed_at": datetime.now(timezone.utc).isoformat(),
                        })
                    else:
                        errors.append(result)
                        failed_files.append({
                            "file": str(file_path),
                            "error": result.get("error", "unknown"),
                            "failed_at": datetime.now(timezone.utc).isoformat(),
                        })

                    # Progressive manifest update — atomic so crash leaves valid JSON
                    _running_cost = batch_cost_tracker.total_cost
                    _write_json_atomic(batch_dir / "batch-manifest.json", {
                        "target": str(target),
                        "pattern": pattern,
                        "depth": depth,
                        "rubric": rubric_name,
                        "total_files": len(files),
                        "validated": len(file_results),
                        "errors": len(errors),
                        "started_at": batch_started,
                        "last_updated_at": datetime.now(timezone.utc).isoformat(),
                        "status": "running",
                        "completed_files": completed_files,
                        "failed_files": failed_files,
                        "running_cost_usd": _running_cost,
                    })

                # Append this file's result to the live batch report
                if isinstance(result, FileResult):
                    with _report_lock:
                        _append_file_to_batch_report(batch_dir / "batch-report.md", result)

                # Check budget after each file — stop queueing new files if exceeded
                if config is not None and config.max_cost is not None:
                    try:
                        batch_cost_tracker.check_budget(config.max_cost)
                    except BudgetExceededError as e:
                        logger.warning(
                            "Budget exceeded after %s: %s — stopping new file validations",
                            file_path, e,
                        )
                        _stop_event.set()

                # Check stop flag — cancel queued (not in-flight) futures, then exit loop
                if _stop_event.is_set():
                    logger.warning(
                        "Batch interrupted — cancelling queued futures, "
                        "waiting for in-flight tasks"
                    )
                    for f in futures:
                        f.cancel()
                    break

    except TimeoutError:
        logger.error("Batch validation timed out after 1 hour")

    finally:
        # Restore original signal handlers
        if _signals_registered:
            try:
                signal.signal(signal.SIGTERM, _old_sigterm)
                signal.signal(signal.SIGINT, _old_sigint)
            except (ValueError, OSError):
                pass

    # Determine final status
    final_status = "interrupted" if _stop_event.is_set() else "completed"

    # Compute aggregate verdict
    batch_verdict = _aggregate_batch(file_results, errors)

    # Build final cost summary
    batch_cs = batch_cost_tracker.summary()
    batch_cost_dict = {
        "total_usd": batch_cs.total_usd,
        "prompt_tokens": batch_cs.prompt_tokens,
        "completion_tokens": batch_cs.completion_tokens,
        "calls": batch_cs.calls,
        "per_file": batch_cs.per_file,
    }

    # Final manifest update
    _write_json_atomic(batch_dir / "batch-manifest.json", {
        "target": str(target),
        "pattern": pattern,
        "depth": depth,
        "rubric": rubric_name,
        "total_files": len(files),
        "validated": len(file_results),
        "errors": len(errors),
        "started_at": batch_started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "status": final_status,
        "completed_files": completed_files,
        "failed_files": failed_files,
        "cost": batch_cost_dict,
    })

    _write_json(batch_dir / "batch-verdict.json", batch_verdict.model_dump())

    if errors:
        _write_json(batch_dir / "errors.json", errors)

    # Finalize report with aggregate summary section
    _finalize_batch_report(batch_dir / "batch-report.md", batch_verdict, errors)

    # Generate CSV audit reports if requested (only when batch completed without interruption)
    if audit_report and file_results:
        try:
            from quorum.audit import generate_batch_audit_reports
            batch_end_dt = datetime.now(timezone.utc)
            generate_batch_audit_reports(
                batch_dir=batch_dir,
                file_results=file_results,
                cost_tracker=batch_cost_tracker,
                run_start=batch_start_dt,
                run_end=batch_end_dt,
            )
        except Exception as e:
            logger.warning("Batch audit report generation failed (non-fatal): %s", e)

    if _stop_event.is_set():
        logger.warning(
            "Batch interrupted: %d/%d files completed | %s",
            len(file_results), len(files), batch_dir,
        )
    else:
        logger.info(
            "Batch complete: %s | %d/%d files | %d total findings | %s",
            batch_verdict.status.value,
            len(file_results),
            len(files),
            batch_verdict.total_findings,
            batch_dir,
        )

    return batch_verdict, batch_dir


def resume_batch_validation(
    batch_dir: Path,
    runs_dir: Path | None = None,
) -> tuple[BatchVerdict, Path]:
    """
    Resume an interrupted or partial batch validation run.

    Reads batch-manifest.json from *batch_dir* to discover which files already
    completed, resolves the original target to get the full file list, skips
    completed files, and validates the remainder using the same config.

    Per-file run_dirs that exist on disk but are NOT in the manifest's
    completed_files list are treated as crashed mid-validation and will be
    re-validated.

    Args:
        batch_dir: Path to an existing batch run directory (must contain
                   batch-manifest.json).
        runs_dir:  Ignored — per-file outputs are written under *batch_dir* to
                   keep the batch self-contained.

    Returns:
        (BatchVerdict, batch_dir) — updated consolidated verdict and the same dir.

    Raises:
        FileNotFoundError: If batch_dir or batch-manifest.json does not exist.
        ValueError: If the manifest is malformed or already completed.
    """
    manifest_path = batch_dir / "batch-manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"No batch-manifest.json found in: {batch_dir}"
        )

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Corrupted batch-manifest.json in {batch_dir}: {e}") from e

    target = manifest.get("target")
    pattern = manifest.get("pattern")
    depth = manifest.get("depth", "quick")
    rubric_name = manifest.get("rubric")
    batch_started = manifest.get("started_at", datetime.now(timezone.utc).isoformat())

    # Restore original config and relationships from manifest (persisted since v0.6.1+)
    saved_config = manifest.get("config")
    config = QuorumConfig.model_validate(saved_config) if saved_config else None
    saved_rel_path = manifest.get("relationships_path")
    relationships_path = Path(saved_rel_path) if saved_rel_path else None

    if not target:
        raise ValueError(f"batch-manifest.json missing 'target' field in {batch_dir}")

    # Build set of already-completed file paths
    completed_entries: list[dict] = manifest.get("completed_files", [])
    completed_file_paths: set[str] = {e["file"] for e in completed_entries}
    failed_entries: list[dict] = manifest.get("failed_files", [])

    # Resolve full file list from the original target
    all_files = resolve_targets(target, pattern)
    remaining_files = [f for f in all_files if str(f) not in completed_file_paths]

    already_done = len(completed_file_paths)
    logger.info(
        "Resume: %d/%d files already completed, %d remaining",
        already_done, len(all_files), len(remaining_files),
    )

    # Reconstruct FileResult objects for already-completed files
    existing_results: list[FileResult] = []
    for entry in completed_entries:
        run_dir_path = Path(entry["run_dir"])
        verdict_path = run_dir_path / "verdict.json"
        try:
            verdict_data = json.loads(verdict_path.read_text(encoding="utf-8"))
            from quorum.models import Verdict as _Verdict
            verdict_obj = _Verdict.model_validate(verdict_data)
            existing_results.append(FileResult(
                file_path=entry["file"],
                verdict=verdict_obj,
                run_dir=entry["run_dir"],
            ))
        except Exception as e:
            logger.warning(
                "Could not reconstruct result for %s from %s: %s — re-validating",
                entry["file"], run_dir_path, e,
            )
            # Treat this file as remaining so it gets re-validated
            remaining_files.append(Path(entry["file"]))
            completed_file_paths.discard(entry["file"])

    # Update manifest to 'running' before we start new work
    completed_files: list[dict] = [e for e in completed_entries
                                   if e["file"] in completed_file_paths]
    errors: list[dict] = []
    _manifest_lock = threading.Lock()
    _report_lock = threading.Lock()

    _write_json_atomic(batch_dir / "batch-manifest.json", {
        "target": str(target),
        "pattern": pattern,
        "depth": depth,
        "rubric": rubric_name,
        "total_files": len(all_files),
        "validated": len(existing_results),
        "errors": 0,
        "started_at": batch_started,
        "resumed_at": datetime.now(timezone.utc).isoformat(),
        "last_updated_at": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "completed_files": completed_files,
        "failed_files": failed_entries,
    })

    new_results: list[FileResult] = []

    if remaining_files:
        # Signal handling for resume too
        _stop_event = threading.Event()
        _old_sigterm: object = None
        _old_sigint: object = None
        _signals_registered = False

        def _handle_signal(signum: int, frame: object) -> None:
            logger.warning(
                "Signal %d received — stopping resumed batch after in-flight tasks", signum
            )
            _stop_event.set()

        try:
            _old_sigterm = signal.signal(signal.SIGTERM, _handle_signal)
            _old_sigint = signal.signal(signal.SIGINT, _handle_signal)
            _signals_registered = True
        except ValueError:
            logger.debug("Signal handlers not registered (not in main thread)")

        try:
            max_workers = min(len(remaining_files), MAX_BATCH_WORKERS)
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(
                        _validate_one_file,
                        file_path, i + already_done, len(all_files),
                        depth, rubric_name, config,
                        batch_dir / "per-file", relationships_path,
                    ): file_path
                    for i, file_path in enumerate(remaining_files, 1)
                }
                for future in as_completed(futures, timeout=3600):
                    file_path = futures[future]
                    try:
                        result = future.result()
                    except CancelledError:
                        logger.debug("Future for %s was cancelled", file_path)
                        continue

                    with _manifest_lock:
                        if isinstance(result, FileResult):
                            new_results.append(result)
                            completed_files.append({
                                "file": str(file_path),
                                "run_dir": result.run_dir,
                                "verdict": result.verdict.status.value,
                                "completed_at": datetime.now(timezone.utc).isoformat(),
                            })
                        else:
                            errors.append(result)

                        _write_json_atomic(batch_dir / "batch-manifest.json", {
                            "target": str(target),
                            "pattern": pattern,
                            "depth": depth,
                            "rubric": rubric_name,
                            "total_files": len(all_files),
                            "validated": len(existing_results) + len(new_results),
                            "errors": len(errors),
                            "started_at": batch_started,
                            "last_updated_at": datetime.now(timezone.utc).isoformat(),
                            "status": "running",
                            "completed_files": completed_files,
                            "failed_files": failed_entries,
                        })

                    if isinstance(result, FileResult):
                        with _report_lock:
                            _append_file_to_batch_report(
                                batch_dir / "batch-report.md", result
                            )

                    if _stop_event.is_set():
                        for f in futures:
                            f.cancel()
                        break

        finally:
            if _signals_registered:
                try:
                    signal.signal(signal.SIGTERM, _old_sigterm)
                    signal.signal(signal.SIGINT, _old_sigint)
                except (ValueError, OSError):
                    pass

        final_status = "interrupted" if _stop_event.is_set() else "completed"
    else:
        final_status = "completed"

    all_results = existing_results + new_results
    batch_verdict = _aggregate_batch(all_results, errors)

    _write_json_atomic(batch_dir / "batch-manifest.json", {
        "target": str(target),
        "pattern": pattern,
        "depth": depth,
        "rubric": rubric_name,
        "total_files": len(all_files),
        "validated": len(all_results),
        "errors": len(errors),
        "started_at": batch_started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "status": final_status,
        "completed_files": completed_files,
        "failed_files": failed_entries,
    })

    _write_json(batch_dir / "batch-verdict.json", batch_verdict.model_dump())

    if errors:
        _write_json(batch_dir / "errors.json", errors)

    _finalize_batch_report(batch_dir / "batch-report.md", batch_verdict, errors)

    logger.info(
        "Resume %s: %s | %d/%d files | %d total findings | %s",
        final_status,
        batch_verdict.status.value,
        len(all_results),
        len(all_files),
        batch_verdict.total_findings,
        batch_dir,
    )

    return batch_verdict, batch_dir


def _aggregate_batch(
    file_results: list[FileResult],
    errors: list[dict],
) -> BatchVerdict:
    """Compute a consolidated batch verdict from per-file results."""
    if not file_results:
        return BatchVerdict(
            status=VerdictStatus.REJECT,
            reasoning="No files were successfully validated.",
            confidence=0.0,
        )

    # Worst-case status wins
    status_priority = {
        VerdictStatus.REJECT: 0,
        VerdictStatus.REVISE: 1,
        VerdictStatus.PASS_WITH_NOTES: 2,
        VerdictStatus.PASS: 3,
    }
    worst_status = min(
        (fr.verdict.status for fr in file_results),
        key=lambda s: status_priority.get(s, 99),
    )

    total_findings = sum(
        len(fr.verdict.report.findings) if fr.verdict.report else 0
        for fr in file_results
    )
    files_passed = sum(1 for fr in file_results if not fr.verdict.is_actionable)
    files_failed = sum(1 for fr in file_results if fr.verdict.is_actionable)
    avg_confidence = sum(fr.verdict.confidence for fr in file_results) / len(file_results)

    # Build reasoning
    parts = [f"{len(file_results)} files validated"]
    if files_passed:
        parts.append(f"{files_passed} passed")
    if files_failed:
        parts.append(f"{files_failed} need work")
    if errors:
        parts.append(f"{len(errors)} failed to process")
    parts.append(f"{total_findings} total findings")
    reasoning = ". ".join(parts) + "."

    return BatchVerdict(
        status=worst_status,
        file_results=file_results,
        total_files=len(file_results) + len(errors),
        total_findings=total_findings,
        files_passed=files_passed,
        files_failed=files_failed,
        confidence=avg_confidence,
        reasoning=reasoning,
    )


def _init_batch_report(path: Path, target: str | Path) -> None:
    """Create batch-report.md with a header and per-file table header."""
    lines = [
        "# Quorum Batch Validation Report",
        "",
        f"**Target:** `{target}`  ",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC  ",
        "",
        "---",
        "",
        "## Per-File Summary",
        "",
        "| File | Status | Findings | Coverage |",
        "|------|--------|----------|----------|",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _append_file_to_batch_report(path: Path, result: "FileResult") -> None:
    """Append a single file's result row to the live batch report."""
    name = Path(result.file_path).name
    finding_count = len(result.verdict.report.findings) if result.verdict.report else 0
    # Show criteria coverage instead of fabricated confidence
    report = result.verdict.report
    if report and report.critic_results:
        total = sum(r.criteria_total for r in report.critic_results)
        evaluated = sum(r.criteria_evaluated for r in report.critic_results if not r.skipped)
        coverage_str = f"{evaluated}/{total} criteria"
    else:
        coverage_str = "—"
    row = (
        f"| `{name}` | {result.verdict.status.value} "
        f"| {finding_count} | {coverage_str} |"
    )
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(row + "\n")
    except OSError as e:
        logger.warning("Could not append to batch report %s: %s", path, e)


def _finalize_batch_report(
    path: Path,
    batch: BatchVerdict,
    errors: list[dict],
) -> None:
    """Append the aggregate summary section to the batch report."""
    lines = [
        "",
        "---",
        "",
        f"## Batch Verdict: {batch.status.value}",
        "",
        f"> {batch.reasoning}",
        "",
        f"**Coverage:** {batch.confidence:.0%} of criteria evaluated  ",
        f"**Files:** {batch.total_files}  ",
        "",
    ]

    if errors:
        lines += [
            "## Errors",
            "",
        ]
        for err in errors:
            lines.append(f"- `{err['file']}`: {err['error']}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Aggregate Findings",
        "",
    ]

    # Collect all findings across files
    all_findings = []
    for fr in batch.file_results:
        if fr.verdict.report:
            for finding in fr.verdict.report.findings:
                all_findings.append(finding)

    if all_findings:
        lines.extend(_format_findings_by_severity(all_findings))
    else:
        lines.append("No issues found across any files.")
        lines.append("")

    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except OSError as e:
        logger.warning("Could not finalize batch report %s: %s", path, e)


def _format_findings_by_severity(findings) -> list[str]:
    """Format findings grouped by severity into Markdown lines."""
    lines = []
    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
        group = [f for f in findings if f.severity == sev]
        if not group:
            continue
        lines.append(f"## {sev.value} ({len(group)})")
        lines.append("")
        for i, finding in enumerate(group, 1):
            lines.append(f"### {i}. {finding.description[:100]}")
            if finding.location:
                lines.append(f"**Location:** `{finding.location}`  ")
            if finding.loci:
                for locus in finding.loci:
                    lines.append(
                        f"**Locus [{locus.role}]:** `{locus.file}:{locus.start_line}-{locus.end_line}`  "
                    )
            lines.append(f"**Critic:** {finding.critic}  ")
            if finding.rubric_criterion:
                lines.append(f"**Criterion:** {finding.rubric_criterion}  ")
            if finding.framework_refs:
                lines.append(f"**Refs:** {', '.join(finding.framework_refs)}  ")
            lines.append("")
            lines.append(f"**Evidence ({finding.evidence.tool}):**")
            lines.append("```")
            lines.append(finding.evidence.result[:500])
            lines.append("```")
            if finding.remediation:
                lines.append("")
                lines.append(f"**Suggested fix:** {finding.remediation[:200]}")
            lines.append("")
    return lines


def _write_report(
    path: Path,
    verdict,
    target: Path,
    rubric,
    config: QuorumConfig,
    fix_report=None,
    tester_result: TesterResult | None = None,
) -> None:
    """Write a Markdown validation report."""

    report = verdict.report
    display_target = target.name if target.is_absolute() else target
    lines = [
        f"# Quorum Validation Report",
        f"",
        f"**Target:** `{display_target}`  ",
        f"**Rubric:** {rubric.name} v{rubric.version}  ",
        f"**Depth:** {config.depth_profile}  ",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC  ",
        f"",
        f"---",
        f"",
        f"## Verdict: {verdict.status.value}",
        f"",
        f"> {verdict.reasoning}",
        f"",
        f"**Coverage:** {verdict.confidence:.0%} of criteria evaluated",
        f"",
    ]

    if report and report.findings:
        lines.extend(_format_findings_by_severity(report.findings))
    else:
        lines.append("## Findings")
        lines.append("")
        lines.append("No issues found.")
        lines.append("")

    if fix_report and fix_report.proposals:
        n = len(fix_report.proposals)
        m = fix_report.findings_addressed + fix_report.findings_skipped
        lines += [
            "---",
            "",
            "## Fix Proposals",
            "",
            f"The Fixer proposed {n} change{'s' if n != 1 else ''} for {m} CRITICAL/HIGH finding{'s' if m != 1 else ''}:",
            "",
        ]
        for i, proposal in enumerate(fix_report.proposals, 1):
            confidence_pct = int(proposal.confidence * 100)
            lines += [
                f"### {i}. Fix for: {proposal.finding_description[:100]}",
                f"**Confidence:** {confidence_pct}%  ",
                f"**Explanation:** {proposal.explanation}",
                "",
                "```diff",
                f"- {proposal.original_text}",
                f"+ {proposal.replacement_text}",
                "```",
                "",
            ]
        if fix_report.skip_reasons:
            lines += [
                f"**Skipped ({fix_report.findings_skipped}):**",
                "",
            ]
            for reason in fix_report.skip_reasons:
                lines.append(f"- {reason}")
            lines.append("")

    if tester_result is not None:
        from quorum.models import VerificationStatus

        l1_contradicted = sum(
            1 for vr in tester_result.verification_results
            if vr.status == VerificationStatus.CONTRADICTED and vr.level == 1
        )
        l2_contradicted = sum(
            1 for vr in tester_result.verification_results
            if vr.status == VerificationStatus.CONTRADICTED and vr.level == 2
        )
        verification_rate_pct = f"{tester_result.verification_rate:.0%}"

        lines += [
            "---",
            "",
            "## Verification (Tester)",
            "",
            "| Metric | Count |",
            "|--------|-------|",
            f"| Verified | {tester_result.verified_count} |",
            f"| Unverified | {tester_result.unverified_count} |",
            f"| Contradicted (L1, auto-excluded) | {l1_contradicted} |",
            f"| Contradicted (L2, annotated) | {l2_contradicted} |",
            f"| **Verification Rate** | {verification_rate_pct} |",
            "",
        ]

        if l1_contradicted > 0:
            lines += [
                "### Excluded Findings (L1 Contradicted)",
                "",
            ]
            for vr in tester_result.verification_results:
                if vr.status == VerificationStatus.CONTRADICTED and vr.level == 1:
                    lines.append(
                        f"- {vr.original_finding_id}: {vr.explanation}"
                    )
            lines.append("")

    if report:
        lines += [
            "---",
            "",
            "## Summary",
            "",
            f"| Severity | Count |",
            f"|----------|-------|",
            f"| CRITICAL | {report.critical_count} |",
            f"| HIGH     | {report.high_count} |",
            f"| MEDIUM   | {report.medium_count} |",
            f"| LOW      | {report.low_count} |",
            f"| INFO     | {report.info_count} |",
            f"| **Total** | **{len(report.findings)}** |",
            "",
        ]

    path.write_text("\n".join(lines), encoding="utf-8")
