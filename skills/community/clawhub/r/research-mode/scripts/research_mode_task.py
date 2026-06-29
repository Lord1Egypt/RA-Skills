from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from research_mode_utils import (
    StateEditor,
    StateNotFoundError,
    ValidationError,
    append_jsonl,
    atomic_text_write,
    ensure_dir,
    pending_result_path,
    read_json,
    read_jsonl,
    resolve_under_root,
    utc_now,
    validate_research_id,
)


def normalize_task_state_defaults(state: dict[str, Any]) -> bool:
    changed = False

    def ensure_mapping(key: str) -> dict[str, Any]:
        nonlocal changed
        value = state.get(key)
        if not isinstance(value, dict):
            value = {}
            state[key] = value
            changed = True
        return value

    owner = ensure_mapping("owner")
    for key in ("channel", "chat_id", "thread_id", "topic_id", "disabled_reason"):
        if key not in owner:
            owner[key] = None
            changed = True

    delivery = ensure_mapping("delivery")
    delivery_defaults = {
        "update_policy": "milestone",
        "milestone_every_iterations": 2,
        "last_update_at": None,
        "sent_updates": 0,
        "primary_file": None,
        "attachments": [],
        "summary_text": None,
        "channel_strategy": None,
        "review_ready": False,
        "ready": False,
        "package_path": None,
        "notification_blocked": None,
    }
    for key, value in delivery_defaults.items():
        if key not in delivery:
            delivery[key] = list(value) if isinstance(value, list) else value
            changed = True

    if "delivery_intents" not in state or not isinstance(
        state.get("delivery_intents"), list
    ):
        state["delivery_intents"] = []
        changed = True

    queue = ensure_mapping("queue")
    queue_defaults = {
        "status": "free",
        "waiting_since": None,
        "position": None,
        "blocked_by_task_id": None,
        "blocked_by_run_id": None,
        "active_task_id": None,
        "active_run_id": None,
        "last_acquired_at": None,
        "last_released_at": None,
    }
    for key, value in queue_defaults.items():
        if key not in queue:
            queue[key] = value
            changed = True

    reliability = ensure_mapping("reliability")
    reliability_defaults = {
        "schema_version": 1,
        "failure_counters": {},
        "last_events": [],
    }
    for key, value in reliability_defaults.items():
        if key not in reliability:
            if isinstance(value, dict):
                reliability[key] = dict(value)
            elif isinstance(value, list):
                reliability[key] = list(value)
            else:
                reliability[key] = value
            changed = True

    return changed


class ResearchTask:
    def __init__(self, task_dir: Path):
        self.task_dir = task_dir.resolve()
        self.state_path = self.task_dir / "state.json"
        self.sources_path = self.task_dir / "sources.jsonl"
        self.findings_path = self.task_dir / "findings.jsonl"
        self.final_report_path = self.task_dir / "final-report.md"
        self.iterations_dir = self.task_dir / "iterations"
        self.tmp_dir = self.task_dir / ".tmp"
        self.input_dir = self.task_dir / "input"
        self.corpus_dir = self.input_dir / "corpus"
        self.corpus_manifest_path = self.input_dir / "corpus-manifest.json"
        self.workspace_dir = self.task_dir / "workspace"
        self.workspace_analysis_dir = self.workspace_dir / "analysis"
        self.workspace_tools_dir = self.workspace_dir / "tools"
        self.workspace_data_dir = self.workspace_dir / "data"
        self.workspace_outputs_dir = self.workspace_dir / "outputs"
        self.workspace_tmp_dir = self.workspace_dir / "tmp"
        self.workspace_screenshots_dir = self.workspace_outputs_dir / "screenshots"
        self.workspace_vision_dir = self.workspace_outputs_dir / "vision"
        self.sqlite_db_path = self.workspace_data_dir / "analysis.sqlite"
        self.sqlite_schema_path = self.workspace_analysis_dir / "schema.sql"
        self.sqlite_queries_dir = self.workspace_analysis_dir / "queries"
        self.sqlite_imports_dir = self.workspace_analysis_dir / "imports"
        self.runtime_dir = self.task_dir / ".runtime"
        self.venv_dir = self.runtime_dir / "venv"
        self.uv_cache_dir = self.runtime_dir / "uv-cache"
        self.runtime_meta_path = self.runtime_dir / "runtime.json"
        self.task_playbook_path = self.task_dir / "task-playbook.md"
        self.runs_path = self.task_dir / "runs.tsv"
        self.resolved_implicitly: bool = False

    @classmethod
    def from_args(
        cls, root: Path, research_id: str | None = None, path: str | None = None
    ) -> "ResearchTask":
        root = root.expanduser().resolve()
        if path:
            task_dir = resolve_under_root(root, path, label="task path")
            if task_dir.name == "state.json":
                task_dir = task_dir.parent
            return cls(task_dir)
        if not research_id:
            raise ValidationError("Either --id or --path is required")
        safe_id = validate_research_id(research_id)
        return cls(resolve_under_root(root, safe_id, label="task id"))

    def exists(self) -> bool:
        return self.state_path.exists()

    def load_state(self) -> dict[str, Any]:
        if not self.state_path.exists():
            raise StateNotFoundError(f"State file not found: {self.state_path}")
        state = read_json(self.state_path)
        normalize_task_state_defaults(state)
        return state

    def read_state(self) -> dict[str, Any]:
        return self.load_state()

    def ensure_layout(self) -> None:
        ensure_dir(self.task_dir)
        ensure_dir(self.iterations_dir)
        ensure_dir(self.tmp_dir)
        ensure_dir(self.input_dir)
        ensure_dir(self.corpus_dir)
        ensure_dir(self.workspace_dir)
        ensure_dir(self.workspace_analysis_dir)
        ensure_dir(self.workspace_tools_dir)
        ensure_dir(self.workspace_data_dir)
        ensure_dir(self.workspace_outputs_dir)
        ensure_dir(self.workspace_tmp_dir)
        ensure_dir(self.workspace_screenshots_dir)
        ensure_dir(self.workspace_vision_dir)
        ensure_dir(self.sqlite_queries_dir)
        ensure_dir(self.sqlite_imports_dir)
        self.sources_path.touch(exist_ok=True)
        self.findings_path.touch(exist_ok=True)

    def finish_iteration(self, run_id: str, payload: dict[str, Any]) -> dict[str, int]:
        now = utc_now()
        state = self.load_state()
        iteration_index = int(
            state["lock"].get("iteration_index")
            or (int(state["progress"].get("iteration_count") or 0) + 1)
        )

        existing_sources = read_jsonl(self.sources_path)
        existing_findings = read_jsonl(self.findings_path)

        def source_key(s: dict[str, Any]) -> str:
            return str(s.get("url") or s.get("title") or "").strip().lower()

        def finding_key(f: dict[str, Any]) -> str:
            return str(f.get("text") or "").strip().lower()

        seen_source_keys = {source_key(s) for s in existing_sources}
        seen_finding_keys = {finding_key(f) for f in existing_findings}

        sources_records: list[dict[str, Any]] = []
        duplicate_sources = 0
        for source in payload["sources"]:
            key = source_key(source)
            if key and key in seen_source_keys:
                duplicate_sources += 1
                continue
            record = {
                "research_id": state["id"],
                "run_id": run_id,
                "iteration": iteration_index,
                "recorded_at": now,
                **source,
            }
            sources_records.append(record)
            if key:
                seen_source_keys.add(key)

        findings_records: list[dict[str, Any]] = []
        duplicate_findings = 0
        for finding in payload["findings"]:
            key = finding_key(finding)
            if key and key in seen_finding_keys:
                duplicate_findings += 1
                continue
            record = {
                "research_id": state["id"],
                "run_id": run_id,
                "iteration": iteration_index,
                "recorded_at": now,
                **finding,
            }
            findings_records.append(record)
            if key:
                seen_finding_keys.add(key)

        append_jsonl(self.sources_path, sources_records)
        append_jsonl(self.findings_path, findings_records)

        self.write_iteration_markdown(
            iteration_index=iteration_index,
            run_id=run_id,
            status="finished",
            phase=payload["phase"],
            summary=payload["summary"],
            next_angle=payload["next_angle"],
            meaningful_progress=payload["meaningful_progress"],
            sources=payload["sources"],
            findings=payload["findings"],
            open_questions=payload["open_questions"],
            code_used=payload.get("code_used", False),
            analysis_artifacts=payload.get("analysis_artifacts") or [],
            packages_used=payload.get("packages_used") or [],
            database_used=payload.get("database_used", False),
            database_artifacts=payload.get("database_artifacts") or [],
            database_summary=payload.get("database_summary"),
            vision_used=payload.get("vision_used", False),
            vision_artifacts=payload.get("vision_artifacts") or [],
            vision_summary=payload.get("vision_summary"),
        )
        return {
            "new_sources": len(sources_records),
            "new_findings": len(findings_records),
            "duplicate_sources": duplicate_sources,
            "duplicate_findings": duplicate_findings,
        }

    def write_iteration_markdown(
        self,
        *,
        iteration_index: int,
        run_id: str,
        status: str,
        phase: str,
        summary: str,
        next_angle: str | None,
        meaningful_progress: bool,
        sources: list[dict[str, Any]],
        findings: list[dict[str, Any]],
        open_questions: list[str],
        code_used: bool = False,
        analysis_artifacts: list[dict[str, Any]] | None = None,
        packages_used: list[str] | None = None,
        database_used: bool = False,
        database_artifacts: list[dict[str, Any]] | None = None,
        database_summary: dict[str, Any] | None = None,
        vision_used: bool = False,
        vision_artifacts: list[dict[str, Any]] | None = None,
        vision_summary: dict[str, Any] | None = None,
        note: str | None = None,
    ) -> Path:
        ensure_dir(self.iterations_dir)
        path = self.iterations_dir / f"{iteration_index:03d}.md"
        lines: list[str] = []
        lines.append(f"# Iteration {iteration_index:03d}")
        lines.append("")
        lines.append(f"- Run ID: `{run_id}`")
        lines.append(f"- Status: `{status}`")
        lines.append(f"- Phase: `{phase}`")
        lines.append(f"- Meaningful progress: {'yes' if meaningful_progress else 'no'}")
        lines.append(f"- Code used: {'yes' if code_used else 'no'}")
        lines.append(f"- Database used: {'yes' if database_used else 'no'}")
        lines.append(f"- Vision used: {'yes' if vision_used else 'no'}")
        if note:
            lines.append(f"- Note: {note}")
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        lines.append(summary.strip() or "(empty)")
        lines.append("")
        if sources:
            lines.append("## Sources")
            lines.append("")
            for source in sources:
                title = source.get("title") or source.get("url") or "untitled source"
                url = source.get("url")
                note_text = source.get("note")
                if url:
                    bullet = f"- [{title}]({url})"
                else:
                    bullet = f"- {title}"
                if note_text:
                    bullet += f" — {note_text}"
                lines.append(bullet)
            lines.append("")
        if findings:
            lines.append("## Findings")
            lines.append("")
            for finding in findings:
                kind = finding.get("kind") or "note"
                text = finding.get("text") or json.dumps(finding, ensure_ascii=False)
                refs = finding.get("source_urls") or []
                bullet = f"- **{kind}**: {text}"
                if refs:
                    bullet += f" (refs: {', '.join(refs)})"
                lines.append(bullet)
            lines.append("")
        if open_questions:
            lines.append("## Open questions")
            lines.append("")
            for question in open_questions:
                lines.append(f"- {question}")
            lines.append("")
        if packages_used:
            lines.append("## Packages used")
            lines.append("")
            for package in packages_used:
                lines.append(f"- {package}")
            lines.append("")
        if analysis_artifacts:
            lines.append("## Analysis artifacts")
            lines.append("")
            for artifact in analysis_artifacts:
                kind = artifact.get("kind") or "artifact"
                artifact_path = artifact.get("path") or "(missing path)"
                note_text = artifact.get("note")
                bullet = f"- **{kind}**: `{artifact_path}`"
                if note_text:
                    bullet += f" — {note_text}"
                lines.append(bullet)
            lines.append("")
        if database_summary:
            lines.append("## Database summary")
            lines.append("")
            db_path = database_summary.get("db_path")
            if db_path:
                lines.append(f"- DB path: `{db_path}`")
            purpose = database_summary.get("purpose")
            if purpose:
                lines.append(f"- Purpose: {purpose}")
            tables = database_summary.get("tables") or []
            if tables:
                lines.append(f"- Tables: {', '.join(str(t) for t in tables)}")
            row_counts = database_summary.get("row_counts") or {}
            if row_counts:
                lines.append("- Row counts:")
                for table_name, row_count in row_counts.items():
                    lines.append(f"  - {table_name}: {row_count}")
            lines.append("")
        if database_artifacts:
            lines.append("## Database artifacts")
            lines.append("")
            for artifact in database_artifacts:
                kind = artifact.get("kind") or "artifact"
                artifact_path = artifact.get("path") or "(missing path)"
                note_text = artifact.get("note")
                bullet = f"- **{kind}**: `{artifact_path}`"
                if note_text:
                    bullet += f" — {note_text}"
                lines.append(bullet)
            lines.append("")
        if vision_summary:
            lines.append("## Vision summary")
            lines.append("")
            purpose = vision_summary.get("purpose")
            if purpose:
                lines.append(f"- Purpose: {purpose}")
            images_reviewed = vision_summary.get("images_reviewed")
            if images_reviewed is not None:
                lines.append(f"- Images reviewed: {images_reviewed}")
            confidence = vision_summary.get("confidence")
            if confidence:
                lines.append(f"- Confidence: {confidence}")
            lines.append("")
        if vision_artifacts:
            lines.append("## Vision artifacts")
            lines.append("")
            for artifact in vision_artifacts:
                kind = artifact.get("kind") or "artifact"
                artifact_path = artifact.get("path") or "(missing path)"
                note_text = artifact.get("note")
                bullet = f"- **{kind}**: `{artifact_path}`"
                if note_text:
                    bullet += f" — {note_text}"
                lines.append(bullet)
            lines.append("")
        if next_angle:
            lines.append("## Next angle")
            lines.append("")
            lines.append(next_angle)
            lines.append("")
        atomic_text_write(path, "\n".join(lines).rstrip() + "\n")
        return path

    def salvage_partial_progress(
        self,
        stale_run_id: str,
        stale_iteration_index: int,
        stale_phase: str,
    ) -> dict[str, Any] | None:
        try:
            result_file = pending_result_path(self.tmp_dir, stale_run_id)
        except ValidationError:
            return None
        if not result_file.exists():
            return None

        try:
            raw_payload = read_json(result_file)
        except Exception:
            return None

        if not isinstance(raw_payload, dict):
            return None

        summary = str(raw_payload.get("summary") or "").strip()
        if not summary:
            return None

        now = utc_now()
        recovery_note_path = (
            self.workspace_dir
            / f"recovery-note-{stale_iteration_index:03d}-{stale_run_id}.md"
        )

        lines: list[str] = []
        lines.append(f"# Recovery Note — Iteration {stale_iteration_index:03d}")
        lines.append("")
        lines.append("**⚠️ Recovered partial artifact from stale run**")
        lines.append("")
        lines.append(f"- Recovered from run ID: `{stale_run_id}`")
        lines.append(f"- Original iteration: {stale_iteration_index}")
        lines.append(f"- Original phase: `{stale_phase}`")
        lines.append(f"- Recovery timestamp: `{now}`")
        lines.append(f"- Source result file: `{result_file}`")
        lines.append("")
        lines.append(
            "**This is NOT a completed iteration — it is a salvage artifact.**"
        )
        lines.append("")

        if summary:
            lines.append("## Summary")
            lines.append("")
            lines.append(summary)
            lines.append("")

        next_angle = raw_payload.get("next_angle")
        if next_angle:
            lines.append("## Next angle")
            lines.append("")
            lines.append(str(next_angle).strip())
            lines.append("")

        open_questions = raw_payload.get("open_questions") or []
        if open_questions:
            lines.append("## Open questions")
            lines.append("")
            for q in open_questions:
                lines.append(f"- {q}")
            lines.append("")

        sources = raw_payload.get("sources") or []
        if sources:
            lines.append("## Partial sources (not persisted)")
            lines.append("")
            for src in sources:
                title = src.get("title") or src.get("url") or "untitled"
                url = src.get("url")
                bullet = f"- {title}" + (f" — {url}" if url else "")
                lines.append(bullet)
            lines.append("")

        findings = raw_payload.get("findings") or []
        if findings:
            lines.append("## Partial findings (not persisted)")
            lines.append("")
            for finding in findings:
                kind = finding.get("kind") or "note"
                text = finding.get("text") or ""
                bullet = f"- **{kind}**: {text}"
                lines.append(bullet)
            lines.append("")

        recovery_note_path.write_text(
            "\n".join(lines).rstrip() + "\n", encoding="utf-8"
        )

        return {
            "recovery_note_path": str(recovery_note_path),
            "recovery_note_exists": recovery_note_path.exists(),
            "stale_run_id": stale_run_id,
            "stale_iteration_index": stale_iteration_index,
            "stale_phase": stale_phase,
            "recovered_at": now,
            "result_file": str(result_file),
        }


class StateManager:
    def __init__(self, task: ResearchTask):
        self.task = task

    def read(self) -> dict[str, Any]:
        return self.task.read_state()

    def editor(self) -> StateEditor:
        return StateEditor(
            self.task.state_path,
            normalize=normalize_task_state_defaults,
        )
