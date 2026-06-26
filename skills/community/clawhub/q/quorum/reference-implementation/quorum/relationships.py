# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect

"""
Relationship manifest loader for cross-artifact consistency.

Loads quorum-relationships.yaml and provides typed Relationship objects
with resolved file contents for critic evaluation.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


DEFAULT_MANIFEST_NAME = "quorum-relationships.yaml"

# Supported relationship types and their expected role pairs
RELATIONSHIP_TYPES = {
    "implements": {"roles": ("spec", "impl"), "check": "coverage"},
    "documents": {"roles": ("source", "docs"), "check": "accuracy"},
    "delegates": {"roles": ("from", "to"), "check": "boundary"},
    "schema_contract": {"roles": ("producer", "consumer"), "check": "compatibility"},
}


class Relationship(BaseModel):
    """A declared relationship between two artifacts."""
    type: str = Field(description="Relationship type: implements | documents | delegates | schema_contract")
    role_a_name: str = Field(description="Name of the first role (e.g. 'spec', 'source', 'from', 'producer')")
    role_a_path: str = Field(description="Relative path for role A")
    role_b_name: str = Field(description="Name of the second role (e.g. 'impl', 'docs', 'to', 'consumer')")
    role_b_path: str = Field(description="Relative path for role B")
    scope: Optional[str] = Field(default=None, description="Scope qualifier for partial relationships")
    contract: Optional[str] = Field(default=None, description="Contract description for schema_contract relationships")
    check_type: str = Field(default="", description="What kind of check: coverage | accuracy | boundary | compatibility")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in RELATIONSHIP_TYPES:
            raise ValueError(f"Unknown relationship type: {v}. Valid: {list(RELATIONSHIP_TYPES.keys())}")
        return v


class ResolvedRelationship(BaseModel):
    """A relationship with file contents loaded for critic evaluation."""
    relationship: Relationship
    role_a_content: str = Field(description="Full text of role A file")
    role_b_content: str = Field(description="Full text of role B file")
    role_a_exists: bool = True
    role_b_exists: bool = True


def load_manifest(manifest_path: Path) -> list[Relationship]:
    """
    Load and validate a quorum-relationships.yaml manifest.

    Args:
        manifest_path: Path to the YAML manifest

    Returns:
        List of validated Relationship objects

    Raises:
        FileNotFoundError: If manifest doesn't exist
        ValueError: If manifest is malformed
    """
    if not manifest_path.exists():
        raise FileNotFoundError(f"Relationship manifest not found: {manifest_path}")

    with open(manifest_path) as f:
        data = yaml.safe_load(f)

    if not data or "relationships" not in data:
        raise ValueError(f"Manifest must contain a 'relationships' key: {manifest_path}")

    raw_rels = data["relationships"]
    if not isinstance(raw_rels, list):
        raise ValueError("'relationships' must be a list")

    relationships: list[Relationship] = []
    for i, entry in enumerate(raw_rels):
        rel_type = entry.get("type")
        if not rel_type:
            raise ValueError(f"Relationship #{i} missing 'type'")

        if rel_type not in RELATIONSHIP_TYPES:
            raise ValueError(f"Relationship #{i}: unknown type '{rel_type}'. Valid: {list(RELATIONSHIP_TYPES.keys())}")

        type_info = RELATIONSHIP_TYPES[rel_type]
        role_a_name, role_b_name = type_info["roles"]

        role_a_path = entry.get(role_a_name)
        role_b_path = entry.get(role_b_name)

        if not role_a_path:
            raise ValueError(f"Relationship #{i} (type={rel_type}) missing '{role_a_name}' field")
        if not role_b_path:
            raise ValueError(f"Relationship #{i} (type={rel_type}) missing '{role_b_name}' field")

        relationships.append(Relationship(
            type=rel_type,
            role_a_name=role_a_name,
            role_a_path=role_a_path,
            role_b_name=role_b_name,
            role_b_path=role_b_path,
            scope=entry.get("scope"),
            contract=entry.get("contract"),
            check_type=type_info["check"],
        ))

    logger.info("Loaded %d relationships from %s", len(relationships), manifest_path)
    return relationships


def resolve_relationships(
    relationships: list[Relationship],
    base_dir: Path,
) -> list[ResolvedRelationship]:
    """
    Resolve relationships by reading file contents.

    Files that don't exist get empty content + exists=False flag.
    The critic should report missing files as findings.

    Args:
        relationships: List of validated Relationship objects
        base_dir: Base directory for resolving relative file paths

    Returns:
        List of ResolvedRelationship with file contents loaded

    Raises:
        ValueError: If any path attempts to escape base_dir (path traversal)
    """
    resolved: list[ResolvedRelationship] = []

    for rel in relationships:
        path_a = base_dir / rel.role_a_path
        path_b = base_dir / rel.role_b_path

        # Validate paths don't escape base_dir (path traversal protection)
        try:
            path_a.resolve().relative_to(base_dir.resolve())
        except ValueError:
            raise ValueError(f"Path escapes base directory: {rel.role_a_path}")
        try:
            path_b.resolve().relative_to(base_dir.resolve())
        except ValueError:
            raise ValueError(f"Path escapes base directory: {rel.role_b_path}")

        content_a = ""
        exists_a = path_a.exists()
        if exists_a:
            content_a = path_a.read_text(encoding="utf-8", errors="replace")

        content_b = ""
        exists_b = path_b.exists()
        if exists_b:
            content_b = path_b.read_text(encoding="utf-8", errors="replace")

        resolved.append(ResolvedRelationship(
            relationship=rel,
            role_a_content=content_a,
            role_b_content=content_b,
            role_a_exists=exists_a,
            role_b_exists=exists_b,
        ))

    return resolved
