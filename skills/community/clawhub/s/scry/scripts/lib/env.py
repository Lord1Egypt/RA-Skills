"""Environment and configuration for SCRY skill."""

import os
import shutil
from typing import Any, Dict


def get_config() -> Dict[str, Any]:
    """Load configuration from environment and config file."""
    config: Dict[str, Any] = {}

    # Load from config file first (lower priority)
    for config_path in [
        os.path.expanduser("~/.config/scry/.env"),
        os.path.expanduser("~/.config/last30days/.env"),  # Compatibility
    ]:
        if os.path.isfile(config_path):
            with open(config_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and v:
                            config[k] = v

    # Override with environment variables (higher priority)
    env_keys = [
        "OPENAI_API_KEY", "XAI_API_KEY", "SCRAPECREATORS_API_KEY",
        "PARALLEL_API_KEY", "BRAVE_API_KEY", "OPENROUTER_API_KEY",
        "PRODUCTHUNT_TOKEN", "SO_API_KEY", "HF_TOKEN",
        "AUTH_TOKEN", "CT0", "THREADS_ACCESS_TOKEN",
    ]
    for key in env_keys:
        val = os.environ.get(key)
        if val:
            config[key] = val

    # Binary availability
    config["_has_gh"] = shutil.which("gh") is not None
    config["_has_ytdlp"] = shutil.which("yt-dlp") is not None
    config["_has_node"] = shutil.which("node") is not None

    try:
        import scrapling
        config["_has_scrapling"] = True
    except ImportError:
        config["_has_scrapling"] = False

    return config


def summarize_sources(config: Dict[str, Any]) -> Dict[str, bool]:
    """Summarize which sources are available based on config."""
    return {
        # Tier 1 — always available
        "hackernews": True,
        "lobsters": True,
        "devto": True,
        "github": config.get("_has_gh", False),
        "arxiv": True,
        "semantic_scholar": True,
        "openalex": True,
        "bluesky": True,
        "mastodon": True,
        "wikipedia": True,
        "gdelt": True,
        "techmeme": True,
        "polymarket": True,
        "sec_edgar": True,
        "gitlab": True,
        "coingecko": True,
        # Tier 2
        "reddit": True,  # Public JSON, no key needed
        "x_twitter": bool(config.get("AUTH_TOKEN") or config.get("XAI_API_KEY")),
        "youtube": config.get("_has_ytdlp", False),
        "tiktok": bool(config.get("SCRAPECREATORS_API_KEY")),
        "instagram": bool(config.get("SCRAPECREATORS_API_KEY")),
        "product_hunt": bool(config.get("PRODUCTHUNT_TOKEN")),
        "stackoverflow": True,  # Free without key, just lower limits
        "threads": bool(config.get("THREADS_ACCESS_TOKEN")),
        "huggingface": True,  # Works without key for public data
        "substack": True,  # Unofficial API
        # Tier 3
        "google_news": True,  # RSS
    }
