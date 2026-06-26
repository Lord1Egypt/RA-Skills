import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_audit_state import build_state, collect_watched_files, hash_file


def test_hash_file_is_deterministic(tmp_path: Path) -> None:
    f = tmp_path / "test.md"
    f.write_text("hello")
    assert hash_file(f) == hash_file(f)


def test_hash_file_changes_with_content(tmp_path: Path) -> None:
    f = tmp_path / "test.md"
    f.write_text("hello")
    h1 = hash_file(f)
    f.write_text("world")
    h2 = hash_file(f)
    assert h1 != h2


def test_build_state_detects_changes(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "SOUL.md").write_text("v1")
    (workspace / "AGENTS.md").write_text("v1")

    state1 = build_state(workspace)
    assert state1["total_files"] >= 2
    assert len(state1["changed_files"]) >= 2  # all new = all changed

    # Save state and rerun
    state_file = tmp_path / "state.json"
    state_file.write_text(json.dumps(state1))

    state2 = build_state(workspace, state_file)
    assert len(state2["changed_files"]) == 0
    assert len(state2["unchanged_files"]) >= 2

    # Modify one file
    (workspace / "SOUL.md").write_text("v2")
    state3 = build_state(workspace, state_file)
    assert "SOUL.md" in state3["changed_files"]
