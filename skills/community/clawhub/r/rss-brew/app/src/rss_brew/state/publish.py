from __future__ import annotations

import os
from pathlib import Path

from .manifests import write_json


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    tmp_path.write_text(text, encoding="utf-8")
    os.replace(tmp_path, path)


def write_current_pointers(
    *,
    run_records_day: Path,
    daily_dir: Path,
    day: str,
    winner_run_id: str,
    selected_at: str,
) -> None:
    current_payload = {
        "day": day,
        "winner_run_id": winner_run_id,
        "selected_at": selected_at,
    }
    write_json(run_records_day / "CURRENT.json", current_payload)
    write_json(daily_dir / "CURRENT.json", current_payload)
    atomic_write_text(daily_dir / "CURRENT", winner_run_id + "\n")
