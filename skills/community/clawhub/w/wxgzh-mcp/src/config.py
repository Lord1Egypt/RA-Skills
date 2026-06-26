"""Configuration management for wxgzh-mcp."""
import json
import os
from pathlib import Path
from typing import Optional


class Config:
    """Config manager, reads from config/config.json."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Try multiple locations
            locations = [
                os.environ.get("WECHAT_MCP_CONFIG"),
                str(Path(__file__).parent.parent / "config" / "config.json"),
                "config/config.json",
            ]
            config_path = next((loc for loc in locations if loc and Path(loc).exists()), None)

        if config_path is None:
            raise FileNotFoundError(
                "config.json not found. Please copy config.json.example to config.json "
                "and fill in your AppID and AppSecret."
            )

        self.config_path = Path(config_path)
        self._cfg: dict = {}
        self.load()

    def load(self) -> None:
        """Load config from JSON file."""
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._cfg = json.load(f)

        if not self._cfg.get("app_id") or not self._cfg.get("app_secret"):
            raise ValueError(
                "app_id and app_secret are required in config.json. "
                "Please fill in your WeChat Official Account credentials."
            )

    @property
    def app_id(self) -> str:
        return self._cfg.get("app_id", "")

    @property
    def app_secret(self) -> str:
        return self._cfg.get("app_secret", "")

    @property
    def proxy(self) -> Optional[str]:
        return self._cfg.get("proxy")

    def get(self, key: str, default=None):
        return self._cfg.get(key, default)


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
