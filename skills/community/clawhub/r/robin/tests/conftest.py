from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


@pytest.fixture()
def robin_env(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    state_dir = workspace / "data" / "robin"
    (state_dir / "topics").mkdir(parents=True)

    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("ROBIN_STATE_DIR", raising=False)
    monkeypatch.setenv("ROBIN_STATE_DIR", str(state_dir))
    monkeypatch.chdir(workspace)

    config = {
        "topics_dir": "topics",
        "media_dir": "media",
        "min_items_before_review": 1,
        "review_cooldown_days": 60,
    }
    (state_dir / "robin-config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    (state_dir / "robin-review-index.json").write_text(
        json.dumps({"items": {}}, indent=2),
        encoding="utf-8",
    )

    return {
        "tmp_path": tmp_path,
        "workspace": workspace,
        "state_dir": state_dir,
        "topics_dir": state_dir / "topics",
        "media_dir": state_dir / "media",
    }
