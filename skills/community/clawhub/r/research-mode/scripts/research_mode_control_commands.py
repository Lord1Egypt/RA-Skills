from __future__ import annotations

import argparse
import glob
import html
import ipaddress
import json
import re
import shutil
import socket
import urllib.request
from urllib.parse import urlparse
from pathlib import Path
from typing import Any

from research_mode_corpus import (
    build_corpus_entry,
    list_corpus_entries,
    read_corpus_manifest,
    unique_copy_destination,
    write_corpus_manifest,
)
from research_mode_health import build_health_payload
from research_mode_lifecycle_helpers import clear_reviewable_candidate
from research_mode_payloads import (
    normalize_output_contract,
    normalize_string_list,
    parse_output_artifact_arg,
    parse_output_spec_arg,
)
from research_mode_queue import release_global_queue
from research_mode_reasons import reason_for_control_action, set_history_reason
from research_mode_registry import resolve_task_from_args
from research_mode_reporting import refresh_task_playbook
from research_mode_runtime import (
    clear_bound_job,
    enable_cron_job,
    remove_cron_job,
    resume_bound_job,
    snapshot_job_binding,
    suspend_bound_job,
)
from research_mode_task import ResearchTask, StateManager
from research_mode_utils import (
    NO_ACTIVE_LEASE,
    ValidationError,
    is_relative_to,
    json_dump,
    resolve_under_task,
    slugify,
    utc_now,
)

DEFAULT_FINAL_STATUSES = {"complete", "failed", "cancelled"}
REVIEW_WAIT_STATUSES = {"awaiting_review"}
SCRIPT_PATH = Path(__file__).resolve().with_name("research_mode.py")
DEFAULT_WORKER_TIMEOUT_SECONDS = 1800


def _merge_output_specs(
    current: list[dict[str, Any]], updates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    merged = [dict(item) for item in current]
    index_by_id = {
        str(item.get("id")): index
        for index, item in enumerate(merged)
        if str(item.get("id") or "").strip()
    }
    for item in updates:
        output = dict(item)
        output_id = str(output.get("id") or "").strip()
        if output_id in index_by_id:
            merged[index_by_id[output_id]] = output
        else:
            index_by_id[output_id] = len(merged)
            merged.append(output)
    return merged


def _has_glob_magic(text: str) -> bool:
    return any(char in str(text) for char in "*?[")


def _resolve_glob_pattern(raw: str) -> tuple[str, Path]:
    pattern_path = Path(str(raw).strip()).expanduser()
    if not pattern_path.is_absolute():
        pattern_path = (Path.cwd() / pattern_path).resolve()
    anchor = Path(pattern_path.anchor or "/")
    current = anchor
    for part in pattern_path.parts[1:]:
        if _has_glob_magic(part):
            break
        current = current / part
    else:
        current = pattern_path.parent
    return str(pattern_path), current


def _html_to_text(payload: str) -> tuple[str | None, str]:
    title_match = re.search(r"<title[^>]*>(.*?)</title>", payload, flags=re.I | re.S)
    title = html.unescape(title_match.group(1)).strip() if title_match else None
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", payload, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(
        r"</(?:p|div|section|article|li|h1|h2|h3|h4|h5|h6|br|tr)>",
        "\n",
        text,
        flags=re.I,
    )
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    lines = [line.strip() for line in text.splitlines()]
    text = "\n\n".join(line for line in lines if line)
    return title, text.strip()


def _is_blocked_url_ip(ip_text: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_text)
    except ValueError:
        return True
    return any(
        (
            ip.is_loopback,
            ip.is_private,
            ip.is_link_local,
            ip.is_reserved,
            ip.is_multicast,
            ip.is_unspecified,
        )
    )


def _validate_fetchable_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValidationError(
            "attach-url-as-md only supports http:// and https:// URLs"
        )
    host = (parsed.hostname or "").strip().rstrip(".")
    if not host:
        raise ValidationError("attach-url-as-md requires a URL host")
    lowered = host.lower()
    if lowered == "localhost" or lowered.endswith(".localhost"):
        raise ValidationError(f"Blocked local or private host in URL: {host}")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        try:
            resolved = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        except OSError as exc:
            raise ValidationError(f"Failed to resolve URL host: {host} ({exc})") from exc
        for item in resolved:
            sockaddr = item[4]
            ip_text = str(sockaddr[0])
            if _is_blocked_url_ip(ip_text):
                raise ValidationError(f"Blocked local or private host in URL: {host}")
    else:
        if _is_blocked_url_ip(host):
            raise ValidationError(f"Blocked local or private host in URL: {host}")


class _ValidatedRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _validate_fetchable_url(str(newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch_url_as_markdown(
    url: str,
    *,
    title: str | None,
    max_chars: int,
    timeout_seconds: int,
) -> tuple[str, str]:
    _validate_fetchable_url(url)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "OpenClaw-ResearchMode/1.2"},
    )
    try:
        opener = urllib.request.build_opener(_ValidatedRedirectHandler)
        # Scheme is restricted to http/https above.
        with opener.open(request, timeout=timeout_seconds) as response:  # nosec B310
            final_url = str(response.geturl() or url)
            _validate_fetchable_url(final_url)
            raw_bytes = response.read()
            content_type = response.headers.get_content_type()
            charset = response.headers.get_content_charset() or "utf-8"
    except Exception as exc:
        raise ValidationError(f"Failed to fetch URL: {url} ({exc})") from exc

    text = raw_bytes.decode(charset, errors="replace")
    derived_title = None
    if content_type == "text/html" or str(url).lower().endswith((".html", ".htm")):
        derived_title, extracted = _html_to_text(text)
        body = extracted or text
    else:
        body = text.strip()
    body = body.strip()
    if max_chars > 0 and len(body) > max_chars:
        body = body[: max_chars - 1].rstrip() + "…"
    final_title = str(title or derived_title or url).strip()
    markdown = (
        f"# {final_title}\n\nSource URL: {url}\n\n## Snapshot\n\n{body or '(empty)'}\n"
    )
    return final_title, markdown


def _validate_pdf_file(src: Path) -> None:
    if not src.exists() or not src.is_file():
        raise ValidationError(f"PDF file not found: {src}")
    try:
        header = src.read_bytes()[:5]
    except Exception as exc:
        raise ValidationError(f"Failed to read PDF file: {src} ({exc})") from exc
    if header != b"%PDF-":
        raise ValidationError(f"File is not a recognizable PDF: {src}")


def _build_schedule_args(
    *,
    root: str,
    task: ResearchTask,
    state: dict[str, Any],
    template: dict[str, Any],
) -> argparse.Namespace | None:
    every = template.get("tick_every_min") or template.get("every")
    if not every:
        return None
    return argparse.Namespace(
        root=root,
        id=state.get("id"),
        path=str(task.task_dir),
        every=str(every),
        timeout_seconds=int(
            template.get("timeout_seconds") or DEFAULT_WORKER_TIMEOUT_SECONDS
        ),
        thinking=str(template.get("thinking") or "high"),
        agent=template.get("agent"),
        model=template.get("model"),
        name=template.get("name"),
        light_context=bool(template.get("light_context")),
        replace_existing=False,
        dry_run=False,
    )


def _restore_job_for_reopen(
    *,
    task: ResearchTask,
    root: str,
    state: dict[str, Any],
) -> dict[str, Any] | None:
    job = state.get("job") or {}
    history = state.get("history") or {}
    saved_binding = history.get("last_job_binding") or {}
    schedule_template = (
        job.get("schedule_template") or saved_binding.get("schedule_template") or {}
    )

    current_job_id = job.get("job_id")
    if current_job_id:
        if job.get("enabled") is True:
            return {
                "job_id": current_job_id,
                "mode": job.get("mode") or schedule_template.get("mode") or "recurring",
                "tick_every_min": job.get("tick_every_min")
                or schedule_template.get("tick_every_min"),
                "enabled": True,
                "suspended_reason": None,
                "suspended_at": None,
                "schedule_template": schedule_template or job.get("schedule_template"),
                "restore_mode": "preserved",
            }
        action = enable_cron_job(str(current_job_id))
        if action.get("status") != "not-found":
            return {
                "job_id": current_job_id,
                "mode": job.get("mode") or schedule_template.get("mode") or "recurring",
                "tick_every_min": job.get("tick_every_min")
                or schedule_template.get("tick_every_min"),
                "enabled": True,
                "suspended_reason": None,
                "suspended_at": None,
                "schedule_template": schedule_template or job.get("schedule_template"),
                "restore_mode": "re-enabled-current",
            }

    saved_job_id = saved_binding.get("job_id")
    if saved_job_id:
        action = enable_cron_job(str(saved_job_id))
        if action.get("status") != "not-found":
            return {
                "job_id": saved_job_id,
                "mode": saved_binding.get("mode")
                or schedule_template.get("mode")
                or "recurring",
                "tick_every_min": saved_binding.get("tick_every_min")
                or schedule_template.get("tick_every_min"),
                "enabled": True,
                "suspended_reason": None,
                "suspended_at": None,
                "schedule_template": schedule_template
                or saved_binding.get("schedule_template"),
                "restore_mode": "re-enabled-history",
            }

    schedule_args = _build_schedule_args(
        root=root,
        task=task,
        state=state,
        template=schedule_template,
    )
    if schedule_args is None:
        return None

    from research_mode_create_schedule import schedule_task

    payload = schedule_task(task, schedule_args, script_path=SCRIPT_PATH)
    return {
        "job_id": payload.get("job_id"),
        "mode": schedule_template.get("mode") or "recurring",
        "tick_every_min": schedule_template.get("tick_every_min")
        or schedule_args.every,
        "enabled": True,
        "suspended_reason": None,
        "suspended_at": None,
        "schedule_template": schedule_template,
        "restore_mode": "rescheduled",
    }


def transition_command(
    args: argparse.Namespace, *, final_statuses: set[str] | None = None
) -> int:
    if final_statuses is None:
        final_statuses = DEFAULT_FINAL_STATUSES
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    manager = StateManager(task)
    action = args.action
    if action == "resume":
        state = task.read_state()
        health = build_health_payload(task, state)
        if state.get("status") == "paused" and health.get("status") != "ok":
            json_dump(
                {
                    "status": state.get("status"),
                    "action": action,
                    "blocked_by_health": True,
                    "health_status": health.get("status"),
                    "findings": health.get("findings") or [],
                    "recommended_actions": health.get("recommended_actions") or [],
                }
            )
            return 0
    remove_job_id: str | None = None
    stale_stop_release: dict[str, str | None] | None = None
    task_id_for_queue_release: str | None = None
    abandoned_run_id: str | None = None
    with manager.editor() as state:
        now = utc_now()
        status = state.get("status")
        previous_status = status
        if action == "pause":
            if status == "running":
                state["control"]["pause_requested"] = True
                result_status = "pause-requested"
            elif status in REVIEW_WAIT_STATUSES:
                result_status = status
            elif status not in final_statuses:
                state["status"] = "paused"
                result_status = "paused"
                if state.get("job", {}).get("job_id"):
                    suspend_bound_job(state, reason="paused", at=now)
            else:
                result_status = status
        elif action == "resume":
            state["control"]["pause_requested"] = False
            if status == "paused":
                state["status"] = "idle"
                job = state.get("job") or {}
                if job.get("job_id"):
                    resume_bound_job(state)
            result_status = state["status"]
        elif action == "stop":
            if status == "running":
                stale_running_cancelled = False
                lock = state.get("lock") or {}
                if lock.get("status") == "held":
                    from research_mode_lifecycle_helpers import (
                        stale_lock as check_stale_lock,
                    )

                    if check_stale_lock(state):
                        stale_run_id = lock.get("run_id")
                        abandoned_run_id = str(stale_run_id) if stale_run_id else None
                        stale_lease_token = lock.get("lease_token")
                        stale_iteration_index = int(lock.get("iteration_index") or 0)
                        state["status"] = "cancelled"
                        result_status = "cancelled"
                        stale_running_cancelled = True
                        stale_stop_release = {
                            "run_id": stale_run_id,
                            "lease_token": stale_lease_token,
                        }
                        task_id_for_queue_release = str(state.get("id") or task.task_dir.name)
                        state["control"]["stop_requested"] = False
                        state["lock"].update(
                            {
                                "status": "free",
                                "run_id": None,
                                "lease_token": NO_ACTIVE_LEASE,
                                "started_at": None,
                                "iteration_index": None,
                            }
                        )
                        state.setdefault("artifacts", {})["abandoned_run_id"] = (
                            stale_run_id
                        )
                        state.setdefault("artifacts", {})["abandoned_at"] = now
                        state.setdefault("history", {}).setdefault(
                            "audit_trail", []
                        ).append(
                            {
                                "at": now,
                                "event": "run_abandoned_on_stop",
                                "run_id": stale_run_id,
                                "iteration": stale_iteration_index,
                                "reason": "stale_lock_on_stop",
                            }
                        )
                if not stale_running_cancelled:
                    state["control"]["stop_requested"] = True
                    result_status = "stop-requested"
            elif status in REVIEW_WAIT_STATUSES:
                state["status"] = "cancelled"
                result_status = "cancelled"
                job = state.get("job") or {}
                if job.get("job_id"):
                    history = state.setdefault("history", {})
                    history["last_job_binding"] = snapshot_job_binding(state)
                remove_job_id = job.get("job_id")
            elif status not in final_statuses:
                state["status"] = "cancelled"
                result_status = "cancelled"
                remove_job_id = state.get("job", {}).get("job_id")
            else:
                result_status = status
        else:
            raise ValidationError(f"Unsupported action: {action}")
        state["updated_at"] = now
        state["history"]["last_transition"] = action
        normalized_reason = set_history_reason(
            state,
            reason_for_control_action(
                action,
                previous_status=previous_status,
                result_status=result_status,
            ),
        )

    refresh_task_playbook(task)
    queue_release = None
    if stale_stop_release is not None:
        queue_release = release_global_queue(
            task.task_dir.parent,
            task_id=task_id_for_queue_release or task.task_dir.name,
            run_id=stale_stop_release.get("run_id"),
            lease_token=stale_stop_release.get("lease_token"),
            released_by="stop",
        )
    removal_payload = None
    if remove_job_id:
        removal_payload = remove_cron_job(remove_job_id)
        clear_bound_job(
            task, removed_job_id=remove_job_id, removal_payload=removal_payload
        )

    json_dump(
        {
            "status": result_status,
            "action": action,
            "normalized_reason": normalized_reason,
            "removed_job_id": remove_job_id,
            "removal_payload": removal_payload,
            "abandoned_run_id": abandoned_run_id,
            "queue_release": queue_release,
        }
    )
    return 0


def mutate_working_memory_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    manager = StateManager(task)
    with manager.editor() as state:
        now = utc_now()
        working_memory = state.setdefault("working_memory", {})
        summary = str(working_memory.get("summary") or "")
        next_angle = str(working_memory.get("next_angle") or "")
        open_questions = normalize_string_list(
            working_memory.get("open_questions") or []
        )
        constraints = normalize_string_list(working_memory.get("constraints") or [])
        user_instructions = normalize_string_list(
            working_memory.get("user_instructions") or []
        )
        deliverable = working_memory.get("deliverable")
        deliverable = None if deliverable in (None, "") else str(deliverable).strip()
        output_contract = normalize_output_contract(
            working_memory.get("output_contract")
        )
        contract = working_memory.get("contract")

        if getattr(args, "set_next_angle", None) is not None:
            next_angle = str(args.set_next_angle).strip()
        if getattr(args, "append_angle", None):
            appended = str(args.append_angle).strip()
            if appended:
                next_angle = (
                    appended
                    if not next_angle
                    else f"{next_angle}\n\nДоп. угол: {appended}"
                )
        if getattr(args, "set_summary", None) is not None:
            summary = str(args.set_summary).strip()
        if getattr(args, "add_open_question", None):
            question = str(args.add_open_question).strip()
            if question and question not in open_questions:
                open_questions.append(question)
        if getattr(args, "remove_open_question", None):
            needle = str(args.remove_open_question).strip()
            open_questions = [q for q in open_questions if q != needle]
        if getattr(args, "clear_open_questions", False):
            open_questions = []

        if getattr(args, "add_constraint", None):
            item = str(args.add_constraint).strip()
            if item and item not in constraints:
                constraints.append(item)
        if getattr(args, "remove_constraint", None):
            needle = str(args.remove_constraint).strip()
            constraints = [c for c in constraints if c != needle]
        if getattr(args, "clear_constraints", False):
            constraints = []

        if getattr(args, "set_deliverable", None) is not None:
            value = str(args.set_deliverable).strip()
            deliverable = value or None
        if getattr(args, "clear_deliverable", False):
            deliverable = None
        if getattr(args, "deliverable_kind", None) is not None:
            output_contract["kind"] = str(args.deliverable_kind).strip()
        output_specs = [
            parse_output_spec_arg(item)
            for item in (getattr(args, "output", None) or [])
        ]
        if output_specs:
            output_contract["outputs"] = _merge_output_specs(
                output_contract.get("outputs") or [],
                output_specs,
            )
            output_contract = normalize_output_contract(output_contract)

        if getattr(args, "clear_contract", False):
            contract = None
        elif getattr(args, "contract", None) is not None:
            raw = str(args.contract).strip()
            if not raw:
                contract = None
            elif raw.lower() in ("null", "none", ""):
                contract = None
            else:
                try:
                    contract = json.loads(raw)
                except json.JSONDecodeError as e:
                    raise ValidationError(f"Invalid JSON in --contract: {e}")

        if getattr(args, "add_instruction", None):
            item = str(args.add_instruction).strip()
            if item and item not in user_instructions:
                user_instructions.append(item)
        if getattr(args, "remove_instruction", None):
            needle = str(args.remove_instruction).strip()
            user_instructions = [c for c in user_instructions if c != needle]
        if getattr(args, "clear_instructions", False):
            user_instructions = []

        working_memory["summary"] = summary
        working_memory["next_angle"] = next_angle
        working_memory["open_questions"] = open_questions
        working_memory["constraints"] = constraints
        working_memory["deliverable"] = deliverable
        working_memory["output_contract"] = output_contract
        working_memory["user_instructions"] = user_instructions
        working_memory["contract"] = contract
        state["updated_at"] = now
        state.setdefault("history", {})["last_transition"] = "mutate-working-memory"

        payload = {
            "status": state.get("status"),
            "task_id": state.get("id"),
            "summary": summary,
            "next_angle": next_angle,
            "open_questions": open_questions,
            "constraints": constraints,
            "deliverable": deliverable,
            "output_contract": output_contract,
            "user_instructions": user_instructions,
            "contract": contract,
            "working_memory": dict(working_memory),
        }

    refresh_task_playbook(task)
    json_dump(payload)
    return 0


def steering_alias_command(args: argparse.Namespace) -> int:
    text = getattr(args, "text", None)
    if args.action != "set-deliverable" and text is None:
        raise ValidationError(f"{args.action} requires text")
    if (
        args.action == "set-deliverable"
        and text is None
        and not getattr(args, "kind", None)
        and not getattr(args, "output", None)
    ):
        raise ValidationError("set-deliverable requires text, --kind, or --output")
    mutate_args = argparse.Namespace(
        root=args.root,
        id=args.id,
        path=args.path,
        set_next_angle=None,
        append_angle=None,
        set_summary=None,
        add_open_question=None,
        remove_open_question=None,
        clear_open_questions=False,
        add_constraint=None,
        remove_constraint=None,
        clear_constraints=False,
        set_deliverable=None,
        clear_deliverable=False,
        deliverable_kind=None,
        output=[],
        add_instruction=None,
        remove_instruction=None,
        clear_instructions=False,
        contract=None,
        clear_contract=False,
    )
    if args.action == "add-angle":
        mutate_args.append_angle = text
    elif args.action == "add-instruction":
        mutate_args.add_instruction = text
    elif args.action == "add-constraint":
        mutate_args.add_constraint = text
    elif args.action == "set-deliverable":
        mutate_args.set_deliverable = text
        mutate_args.deliverable_kind = getattr(args, "kind", None)
        mutate_args.output = getattr(args, "output", None) or []
    else:
        raise ValidationError(f"Unsupported steering alias action: {args.action}")
    return mutate_working_memory_command(mutate_args)


def bind_job(args: argparse.Namespace) -> int:
    task = ResearchTask.from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    manager = StateManager(task)
    with manager.editor() as state:
        state["job"]["job_id"] = args.job_id
        if args.mode:
            state["job"]["mode"] = args.mode
        if args.every:
            state["job"]["tick_every_min"] = args.every
        if getattr(args, "schedule_template", None) is not None:
            state["job"]["schedule_template"] = args.schedule_template
        else:
            state["job"]["schedule_template"] = state["job"].get("schedule_template")
        state["job"]["enabled"] = True
        state["job"]["suspended_reason"] = None
        state["job"]["suspended_at"] = None
        state["updated_at"] = utc_now()
        state["history"]["last_transition"] = "bind-job"
    refresh_task_playbook(task)
    if not getattr(args, "silent", False):
        json_dump({"status": "ok", "job_id": args.job_id})
    return 0


def unschedule_job(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    state = task.read_state()
    job_id = state.get("job", {}).get("job_id")
    if not job_id:
        json_dump({"status": "no-job", "task_id": state["id"]})
        return 0
    payload = remove_cron_job(job_id)
    clear_bound_job(task, removed_job_id=job_id, removal_payload=payload)
    json_dump(
        {
            "status": "unscheduled",
            "job_id": job_id,
            "task_id": state["id"],
            "payload": payload,
        }
    )
    return 0


def _finalize_corpus_attachment(
    task: ResearchTask,
    *,
    transition: str,
    attached: list[dict[str, object]],
    corpus_mode_override: str | None,
) -> dict[str, object]:
    manager = StateManager(task)
    with manager.editor() as state:
        corpus = state.setdefault("corpus", {})
        corpus["mode"] = corpus_mode_override or corpus.get("mode") or "local"
        corpus["entries"] = list_corpus_entries(task)
        corpus["updated_at"] = utc_now()
        state["updated_at"] = utc_now()
        state.setdefault("history", {})["last_transition"] = transition
        payload = {
            "status": "ok",
            "task_id": state.get("id"),
            "corpus_mode": corpus.get("mode"),
            "attached": attached,
            "corpus_entries": corpus["entries"],
            "corpus_dir": str(task.corpus_dir),
            "corpus_manifest_path": str(task.corpus_manifest_path),
        }
    refresh_task_playbook(task)
    return payload


def attach_input_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    task.ensure_layout()
    label = str(getattr(args, "label", "") or "").strip() or None
    note = str(getattr(args, "note", "") or "").strip() or None
    copied: list[dict[str, object]] = []
    skipped: list[dict[str, str]] = []
    manifest_entries = read_corpus_manifest(task)
    file_inputs = list(getattr(args, "file", []) or [])
    dir_inputs = list(getattr(args, "dir", []) or [])
    glob_inputs = list(getattr(args, "glob", []) or [])
    if not file_inputs and not dir_inputs and not glob_inputs:
        raise ValidationError(
            "attach-input requires at least one --file, --dir, or --glob"
        )

    for raw in file_inputs:
        src = Path(raw).expanduser().resolve()
        if not src.exists() or not src.is_file():
            raise ValidationError(f"Input file not found: {src}")
        dest = unique_copy_destination(task.corpus_dir, src.name)
        shutil.copy2(src, dest)
        entry = build_corpus_entry(
            task,
            dest,
            source_path=str(src),
            label=label,
            note=note,
        )
        manifest_entries.append(entry)
        copied.append(entry)

    for raw in dir_inputs:
        src_dir = Path(raw).expanduser().resolve()
        if not src_dir.exists() or not src_dir.is_dir():
            raise ValidationError(f"Input directory not found: {src_dir}")
        dest_dir = unique_copy_destination(task.corpus_dir, src_dir.name)
        candidates = sorted(src_dir.rglob("*"))
        files_in_dir = [path for path in candidates if path.is_file()]
        if not files_in_dir:
            raise ValidationError(f"Input directory has no files: {src_dir}")
        for src in files_in_dir:
            if src.is_symlink():
                skipped.append(
                    {
                        "source_path": str(src),
                        "reason": "symlink input skipped",
                    }
                )
                continue
            if not is_relative_to(src.resolve(), src_dir):
                skipped.append(
                    {
                        "source_path": str(src),
                        "reason": "resolved path outside input directory skipped",
                    }
                )
                continue
            rel = src.relative_to(src_dir)
            dest = dest_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            entry = build_corpus_entry(
                task,
                dest,
                source_path=str(src),
                label=label,
                note=note,
            )
            manifest_entries.append(entry)
            copied.append(entry)

    for raw in glob_inputs:
        pattern, anchor = _resolve_glob_pattern(raw)
        matched_files = sorted(
            Path(item)
            for item in glob.glob(pattern, recursive=True)
            if Path(item).exists() and Path(item).is_file()
        )
        if not matched_files:
            raise ValidationError(f"Input glob matched no files: {raw}")
        dest_root_name = anchor.name or "glob-import"
        dest_root = unique_copy_destination(task.corpus_dir, dest_root_name)
        for src in matched_files:
            if src.is_symlink():
                skipped.append(
                    {
                        "source_path": str(src),
                        "reason": "symlink input skipped",
                    }
                )
                continue
            resolved_src = src.resolve()
            if not is_relative_to(resolved_src, anchor):
                skipped.append(
                    {
                        "source_path": str(src),
                        "reason": "resolved path outside input glob anchor skipped",
                    }
                )
                continue
            try:
                rel = resolved_src.relative_to(anchor)
            except ValueError:
                rel = Path(resolved_src.name)
            dest = dest_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                dest = unique_copy_destination(dest.parent, dest.name)
            shutil.copy2(resolved_src, dest)
            entry = build_corpus_entry(
                task,
                dest,
                source_path=str(src),
                label=label,
                note=note,
            )
            manifest_entries.append(entry)
            copied.append(entry)
    write_corpus_manifest(task, manifest_entries)

    payload = _finalize_corpus_attachment(
        task,
        transition="attach-input",
        attached=copied,
        corpus_mode_override=getattr(args, "corpus_mode", None),
    )
    payload["skipped"] = skipped
    json_dump(payload)
    return 0


def attach_note_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    task.ensure_layout()
    text = str(getattr(args, "text", "") or "").rstrip()
    if not text.strip():
        raise ValidationError("attach-note requires non-empty text")
    title = str(getattr(args, "title", "") or "").strip() or "note"
    label = str(getattr(args, "label", "") or "").strip() or None
    note = str(getattr(args, "note", "") or "").strip() or None
    extension = (
        str(getattr(args, "extension", "md") or "md").strip().lstrip(".") or "md"
    )
    dest = unique_copy_destination(task.corpus_dir, f"{slugify(title)}.{extension}")
    dest.write_text(text.rstrip() + "\n", encoding="utf-8")

    manifest_entries = read_corpus_manifest(task)
    entry = build_corpus_entry(
        task,
        dest,
        source_path=None,
        label=label,
        note=note,
    )
    manifest_entries.append(entry)
    write_corpus_manifest(task, manifest_entries)

    payload = _finalize_corpus_attachment(
        task,
        transition="attach-note",
        attached=[entry],
        corpus_mode_override=getattr(args, "corpus_mode", None),
    )
    payload["title"] = title
    payload["path"] = entry["path"]
    json_dump(payload)
    return 0


def attach_url_as_md_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    task.ensure_layout()
    url = str(getattr(args, "url", "") or "").strip()
    if not url:
        raise ValidationError("attach-url-as-md requires non-empty --url")
    explicit_title = str(getattr(args, "title", "") or "").strip() or None
    label = str(getattr(args, "label", "") or "").strip() or None
    note = str(getattr(args, "note", "") or "").strip() or None
    max_chars = int(getattr(args, "max_chars", 20000) or 20000)
    timeout_seconds = int(getattr(args, "timeout_seconds", 20) or 20)

    final_title, markdown = _fetch_url_as_markdown(
        url,
        title=explicit_title,
        max_chars=max_chars,
        timeout_seconds=timeout_seconds,
    )
    dest = unique_copy_destination(task.corpus_dir, f"{slugify(final_title)}.md")
    dest.write_text(markdown.rstrip() + "\n", encoding="utf-8")

    manifest_entries = read_corpus_manifest(task)
    entry = build_corpus_entry(
        task,
        dest,
        source_path=None,
        label=label,
        note=note,
    )
    entry["source_url"] = url
    manifest_entries.append(entry)
    write_corpus_manifest(task, manifest_entries)

    payload = _finalize_corpus_attachment(
        task,
        transition="attach-url-as-md",
        attached=[entry],
        corpus_mode_override=getattr(args, "corpus_mode", None),
    )
    payload["title"] = final_title
    payload["path"] = entry["path"]
    payload["source_url"] = url
    json_dump(payload)
    return 0


def _validate_artifact_path(
    artifact_path: str | None,
    task: ResearchTask,
    context: str = "artifact",
) -> str:
    if not artifact_path:
        raise ValidationError(
            f"approval requires a valid {context}, but none was specified"
        )
    path = resolve_under_task(task.task_dir, artifact_path, label=context)
    if not path.exists():
        raise ValidationError(f"approved artifact path does not exist: {artifact_path}")
    if not path.is_file():
        raise ValidationError(f"approved artifact path is not a file: {artifact_path}")
    return str(path)


def _validate_primary_file_path(primary_file: str, task: ResearchTask) -> str:
    if not primary_file:
        raise ValidationError("primary_file cannot be empty")
    raw_path = primary_file.strip()
    path = resolve_under_task(task.task_dir, raw_path, label="primary_file")
    if not path.exists():
        raise ValidationError(f"primary_file does not exist: {raw_path}")
    if not path.is_file():
        raise ValidationError(f"primary_file is not a file: {raw_path}")
    return str(path)


def _validate_attachment_path(attachment: str, task: ResearchTask) -> str:
    raw_path = str(attachment or "").strip()
    if not raw_path:
        raise ValidationError("attachment cannot be empty")
    path = resolve_under_task(task.task_dir, raw_path, label="attachment")
    if not path.exists():
        raise ValidationError(f"attachment does not exist: {raw_path}")
    if not path.is_file():
        raise ValidationError(f"attachment is not a file: {raw_path}")
    return str(path)


def _build_delivery_outputs(
    raw_outputs: list[str],
    task: ResearchTask,
) -> list[dict[str, Any]]:
    outputs = [parse_output_artifact_arg(item) for item in raw_outputs]
    primary_count = sum(1 for item in outputs if item.get("role") == "primary_deliverable")
    if outputs and primary_count != 1:
        raise ValidationError("delivery outputs must declare exactly one primary_deliverable")
    result: list[dict[str, Any]] = []
    for item in outputs:
        validated_path = _validate_primary_file_path(str(item.get("path") or ""), task)
        result.append({**item, "path": validated_path})
    return result


def approve_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    manager = StateManager(task)
    state = task.read_state()
    now = utc_now()

    if state.get("status") not in ("awaiting_review", "complete", "idle"):
        raise ValidationError(
            f"approve is only valid for tasks awaiting review or in idle state, "
            f"got status: {state.get('status')}"
        )

    approved_artifact = (
        getattr(args, "approved_artifact", None)
        or state.get("delivery", {}).get("primary_file")
        or state.get("artifacts", {}).get("final_report_path")
    )
    approved_artifact = _validate_artifact_path(
        approved_artifact, task, "reviewable artifact"
    )

    with manager.editor() as state:
        review = state.setdefault("review", {})
        review["status"] = "approved"
        review["review_gated"] = False
        review["revision_count"] = int(review.get("revision_count") or 0)
        review["last_reviewed_at"] = now
        review["approved_artifact_path"] = approved_artifact
        review_entry = {
            "action": "approve",
            "at": now,
            "feedback": getattr(args, "feedback", None) or getattr(args, "text", None),
            "artifact": approved_artifact,
        }
        review.setdefault("history", []).append(review_entry)
        delivery = state.setdefault("delivery", {})
        delivery["review_ready"] = False
        delivery["ready"] = True

        if state.get("status") != "complete":
            state["status"] = "complete"
            normalized_reason = set_history_reason(state, "approved:user")
            remove_job_id = state.get("job", {}).get("job_id")
        else:
            normalized_reason = set_history_reason(state, "approved:user")
            remove_job_id = None

        state["updated_at"] = now
        state["history"]["last_transition"] = "approve"

    refresh_task_playbook(task)

    removal_payload = None
    if remove_job_id:
        removal_payload = remove_cron_job(remove_job_id)
        clear_bound_job(
            task, removed_job_id=remove_job_id, removal_payload=removal_payload
        )

    json_dump(
        {
            "status": state.get("status"),
            "review_status": "approved",
            "normalized_reason": normalized_reason,
            "approved_artifact_path": approved_artifact,
            "revision_count": review.get("revision_count"),
            "removed_job_id": remove_job_id,
            "removal_payload": removal_payload,
        }
    )
    return 0


def request_changes_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    manager = StateManager(task)
    state = task.read_state()
    now = utc_now()

    if state.get("status") in ("complete", "cancelled", "failed"):
        raise ValidationError(
            f"request-changes is not valid for terminal tasks, got status: {state.get('status')}"
        )

    feedback = getattr(args, "feedback", None) or getattr(args, "text", None)
    if not feedback:
        raise ValidationError("request-changes requires a feedback message")

    with manager.editor() as state:
        review = state.setdefault("review", {})
        review["status"] = "changes_requested"
        review["review_gated"] = False
        review["revision_count"] = int(review.get("revision_count") or 0) + 1
        review["last_feedback"] = feedback
        review["last_feedback_at"] = now
        review["last_reviewed_at"] = now
        review_entry = {
            "action": "request_changes",
            "at": now,
            "revision": review["revision_count"],
            "feedback": feedback,
        }
        review.setdefault("history", []).append(review_entry)

        working_memory = state.setdefault("working_memory", {})
        existing_summary = working_memory.get("summary") or ""
        feedback_prefix = f"[Ревизия {review['revision_count']}] Пользователь запросил изменения: {feedback}"
        if existing_summary:
            working_memory["summary"] = (
                f"{feedback_prefix}\n\nПредыдущий summary: {existing_summary}"
            )
        else:
            working_memory["summary"] = feedback_prefix

        open_questions = working_memory.setdefault("open_questions", [])
        if feedback not in open_questions:
            open_questions.append(f"Доработать по замечаниям: {feedback}")

        clear_reviewable_candidate(state)
        state["status"] = "idle"
        job = state.get("job") or {}
        if job.get("job_id"):
            resume_bound_job(state)
        state["updated_at"] = now
        state["history"]["last_transition"] = "request-changes"
        set_history_reason(
            state, f"revisions:{review['revision_count']}:changes-requested"
        )

    refresh_task_playbook(task)

    json_dump(
        {
            "status": "idle",
            "review_status": "changes_requested",
            "revision_count": review.get("revision_count"),
            "last_feedback": feedback,
            "normalized_reason": state.get("history", {}).get("last_reason"),
        }
    )
    return 0


def reopen_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    manager = StateManager(task)
    state = task.read_state()
    now = utc_now()

    if state.get("status") in ("cancelled",):
        raise ValidationError("Cannot reopen cancelled task")

    feedback = getattr(args, "feedback", None) or getattr(args, "text", None)

    current_status = state.get("status")
    should_restore_job = (
        current_status in REVIEW_WAIT_STATUSES or current_status == "complete"
    )
    restored_job_binding = None
    if should_restore_job:
        restored_job_binding = _restore_job_for_reopen(
            task=task,
            root=args.root,
            state=state,
        )

    with manager.editor() as state:
        review = state.setdefault("review", {})
        was_complete = state.get("status") == "complete"
        was_review_gated = state.get("status") in REVIEW_WAIT_STATUSES
        if was_complete or was_review_gated:
            review["status"] = "pending"
            review["revision_count"] = int(review.get("revision_count") or 0) + 1
            review["review_gated"] = False
            review["last_reviewed_at"] = now
            review["approved_artifact_path"] = None
            review_entry = {
                "action": "reopen",
                "at": now,
                "revision": review["revision_count"],
                "feedback": feedback,
            }
            review.setdefault("history", []).append(review_entry)

            history = state.setdefault("history", {})
            if restored_job_binding and restored_job_binding.get("job_id"):
                state["job"]["job_id"] = restored_job_binding["job_id"]
                if restored_job_binding.get("mode"):
                    state["job"]["mode"] = restored_job_binding["mode"]
                if restored_job_binding.get("tick_every_min"):
                    state["job"]["tick_every_min"] = restored_job_binding[
                        "tick_every_min"
                    ]
                state["job"]["enabled"] = restored_job_binding.get("enabled", True)
                state["job"]["suspended_reason"] = restored_job_binding.get(
                    "suspended_reason"
                )
                state["job"]["suspended_at"] = restored_job_binding.get("suspended_at")
                state["job"]["schedule_template"] = restored_job_binding.get(
                    "schedule_template"
                )
                history["last_job_binding"] = None

        if feedback:
            review["last_feedback"] = feedback
            review["last_feedback_at"] = now
            working_memory = state.setdefault("working_memory", {})
            existing_summary = working_memory.get("summary") or ""
            prefix = f"[Reopen rev {review.get('revision_count', 1)}] {feedback}"
            working_memory["summary"] = (
                f"{prefix}\n\n{existing_summary}" if existing_summary else prefix
            )
            open_questions = working_memory.setdefault("open_questions", [])
            if feedback not in open_questions:
                open_questions.append(f"Reopen: {feedback}")

        state["status"] = "idle"
        state["updated_at"] = now
        state["history"]["last_transition"] = "reopen"
        set_history_reason(state, "reopened:user")

    refresh_task_playbook(task)

    json_dump(
        {
            "status": "idle",
            "review_status": review.get("status"),
            "revision_count": review.get("revision_count"),
            "last_feedback": feedback,
            "normalized_reason": state.get("history", {}).get("last_reason"),
            "restored_job_id": restored_job_binding.get("job_id")
            if restored_job_binding
            else None,
            "restore_mode": restored_job_binding.get("restore_mode")
            if restored_job_binding
            else None,
        }
    )
    return 0


def mark_delivered_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    manager = StateManager(task)
    now = utc_now()

    explicit_primary_file = getattr(args, "primary_file", None)
    ready_flag = getattr(args, "ready", False)
    structured_outputs = _build_delivery_outputs(
        getattr(args, "output", None) or [],
        task,
    )
    structured_primary = next(
        (
            item
            for item in structured_outputs
            if item.get("role") == "primary_deliverable"
        ),
        None,
    )

    if explicit_primary_file is not None:
        validated_primary = _validate_primary_file_path(
            str(explicit_primary_file), task
        )
    elif structured_primary is not None:
        validated_primary = str(structured_primary.get("path") or "")
    else:
        validated_primary = None

    if ready_flag:
        state_for_check = task.read_state()
        existing_primary = state_for_check.get("delivery", {}).get("primary_file")
        primary_for_ready = validated_primary or existing_primary
        if not primary_for_ready:
            raise ValidationError(
                "cannot set delivery.ready=true without a valid primary_file; "
                "specify --primary-file or ensure one already exists in delivery state"
            )
        if validated_primary is None and existing_primary:
            _validate_primary_file_path(existing_primary, task)

    with manager.editor() as state:
        delivery = state.setdefault("delivery", {})
        if explicit_primary_file is not None:
            delivery["primary_file"] = validated_primary
        if structured_outputs:
            delivery["outputs"] = structured_outputs
            delivery["primary_file"] = validated_primary
            delivery["attachments"] = [
                str(item.get("path") or "")
                for item in structured_outputs
                if item.get("role") != "primary_deliverable" and item.get("path")
            ]
        if getattr(args, "summary_text", None) is not None:
            delivery["summary_text"] = str(args.summary_text).strip()
        if getattr(args, "channel_strategy", None) is not None:
            delivery["channel_strategy"] = str(args.channel_strategy).strip()
        attachments = getattr(args, "attachments", None)
        if attachments:
            existing = list(delivery.get("attachments") or [])
            for att in attachments:
                att_str = _validate_attachment_path(str(att), task)
                if att_str and att_str not in existing:
                    existing.append(att_str)
            delivery["attachments"] = existing
        if ready_flag:
            delivery["ready"] = True
        state["updated_at"] = now
        state.setdefault("history", {})["last_transition"] = "mark-delivered"

    refresh_task_playbook(task)

    state_after = task.read_state()
    delivery_after = state_after.get("delivery") or {}

    json_dump(
        {
            "status": state_after.get("status"),
            "task_id": state_after.get("id"),
            "delivery_ready": delivery_after.get("ready", False),
            "outputs": delivery_after.get("outputs") or [],
            "primary_file": delivery_after.get("primary_file"),
            "attachments": delivery_after.get("attachments") or [],
            "summary_text": delivery_after.get("summary_text"),
            "channel_strategy": delivery_after.get("channel_strategy"),
        }
    )
    return 0


def attach_pdf_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    task.ensure_layout()
    label = str(getattr(args, "label", "") or "").strip() or None
    note = str(getattr(args, "note", "") or "").strip() or None
    pdf_inputs = list(getattr(args, "file", []) or [])
    if not pdf_inputs:
        raise ValidationError("attach-pdf requires at least one --file")

    manifest_entries = read_corpus_manifest(task)
    attached: list[dict[str, object]] = []
    for raw in pdf_inputs:
        src = Path(raw).expanduser().resolve()
        _validate_pdf_file(src)
        dest_name = src.name if src.suffix.lower() == ".pdf" else f"{src.name}.pdf"
        dest = unique_copy_destination(task.corpus_dir, dest_name)
        shutil.copy2(src, dest)
        entry = build_corpus_entry(
            task,
            dest,
            source_path=str(src),
            label=label,
            note=note,
        )
        entry["content_hint"] = "pdf"
        manifest_entries.append(entry)
        attached.append(entry)
    write_corpus_manifest(task, manifest_entries)

    payload = _finalize_corpus_attachment(
        task,
        transition="attach-pdf",
        attached=attached,
        corpus_mode_override=getattr(args, "corpus_mode", None),
    )
    json_dump(payload)
    return 0
