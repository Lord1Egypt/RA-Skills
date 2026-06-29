from __future__ import annotations

import os
import re
import shlex
import shutil
import sqlite3
import subprocess  # nosec B404
import sys
import textwrap
import json
from pathlib import Path
from typing import Any

from research_mode_payloads import normalize_string_list
from research_mode_reporting import refresh_task_playbook
from research_mode_task import ResearchTask, StateManager
from research_mode_utils import (
    ResearchModeError,
    ValidationError,
    atomic_json_write,
    ensure_dir,
    read_json,
    utc_now,
)


def extract_json_from_stdout(stdout: str) -> dict[str, Any]:
    stdout = stdout.strip()
    if not stdout:
        raise ValidationError("Expected JSON output, got empty stdout")
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        match = re.search(r"(\{.*\}|\[.*\])", stdout, re.DOTALL)
        if not match:
            raise ValidationError(f"Could not parse JSON output: {stdout[:400]}")
        return json.loads(match.group(1))


def _quote_sqlite_identifier(identifier: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identifier):
        raise ValidationError(f"Unsafe SQLite identifier: {identifier!r}")
    return f'"{identifier}"'


def _is_cron_job_not_found_error(output: str) -> bool:
    normalized = " ".join(str(output or "").lower().split())
    return (
        "unknown cron job id" in normalized
        or "id not found" in normalized
        or "job id not found" in normalized
        or "cron job not found" in normalized
    )


def _run_cron_action(action: str, job_id: str) -> dict[str, Any]:
    try:
        completed = subprocess.run(  # nosec B603 B607
            ["openclaw", "cron", action, job_id, "--timeout", "30000"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        combined = (exc.stderr or "") + " " + (exc.stdout or "")
        if _is_cron_job_not_found_error(combined):
            return {
                "status": "not-found",
                "job_id": job_id,
                "error": (exc.stderr or exc.stdout or "").strip()
                or "cron job id not found",
            }
        raise ValidationError(
            f"openclaw cron {action} failed for {job_id}: {(exc.stderr or exc.stdout or '').strip()}"
        ) from exc
    action_status = {
        "disable": "disabled",
        "enable": "enabled",
    }.get(action, f"{action}d")
    payload: dict[str, Any] = {"status": action_status, "job_id": job_id}
    stdout = (completed.stdout or "").strip()
    if stdout:
        try:
            payload["output"] = extract_json_from_stdout(stdout)
        except ValidationError:
            payload["output"] = stdout
    return payload


def disable_cron_job(job_id: str) -> dict[str, Any]:
    return _run_cron_action("disable", job_id)


def enable_cron_job(job_id: str) -> dict[str, Any]:
    return _run_cron_action("enable", job_id)


def snapshot_job_binding(state: dict[str, Any]) -> dict[str, Any] | None:
    job = state.get("job") or {}
    if not job.get("job_id"):
        return None
    return {
        "job_id": job.get("job_id"),
        "mode": job.get("mode"),
        "tick_every_min": job.get("tick_every_min"),
        "enabled": job.get("enabled"),
        "suspended_reason": job.get("suspended_reason"),
        "suspended_at": job.get("suspended_at"),
        "schedule_template": job.get("schedule_template"),
    }


def suspend_bound_job(state: dict[str, Any], *, reason: str, at: str) -> bool:
    job = state.setdefault("job", {})
    job_id = job.get("job_id")
    if not job_id:
        return False

    current_reason = job.get("suspended_reason")
    if job.get("enabled") is False and current_reason == reason:
        return False

    action = disable_cron_job(str(job_id))
    if action.get("status") == "not-found":
        job["enabled"] = None
        job["suspended_reason"] = None
        job["suspended_at"] = None
        return False
    job["enabled"] = False
    job["suspended_reason"] = reason
    job["suspended_at"] = at
    return True


def resume_bound_job(state: dict[str, Any]) -> bool:
    job = state.setdefault("job", {})
    job_id = job.get("job_id")
    if not job_id:
        return False

    if job.get("enabled") is True:
        job["suspended_reason"] = None
        job["suspended_at"] = None
        return False

    action = enable_cron_job(str(job_id))
    if action.get("status") == "not-found":
        job["enabled"] = None
        job["suspended_reason"] = None
        job["suspended_at"] = None
        return False
    job["enabled"] = True
    job["suspended_reason"] = None
    job["suspended_at"] = None
    return True


def remove_cron_job(job_id: str) -> dict[str, Any]:
    try:
        completed = subprocess.run(  # nosec B603 B607
            ["openclaw", "cron", "rm", job_id, "--json"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        combined = (exc.stderr or "") + " " + (exc.stdout or "")
        if _is_cron_job_not_found_error(combined):
            return {
                "status": "not-found",
                "job_id": job_id,
                "error": (exc.stderr or exc.stdout or "").strip()
                or "cron job id not found",
            }
        raise ValidationError(
            f"openclaw cron rm failed for {job_id}: {(exc.stderr or exc.stdout or '').strip()}"
        ) from exc
    payload = extract_json_from_stdout(completed.stdout)
    return payload


def clear_bound_job(
    task: ResearchTask,
    *,
    removed_job_id: str,
    removal_payload: dict[str, Any] | None = None,
) -> None:
    manager = StateManager(task)
    with manager.editor() as state:
        job = state.setdefault("job", {})
        job["last_removed_job_id"] = removed_job_id
        if removal_payload is not None:
            job["last_removed_payload"] = removal_payload
        job["job_id"] = None
        job["mode"] = None
        job["enabled"] = None
        job["suspended_reason"] = None
        job["suspended_at"] = None
        state["updated_at"] = utc_now()
        state.setdefault("history", {})["last_transition"] = "clear-bound-job"
    refresh_task_playbook(task)


def venv_python_path(task: ResearchTask) -> Path:
    return task.venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def venv_activate_path(task: ResearchTask) -> Path:
    return task.venv_dir / ("Scripts/activate" if os.name == "nt" else "bin/activate")


def ensure_sqlite_runtime_store(task: ResearchTask) -> dict[str, Any]:
    task.ensure_layout()
    schema_sql = textwrap.dedent(
        """
        -- Research Mode SQLite bootstrap schema (optional structured-analysis layer)
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS _rm_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS _rm_sources (
            source_id TEXT PRIMARY KEY,
            source_ref TEXT,
            source_title TEXT,
            source_url TEXT,
            imported_at TEXT,
            note TEXT
        );

        CREATE TABLE IF NOT EXISTS _rm_artifacts (
            artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            path TEXT NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        INSERT INTO _rm_meta (key, value) VALUES
            ('schema_version', '1'),
            ('task_scoped', 'true')
        ON CONFLICT(key) DO NOTHING;
        """
    ).strip() + "\n"
    if not task.sqlite_schema_path.exists():
        task.sqlite_schema_path.write_text(schema_sql, encoding="utf-8")

    with sqlite3.connect(task.sqlite_db_path) as conn:
        conn.executescript(schema_sql)
        conn.execute(
            "INSERT INTO _rm_meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            ("task_id", task.task_dir.name),
        )
        conn.execute(
            "INSERT INTO _rm_meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            ("db_purpose", "optional structured-analysis store for research-mode"),
        )
        conn.execute(
            "INSERT INTO _rm_meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            ("updated_at", utc_now()),
        )
        conn.commit()

        tables = [
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            ).fetchall()
        ]
        row_counts = {
            table_name: int(
                conn.execute(
                    f"SELECT COUNT(*) FROM {_quote_sqlite_identifier(table_name)}"  # nosec B608
                ).fetchone()[0]
            )
            for table_name in tables
        }

    return {
        "sqlite_ready": True,
        "default_sqlite_db_path": str(task.sqlite_db_path),
        "sqlite_schema_path": str(task.sqlite_schema_path),
        "sqlite_queries_dir": str(task.sqlite_queries_dir),
        "sqlite_imports_dir": str(task.sqlite_imports_dir),
        "database_summary": {
            "db_path": str(task.sqlite_db_path),
            "purpose": "optional structured-analysis store for research-mode",
            "tables": tables,
            "row_counts": row_counts,
        },
    }


def prepare_runtime_payload(
    task: ResearchTask,
    state: dict[str, Any],
    args: Any,
    *,
    script_path: Path,
) -> dict[str, Any]:
    task.ensure_layout()
    ensure_dir(task.runtime_dir)
    ensure_dir(task.uv_cache_dir)

    packages_requested = [pkg.strip() for pkg in (args.package or []) if pkg.strip()]
    if getattr(args, "recreate", False) and task.venv_dir.exists():
        shutil.rmtree(task.venv_dir)

    uv_path = shutil.which("uv")
    tool = "uv" if uv_path else "venv"
    python_bin = venv_python_path(task)
    activate_path = venv_activate_path(task)
    venv_created = False
    env = os.environ.copy()
    env.setdefault("UV_CACHE_DIR", str(task.uv_cache_dir))

    if not python_bin.exists():
        venv_created = True
        if uv_path:
            cmd = [uv_path, "venv", str(task.venv_dir)]
            if getattr(args, "python", None):
                cmd.extend(["--python", args.python])
            subprocess.run(  # nosec B603
                cmd, check=True, capture_output=True, text=True, env=env
            )
        else:
            base_python = getattr(args, "python", None) or sys.executable
            subprocess.run(  # nosec B603
                [base_python, "-m", "venv", str(task.venv_dir)],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )

    packages_installed_now: list[str] = []
    if packages_requested:
        if uv_path:
            install_cmd = [uv_path, "pip", "install", "--python", str(python_bin)]
            install_cmd.extend(packages_requested)
        else:
            install_cmd = [str(python_bin), "-m", "pip", "install", *packages_requested]
        subprocess.run(  # nosec B603
            install_cmd, check=True, capture_output=True, text=True, env=env
        )
        packages_installed_now = packages_requested

    meta_existing: dict[str, Any] = {}
    if task.runtime_meta_path.exists():
        try:
            loaded_meta = read_json(task.runtime_meta_path)
            if isinstance(loaded_meta, dict):
                meta_existing = loaded_meta
        except ResearchModeError:
            meta_existing = {}

    installed_packages = sorted(
        {
            *normalize_string_list(meta_existing.get("packages_installed") or []),
            *packages_installed_now,
        }
    )
    sqlite_runtime = ensure_sqlite_runtime_store(task)

    runtime_meta = {
        "research_id": state["id"],
        "tool": tool,
        "workspace_dir": str(task.workspace_dir),
        "workspace_analysis_dir": str(task.workspace_analysis_dir),
        "workspace_tools_dir": str(task.workspace_tools_dir),
        "workspace_data_dir": str(task.workspace_data_dir),
        "workspace_outputs_dir": str(task.workspace_outputs_dir),
        "workspace_tmp_dir": str(task.workspace_tmp_dir),
        "workspace_screenshots_dir": str(task.workspace_screenshots_dir),
        "workspace_vision_dir": str(task.workspace_vision_dir),
        "runtime_dir": str(task.runtime_dir),
        "venv_dir": str(task.venv_dir),
        "venv_python": str(python_bin),
        "activate_path": str(activate_path),
        "uv_cache_dir": str(task.uv_cache_dir),
        "packages_installed": installed_packages,
        "analysis_dirs_initialized": True,
        **sqlite_runtime,
        "updated_at": utc_now(),
        "created_at": meta_existing.get("created_at") or utc_now(),
    }
    atomic_json_write(task.runtime_meta_path, runtime_meta)

    return {
        "status": "prepared",
        "task_id": state["id"],
        "task_dir": str(task.task_dir),
        "tool": tool,
        "workspace_dir": str(task.workspace_dir),
        "workspace_analysis_dir": str(task.workspace_analysis_dir),
        "workspace_tools_dir": str(task.workspace_tools_dir),
        "workspace_data_dir": str(task.workspace_data_dir),
        "workspace_outputs_dir": str(task.workspace_outputs_dir),
        "workspace_tmp_dir": str(task.workspace_tmp_dir),
        "workspace_screenshots_dir": str(task.workspace_screenshots_dir),
        "workspace_vision_dir": str(task.workspace_vision_dir),
        "sqlite_ready": sqlite_runtime["sqlite_ready"],
        "default_sqlite_db_path": sqlite_runtime["default_sqlite_db_path"],
        "sqlite_schema_path": sqlite_runtime["sqlite_schema_path"],
        "sqlite_queries_dir": sqlite_runtime["sqlite_queries_dir"],
        "sqlite_imports_dir": sqlite_runtime["sqlite_imports_dir"],
        "database_summary": sqlite_runtime["database_summary"],
        "runtime_dir": str(task.runtime_dir),
        "venv_dir": str(task.venv_dir),
        "python": str(python_bin),
        "activate": str(activate_path),
        "uv_cache_dir": str(task.uv_cache_dir),
        "venv_created": venv_created,
        "packages_requested": packages_requested,
        "packages_installed_now": packages_installed_now,
        "runtime_meta_path": str(task.runtime_meta_path),
        "commands": {
            "python": str(python_bin),
            "activate": f". {shlex.quote(str(activate_path))}",
            "prepare_again": (
                f"python3 {shlex.quote(str(script_path))} prepare-runtime --root "
                f"{shlex.quote(str(task.task_dir.parent))} --id {shlex.quote(state['id'])}"
            ),
        },
    }


def render_worker_prompt_text(
    state: dict[str, Any],
    task: ResearchTask,
    script_path: Path,
) -> str:
    root_arg = shlex.quote(str(task.task_dir.parent))
    task_id = shlex.quote(state["id"])
    script = shlex.quote(str(script_path))
    return (
        textwrap.dedent(
            f"""
        You are the isolated research worker for research_id={state["id"]}.
        Use the helper script {script_path} for every state transition. Do not edit state.json manually.

        Protocol:
        1. Run: python3 {script} begin --root {root_arg} --id {task_id}
        2. If the JSON status is one of skipped/paused/complete/cancelled/failed, stop immediately and reply exactly NO_REPLY.
        3. If status=leased, use the returned JSON as the work order for this single bounded iteration.
           Read and actively use:
           - working_memory.summary / next_angle / open_questions
           - corpus.mode / corpus.entries
           - input_layer.constraints / deliverable / user_instructions
           - rules_profile when rules_profile.exists=true
           - execution_guidance
        4. Perform exactly one focused research iteration. You may use available tools such as search, fetch, browser, image analysis, MCP, file tools, exec, and messaging if needed.
           You are allowed to create files, write scripts, run analysis code, and build task-local tooling under paths.workspace_dir / paths.runtime_dir.
           Treat code as a first-class helper whenever it improves accuracy, scale, or reproducibility — especially for structured data, parsing, extraction, normalization, scoring, comparisons, and calculations.
           For larger structured workloads, also treat SQLite as a first-class helper. Prefer task-local SQLite when repeated filtering, deduplication, joins, aggregations, ranking, or queue-building would be easier than juggling JSON/markdown by hand.
           Treat vision/image analysis as a first-class helper for visual workloads — especially screenshots, maps, charts, graphs, dashboards, UI states, and user-provided images.
           If corpus.mode is local or hybrid, inspect files under paths.corpus_dir before deciding whether web search is needed.
           If you need an isolated Python environment or extra packages, first run:
           python3 {script} prepare-runtime --root {root_arg} --id {task_id}
           This prepares a task-local workspace plus .runtime/venv (using uv when available, otherwise stdlib venv), so you can do fuller code/data work without polluting the main workspace.
           After prepare-runtime, run task-local Python scripts that use installed runtime packages with the venv Python from paths.venv_dir (or runtime_meta.venv_python), not the system python3.
           Preferred layout after prepare-runtime:
           - scripts and analysis helpers -> paths.workspace_analysis_dir / paths.workspace_tools_dir
           - intermediate structured data -> paths.workspace_data_dir
           - outputs, tables, derived artifacts -> paths.workspace_outputs_dir
           - disposable scratch work -> paths.workspace_tmp_dir
           - raw screenshots -> paths.workspace_screenshots_dir
           - vision notes / derived visual outputs -> paths.workspace_vision_dir
           - SQLite DB target -> paths.sqlite_db_path
           - SQLite schema file -> paths.sqlite_schema_path
           - saved SQL queries -> paths.sqlite_queries_dir
           Before designing task-specific SQLite tables, identify: (a) the 1-3 core entities, (b) relationships between them, (c) likely dedup keys, and (d) provenance fields like source_id/captured_at/note/confidence. Start with the smallest useful schema and expand only if needed.
           You may use Python's stdlib sqlite3 or the sqlite3 CLI. Save schema/query files when SQLite materially influences the analysis.
           If images/screenshots materially influence the analysis, save the raw image plus any derived note/output artifact. Use vision as a helper, not as the sole source of truth when a more reliable structured or textual path exists.
           If code materially influences your conclusions, save the script/output artifacts and report them in the result JSON.
           If phase=preflight, do not perform broad research. Inspect the goal, constraints, corpus mode, available inputs, rules_profile, runtime/tool needs, and likely blockers. Fill result.preflight.decision with go, go_with_warnings, needs_setup, or blocked. Use warnings for non-blocking risks and blockers for issues that must pause the task.
           If phase=verify, evaluate research adequacy before finalization. Do not draft the final deliverable in this phase. Fill result.adequacy with goal alignment, coverage, gaps, evidence risks, contradictions, validation evidence, and the recommended next phase.
           If phase=finalize, produce the human-reviewable candidate only after adequacy has passed. Record the finalization trace in result.finalization and provide final_report_markdown or a reviewable candidate artifact.
           If phase=synthesize, prefer the accumulated task artifacts over noisy new searching; you may scaffold from:
           python3 {script} draft-report --root {root_arg} --id {task_id} --format markdown
           If a deliverable is specified, shape the iteration toward that output form.
           If constraints are present, do not violate them for convenience.
           Use only paths returned in the work order (especially paths.workspace_* and paths.sqlite_*). Never invent shortened absolute paths such as /tmp/research/...; if you need a shell path, copy it exactly from the work order or derive it from TASK_DIR in code.
        5. Write the result JSON to the provided paths.result_file using this schema:
           {{
             "summary": "short but concrete iteration summary",
             "next_angle": "the next most useful angle to investigate",
             "meaningful_progress": true,
             "code_used": false,
             "phase": "preflight|search|analyze|synthesize|verify|finalize",
             "open_questions": ["..."],
             "sources": [{{"url": "...", "title": "...", "note": "..."}}],
             "findings": [{{"kind": "fact|synthesis|risk|gap|plan", "text": "...", "source_urls": ["..."]}}],
             "analysis_artifacts": [{{"path": "workspace/analysis/script.py", "kind": "script|table|dataset|notebook|artifact", "note": "why it matters"}}],
             "packages_used": ["pandas"],
             "database_used": false,
             "database_artifacts": [{{"path": "workspace/data/analysis.sqlite", "kind": "sqlite-db|schema|query|export", "note": "why it matters"}}],
             "database_summary": {{"db_path": "workspace/data/analysis.sqlite", "purpose": "dedup + ranking", "tables": ["records"], "row_counts": {{"records": 42}}}},
             "vision_used": false,
             "vision_artifacts": [{{"path": "workspace/outputs/screenshots/map.png", "kind": "screenshot|photo|chart|vision-note", "note": "why it matters"}}],
             "vision_summary": {{"purpose": "map triage", "images_reviewed": 2, "confidence": "medium"}},
             "preflight": {{
               "decision": "go|go_with_warnings|needs_setup|blocked",
               "warnings": ["non-blocking setup or evidence risk"],
               "blockers": ["blocking setup issue"],
               "notes": "short optional setup note"
             }},
             "adequacy": {{
               "status": "not_started|passed|needs_research|needs_analysis|needs_synthesis|needs_user_input|needs_intervention",
               "goal_alignment": "whether the current evidence answers the user's goal",
               "coverage_summary": "what has and has not been covered",
               "covered_requirements": [{{"requirement": "...", "evidence": "..."}}],
               "coverage_gaps": [{{"gap": "...", "severity": "blocking|minor"}}],
               "evidence_risks": [{{"risk": "...", "severity": "blocking|minor"}}],
               "contradictions": [{{"contradiction": "...", "severity": "blocking|minor"}}],
               "recommended_next_phase": "search|analyze|synthesize|verify|finalize",
               "recommended_next_angle": "what to do next if not passed",
               "blocking_reasons": ["..."],
               "validation_evidence": [{{"check": "goal_alignment", "result": "passed|failed", "reason": "..."}}]
             }},
             "notify_recommendation": "auto|silent|milestone|blocker|final",
             "should_complete": false,
             "final_report_markdown": null
           }}
        6. Finalize with: python3 {script} finish --root {root_arg} --id {task_id} --run-id <run_id_from_begin> --result-file <paths.result_file>
           Never exit successfully after status=leased until either finish or fail has completed. If you have written paths.result_file, your next tool call must be finish; if finish cannot run, call fail with the run id instead of replying NO_REPLY.
        7. This cron worker is scheduled with internal-only delivery (`--no-deliver`). A normal assistant reply will NOT reach the human.
           - If finish/fail returns delivery_intent.status="pending", send delivery_intent.update_text via the available messaging surface to delivery_intent.notification_target.
           - Include delivery_intent.primary_file / attachments when the messaging surface supports safe file delivery.
           - After a successful send, run: python3 {script} record-notification --root {root_arg} --id {task_id} --delivery-intent-id <delivery_intent.id> --status sent
           - If sending fails, run: python3 {script} record-notification --root {root_arg} --id {task_id} --delivery-intent-id <delivery_intent.id> --status failed --error "<short reason>"
             Add --error-code delivery_channel_addressing_failed when the provider rejected the target shape (for example wrong channel/thread/topic/root target).
           - If delivery_intent.status="blocked", do not pretend it was sent; leave the blocked state visible and reply exactly NO_REPLY.
           - If there is no pending delivery_intent, reply exactly NO_REPLY.
        8. On any error after leasing a run, call: python3 {script} fail --root {root_arg} --id {task_id} --run-id <run_id_from_begin> --error "..." [--requires-user-input]

        Rules:
        - One iteration only. No inner loops.
        - Prefer 2-5 strong sources over noisy breadth.
        - Write user-facing summaries and final deliverables in the same language as the user's goal/instructions unless the user asks for another language.
        - Prefer list-producing discovery tools before synthesis-first search; if execution_guidance marks the task as RU/local/regional, treat regional/local discovery as the default and use synthesis-first search mainly for later synthesis / global context, while leaving other follow-up tools to case-by-case judgment.
        - Record honest no-progress iterations with meaningful_progress=false.
        - Prefer the simplest reproducible code path that helps; do not overbuild mini-products.
        - If code was used for a meaningful conclusion, save the relevant script/output and list it in analysis_artifacts.
        - If SQLite was used materially, persist the DB/schema/query artifacts and summarize the purpose/tables in database_summary.
        - If vision was used materially, persist the screenshot/image artifacts and summarize the visual purpose/confidence in vision_summary.
        - Avoid expected-failure probe commands in cron. If a missing page, empty search, blocked fetch, or absent CLI result is a normal research outcome, handle it as data and keep the shell/tool exit code successful.
        - Before reading generated files or running ad-hoc SQLite diagnostics, verify the path/query exists or wrap the diagnostic so "not found"/"no rows" is recorded in your notes instead of surfacing as a failed tool call.
        - Keep user messaging sparse: milestone/blocker/final only.
        - Treat constraints as hard boundaries.
        - Treat deliverable as the target output shape for synthesis and finalization.
        - Before finalization, use phase=verify to decide whether the research itself is sufficient. If it is not sufficient, set result.adequacy.status to the appropriate rework status and recommend search, analyze, or synthesize.
        - Set result.adequacy.status='passed' only when the accumulated evidence is sufficient for the user's goal and explicit constraints.
        - In phase=finalize, focus on packaging a human-reviewable result; do not use finalization to hide unresolved research gaps.
        - Never assume a plain reply is user-visible in this cron context; use delivery_intent + record-notification for user-visible updates.
        - When there is nothing to send, reply NO_REPLY.
        """
        ).strip()
        + "\n"
    )
