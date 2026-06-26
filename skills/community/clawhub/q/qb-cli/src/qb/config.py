"""Configuration file management."""

import json
import os
from pathlib import Path
from typing import Optional

DEFAULT_CONFIG_DIR = Path.home() / ".qb"


def get_config_dir(override: Optional[Path] = None) -> Path:
    """Resolve config directory: CLI flag > env var > default."""
    if override:
        return override
    env_dir = os.environ.get("QB_CONFIG_DIR")
    if env_dir:
        return Path(env_dir)
    return DEFAULT_CONFIG_DIR


def load_config(config_dir: Optional[Path] = None) -> dict:
    """Load config from config.json and environment variables.

    Precedence: environment variables > config.json > defaults.
    """
    d = get_config_dir(config_dir)
    config_path = d / "config.json"

    config = {}
    if config_path.exists():
        config = json.loads(config_path.read_text())

    # Env vars override config file values
    return {
        "client_id": os.environ.get("QB_CLIENT_ID") or config.get("client_id", ""),
        "client_secret": os.environ.get("QB_CLIENT_SECRET") or config.get("client_secret", ""),
        "environment": os.environ.get("QB_ENVIRONMENT") or config.get("environment", "sandbox"),
    }


def save_config(config: dict, config_dir: Optional[Path] = None) -> Path:
    """Save config to config.json. Returns path to saved file."""
    d = get_config_dir(config_dir)
    d.mkdir(parents=True, exist_ok=True)
    config_path = d / "config.json"
    config_path.write_text(json.dumps(config, indent=2))
    config_path.chmod(0o600)
    return config_path
