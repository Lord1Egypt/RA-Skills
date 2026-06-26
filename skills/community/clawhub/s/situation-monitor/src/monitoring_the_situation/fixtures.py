from __future__ import annotations

from pathlib import Path
import json

from .models import MessageRecord


def load_fixture_messages(path: Path) -> list[MessageRecord]:
    payload = json.loads(path.read_text())
    return [MessageRecord.from_dict(item) for item in payload]
