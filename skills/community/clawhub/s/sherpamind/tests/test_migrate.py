from pathlib import Path
import sqlite3

from sherpamind.migrate import archive_legacy_state, migrate_legacy_state


def test_migrate_legacy_state_copies_state_files(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    legacy_state = tmp_path / "state"
    legacy_state.mkdir(parents=True, exist_ok=True)
    legacy_db = legacy_state / "sherpamind.sqlite3"
    conn = sqlite3.connect(legacy_db)
    conn.execute("CREATE TABLE accounts(id INTEGER)")
    conn.commit()
    conn.close()
    (legacy_state / "watch_state.json").write_text("{}")

    result = migrate_legacy_state(tmp_path)

    assert result.status == "ok"
    assert (tmp_path / ".SherpaMind" / "private" / "data" / "sherpamind.sqlite3").exists()
    assert (tmp_path / ".SherpaMind" / "private" / "state" / "watch_state.json").exists()
    assert len(result.stats["copied"]) == 2


def test_migrate_legacy_state_replaces_empty_destination_sqlite(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    legacy_state = tmp_path / "state"
    legacy_state.mkdir(parents=True, exist_ok=True)
    legacy_db = legacy_state / "sherpamind.sqlite3"
    conn = sqlite3.connect(legacy_db)
    conn.execute("CREATE TABLE accounts(id INTEGER)")
    conn.commit()
    conn.close()

    destination = tmp_path / ".SherpaMind" / "private" / "data"
    destination.mkdir(parents=True, exist_ok=True)
    sqlite3.connect(destination / "sherpamind.sqlite3").close()

    result = migrate_legacy_state(tmp_path)

    assert result.status == "ok"
    assert len(result.stats["replaced"]) == 1


def test_archive_legacy_state_moves_repo_local_state(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    legacy_state = tmp_path / "state"
    legacy_state.mkdir(parents=True, exist_ok=True)
    (legacy_state / "sherpamind.sqlite3").write_text("db")
    (legacy_state / "watch_state.json").write_text("{}")

    result = archive_legacy_state(tmp_path)

    assert result.status == "ok"
    assert (tmp_path / ".SherpaMind" / "private" / "state" / "legacy" / "sherpamind.sqlite3").exists()
    assert (tmp_path / ".SherpaMind" / "private" / "state" / "legacy" / "watch_state.json").exists()
