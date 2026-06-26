"""Source registry for SCRY skill — discovers and manages all sources."""

import importlib
import os
import shutil
from typing import Any, Dict, List, Optional

from .source_base import Source, SourceMeta

# All source module names in sources/ directory
SOURCE_MODULES = [
    # Tier 1 — zero API keys
    "hackernews", "lobsters", "devto", "github", "arxiv",
    "semantic_scholar", "openalex", "bluesky", "mastodon",
    "wikipedia", "gdelt", "techmeme", "polymarket",
    "sec_edgar", "gitlab", "coingecko",
    # Tier 2 — optional keys
    "reddit", "x_twitter", "youtube", "tiktok", "instagram",
    "product_hunt", "stackoverflow", "threads", "huggingface", "substack",
    # Tier 3 — scrapling
    "google_news",
]


class SourceRegistry:
    def __init__(self):
        self._sources: Dict[str, Source] = {}
        self._load_errors: Dict[str, str] = {}

    def discover(self) -> None:
        """Discover and load all available source modules."""
        for module_name in SOURCE_MODULES:
            try:
                mod = importlib.import_module(f".sources.{module_name}", package="lib")
                # Each module should have a get_source() function
                if hasattr(mod, "get_source"):
                    source = mod.get_source()
                    self._sources[source.meta().id] = source
            except ImportError as e:
                self._load_errors[module_name] = str(e)
            except Exception as e:
                self._load_errors[module_name] = str(e)

    def get_available(self, config: Dict[str, Any]) -> List[Source]:
        """Get all sources that are available (keys/binaries present)."""
        return [s for s in self._sources.values() if s.is_available(config)]

    def get_by_tier(self, tier: int, config: Dict[str, Any]) -> List[Source]:
        """Get available sources by tier."""
        return [s for s in self.get_available(config) if s.meta().tier == tier]

    def get_by_id(self, source_id: str) -> Optional[Source]:
        return self._sources.get(source_id)

    def get_by_ids(self, source_ids: List[str], config: Dict[str, Any]) -> List[Source]:
        """Get specific sources by ID, filtering to available ones."""
        result = []
        for sid in source_ids:
            s = self._sources.get(sid)
            if s and s.is_available(config):
                result.append(s)
        return result

    def get_for_domain(self, domain: str, config: Dict[str, Any]) -> List[Source]:
        """Get sources relevant to a domain, sorted by domain affinity."""
        available = self.get_available(config)
        scored = []
        for s in available:
            m = s.meta()
            if domain in m.domains or "general" in m.domains:
                scored.append((s, 2 if domain in m.domains else 1))
            else:
                scored.append((s, 0))
        scored.sort(key=lambda x: (-x[1], x[0].meta().tier))
        return [s for s, _ in scored]

    def all_metas(self) -> List[SourceMeta]:
        return [s.meta() for s in self._sources.values()]

    @property
    def load_errors(self) -> Dict[str, str]:
        return self._load_errors


def build_config() -> Dict[str, Any]:
    """Build config dict from environment variables."""
    config = {}
    env_keys = [
        "OPENAI_API_KEY", "XAI_API_KEY", "SCRAPECREATORS_API_KEY",
        "PARALLEL_API_KEY", "BRAVE_API_KEY", "OPENROUTER_API_KEY",
        "PRODUCTHUNT_TOKEN", "SO_API_KEY", "HF_TOKEN",
        "AUTH_TOKEN", "CT0",
        "THREADS_ACCESS_TOKEN",
    ]
    for key in env_keys:
        val = os.environ.get(key)
        if val:
            config[key] = val

    # Check for config file
    config_file = os.path.expanduser("~/.config/scry/.env")
    if os.path.isfile(config_file):
        with open(config_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and v and k not in config:
                        config[k] = v

    # Check binaries
    config["_has_gh"] = shutil.which("gh") is not None
    config["_has_ytdlp"] = shutil.which("yt-dlp") is not None
    config["_has_node"] = shutil.which("node") is not None

    # Check scrapling
    try:
        import scrapling
        config["_has_scrapling"] = True
    except ImportError:
        config["_has_scrapling"] = False

    return config
