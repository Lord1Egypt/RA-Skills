from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import shutil


def discover_workspace_root(*, repo_root: Path | None = None, cwd: Path | None = None) -> Path:
    explicit = os.getenv("SHERPAMIND_WORKSPACE_ROOT")
    if explicit:
        return Path(explicit).resolve()
    repo = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    if repo.parent.name == "skills":
        return repo.parent.parent.resolve()
    return (cwd or Path.cwd()).resolve()


@dataclass(frozen=True)
class SherpaMindPaths:
    workspace_root: Path
    root: Path
    private_root: Path
    config_root: Path
    secrets_root: Path
    data_root: Path
    state_root: Path
    logs_root: Path
    runtime_root: Path
    public_root: Path
    exports_root: Path
    docs_root: Path
    settings_file: Path
    api_key_file: Path
    api_user_file: Path
    db_path: Path
    watch_state_path: Path
    service_state_file: Path
    service_log: Path
    runtime_venv: Path
    legacy_env_file: Path


SECRET_FILE_MODE = 0o600


def resolve_paths() -> SherpaMindPaths:
    workspace_root = discover_workspace_root()
    root = workspace_root / ".SherpaMind"
    private_root = root / "private"
    config_root = private_root / "config"
    secrets_root = private_root / "secrets"
    data_root = private_root / "data"
    state_root = private_root / "state"
    logs_root = private_root / "logs"
    runtime_root = private_root / "runtime"
    public_root = root / "public"
    exports_root = public_root / "exports"
    docs_root = public_root / "docs"
    return SherpaMindPaths(
        workspace_root=workspace_root,
        root=root,
        private_root=private_root,
        config_root=config_root,
        secrets_root=secrets_root,
        data_root=data_root,
        state_root=state_root,
        logs_root=logs_root,
        runtime_root=runtime_root,
        public_root=public_root,
        exports_root=exports_root,
        docs_root=docs_root,
        settings_file=config_root / "settings.env",
        api_key_file=secrets_root / "sherpadesk_api_key.txt",
        api_user_file=secrets_root / "sherpadesk_api_user.txt",
        db_path=data_root / "sherpamind.sqlite3",
        watch_state_path=state_root / "watch_state.json",
        service_state_file=state_root / "service-state.json",
        service_log=logs_root / "service.log",
        runtime_venv=runtime_root / "venv",
        legacy_env_file=private_root / "config.env",
    )


def _write_secret_file(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8")
    try:
        path.chmod(SECRET_FILE_MODE)
    except OSError:
        pass


def _read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _write_settings_file(path: Path, values: dict[str, str]) -> None:
    ordered_keys = [
        "SHERPADESK_API_BASE_URL",
        "SHERPADESK_ORG_KEY",
        "SHERPAMIND_INSTANCE_KEY",
        "SHERPADESK_INSTANCE_KEY",
        "SHERPAMIND_NOTIFY_CHANNEL",
        "SHERPAMIND_REQUEST_MIN_INTERVAL_SECONDS",
        "SHERPAMIND_REQUEST_TIMEOUT_SECONDS",
        "SHERPAMIND_SEED_PAGE_SIZE",
        "SHERPAMIND_SEED_MAX_PAGES",
        "SHERPAMIND_HOT_OPEN_PAGES",
        "SHERPAMIND_WARM_CLOSED_PAGES",
        "SHERPAMIND_WARM_CLOSED_DAYS",
        "SHERPAMIND_COLD_CLOSED_PAGES_PER_RUN",
        "SHERPAMIND_SERVICE_HOT_OPEN_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_WARM_CLOSED_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_COLD_CLOSED_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_ENRICHMENT_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_PUBLIC_SNAPSHOT_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_VECTOR_REFRESH_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_DOCTOR_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_ENRICHMENT_LIMIT",
        "SHERPAMIND_SERVICE_COLD_BOOTSTRAP_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_ENRICHMENT_BOOTSTRAP_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_ENRICHMENT_BOOTSTRAP_LIMIT",
        "SHERPAMIND_COLD_CLOSED_BOOTSTRAP_PAGES_PER_RUN",
        "SHERPAMIND_API_HOURLY_LIMIT",
        "SHERPAMIND_API_BUDGET_WARN_RATIO",
        "SHERPAMIND_API_BUDGET_CRITICAL_RATIO",
        "SHERPAMIND_API_REQUEST_LOG_RETENTION_DAYS",
    ]
    lines = [
        "# SherpaMind staged non-secret settings",
        "# Runtime state lives under .SherpaMind/private/ outside the skill tree.",
        "# Secrets are stored separately under .SherpaMind/private/secrets/.",
    ]
    for key in ordered_keys:
        if key in values:
            lines.append(f"{key}={values[key]}")
    for key in sorted(values):
        if key not in ordered_keys:
            lines.append(f"{key}={values[key]}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _merge_legacy_settings_into_current(paths: SherpaMindPaths) -> None:
    legacy_values = _read_env_file(paths.legacy_env_file)
    current_settings = _read_env_file(paths.settings_file)
    changed_settings = False
    for key in [
        "SHERPADESK_API_BASE_URL",
        "SHERPADESK_ORG_KEY",
        "SHERPADESK_INSTANCE_KEY",
        "SHERPAMIND_NOTIFY_CHANNEL",
        "SHERPAMIND_REQUEST_MIN_INTERVAL_SECONDS",
        "SHERPAMIND_REQUEST_TIMEOUT_SECONDS",
        "SHERPAMIND_SEED_PAGE_SIZE",
        "SHERPAMIND_SEED_MAX_PAGES",
        "SHERPAMIND_HOT_OPEN_PAGES",
        "SHERPAMIND_WARM_CLOSED_PAGES",
        "SHERPAMIND_WARM_CLOSED_DAYS",
        "SHERPAMIND_COLD_CLOSED_PAGES_PER_RUN",
        "SHERPAMIND_SERVICE_HOT_OPEN_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_WARM_CLOSED_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_COLD_CLOSED_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_ENRICHMENT_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_PUBLIC_SNAPSHOT_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_VECTOR_REFRESH_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_DOCTOR_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_ENRICHMENT_LIMIT",
        "SHERPAMIND_SERVICE_COLD_BOOTSTRAP_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_ENRICHMENT_BOOTSTRAP_EVERY_SECONDS",
        "SHERPAMIND_SERVICE_ENRICHMENT_BOOTSTRAP_LIMIT",
        "SHERPAMIND_COLD_CLOSED_BOOTSTRAP_PAGES_PER_RUN",
        "SHERPAMIND_API_HOURLY_LIMIT",
        "SHERPAMIND_API_BUDGET_WARN_RATIO",
        "SHERPAMIND_API_BUDGET_CRITICAL_RATIO",
        "SHERPAMIND_API_REQUEST_LOG_RETENTION_DAYS",
    ]:
        value = legacy_values.get(key)
        if value is not None and key not in current_settings:
            current_settings[key] = value
            changed_settings = True
    if changed_settings or (legacy_values and not paths.settings_file.exists()):
        _write_settings_file(paths.settings_file, current_settings)
    if not paths.api_key_file.exists() and legacy_values.get("SHERPADESK_API_KEY"):
        _write_secret_file(paths.api_key_file, legacy_values["SHERPADESK_API_KEY"])
    if not paths.api_user_file.exists() and legacy_values.get("SHERPADESK_API_USER"):
        _write_secret_file(paths.api_user_file, legacy_values["SHERPADESK_API_USER"])


def _move_if_missing(source: Path, target: Path) -> None:
    if source.exists() and not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))


def _move_children_if_target_empty(source_dir: Path, target_dir: Path) -> None:
    if not source_dir.exists():
        return
    target_dir.mkdir(parents=True, exist_ok=True)
    if any(target_dir.iterdir()):
        return
    for child in sorted(source_dir.iterdir()):
        shutil.move(str(child), str(target_dir / child.name))
    try:
        source_dir.rmdir()
    except OSError:
        pass


def _migrate_flat_layout_into_private(paths: SherpaMindPaths) -> None:
    flat_to_private = [
        (paths.root / "config", paths.config_root),
        (paths.root / "secrets", paths.secrets_root),
        (paths.root / "data", paths.data_root),
        (paths.root / "state", paths.state_root),
        (paths.root / "logs", paths.logs_root),
        (paths.root / "runtime", paths.runtime_root),
    ]
    for source_dir, target_dir in flat_to_private:
        if source_dir == target_dir:
            continue
        _move_children_if_target_empty(source_dir, target_dir)
        if source_dir.exists() and not any(source_dir.iterdir()):
            try:
                source_dir.rmdir()
            except OSError:
                pass


def _migrate_legacy_private_layout(paths: SherpaMindPaths) -> None:
    _merge_legacy_settings_into_current(paths)
    _move_if_missing(paths.private_root / "sherpamind.sqlite3", paths.db_path)
    _move_if_missing(paths.private_root / "watch_state.json", paths.watch_state_path)
    _move_if_missing(paths.private_root / "service-state.json", paths.service_state_file)
    _move_if_missing(paths.private_root / "logs" / "service.log", paths.service_log)
    _move_children_if_target_empty(paths.private_root / "runtime", paths.runtime_root)


def ensure_path_layout() -> SherpaMindPaths:
    paths = resolve_paths()
    for path in [
        paths.root,
        paths.private_root,
        paths.config_root,
        paths.secrets_root,
        paths.data_root,
        paths.state_root,
        paths.logs_root,
        paths.runtime_root,
        paths.public_root,
        paths.exports_root,
        paths.docs_root,
    ]:
        path.mkdir(parents=True, exist_ok=True)
    _migrate_flat_layout_into_private(paths)
    _migrate_legacy_private_layout(paths)
    if not paths.settings_file.exists():
        _write_settings_file(paths.settings_file, {"SHERPADESK_API_BASE_URL": "https://api.sherpadesk.com"})
    return paths
