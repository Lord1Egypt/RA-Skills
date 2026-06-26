"""
SoulForge Configuration Management
"""

import os
import json
from pathlib import Path
from typing import List, Optional


class SoulForgeConfig:
    """Configuration for SoulForge memory evolution system."""

    DEFAULT_CONFIG = {
        "workspace": "~/.openclaw/workspace",
        "memory_paths": [
            "memory/",
            ".learnings/",
        ],
        "target_files": [
            "SOUL.md",
            "USER.md",
            "IDENTITY.md",
            "MEMORY.md",
            "AGENTS.md",
            "TOOLS.md",
        ],
        "trigger_threshold": 3,
        "backup_enabled": True,
        "backup_dir": None,  # Derived from workspace to ensure agent isolation
        "state_dir": None,   # Derived from workspace to ensure agent isolation
        "minimax_api_key_env": "MINIMAX_API_KEY",
        "model": "MiniMax-M2.7",
        "log_level": "INFO",
        "dry_run": False,
        "hawk_bridge_enabled": True,
        "hawk_db_path": "~/.hawk/lancedb",
        "hawk_table_name": "hawk_memories",
    }

    def __init__(self, config_path: Optional[str] = None, overrides: Optional[dict] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config.json file. If None, uses default locations.
            overrides: Dict of config values to override. Useful for CLI args.
        """
        self._config = self.DEFAULT_CONFIG.copy()

        # Try to load from config file
        if config_path:
            self._load_from_file(config_path)
        else:
            # Search in default locations
            for candidate in [
                Path("soulforge/config.json"),
                Path("~/.openclaw/skills/soul-forge/soulforge/config.json").expanduser(),
                Path("~/.soulforgerc").expanduser(),
            ]:
                if candidate.exists():
                    self._load_from_file(str(candidate))
                    break

        # Apply environment variable overrides
        self._apply_env_overrides()

        # Apply runtime overrides
        if overrides:
            self._config.update(overrides)

        # Expand paths
        self.workspace = str(Path(self._config["workspace"]).expanduser().resolve())

    def _load_from_file(self, path: str) -> None:
        """Load configuration from JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        self._config.update(loaded)

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # MiniMax API Key
        api_key_env = self._config.get("minimax_api_key_env", "MINIMAX_API_KEY")
        if api_key_env in os.environ:
            self._config["minimax_api_key"] = os.environ[api_key_env]

        # Workspace override
        if "SOULFORGE_WORKSPACE" in os.environ:
            self._config["workspace"] = os.environ["SOULFORGE_WORKSPACE"]

    def get(self, key: str, default=None):
        """Get a configuration value."""
        return self._config.get(key, default)

    @property
    def memory_paths(self) -> List[str]:
        """Get list of memory source paths (relative to workspace)."""
        base = Path(self.workspace)
        return [str(base / p) for p in self._config["memory_paths"]]

    @property
    def target_files(self) -> List[str]:
        """Get list of target files to update (relative to workspace)."""
        base = Path(self.workspace)
        return [str(base / f) for f in self._config["target_files"]]

    @property
    def backup_dir(self) -> str:
        """
        Get backup directory path.

        IMPORTANT: Each agent/workspace gets its own isolated backup directory.
        The directory name is derived from the workspace path to ensure isolation.
        e.g., ~/.openclaw/workspace -> .soulforge-main/backups/
               ~/.openclaw/workspace-wukong -> .soulforge-wukong/backups/
        """
        base = Path(self.workspace)
        # Derive agent-specific directory name from workspace path
        # e.g., "workspace" or "workspace-wukong" -> ".soulforge-workspace" or ".soulforge-wukong"
        workspace_name = base.name  # e.g., "workspace", "workspace-wukong"
        agent_suffix = workspace_name.replace("workspace-", "") if workspace_name != "workspace" else "main"
        agent_dir = f".soulforge-{agent_suffix}"
        return str(base / agent_dir / "backups")

    @property
    def state_dir(self) -> str:
        """
        Get state directory path for this agent/workspace.

        State includes synthesis cache, last-run info, etc.
        Isolated per agent to prevent cross-contamination.
        """
        base = Path(self.workspace)
        workspace_name = base.name
        agent_suffix = workspace_name.replace("workspace-", "") if workspace_name != "workspace" else "main"
        agent_dir = f".soulforge-{agent_suffix}"
        return str(base / agent_dir)

    @property
    def minimax_api_key(self) -> str:
        """Get MiniMax API key."""
        return self._config.get("minimax_api_key", os.environ.get("MINIMAX_API_KEY", ""))

    @property
    def minimax_base_url(self) -> str:
        """Get MiniMax API base URL."""
        return self._config.get(
            "minimax_base_url",
            os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
        )

    @property
    def trigger_threshold(self) -> int:
        """Get pattern trigger threshold."""
        return self._config.get("trigger_threshold", 3)

    @property
    def is_dry_run(self) -> bool:
        """Check if running in dry-run mode."""
        return self._config.get("dry_run", False)

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self._config.get("log_level", "INFO")

    def to_dict(self) -> dict:
        """Export configuration as dict (for debugging)."""
        return self._config.copy()

    def __repr__(self) -> str:
        return f"SoulForgeConfig(workspace={self.workspace}, threshold={self.trigger_threshold})"
