"""MCP Server configuration for Agent Memory V12"""
from __future__ import annotations
import os
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import __version__

logger = logging.getLogger(__name__)

@dataclass
class MCPConfig:
    """Configuration for Agent Memory MCP Server."""
    # Server identity
    server_name: str = "agent-memory"
    server_version: str = ""  # 空字符串时自动从 __version__ 获取

    # Transport
    transport: str = "stdio"  # "stdio" or "streamable-http"
    host: str = "127.0.0.1"
    port: int = 8765

    # Authentication
    api_key: str = ""
    require_auth: bool = False

    # Tool access control
    core_tools: list[str] = field(default_factory=lambda: [
        "memory.remember", "memory.recall", "memory.context_for", "memory.command",
    ])
    extended_tools: list[str] = field(default_factory=lambda: [
        "memory.correct", "memory.delete",
        "memory.spirit_check", "memory.get_profile", "memory.report",
        "memory.share_skill", "memory.learn_skill",
    ])

    @property
    def enabled_tools(self) -> list[str]:
        """All enabled tools = core + extended."""
        return self.core_tools + self.extended_tools

    # Privacy defaults
    default_sensitivity: str = "normal"  # public/normal/internal/confidential/private
    default_scope: str = "personal"  # personal/work/enterprise

    # Rate limiting
    max_requests_per_minute: int = 60
    max_write_per_minute: int = 20

    # Spirit integration
    spirit_auto_check: bool = True
    spirit_check_interval_seconds: int = 300

    def __post_init__(self):
        if not self.server_version:
            self.server_version = __version__

    @classmethod
    def from_file(cls, path: str | Path) -> "MCPConfig":
        """Load config from JSON file."""
        path = Path(path)
        if not path.exists():
            logger.info("MCP config file not found, using defaults: %s", path)
            return cls()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    @classmethod
    def from_env(cls) -> "MCPConfig":
        """Load config from environment variables."""
        return cls(
            server_name=os.getenv("MCP_SERVER_NAME", "agent-memory"),
            transport=os.getenv("MCP_TRANSPORT", "stdio"),
            host=os.getenv("MCP_HOST", "127.0.0.1"),
            port=int(os.getenv("MCP_PORT", "8765")),
            api_key=os.getenv("MCP_API_KEY", ""),
            require_auth=os.getenv("MCP_REQUIRE_AUTH", "false").lower() == "true",
            default_sensitivity=os.getenv("MCP_DEFAULT_SENSITIVITY", "normal"),
            default_scope=os.getenv("MCP_DEFAULT_SCOPE", "personal"),
            max_requests_per_minute=int(os.getenv("MCP_MAX_RPM", "60")),
            max_write_per_minute=int(os.getenv("MCP_MAX_WRITE_RPM", "20")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}
