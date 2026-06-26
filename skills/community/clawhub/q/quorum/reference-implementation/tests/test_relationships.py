"""Unit & integration tests for relationship manifest loading and resolution."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from quorum.relationships import (
    RELATIONSHIP_TYPES,
    Relationship,
    ResolvedRelationship,
    load_manifest,
    resolve_relationships,
)

FIXTURES = Path(__file__).parent / "fixtures" / "relationships"


# ── Manifest loading ─────────────────────────────────────────────────────────


class TestLoadManifest:
    def test_load_valid_manifest(self):
        rels = load_manifest(FIXTURES / "quorum-relationships.yaml")
        assert len(rels) == 2
        assert all(isinstance(r, Relationship) for r in rels)

    def test_relationship_types(self):
        rels = load_manifest(FIXTURES / "quorum-relationships.yaml")
        types = {r.type for r in rels}
        assert "documents" in types
        assert "implements" in types

    def test_missing_manifest_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_manifest(tmp_path / "missing.yaml")

    def test_empty_manifest_raises(self, tmp_path):
        f = tmp_path / "empty.yaml"
        f.write_text("")
        with pytest.raises(ValueError, match="relationships"):
            load_manifest(f)

    def test_missing_relationships_key_raises(self, tmp_path):
        f = tmp_path / "bad.yaml"
        f.write_text("other_key: true\n")
        with pytest.raises(ValueError, match="relationships"):
            load_manifest(f)

    def test_invalid_type_raises(self, tmp_path):
        f = tmp_path / "bad.yaml"
        yaml.dump({"relationships": [{"type": "invalid_type", "a": "x", "b": "y"}]}, open(f, "w"))
        with pytest.raises(ValueError, match="unknown type"):
            load_manifest(f)

    def test_missing_role_fields_raises(self, tmp_path):
        f = tmp_path / "bad.yaml"
        yaml.dump({"relationships": [{"type": "implements"}]}, open(f, "w"))
        with pytest.raises(ValueError, match="missing"):
            load_manifest(f)

    def test_relationships_not_list_raises(self, tmp_path):
        f = tmp_path / "bad.yaml"
        yaml.dump({"relationships": "not a list"}, open(f, "w"))
        with pytest.raises(ValueError, match="list"):
            load_manifest(f)


# ── Relationship model ───────────────────────────────────────────────────────


class TestRelationshipModel:
    def test_valid_types(self):
        for rel_type in RELATIONSHIP_TYPES:
            r = Relationship(
                type=rel_type,
                role_a_name="a",
                role_a_path="a.txt",
                role_b_name="b",
                role_b_path="b.txt",
            )
            assert r.type == rel_type

    def test_invalid_type_rejected(self):
        from pydantic import ValidationError
        with pytest.raises(ValidationError, match="Unknown relationship type"):
            Relationship(
                type="bogus",
                role_a_name="a",
                role_a_path="a.txt",
                role_b_name="b",
                role_b_path="b.txt",
            )


# ── Resolve relationships ────────────────────────────────────────────────────


class TestResolveRelationships:
    def test_resolve_existing_files(self):
        rels = load_manifest(FIXTURES / "quorum-relationships.yaml")
        resolved = resolve_relationships(rels, base_dir=FIXTURES)
        assert len(resolved) == 2
        for r in resolved:
            assert isinstance(r, ResolvedRelationship)

    def test_existing_file_content_loaded(self):
        rels = load_manifest(FIXTURES / "quorum-relationships.yaml")
        resolved = resolve_relationships(rels, base_dir=FIXTURES)
        # doc-a.md should be loaded
        docs_rel = next(r for r in resolved if r.relationship.type == "documents")
        assert docs_rel.role_a_exists or docs_rel.role_b_exists

    def test_missing_file_flagged(self, tmp_path):
        rels = [
            Relationship(
                type="implements",
                role_a_name="spec",
                role_a_path="missing-spec.yaml",
                role_b_name="impl",
                role_b_path="missing-impl.py",
            )
        ]
        resolved = resolve_relationships(rels, base_dir=tmp_path)
        assert resolved[0].role_a_exists is False
        assert resolved[0].role_b_exists is False
        assert resolved[0].role_a_content == ""

    def test_path_traversal_blocked(self, tmp_path):
        rels = [
            Relationship(
                type="documents",
                role_a_name="source",
                role_a_path="../../etc/passwd",
                role_b_name="docs",
                role_b_path="doc.md",
            )
        ]
        with pytest.raises(ValueError, match="escapes"):
            resolve_relationships(rels, base_dir=tmp_path)
