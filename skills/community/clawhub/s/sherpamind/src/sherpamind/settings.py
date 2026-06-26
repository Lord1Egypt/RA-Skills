from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from .paths import ensure_path_layout


@dataclass(frozen=True)
class Settings:
    api_base_url: str
    api_key: str | None
    api_user: str | None
    org_key: str | None
    instance_key: str | None
    db_path: Path
    watch_state_path: Path
    notify_channel: str | None
    request_min_interval_seconds: float
    request_timeout_seconds: float
    seed_page_size: int
    seed_max_pages: int | None
    hot_open_pages: int
    warm_closed_pages: int
    warm_closed_days: int
    cold_closed_pages_per_run: int
    service_hot_open_every_seconds: int = 300
    service_warm_closed_every_seconds: int = 14400
    service_cold_closed_every_seconds: int = 86400
    service_enrichment_every_seconds: int = 7200
    service_public_snapshot_every_seconds: int = 1800
    service_vector_refresh_every_seconds: int = 1800
    service_doctor_every_seconds: int = 43200
    service_enrichment_limit: int = 25
    service_cold_bootstrap_every_seconds: int = 1800
    service_enrichment_bootstrap_every_seconds: int = 900
    service_enrichment_bootstrap_limit: int = 240
    cold_closed_bootstrap_pages_per_run: int = 10
    api_hourly_limit: int = 600
    api_budget_warn_ratio: float = 0.7
    api_budget_critical_ratio: float = 0.85
    api_request_log_retention_days: int = 14


def _read_key_value_file(path: Path) -> dict[str, str]:
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


def _read_secret_file(path: Path) -> str | None:
    if not path.exists():
        return None
    value = path.read_text(encoding="utf-8").strip()
    return value or None


def _write_key_value_file(path: Path, values: dict[str, str]) -> None:
    ordered_keys = [
        "SHERPADESK_API_BASE_URL",
        "SHERPADESK_ORG_KEY",
        "SHERPADESK_INSTANCE_KEY",
        "SHERPAMIND_NOTIFY_CHANNEL",
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


def _env_or_file(key: str, file_values: dict[str, str], default: str | None = None) -> str | None:
    return os.getenv(key) or file_values.get(key) or default


def stage_connection_settings(
    *,
    api_base_url: str | None = None,
    org_key: str | None = None,
    instance_key: str | None = None,
    notify_channel: str | None = None,
) -> Path:
    paths = ensure_path_layout()
    current = _read_key_value_file(paths.settings_file)
    updates = {
        "SHERPADESK_API_BASE_URL": api_base_url,
        "SHERPADESK_ORG_KEY": org_key,
        "SHERPADESK_INSTANCE_KEY": instance_key,
        "SHERPAMIND_NOTIFY_CHANNEL": notify_channel,
    }
    for key, value in updates.items():
        if value is not None:
            current[key] = value
    _write_key_value_file(paths.settings_file, current)
    return paths.settings_file


def stage_api_key(*, api_key: str | None = None, from_file: Path | None = None) -> Path:
    paths = ensure_path_layout()
    value = api_key
    if from_file is not None:
        value = from_file.read_text(encoding="utf-8").strip()
    if value is None:
        raise ValueError("api_key or from_file is required")
    paths.api_key_file.write_text(value.strip() + "\n", encoding="utf-8")
    try:
        paths.api_key_file.chmod(0o600)
    except OSError:
        pass
    return paths.api_key_file


def stage_api_user(*, api_user: str | None = None, from_file: Path | None = None) -> Path:
    paths = ensure_path_layout()
    value = api_user
    if from_file is not None:
        value = from_file.read_text(encoding="utf-8").strip()
    if value is None:
        raise ValueError("api_user or from_file is required")
    paths.api_user_file.write_text(value.strip() + "\n", encoding="utf-8")
    try:
        paths.api_user_file.chmod(0o600)
    except OSError:
        pass
    return paths.api_user_file


def load_settings() -> Settings:
    paths = ensure_path_layout()
    file_values = _read_key_value_file(paths.settings_file)
    seed_max_pages_raw = _env_or_file("SHERPAMIND_SEED_MAX_PAGES", file_values)
    return Settings(
        api_base_url=_env_or_file("SHERPADESK_API_BASE_URL", file_values, "https://api.sherpadesk.com") or "https://api.sherpadesk.com",
        api_key=os.getenv("SHERPADESK_API_KEY") or _read_secret_file(paths.api_key_file),
        api_user=os.getenv("SHERPADESK_API_USER") or _read_secret_file(paths.api_user_file),
        org_key=_env_or_file("SHERPADESK_ORG_KEY", file_values),
        instance_key=_env_or_file("SHERPADESK_INSTANCE_KEY", file_values),
        db_path=paths.db_path,
        watch_state_path=paths.watch_state_path,
        notify_channel=_env_or_file("SHERPAMIND_NOTIFY_CHANNEL", file_values),
        request_min_interval_seconds=float(_env_or_file("SHERPAMIND_REQUEST_MIN_INTERVAL_SECONDS", file_values, "8.0") or "8.0"),
        request_timeout_seconds=float(_env_or_file("SHERPAMIND_REQUEST_TIMEOUT_SECONDS", file_values, "30.0") or "30.0"),
        seed_page_size=int(_env_or_file("SHERPAMIND_SEED_PAGE_SIZE", file_values, "100") or "100"),
        seed_max_pages=int(seed_max_pages_raw) if seed_max_pages_raw else None,
        hot_open_pages=int(_env_or_file("SHERPAMIND_HOT_OPEN_PAGES", file_values, "5") or "5"),
        warm_closed_pages=int(_env_or_file("SHERPAMIND_WARM_CLOSED_PAGES", file_values, "10") or "10"),
        warm_closed_days=int(_env_or_file("SHERPAMIND_WARM_CLOSED_DAYS", file_values, "7") or "7"),
        cold_closed_pages_per_run=int(_env_or_file("SHERPAMIND_COLD_CLOSED_PAGES_PER_RUN", file_values, "2") or "2"),
        service_hot_open_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_HOT_OPEN_EVERY_SECONDS", file_values, "300") or "300"),
        service_warm_closed_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_WARM_CLOSED_EVERY_SECONDS", file_values, "14400") or "14400"),
        service_cold_closed_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_COLD_CLOSED_EVERY_SECONDS", file_values, "86400") or "86400"),
        service_enrichment_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_ENRICHMENT_EVERY_SECONDS", file_values, "7200") or "7200"),
        service_public_snapshot_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_PUBLIC_SNAPSHOT_EVERY_SECONDS", file_values, "1800") or "1800"),
        service_vector_refresh_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_VECTOR_REFRESH_EVERY_SECONDS", file_values, "1800") or "1800"),
        service_doctor_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_DOCTOR_EVERY_SECONDS", file_values, "43200") or "43200"),
        service_enrichment_limit=int(_env_or_file("SHERPAMIND_SERVICE_ENRICHMENT_LIMIT", file_values, "60") or "60"),
        service_cold_bootstrap_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_COLD_BOOTSTRAP_EVERY_SECONDS", file_values, "1800") or "1800"),
        service_enrichment_bootstrap_every_seconds=int(_env_or_file("SHERPAMIND_SERVICE_ENRICHMENT_BOOTSTRAP_EVERY_SECONDS", file_values, "900") or "900"),
        service_enrichment_bootstrap_limit=int(_env_or_file("SHERPAMIND_SERVICE_ENRICHMENT_BOOTSTRAP_LIMIT", file_values, "240") or "240"),
        cold_closed_bootstrap_pages_per_run=int(_env_or_file("SHERPAMIND_COLD_CLOSED_BOOTSTRAP_PAGES_PER_RUN", file_values, "10") or "10"),
        api_hourly_limit=int(_env_or_file("SHERPAMIND_API_HOURLY_LIMIT", file_values, "600") or "600"),
        api_budget_warn_ratio=float(_env_or_file("SHERPAMIND_API_BUDGET_WARN_RATIO", file_values, "0.7") or "0.7"),
        api_budget_critical_ratio=float(_env_or_file("SHERPAMIND_API_BUDGET_CRITICAL_RATIO", file_values, "0.85") or "0.85"),
        api_request_log_retention_days=int(_env_or_file("SHERPAMIND_API_REQUEST_LOG_RETENTION_DAYS", file_values, "14") or "14"),
    )
