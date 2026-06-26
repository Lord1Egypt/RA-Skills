"""
Pydantic request/response models for ScopeCheck API.
"""

from pydantic import BaseModel, ConfigDict, Field


class CheckScopeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_content: str = Field(
        ...,
        min_length=1,
        max_length=500_000,
        description="Raw content of the SKILL.md file to analyze.",
    )


class DeclaredScope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    env: list[str] = Field(default_factory=list)
    bins: list[str] = Field(default_factory=list)


class DetectedScope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    env_vars: list[str] = Field(default_factory=list)
    cli_tools: list[str] = Field(default_factory=list)
    filesystem_paths: list[str] = Field(default_factory=list)
    network_urls: list[str] = Field(default_factory=list)


class CheckScopeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_name: str = Field(..., description="Extracted skill name.")
    declared: DeclaredScope = Field(..., description="What the skill declares it needs.")
    detected: DetectedScope = Field(..., description="What the skill actually accesses.")
    undeclared_access: list[str] = Field(
        ...,
        description="Resources detected but not declared — potential risk.",
    )
