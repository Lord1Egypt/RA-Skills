"""Configuration management — API key, base URL, output directory."""

import json
import os
from pathlib import Path

from sparki_cli.constants import DEFAULT_BASE_URL, DEFAULT_UPLOAD_TG_LINK

DEFAULT_CONFIG_DIR = Path.home() / ".openclaw" / "config"


class Config:
    def __init__(self, config_dir: Path | None = None):
        self.config_dir = config_dir or DEFAULT_CONFIG_DIR
        self.config_file = self.config_dir / "sparki.json"
        self._data: dict = {}
        if self.config_file.exists():
            self._data = json.loads(self.config_file.read_text())

    @property
    def api_key(self) -> str | None:
        env_key = os.environ.get("SPARKI_API_KEY")
        if env_key:
            return env_key
        return self._data.get("api_key")

    @property
    def base_url(self) -> str:
        return self._data.get("base_url", DEFAULT_BASE_URL)

    @property
    def default_output_dir(self) -> Path:
        configured = self._data.get("default_output_dir")
        if configured:
            return Path(configured).expanduser()
        return Path.home() / ".openclaw" / "workspace" / "sparki" / "videos"

    @property
    def upload_tg(self) -> str:
        env = os.environ.get("SPARKI_UPLOAD_TG_LINK")
        if env:
            return env
        return self._data.get("upload_tg", DEFAULT_UPLOAD_TG_LINK)

    def save(self, api_key: str | None = None, base_url: str | None = None, default_output_dir: str | None = None) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if api_key is not None:
            self._data["api_key"] = api_key
        if base_url is not None:
            self._data["base_url"] = base_url
        elif "base_url" not in self._data:
            self._data["base_url"] = DEFAULT_BASE_URL
        if default_output_dir is not None:
            self._data["default_output_dir"] = default_output_dir
        self.config_file.write_text(json.dumps(self._data, indent=2))
