#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


_REGISTRY_DIR = Path(__file__).resolve().parent.parent / "state" / "campaigns"


def _campaign_dir(campaign_id: str) -> Path:
    return _REGISTRY_DIR / campaign_id


def save_campaign_brief(campaign_id: str, brief: dict[str, Any]) -> str:
    campaign_dir = _campaign_dir(campaign_id)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    path = campaign_dir / "brief.json"
    path.write_text(json.dumps(brief, ensure_ascii=False, indent=2))
    return str(path)


def save_campaign_registry_entry(campaign_id: str, data: dict[str, Any]) -> str:
    campaign_dir = _campaign_dir(campaign_id)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    path = campaign_dir / "registry.json"
    existing: dict[str, Any] = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text())
        except Exception:
            existing = {}
    payload = {
        **existing,
        "campaignId": campaign_id,
        "updatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        **(data or {}),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return str(path)
