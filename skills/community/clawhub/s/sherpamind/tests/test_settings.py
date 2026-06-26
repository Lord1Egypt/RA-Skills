from pathlib import Path

from sherpamind.settings import load_settings, stage_api_key, stage_connection_settings


def test_load_settings_reads_request_controls(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    monkeypatch.setenv("SHERPAMIND_REQUEST_MIN_INTERVAL_SECONDS", "3.5")
    monkeypatch.setenv("SHERPAMIND_REQUEST_TIMEOUT_SECONDS", "45")
    settings = load_settings()
    assert settings.request_min_interval_seconds == 3.5
    assert settings.request_timeout_seconds == 45.0


def test_load_settings_defaults_paths(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    settings = load_settings()
    assert settings.db_path == tmp_path / ".SherpaMind" / "private" / "data" / "sherpamind.sqlite3"
    assert settings.watch_state_path == tmp_path / ".SherpaMind" / "private" / "state" / "watch_state.json"


def test_load_settings_reads_seed_controls(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    monkeypatch.setenv("SHERPAMIND_SEED_PAGE_SIZE", "50")
    monkeypatch.setenv("SHERPAMIND_SEED_MAX_PAGES", "3")
    settings = load_settings()
    assert settings.seed_page_size == 50
    assert settings.seed_max_pages == 3


def test_load_settings_reads_service_controls(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    monkeypatch.setenv("SHERPAMIND_SERVICE_HOT_OPEN_EVERY_SECONDS", "123")
    monkeypatch.setenv("SHERPAMIND_SERVICE_ENRICHMENT_LIMIT", "77")
    monkeypatch.setenv("SHERPAMIND_SERVICE_COLD_BOOTSTRAP_EVERY_SECONDS", "456")
    monkeypatch.setenv("SHERPAMIND_SERVICE_ENRICHMENT_BOOTSTRAP_LIMIT", "222")
    monkeypatch.setenv("SHERPAMIND_COLD_CLOSED_BOOTSTRAP_PAGES_PER_RUN", "9")
    settings = load_settings()
    assert settings.service_hot_open_every_seconds == 123
    assert settings.service_enrichment_limit == 77
    assert settings.service_cold_bootstrap_every_seconds == 456
    assert settings.service_enrichment_bootstrap_limit == 222
    assert settings.cold_closed_bootstrap_pages_per_run == 9


def test_staged_settings_and_secrets_are_loaded(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    settings_file = stage_connection_settings(org_key="org1", instance_key="inst1")
    api_key_file = stage_api_key(api_key="secret")
    assert settings_file.exists()
    assert api_key_file.exists()
    settings = load_settings()
    assert settings.api_key == "secret"
    assert settings.org_key == "org1"
    assert settings.instance_key == "inst1"
