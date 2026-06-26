from pathlib import Path

from sherpamind.paths import discover_workspace_root, ensure_path_layout, resolve_paths


def test_resolve_paths_uses_workspace_root(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    paths = resolve_paths()
    assert paths.root == tmp_path / ".SherpaMind"
    assert paths.config_root == tmp_path / ".SherpaMind" / "private" / "config"
    assert paths.secrets_root == tmp_path / ".SherpaMind" / "private" / "secrets"
    assert paths.data_root == tmp_path / ".SherpaMind" / "private" / "data"
    assert paths.state_root == tmp_path / ".SherpaMind" / "private" / "state"
    assert paths.runtime_venv == tmp_path / ".SherpaMind" / "private" / "runtime" / "venv"


def test_ensure_path_layout_creates_directories(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SHERPAMIND_WORKSPACE_ROOT", str(tmp_path))
    paths = ensure_path_layout()
    assert paths.config_root.exists()
    assert paths.secrets_root.exists()
    assert paths.data_root.exists()
    assert paths.state_root.exists()
    assert paths.public_root.exists()
    assert paths.exports_root.exists()
    assert paths.docs_root.exists()


def test_discover_workspace_root_prefers_openclaw_workspace_parent(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("SHERPAMIND_WORKSPACE_ROOT", raising=False)
    repo_root = tmp_path / "skills" / "sherpamind"
    repo_root.mkdir(parents=True)
    assert discover_workspace_root(repo_root=repo_root, cwd=tmp_path / "elsewhere") == tmp_path
