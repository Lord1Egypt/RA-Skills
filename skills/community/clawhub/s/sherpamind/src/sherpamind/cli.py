from __future__ import annotations

from dataclasses import asdict, is_dataclass
import json
from pathlib import Path

import typer
from rich import print

from .analysis import (
    get_api_usage_summary,
    get_dataset_summary,
    get_enrichment_coverage,
    get_insight_snapshot,
    list_open_ticket_ages,
    list_recent_account_activity,
    list_recent_tickets,
    list_technician_recent_load,
    list_ticket_attachment_summary,
    list_ticket_counts_by_account,
    list_ticket_counts_by_priority,
    list_ticket_counts_by_status,
    list_ticket_counts_by_technician,
    list_ticket_log_types,
    search_ticket_document_chunks,
    search_ticket_documents,
)
from .automation import doctor_automation, remove_managed_cron_jobs
from .client import SherpaDeskClient
from .documents import export_ticket_chunks, export_ticket_documents, materialize_ticket_documents
from .freshness import get_sync_freshness
from .enrichment import enrich_priority_ticket_details
from .migrate import archive_legacy_state, migrate_legacy_state
from .paths import ensure_path_layout
from .observability import generate_runtime_status_artifacts
from .public_artifacts import generate_public_snapshot
from .service_manager import (
    doctor_service,
    install_service,
    restart_service,
    service_status,
    start_service,
    stop_service,
    uninstall_service,
)
from .service_runtime import run_pending_tasks, run_service_loop
from .ingest import (
    seed_all,
    sync_cold_closed_audit,
    sync_delta,
    sync_hot_open_tickets,
    sync_warm_closed_tickets,
)
from .settings import load_settings, stage_api_key, stage_api_user, stage_connection_settings
from .summaries import get_account_summary, get_technician_summary, get_ticket_summary
from .vector_exports import export_embedding_manifest, export_embedding_ready_chunks, get_retrieval_readiness_summary
from .vector_index import build_vector_index, get_vector_index_status, search_vector_index
from .watch import watch_new_tickets
from .db import backfill_ticket_entity_stubs, backfill_ticket_technician_stubs, initialize_db

app = typer.Typer(help="SherpaMind CLI")


def _json_ready(value):
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {key: _json_ready(inner) for key, inner in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(inner) for inner in value]
    return value


def _build_client() -> SherpaDeskClient:
    settings = load_settings()
    if not settings.api_key:
        raise typer.BadParameter("SherpaDesk API key is required for live API commands. Stage it in .SherpaMind/private/secrets/sherpadesk_api_key.txt or use `stage-api-key`.")
    return SherpaDeskClient(
        api_base_url=settings.api_base_url,
        api_key=settings.api_key,
        api_user=settings.api_user,
        org_key=settings.org_key,
        instance_key=settings.instance_key,
        timeout_seconds=settings.request_timeout_seconds,
        min_interval_seconds=settings.request_min_interval_seconds,
        request_tracking_db_path=settings.db_path,
    )


@app.command("init-db")
def init_db() -> None:
    settings = load_settings()
    initialize_db(settings.db_path)
    print({"status": "ok", "db": str(settings.db_path)})


@app.command("backfill-technician-stubs")
def backfill_technician_stubs() -> None:
    settings = load_settings()
    initialize_db(settings.db_path)
    print(json.dumps(backfill_ticket_technician_stubs(settings.db_path), indent=2))


@app.command("backfill-ticket-entity-stubs")
def backfill_ticket_entity_stubs_command() -> None:
    settings = load_settings()
    initialize_db(settings.db_path)
    print(json.dumps(backfill_ticket_entity_stubs(settings.db_path), indent=2))


@app.command("workspace-layout")
def workspace_layout() -> None:
    paths = ensure_path_layout()
    print(json.dumps({
        "workspace_root": str(paths.workspace_root),
        "root": str(paths.root),
        "config_root": str(paths.config_root),
        "secrets_root": str(paths.secrets_root),
        "data_root": str(paths.data_root),
        "state_root": str(paths.state_root),
        "logs_root": str(paths.logs_root),
        "runtime_root": str(paths.runtime_root),
        "public_root": str(paths.public_root),
        "runtime_venv": str(paths.runtime_venv),
        "db_path": str(paths.db_path),
        "watch_state_path": str(paths.watch_state_path),
        "exports_root": str(paths.exports_root),
        "docs_root": str(paths.docs_root),
        "settings_file": str(paths.settings_file),
        "api_key_file": str(paths.api_key_file),
        "api_user_file": str(paths.api_user_file),
        "service_log": str(paths.service_log),
        "service_state_file": str(paths.service_state_file),
    }, indent=2))


@app.command("configure")
def configure(
    org_key: str | None = None,
    instance_key: str | None = None,
    api_base_url: str | None = None,
    notify_channel: str | None = None,
) -> None:
    settings_file = stage_connection_settings(
        api_base_url=api_base_url,
        org_key=org_key,
        instance_key=instance_key,
        notify_channel=notify_channel,
    )
    print(json.dumps({
        "status": "ok",
        "settings_file": str(settings_file),
        "updated_keys": [
            key for key, value in {
                "SHERPADESK_API_BASE_URL": api_base_url,
                "SHERPADESK_ORG_KEY": org_key,
                "SHERPAMIND_NOTIFY_CHANNEL": notify_channel,
                "SHERPADESK_INSTANCE_KEY": instance_key,
            }.items() if value is not None
        ],
        "note": "Non-secret settings were updated. Stage secrets separately under .SherpaMind/private/secrets/.",
    }, indent=2))


@app.command("stage-api-key")
def stage_api_key_cmd(
    from_file: Path | None = None,
    value: str | None = None,
) -> None:
    secret_path = stage_api_key(api_key=value, from_file=from_file)
    print(json.dumps({"status": "ok", "api_key_file": str(secret_path)}, indent=2))


@app.command("stage-api-user")
def stage_api_user_cmd(
    from_file: Path | None = None,
    value: str | None = None,
) -> None:
    secret_path = stage_api_user(api_user=value, from_file=from_file)
    print(json.dumps({"status": "ok", "api_user_file": str(secret_path)}, indent=2))


@app.command("doctor")
def doctor() -> None:
    settings = load_settings()
    paths = ensure_path_layout()
    legacy_db = paths.workspace_root / "state" / "sherpamind.sqlite3"
    legacy_watch = paths.workspace_root / "state" / "watch_state.json"
    checks = {
        "settings_file_exists": paths.settings_file.exists(),
        "api_key_file_exists": paths.api_key_file.exists(),
        "api_user_file_exists": paths.api_user_file.exists(),
        "runtime_venv_exists": paths.runtime_venv.exists(),
        "db_exists": settings.db_path.exists(),
        "watch_state_exists": settings.watch_state_path.exists(),
        "legacy_db_exists": legacy_db.exists(),
        "legacy_watch_state_exists": legacy_watch.exists(),
        "api_key_present": bool(settings.api_key),
        "org_key_present": bool(settings.org_key),
        "instance_key_present": bool(settings.instance_key),
    }
    print(json.dumps({
        "status": "ok",
        "paths": {
            "root": str(paths.root),
            "config_root": str(paths.config_root),
            "secrets_root": str(paths.secrets_root),
            "data_root": str(paths.data_root),
            "state_root": str(paths.state_root),
            "logs_root": str(paths.logs_root),
            "public_root": str(paths.public_root),
            "settings_file": str(paths.settings_file),
            "api_key_file": str(paths.api_key_file),
            "api_user_file": str(paths.api_user_file),
            "runtime_venv": str(paths.runtime_venv),
            "db_path": str(settings.db_path),
            "service_log": str(paths.service_log),
            "service_state_file": str(paths.service_state_file),
        },
        "checks": checks,
        "service": doctor_service(),
        "legacy_cron": doctor_automation(),
        "api_usage": get_api_usage_summary(settings.db_path),
    }, indent=2))


@app.command("migrate-legacy-state")
def migrate_state() -> None:
    paths = ensure_path_layout()
    result = migrate_legacy_state(paths.workspace_root)
    print(json.dumps(result.__dict__, indent=2))


@app.command("cleanup-legacy-cron")
def cleanup_legacy_cron() -> None:
    result = remove_managed_cron_jobs()
    print(json.dumps(result.__dict__, indent=2))


@app.command("archive-legacy-state")
def archive_legacy() -> None:
    paths = ensure_path_layout()
    result = archive_legacy_state(paths.workspace_root)
    print(json.dumps(result.__dict__, indent=2))


@app.command("setup")
def setup(
    migrate_legacy: bool = True,
    initialize_db_only: bool = False,
    install_service_now: bool = False,
    cleanup_legacy_cron_now: bool = True,
) -> None:
    settings = load_settings()
    paths = ensure_path_layout()
    steps = []
    if migrate_legacy:
        migration = migrate_legacy_state(paths.workspace_root)
        steps.append({"migration": migration.__dict__})
    initialize_db(settings.db_path)
    steps.append({"init_db": str(settings.db_path)})
    if cleanup_legacy_cron_now:
        try:
            cleanup = remove_managed_cron_jobs()
            steps.append({"legacy_cron_cleanup": cleanup.__dict__})
        except Exception as exc:
            steps.append({"legacy_cron_cleanup_error": f"{type(exc).__name__}: {exc}"})
    try:
        archive = archive_legacy_state(paths.workspace_root)
        steps.append({"legacy_state_archive": archive.__dict__})
    except Exception as exc:
        steps.append({"legacy_state_archive_error": f"{type(exc).__name__}: {exc}"})
    if not initialize_db_only and settings.db_path.exists():
        try:
            snapshot = generate_public_snapshot(settings.db_path)
            steps.append({"public_snapshot": snapshot})
        except Exception as exc:
            steps.append({"public_snapshot_error": f"{type(exc).__name__}: {exc}"})
    if install_service_now:
        try:
            service = install_service(start_now=True)
            steps.append({"service_install": service.__dict__})
        except Exception as exc:
            steps.append({"service_install_error": f"{type(exc).__name__}: {exc}"})
    print(json.dumps({
        "status": "ok",
        "message": "SherpaMind setup flow completed.",
        "steps": steps,
        "next": [
            "python3 scripts/run.py bootstrap-audit",
            "python3 scripts/run.py doctor",
            "python3 scripts/run.py stage-api-key --from-file <path-to-token-file>",
            "python3 scripts/run.py discover-orgs",
            "python3 scripts/run.py configure --org-key <org> --instance-key <instance>",
            "python3 scripts/run.py seed",
            "python3 scripts/run.py install-service",
        ],
    }, indent=2))


@app.command("bootstrap-audit")
def bootstrap_audit(summary: bool = False) -> None:
    settings = load_settings()
    paths = ensure_path_layout()
    service = doctor_service()
    checks = {
        "python3": True,
        "systemctl_user": service.get("systemctl_user_available", True),
    }
    onboarding_steps = []

    def add_step(step: str, details: str, command: str | None = None, user_action_required: bool = True) -> None:
        onboarding_steps.append({
            "step": step,
            "details": details,
            "command": command,
            "user_action_required": user_action_required,
        })

    if not paths.runtime_venv.exists():
        add_step("bootstrap-runtime", "Bootstrap the runtime venv and staged runtime directories.", "python3 scripts/bootstrap.py")
    if not paths.api_key_file.exists():
        add_step("stage-api-key", f"Stage the SherpaDesk API key in {paths.api_key_file} or use stage-api-key.", "python3 scripts/run.py stage-api-key --from-file <path-to-token-file>")
    if not settings.org_key or not settings.instance_key:
        add_step("discover-and-configure-org-instance", "Discover orgs/instances, then persist the chosen org/instance in non-secret settings.", "python3 scripts/run.py discover-orgs")
    if not settings.db_path.exists():
        add_step("initialize-db", "Initialize the local SQLite store and runtime scaffolding.", "python3 scripts/run.py setup")
    if not service.get("unit_exists"):
        add_step("install-service", "Optionally install the user-level background service after bootstrap and seeding are complete.", "python3 scripts/run.py install-service", user_action_required=False)

    payload = {
        "ready": len(onboarding_steps) == 0,
        "workspace_root": str(paths.workspace_root),
        "runtime_root": str(paths.root),
        "runtime_paths": {
            "config_root": str(paths.config_root),
            "secrets_root": str(paths.secrets_root),
            "data_root": str(paths.data_root),
            "state_root": str(paths.state_root),
            "logs_root": str(paths.logs_root),
            "runtime_root": str(paths.runtime_root),
            "public_root": str(paths.public_root),
            "settings_file": str(paths.settings_file),
            "api_key_file": str(paths.api_key_file),
            "api_user_file": str(paths.api_user_file),
            "db_path": str(paths.db_path),
        },
        "credentials": {
            "api_key_present": bool(settings.api_key),
            "org_key_present": bool(settings.org_key),
            "instance_key_present": bool(settings.instance_key),
            "api_user_present": bool(settings.api_user),
        },
        "service": service,
        "checks": checks,
        "summary": {
            "blocking_step_count": sum(1 for step in onboarding_steps if step["user_action_required"]),
            "nonblocking_step_count": sum(1 for step in onboarding_steps if not step["user_action_required"]),
        },
        "onboarding_steps": onboarding_steps,
    }
    if summary:
        print(f"ready={payload['ready']}")
        print(f"runtime_root={paths.root}")
        print(f"settings_file={paths.settings_file}")
        print(f"api_key_file={paths.api_key_file}")
        print(f"blocking_step_count={payload['summary']['blocking_step_count']}")
        print(f"nonblocking_step_count={payload['summary']['nonblocking_step_count']}")
        for step in onboarding_steps:
            print(f"next_step={step['step']}: {step['details']}")
            if step['command']:
                print(f"next_command={step['command']}")
        return
    print(json.dumps(payload, indent=2))


@app.command("install-service")
def install_service_cmd(start_now: bool = True) -> None:
    result = install_service(start_now=start_now)
    print(json.dumps(result.__dict__, indent=2))


@app.command("uninstall-service")
def uninstall_service_cmd(stop_now: bool = True) -> None:
    result = uninstall_service(stop_now=stop_now)
    print(json.dumps(result.__dict__, indent=2))


@app.command("start-service")
def start_service_cmd() -> None:
    result = start_service()
    print(json.dumps(result.__dict__, indent=2))


@app.command("stop-service")
def stop_service_cmd() -> None:
    result = stop_service()
    print(json.dumps(result.__dict__, indent=2))


@app.command("restart-service")
def restart_service_cmd() -> None:
    result = restart_service()
    print(json.dumps(result.__dict__, indent=2))


@app.command("service-status")
def service_status_cmd() -> None:
    print(json.dumps(service_status(), indent=2))


@app.command("service-run")
def service_run() -> None:
    raise SystemExit(run_service_loop())


@app.command("service-run-once")
def service_run_once() -> None:
    settings = load_settings()
    print(json.dumps(_json_ready(run_pending_tasks(settings)), indent=2))


@app.command("discover-orgs")
def discover_orgs() -> None:
    client = _build_client()
    result = client.discover_organizations()
    print(json.dumps(result, indent=2))


@app.command("seed")
def seed() -> None:
    settings = load_settings()
    result = seed_all(settings)
    print(json.dumps(result.__dict__, indent=2))


@app.command("sync")
def sync() -> None:
    settings = load_settings()
    result = sync_delta(settings)
    print(json.dumps(result.__dict__, indent=2))


@app.command("watch")
def watch() -> None:
    settings = load_settings()
    result = watch_new_tickets(settings)
    print(json.dumps(result.__dict__, indent=2))


@app.command("sync-hot-open")
def sync_hot_open() -> None:
    settings = load_settings()
    result = sync_hot_open_tickets(settings)
    print(json.dumps(result.__dict__, indent=2))


@app.command("sync-warm-closed")
def sync_warm_closed() -> None:
    settings = load_settings()
    result = sync_warm_closed_tickets(settings)
    print(json.dumps(result.__dict__, indent=2))


@app.command("sync-cold-closed-audit")
def sync_cold_closed() -> None:
    settings = load_settings()
    result = sync_cold_closed_audit(settings)
    print(json.dumps(result.__dict__, indent=2))


@app.command("enrich-priority-ticket-details")
def enrich_priority_details(limit: int = 50, materialize_docs: bool = True) -> None:
    settings = load_settings()
    result = enrich_priority_ticket_details(settings, limit=limit, materialize_docs=materialize_docs)
    print(json.dumps(result.__dict__, indent=2))


@app.command("materialize-ticket-docs")
def materialize_docs(limit: int = 0) -> None:
    settings = load_settings()
    initialize_db(settings.db_path)
    effective_limit = None if limit <= 0 else limit
    result = materialize_ticket_documents(settings.db_path, limit=effective_limit)
    print(json.dumps(result, indent=2))


@app.command("dataset-summary")
def dataset_summary() -> None:
    settings = load_settings()
    print(json.dumps(get_dataset_summary(settings.db_path), indent=2))


@app.command("report-api-usage")
def report_api_usage() -> None:
    settings = load_settings()
    usage = get_api_usage_summary(settings.db_path)
    usage["configured_hourly_limit"] = settings.api_hourly_limit
    usage["configured_warn_ratio"] = settings.api_budget_warn_ratio
    usage["configured_critical_ratio"] = settings.api_budget_critical_ratio
    usage["configured_retention_days"] = settings.api_request_log_retention_days
    print(json.dumps(usage, indent=2))


@app.command("insight-snapshot")
def insight_snapshot() -> None:
    settings = load_settings()
    print(json.dumps(get_insight_snapshot(settings.db_path), indent=2))


@app.command("report-enrichment-coverage")
def report_enrichment_coverage() -> None:
    settings = load_settings()
    print(json.dumps(get_enrichment_coverage(settings.db_path), indent=2))


@app.command("report-ticket-counts")
def report_ticket_counts(limit: int = 20) -> None:
    settings = load_settings()
    rows = list_ticket_counts_by_account(settings.db_path, limit=limit)
    print(json.dumps(rows, indent=2))


@app.command("report-status-counts")
def report_status_counts() -> None:
    settings = load_settings()
    rows = list_ticket_counts_by_status(settings.db_path)
    print(json.dumps(rows, indent=2))


@app.command("report-priority-counts")
def report_priority_counts() -> None:
    settings = load_settings()
    rows = list_ticket_counts_by_priority(settings.db_path)
    print(json.dumps(rows, indent=2))


@app.command("report-technician-counts")
def report_technician_counts(limit: int = 20) -> None:
    settings = load_settings()
    rows = list_ticket_counts_by_technician(settings.db_path, limit=limit)
    print(json.dumps(rows, indent=2))


@app.command("report-ticket-log-types")
def report_ticket_log_types(limit: int = 20) -> None:
    settings = load_settings()
    rows = list_ticket_log_types(settings.db_path, limit=limit)
    print(json.dumps(rows, indent=2))


@app.command("report-attachment-summary")
def report_attachment_summary(limit: int = 20) -> None:
    settings = load_settings()
    rows = list_ticket_attachment_summary(settings.db_path, limit=limit)
    print(json.dumps(rows, indent=2))


@app.command("recent-tickets")
def recent_tickets(limit: int = 20) -> None:
    settings = load_settings()
    rows = list_recent_tickets(settings.db_path, limit=limit)
    print(json.dumps(rows, indent=2))


@app.command("open-ticket-ages")
def open_ticket_ages(limit: int = 20) -> None:
    settings = load_settings()
    rows = list_open_ticket_ages(settings.db_path, limit=limit)
    print(json.dumps(rows, indent=2))


@app.command("recent-account-activity")
def recent_account_activity(days: int = 7, limit: int = 20) -> None:
    settings = load_settings()
    rows = list_recent_account_activity(settings.db_path, days=days, limit=limit)
    print(json.dumps(rows, indent=2))


@app.command("recent-technician-load")
def recent_technician_load(days: int = 7, limit: int = 20) -> None:
    settings = load_settings()
    rows = list_technician_recent_load(settings.db_path, days=days, limit=limit)
    print(json.dumps(rows, indent=2))


@app.command("account-summary")
def account_summary(account_query: str, limit_open: int = 10, limit_recent: int = 10) -> None:
    settings = load_settings()
    print(json.dumps(get_account_summary(settings.db_path, account_query, limit_open=limit_open, limit_recent=limit_recent), indent=2))


@app.command("technician-summary")
def technician_summary(technician_query: str, limit_open: int = 10, limit_recent: int = 10) -> None:
    settings = load_settings()
    print(json.dumps(get_technician_summary(settings.db_path, technician_query, limit_open=limit_open, limit_recent=limit_recent), indent=2))


@app.command("ticket-summary")
def ticket_summary(ticket_query: str, limit_logs: int = 10, limit_attachments: int = 10) -> None:
    settings = load_settings()
    print(json.dumps(get_ticket_summary(settings.db_path, ticket_query, limit_logs=limit_logs, limit_attachments=limit_attachments), indent=2))


@app.command("search-ticket-docs")
def search_docs(
    query: str,
    limit: int = 20,
    account: str | None = None,
    status: str | None = None,
    technician: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    class_name: str | None = None,
    submission_category: str | None = None,
    resolution_category: str | None = None,
    department: str | None = None,
) -> None:
    settings = load_settings()
    rows = search_ticket_documents(
        settings.db_path,
        query=query,
        limit=limit,
        account=account,
        status=status,
        technician=technician,
        priority=priority,
        category=category,
        class_name=class_name,
        submission_category=submission_category,
        resolution_category=resolution_category,
        department=department,
    )
    print(json.dumps(rows, indent=2))


@app.command("search-ticket-chunks")
def search_chunks(
    query: str,
    limit: int = 20,
    account: str | None = None,
    status: str | None = None,
    technician: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    class_name: str | None = None,
    submission_category: str | None = None,
    resolution_category: str | None = None,
    department: str | None = None,
) -> None:
    settings = load_settings()
    rows = search_ticket_document_chunks(
        settings.db_path,
        query=query,
        limit=limit,
        account=account,
        status=status,
        technician=technician,
        priority=priority,
        category=category,
        class_name=class_name,
        submission_category=submission_category,
        resolution_category=resolution_category,
        department=department,
    )
    print(json.dumps(rows, indent=2))


@app.command("export-ticket-docs")
def export_ticket_docs(output_path: str = "", limit: int = 0) -> None:
    settings = load_settings()
    paths = ensure_path_layout()
    effective_limit = None if limit <= 0 else limit
    resolved_output = Path(output_path) if output_path else (paths.exports_root / "ticket-docs.jsonl")
    result = export_ticket_documents(settings.db_path, resolved_output, limit=effective_limit)
    print(json.dumps(result, indent=2))


@app.command("export-ticket-chunks")
def export_ticket_chunks_cmd(output_path: str = "", limit: int = 0) -> None:
    settings = load_settings()
    paths = ensure_path_layout()
    effective_limit = None if limit <= 0 else limit
    resolved_output = Path(output_path) if output_path else (paths.exports_root / "ticket-chunks.jsonl")
    result = export_ticket_chunks(settings.db_path, resolved_output, limit=effective_limit)
    print(json.dumps(result, indent=2))


@app.command("export-embedding-chunks")
def export_embedding_chunks_cmd(output_path: str = "", limit: int = 0) -> None:
    settings = load_settings()
    paths = ensure_path_layout()
    effective_limit = None if limit <= 0 else limit
    resolved_output = Path(output_path) if output_path else (paths.exports_root / "embedding-ticket-chunks.jsonl")
    result = export_embedding_ready_chunks(settings.db_path, resolved_output, limit=effective_limit)
    print(json.dumps(result, indent=2))


@app.command("export-embedding-manifest")
def export_embedding_manifest_cmd(output_path: str = "", limit: int = 0) -> None:
    settings = load_settings()
    paths = ensure_path_layout()
    effective_limit = None if limit <= 0 else limit
    resolved_output = Path(output_path) if output_path else (paths.exports_root / "embedding-ticket-chunks.manifest.json")
    result = export_embedding_manifest(settings.db_path, resolved_output, limit=effective_limit)
    print(json.dumps(result, indent=2))


@app.command("build-vector-index")
def build_vector_index_cmd(limit: int = 0, dims: int = 256) -> None:
    settings = load_settings()
    effective_limit = None if limit <= 0 else limit
    result = build_vector_index(settings.db_path, dims=dims, limit=effective_limit)
    print(json.dumps(result, indent=2))


@app.command("report-vector-index-status")
def report_vector_index_status() -> None:
    settings = load_settings()
    print(json.dumps(get_vector_index_status(settings.db_path), indent=2))


@app.command("report-retrieval-readiness")
def report_retrieval_readiness(limit: int = 0) -> None:
    settings = load_settings()
    effective_limit = None if limit <= 0 else limit
    print(json.dumps(get_retrieval_readiness_summary(settings.db_path, limit=effective_limit), indent=2))


@app.command("search-vector-index")
def search_vector_index_cmd(
    query: str,
    limit: int = 10,
    account: str | None = None,
    status: str | None = None,
    technician: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    class_name: str | None = None,
    submission_category: str | None = None,
    resolution_category: str | None = None,
    department: str | None = None,
) -> None:
    settings = load_settings()
    rows = search_vector_index(
        settings.db_path,
        query_text=query,
        limit=limit,
        account=account,
        status=status,
        technician=technician,
        priority=priority,
        category=category,
        class_name=class_name,
        submission_category=submission_category,
        resolution_category=resolution_category,
        department=department,
    )
    print(json.dumps(rows, indent=2))


@app.command("generate-public-snapshot")
def generate_snapshot() -> None:
    settings = load_settings()
    result = generate_public_snapshot(settings.db_path)
    print(json.dumps(result, indent=2))


@app.command("generate-runtime-status")
def generate_runtime_status() -> None:
    settings = load_settings()
    result = generate_runtime_status_artifacts(settings.db_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    app()
