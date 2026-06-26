#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def load_config() -> dict[str, Any]:
    config_path = Path(__file__).resolve().parents[1] / "config" / "defaults.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    api_base_url = os.getenv("XINYI_API_BASE_URL")
    if api_base_url:
        config["apiBaseUrl"] = api_base_url

    timeout_seconds = os.getenv("XINYI_TIMEOUT_SECONDS")
    if timeout_seconds:
        try:
            config["timeoutSeconds"] = max(1, int(timeout_seconds))
        except ValueError:
            pass

    return config
