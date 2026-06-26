# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Configuration system for Quorum.
Loads YAML depth profiles and merges CLI overrides.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field, field_validator


VALID_CRITICS = {
    "correctness",
    "security",
    "completeness",
    "architecture",
    "delegation",
    "style",
    "tester",
    "code_hygiene",
    # cross_consistency is NOT listed here — it's a Phase 2 critic activated
    # via --relationships flag, not the critics list in config.
}

VALID_DEPTHS = {"quick", "standard", "thorough"}


class ModelTiers(BaseModel):
    """Two-tier model configuration — never hardcode model names directly."""
    tier_1: str = Field(
        description="Your strongest model (for judgment-heavy roles like Correctness, Aggregator)"
    )
    tier_2: str = Field(
        description="Cost-efficient capable model (for execution-heavy roles)"
    )


class QuorumConfig(BaseModel):
    """
    Runtime configuration for a Quorum validation run.
    Loaded from a YAML depth profile and merged with CLI overrides.
    """
    critics: list[str] = Field(description="List of critics to run")
    model_tier1: str = Field(description="Tier 1 model identifier (e.g. claude-opus-4)")
    model_tier2: str = Field(description="Tier 2 model identifier (e.g. claude-sonnet-4)")
    max_fix_loops: int = Field(default=0, ge=0, le=3)
    depth_profile: str = Field(default="standard")
    api_keys: dict[str, str] = Field(default_factory=dict)
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=256)
    enable_prescreen: bool = Field(
        default=True,
        description="Run deterministic pre-screen checks before LLM critics",
    )
    max_cost: float | None = Field(
        default=None,
        description="Maximum allowed LLM spend in USD. Stops batch after each file if exceeded.",
    )

    @field_validator("critics")
    @classmethod
    def validate_critics(cls, v: list[str]) -> list[str]:
        invalid = set(v) - VALID_CRITICS
        if invalid:
            raise ValueError(f"Unknown critics: {invalid}. Valid: {VALID_CRITICS}")
        if not v:
            raise ValueError("At least one critic is required")
        return v

    @field_validator("depth_profile")
    @classmethod
    def validate_depth(cls, v: str) -> str:
        if v not in VALID_DEPTHS:
            raise ValueError(f"depth_profile must be one of: {VALID_DEPTHS}")
        return v

    @classmethod
    def from_yaml(cls, path: Path) -> "QuorumConfig":
        """Load config from a YAML depth profile file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        # Resolve env-var API keys if present
        resolved_keys: dict[str, str] = {}
        for key, val in data.get("api_keys", {}).items():
            if isinstance(val, str) and val.startswith("$"):
                env_name = val[1:]
                resolved_keys[key] = os.environ.get(env_name, "")
            else:
                resolved_keys[key] = val
        data["api_keys"] = resolved_keys
        return cls(**data)

    def with_overrides(self, **overrides: Any) -> "QuorumConfig":
        """Return a copy of this config with the given fields overridden."""
        data = self.model_dump()
        data.update({k: v for k, v in overrides.items() if v is not None})
        return QuorumConfig(**data)


def load_config(
    depth: str = "quick",
    config_path: Optional[Path] = None,
    **overrides: Any,
) -> QuorumConfig:
    """
    Load a QuorumConfig from a depth profile YAML.

    Search order:
    1. Explicit config_path if provided
    2. configs/{depth}.yaml relative to this file's package
    3. configs/{depth}.yaml relative to cwd
    """
    if config_path is not None:
        return QuorumConfig.from_yaml(config_path).with_overrides(**overrides)

    # Look in the package's configs/ directory
    pkg_configs = Path(__file__).parent / "configs"
    candidate = pkg_configs / f"{depth}.yaml"
    if candidate.exists():
        return QuorumConfig.from_yaml(candidate).with_overrides(**overrides)

    # Fall back to cwd
    cwd_candidate = Path.cwd() / "configs" / f"{depth}.yaml"
    if cwd_candidate.exists():
        return QuorumConfig.from_yaml(cwd_candidate).with_overrides(**overrides)

    raise FileNotFoundError(
        f"No config found for depth='{depth}'. "
        f"Looked in: {candidate}, {cwd_candidate}"
    )
