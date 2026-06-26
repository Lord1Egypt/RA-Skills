# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Quorum CLI — Command-line interface.

Usage:
  quorum run --target <file> [--depth quick|standard|thorough] [--rubric <name>]
  quorum rubrics list
  quorum config init

First-run setup: if no API key is configured, quorum will prompt for one.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

import click
import yaml

from quorum.__init__ import __version__

logger = logging.getLogger("quorum")


# ──────────────────────────────────────────────────────────────────────────────
# Root group
# ──────────────────────────────────────────────────────────────────────────────

@click.group()
@click.version_option(__version__, prog_name="quorum")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug logging")
def cli(verbose: bool) -> None:
    """
    Quorum — Multi-critic quality validation.

    Evaluates artifacts (configs, research, code) against domain-specific
    rubrics using specialized critics, each required to provide grounded evidence.
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(levelname)s [%(name)s] %(message)s",
        stream=sys.stderr,
    )


# ──────────────────────────────────────────────────────────────────────────────
# quorum run
# ──────────────────────────────────────────────────────────────────────────────

@cli.command("run")
@click.option(
    "--target", "-t",
    required=False,
    default=None,
    type=str,
    help="File, directory, or glob pattern to validate",
)
@click.option(
    "--resume",
    default=None,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help=(
        "Resume an interrupted batch run from its directory "
        "(e.g. ./quorum-runs/batch-20260309-023000). "
        "Mutually exclusive with --target."
    ),
)
@click.option(
    "--pattern", "-p",
    default=None,
    help="Glob filter when target is a directory (e.g. '*.md', '**/*.yaml')",
)
@click.option(
    "--depth", "-d",
    default="quick",
    type=click.Choice(["quick", "standard", "thorough"], case_sensitive=False),
    show_default=True,
    help="Validation depth profile",
)
@click.option(
    "--rubric", "-r",
    default=None,
    help="Rubric name (built-in) or path to a JSON rubric file. Auto-detected if omitted.",
)
@click.option(
    "--config", "-c",
    default=None,
    type=click.Path(exists=True, path_type=Path),
    help="Path to a custom YAML config file (overrides depth profile)",
)
@click.option(
    "--output-dir", "-o",
    default=None,
    type=click.Path(path_type=Path),
    help="Directory for run outputs (default: ./quorum-runs/)",
)
@click.option(
    "--relationships", "-R",
    default=None,
    type=click.Path(exists=True, path_type=Path),
    help="Path to quorum-relationships.yaml manifest for cross-artifact validation (Phase 2)",
)
@click.option(
    "--fix-loops",
    default=None,
    type=click.IntRange(0, 3),
    metavar="N",
    help="Fix-and-revalidate loops (0-3). Overrides depth profile default.",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    default=False,
    help="Print full evidence for all findings (not just CRITICAL/HIGH)",
)
@click.option(
    "--no-learning",
    is_flag=True,
    default=False,
    help="Disable learning memory for this run (do not read or write known_issues.json)",
)
@click.option(
    "--max-cost",
    default=None,
    type=float,
    metavar="USD",
    help="Budget cap in USD. Stops batch after each file if total spend exceeds this.",
)
@click.option(
    "--yes", "-y",
    is_flag=True,
    default=False,
    help="Skip pre-run cost estimate confirmation prompt.",
)
@click.option(
    "--audit-report",
    is_flag=True,
    default=False,
    help="Generate audit-detail.csv and audit-summary.csv in the run directory. Auto-enabled at --depth thorough.",
)
@click.option(
    "--estimate-time",
    is_flag=True,
    default=False,
    help="Show a time estimate for the run (files, duration, recommended --timeout) then exit without validating.",
)
def run_cmd(
    target: str | None,
    pattern: str | None,
    depth: str,
    rubric: str | None,
    config: Path | None,
    output_dir: Path | None,
    relationships: Path | None,
    fix_loops: int | None,
    verbose: bool,
    no_learning: bool,
    resume: Path | None,
    max_cost: float | None,
    yes: bool,
    audit_report: bool,
    estimate_time: bool,
) -> None:
    """
    Validate artifacts against a rubric.

    Supports single files, directories, and glob patterns.

    Examples:

      quorum run --target my-config.yaml

      quorum run --target research.md --depth standard --rubric research-synthesis

      quorum run --target ./docs/ --pattern "*.md"

      quorum run --target ./pipeline/ --rubric agent-config --depth thorough

      quorum run --target policy.md --rubric ./rubrics/rfc3647.json

      quorum run --resume ./quorum-runs/batch-20260309-023000
    """
    from quorum.output import print_verdict, print_batch_verdict, print_error, print_warning

    # Validate mutual exclusivity
    if resume is not None and target is not None:
        print_error("--resume and --target are mutually exclusive.")
        sys.exit(1)
    if resume is None and target is None:
        print_error("Provide --target <path> to start a new run, or --resume <batch-dir> to continue an interrupted one.")
        sys.exit(1)

    # Check for API keys before doing any work (skip for --estimate-time, no LLM needed)
    if not estimate_time and not _has_api_key():
        _first_run_setup()
        if not _has_api_key():
            print_error(
                "No API key configured. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, "
                "or another LiteLLM-supported provider key in your environment."
            )
            sys.exit(1)

    try:
        from quorum.config import load_config, QuorumConfig
        from quorum.pipeline import resolve_targets, run_validation, run_batch_validation, resume_batch_validation

        # ── Resume mode ──────────────────────────────────────────────────────
        if resume is not None:
            import json as _json
            manifest_path = resume / "batch-manifest.json"
            try:
                manifest = _json.loads(manifest_path.read_text())
            except FileNotFoundError:
                print_error(f"No batch-manifest.json found in: {resume}")
                sys.exit(1)
            except _json.JSONDecodeError as e:
                print_error(f"Corrupted batch-manifest.json: {e}")
                sys.exit(1)

            completed = len(manifest.get("completed_files", []))
            total = manifest.get("total_files", "?")
            remaining = (total - completed) if isinstance(total, int) else "?"
            click.echo(
                f"Resuming batch from {resume}  "
                f"({completed} already done, {remaining} remaining) ...",
                err=True,
            )

            batch_verdict, batch_dir = resume_batch_validation(batch_dir=resume)
            print_batch_verdict(batch_verdict, batch_dir=batch_dir, verbose=verbose)

            if batch_verdict.is_actionable:
                sys.exit(2)
            return

        # ── Normal run mode ──────────────────────────────────────────────────
        # Load config
        if config:
            quorum_config = QuorumConfig.from_yaml(config)
        else:
            quorum_config = load_config(depth=depth)

        # Apply --fix-loops override if provided
        if fix_loops is not None:
            quorum_config = quorum_config.with_overrides(max_fix_loops=fix_loops)

        # Apply --max-cost override if provided
        if max_cost is not None:
            quorum_config = quorum_config.with_overrides(max_cost=max_cost)

        # Resolve targets to determine single vs batch mode
        target_path = Path(target)
        is_batch = (
            target_path.is_dir()
            or pattern is not None
            or "*" in target
            or "?" in target
        )

        # --estimate-time: resolve files, print estimate table, exit without validating
        if estimate_time:
            if is_batch:
                files = resolve_targets(target, pattern)
            else:
                files = [target_path]
            _show_time_estimate(files, depth, quorum_config)
            sys.exit(0)

        # Auto-enable audit report at thorough depth
        effective_audit = audit_report or (depth == "thorough")

        if is_batch:
            files = resolve_targets(target, pattern)
            click.echo(
                f"Batch mode: {len(files)} file(s) "
                f"({quorum_config.depth_profile} depth, "
                f"critics: {', '.join(quorum_config.critics)}) ...",
                err=True,
            )
            if relationships:
                click.echo(f"Phase 2: cross-artifact validation enabled ({relationships})", err=True)

            # Pre-run cost estimate
            _show_cost_estimate_and_confirm(files, quorum_config, yes)

            batch_verdict, batch_dir = run_batch_validation(
                target=target,
                pattern=pattern,
                depth=depth,
                rubric_name=rubric,
                config=quorum_config,
                runs_dir=output_dir or Path("quorum-runs"),
                relationships_path=relationships,
                audit_report=effective_audit,
            )
            # Note: learning memory is not applied per-file in batch mode

            print_batch_verdict(batch_verdict, batch_dir=batch_dir, verbose=verbose)
            _print_batch_cost_summary(batch_dir)

            if effective_audit:
                _print_audit_report_path(batch_dir)

            if batch_verdict.is_actionable:
                sys.exit(2)
        else:
            click.echo(
                f"Running Quorum ({quorum_config.depth_profile} depth, "
                f"critics: {', '.join(quorum_config.critics)}) ...",
                err=True,
            )
            if relationships:
                click.echo(f"Phase 2: cross-artifact validation enabled ({relationships})", err=True)

            if quorum_config.max_fix_loops > 0:
                click.echo(
                    f"  Fix loops: up to {quorum_config.max_fix_loops} "
                    "fix-and-revalidate loop(s) enabled",
                    err=True,
                )

            verdict, run_dir = run_validation(
                target_path=target_path,
                depth=depth,
                rubric_name=rubric,
                config=quorum_config,
                runs_dir=output_dir or Path("quorum-runs"),
                relationships_path=relationships,
                enable_learning=not no_learning,
                audit_report=effective_audit,
            )

            # Show fix loop progress summary if loops ran
            _print_fix_loop_summary(run_dir)

            # Show learning memory update summary
            if not no_learning:
                _print_learning_summary(run_dir)

            print_verdict(verdict, run_dir=run_dir, verbose=verbose)
            _print_run_cost_summary(run_dir)

            if effective_audit:
                _print_audit_report_path(run_dir)

            if verdict.is_actionable:
                sys.exit(2)

    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.debug("Unexpected error", exc_info=True)
        from quorum.output import print_error
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# quorum rubrics
# ──────────────────────────────────────────────────────────────────────────────

@cli.group("rubrics")
def rubrics_group() -> None:
    """Manage rubrics."""


@rubrics_group.command("list")
def rubrics_list() -> None:
    """List all available built-in rubrics."""
    from quorum.rubrics.loader import RubricLoader
    from quorum.output import print_rubric_list

    loader = RubricLoader()
    names = loader.list_builtin()

    if names:
        print_rubric_list(names)
    else:
        click.echo("No built-in rubrics found. Have you installed the package correctly?")


@rubrics_group.command("show")
@click.argument("name")
def rubrics_show(name: str) -> None:
    """Show criteria for a rubric."""
    from quorum.rubrics.loader import RubricLoader
    from quorum.output import print_error

    loader = RubricLoader()
    try:
        rubric = loader.load(name)
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    click.echo(f"\n{rubric.name} (v{rubric.version})")
    click.echo(f"Domain: {rubric.domain}")
    if rubric.description:
        click.echo(f"{rubric.description}")
    click.echo()
    click.echo(f"{'ID':<12} {'Severity':<10} {'Criterion'}")
    click.echo("─" * 80)
    for c in rubric.criteria:
        click.echo(f"{c.id:<12} {c.severity.value:<10} {c.criterion[:60]}")
    click.echo()


# ──────────────────────────────────────────────────────────────────────────────
# quorum config
# ──────────────────────────────────────────────────────────────────────────────

@cli.group("config")
def config_group() -> None:
    """Manage Quorum configuration."""


@config_group.command("init")
def config_init() -> None:
    """Interactive first-run setup — creates quorum-config.yaml."""
    _first_run_setup(force=True)


# ──────────────────────────────────────────────────────────────────────────────
# quorum issues
# ──────────────────────────────────────────────────────────────────────────────


@cli.group("issues")
def issues_group() -> None:
    """Manage learning memory (known recurring failure patterns)."""


@issues_group.command("list")
def issues_list() -> None:
    """Show all known issues (pattern_id, description, frequency, mandatory, last_seen)."""
    from quorum.learning import LearningMemory

    lm = LearningMemory()
    issues = lm.load()

    if not issues:
        click.echo("No known issues found.")
        click.echo(f"  (learning memory path: {lm.path})")
        return

    click.echo(f"\n{'ID':<14} {'Freq':<6} {'Mand':<6} {'Last Seen':<12} Description")
    click.echo("─" * 80)
    for issue in sorted(issues, key=lambda i: -i.frequency):
        mand = "yes" if issue.mandatory else "no"
        click.echo(
            f"{issue.pattern_id:<14} {issue.frequency:<6} {mand:<6} "
            f"{issue.last_seen:<12} {issue.description[:48]}"
        )
    click.echo(f"\n{len(issues)} pattern(s) in {lm.path}")


@issues_group.command("promote")
@click.option(
    "--threshold",
    default=3,
    show_default=True,
    type=int,
    help="Promote all patterns with frequency >= this threshold to mandatory",
)
def issues_promote(threshold: int) -> None:
    """Manually promote recurring patterns to mandatory checks."""
    from quorum.learning import LearningMemory

    lm = LearningMemory()
    promoted = lm.promote(threshold=threshold)
    if promoted:
        click.echo(f"Promoted {promoted} pattern(s) to mandatory (threshold={threshold}).")
    else:
        click.echo(f"No patterns to promote at threshold={threshold}.")


@issues_group.command("reset")
def issues_reset() -> None:
    """Clear known_issues.json (prompts for confirmation)."""
    from quorum.learning import LearningMemory

    lm = LearningMemory()
    if not lm.path.exists():
        click.echo(f"No known_issues.json found at {lm.path}.")
        return

    issues = lm.load()
    click.confirm(
        f"Delete {lm.path} ({len(issues)} pattern(s))?",
        abort=True,
    )
    lm.path.unlink()
    click.echo("known_issues.json cleared.")


# ──────────────────────────────────────────────────────────────────────────────
# First-run helpers
# ──────────────────────────────────────────────────────────────────────────────

def _print_fix_loop_summary(run_dir: Path) -> None:
    """Print a summary of any fix loops that ran, based on run directory contents."""
    import json as _json

    loop_files = sorted(run_dir.glob("fix-proposals-loop-*.json"))
    if not loop_files:
        return

    click.echo("", err=True)
    click.echo("Fix loop summary:", err=True)
    for loop_file in loop_files:
        try:
            data = _json.loads(loop_file.read_text())
            loop_num = data.get("loop_number", "?")
            rv = data.get("revalidation_verdict") or "N/A"
            delta = data.get("revalidation_delta") or ""
            n_proposals = len(data.get("proposals", []))
            click.echo(
                f"  Loop {loop_num}: {n_proposals} proposal(s), "
                f"verdict={rv}"
                + (f" — {delta}" if delta else ""),
                err=True,
            )
        except Exception:
            pass  # Non-fatal: loop summary is informational only

    fixed_artifact = run_dir / "artifact-fixed.txt"
    if fixed_artifact.exists():
        click.echo(f"  Fixed artifact: {fixed_artifact}", err=True)
    click.echo("", err=True)


def _print_learning_summary(run_dir: Path) -> None:
    """Print learning memory update summary from the run manifest."""
    import json as _json
    manifest_path = run_dir / "run-manifest.json"
    if not manifest_path.exists():
        return
    try:
        data = _json.loads(manifest_path.read_text())
        learning = data.get("learning")
        if not learning:
            return
        new = learning.get("new_patterns", 0)
        updated = learning.get("updated_patterns", 0)
        promoted = learning.get("promoted_patterns", 0)
        total = learning.get("total_known", 0)
        if new or updated or promoted:
            click.echo(
                f"Learning memory: +{new} new pattern(s), "
                f"{updated} updated, {promoted} promoted to mandatory "
                f"({total} total known)",
                err=True,
            )
    except Exception:
        pass  # Non-fatal: summary is informational only


def _has_api_key() -> bool:
    """Check if any LiteLLM-supported API key is configured in the environment."""
    provider_keys = [
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "MISTRAL_API_KEY",
        "GROQ_API_KEY",
        "COHERE_API_KEY",
        "AZURE_API_KEY",
        "GEMINI_API_KEY",
        "TOGETHER_API_KEY",
    ]
    return any(os.environ.get(k) for k in provider_keys)


def _first_run_setup(force: bool = False) -> None:
    """
    Interactive first-run configuration.

    Asks two questions:
    1. Which model tier to use (determines tier_1 and tier_2)
    2. Default depth profile

    Writes a quorum-config.yaml to cwd.
    """
    config_path = Path("quorum-config.yaml")
    if config_path.exists() and not force:
        return  # Already configured

    click.echo()
    click.echo("Welcome to Quorum! Let's set up your configuration.")
    click.echo()

    # Question 1: Model preference
    click.echo("Which LLM provider do you want to use?")
    click.echo("  1) Anthropic (Claude) — set ANTHROPIC_API_KEY")
    click.echo("  2) OpenAI (GPT-4)    — set OPENAI_API_KEY")
    click.echo("  3) Other (I'll configure manually)")
    click.echo()

    provider_choice = click.prompt(
        "Provider", type=click.Choice(["1", "2", "3"]), default="1"
    )

    if provider_choice == "1":
        tier_1 = "anthropic/claude-opus-4-0"
        tier_2 = "anthropic/claude-sonnet-4-20250514"
        key_var = "ANTHROPIC_API_KEY"
    elif provider_choice == "2":
        tier_1 = "gpt-4o"
        tier_2 = "gpt-4o-mini"
        key_var = "OPENAI_API_KEY"
    else:
        tier_1 = click.prompt("Tier 1 model name (strong model)", default="anthropic/claude-opus-4-0")
        tier_2 = click.prompt("Tier 2 model name (efficient model)", default="anthropic/claude-sonnet-4-20250514")
        key_var = None

    if key_var and not os.environ.get(key_var):
        api_key = click.prompt(
            f"Paste your {key_var} (leave blank to set it yourself later)",
            default="",
            hide_input=True,
        )
        if api_key:
            os.environ[key_var] = api_key
            click.echo(f"  ✓ {key_var} saved to environment for this session")
            click.echo(f"  (Add 'export {key_var}=...' to your shell profile to persist it)")

    # Question 2: Default depth
    click.echo()
    depth_choice = click.prompt(
        "Default depth profile",
        type=click.Choice(["quick", "standard", "thorough"]),
        default="quick",
    )

    # Write config
    config_data = {
        "critics": ["correctness", "completeness"],
        "model_tier1": tier_1,
        "model_tier2": tier_2,
        "max_fix_loops": 0,
        "depth_profile": depth_choice,
        "temperature": 0.1,
        "max_tokens": 4096,
    }

    with open(config_path, "w") as f:
        yaml.dump(config_data, f, default_flow_style=False)

    click.echo()
    click.echo(f"✓ Configuration written to {config_path}")
    click.echo(f"  Run: quorum run --target <your-file>")
    click.echo()


def _format_duration(seconds: int) -> str:
    """Format a duration in seconds to a human-readable string."""
    if seconds <= 0:
        return "0 sec"
    if seconds < 60:
        return f"{seconds} sec"
    mins = round(seconds / 60)
    return f"{mins} min"


def _show_time_estimate(files: list, depth: str, config: object) -> None:
    """Print a time estimate table for --estimate-time and exit."""
    from quorum.cost import time_estimate, estimate_cost

    te = time_estimate(files, depth)
    ce = estimate_cost(files, config)

    click.echo()
    click.echo(f"  Files to validate:     {te.files_count}")
    click.echo(
        f"  Estimated duration:    ~{_format_duration(te.estimated_seconds)} "
        f"(range: {_format_duration(te.min_seconds)}\u2013{_format_duration(te.max_seconds)})"
    )
    click.echo(f"  Estimated cost:        ~${ce.estimated_usd:.2f} [approximate]")
    if te.recommended_timeout > 0:
        click.echo(f"  Recommended --timeout: {te.recommended_timeout} seconds (max + 20% buffer)")
    click.echo()


def _show_cost_estimate_and_confirm(
    files: list,
    config: object,
    skip_prompt: bool,
) -> None:
    """
    Show a pre-run cost + time estimate and optionally prompt to continue.

    Skips the prompt when:
    - --yes flag is set
    - estimate is below $0.50 (low-cost run, no need to interrupt)
    - not running in an interactive terminal
    """
    try:
        from quorum.cost import estimate_cost, time_estimate
        ce = estimate_cost(files, config)
        te = time_estimate(files, getattr(config, "depth_profile", "standard"))
        click.echo(
            f"Estimated: ~{_format_duration(te.estimated_seconds)}, "
            f"~${ce.estimated_usd:.2f} "
            f"({ce.files_count} files, {getattr(config, 'depth_profile', '?')}) "
            f"[approximate]",
            err=True,
        )

        if skip_prompt or ce.estimated_usd < 0.50 or not sys.stdin.isatty():
            return

        if not click.confirm("Proceed with validation?", default=True):
            click.echo("Aborted.", err=True)
            sys.exit(0)
    except Exception:
        pass  # Estimate is best-effort — never block a run


def _print_run_cost_summary(run_dir: Path) -> None:
    """Print cost summary from a single-file run manifest."""
    import json as _json
    manifest_path = run_dir / "run-manifest.json"
    if not manifest_path.exists():
        return
    try:
        data = _json.loads(manifest_path.read_text())
        cost = data.get("cost")
        if not cost:
            return
        _emit_cost_line(cost)
    except Exception:
        pass


def _print_batch_cost_summary(batch_dir: Path) -> None:
    """Print cost summary from a batch manifest."""
    import json as _json
    manifest_path = batch_dir / "batch-manifest.json"
    if not manifest_path.exists():
        return
    try:
        data = _json.loads(manifest_path.read_text())
        cost = data.get("cost")
        if not cost:
            return
        _emit_cost_line(cost)
    except Exception:
        pass


def _print_audit_report_path(run_dir: Path) -> None:
    """Print the path to audit-detail.csv if it exists."""
    detail_path = run_dir / "audit-detail.csv"
    if detail_path.exists():
        click.echo(f"Audit report: {detail_path}", err=True)


def _emit_cost_line(cost: dict) -> None:
    """Emit the formatted cost line(s) to stderr."""
    total = cost.get("total_usd", 0.0)
    prompt_t = cost.get("prompt_tokens", 0)
    completion_t = cost.get("completion_tokens", 0)
    calls = cost.get("calls", 0)
    click.echo(
        f"Cost: ${total:.4f} "
        f"({prompt_t:,} prompt + {completion_t:,} completion tokens across {calls} calls)",
        err=True,
    )
    per_file = cost.get("per_file", {})
    if per_file:
        # Sort by cost descending, show top 5
        sorted_files = sorted(per_file.items(), key=lambda x: -x[1])[:5]
        parts = " | ".join(f"{Path(fp).name} ${c:.4f}" for fp, c in sorted_files)
        click.echo(f"Per-file: {parts}", err=True)
