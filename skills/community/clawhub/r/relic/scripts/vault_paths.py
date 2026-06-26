#!/usr/bin/env python3
"""Shared vault path helpers for relic scripts."""
from __future__ import annotations

import os
from pathlib import Path


def get_default_vault_path() -> Path:
    """Return the default relic vault path inside the OpenClaw workspace."""
    return Path.home() / '.openclaw' / 'workspace' / 'projects' / 'relic' / 'vault'


def get_vault_path() -> Path:
    """Return the configured relic vault path."""
    configured_path = os.environ.get('RELIC_VAULT_PATH')
    if configured_path:
        return Path(configured_path).expanduser().resolve()
    return get_default_vault_path()
