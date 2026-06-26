#!/usr/bin/env python3
"""
Minimal schema migration diff generator for schema-migration-diff skill.
Provides core functionality for comparing schemas and generating diffs.
"""

from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ChangeType(Enum):
    """Types of schema changes."""
    ADDED = "ADDED"
    REMOVED = "REMOVED"
    MODIFIED = "MODIFIED"
    RENAMED = "RENAMED"


class ComponentType(Enum):
    """Types of schema components."""
    ENTITY = "ENTITY"
    PROPERTY = "PROPERTY"
    RELATIONSHIP = "RELATIONSHIP"
    CONSTRAINT = "CONSTRAINT"


@dataclass
class Change:
    """Represents a schema change."""
    change_type: ChangeType
    component_type: ComponentType
    name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    risk_level: str = "Low"  # Low, Medium, High

    def __repr__(self):
        if self.change_type == ChangeType.RENAMED:
            return f"~ {self.name}: {self.old_value} → {self.new_value}"
        elif self.change_type == ChangeType.ADDED:
            return f"+ {self.name}"
        elif self.change_type == ChangeType.REMOVED:
            return f"- {self.name}"
        else:
            return f"* {self.name}"


class SchemaDiff:
    """Represents schema differences between versions."""

    def __init__(self, schema_v1_name: str = "v1",
                 schema_v2_name: str = "v2"):
        """Initialize schema diff."""
        self.schema_v1_name = schema_v1_name
        self.schema_v2_name = schema_v2_name
        self.changes: List[Change] = []
        self.entities_v1: Set[str] = set()
        self.entities_v2: Set[str] = set()
        self.properties_v1: Dict[str, Set[str]] = {}
        self.properties_v2: Dict[str, Set[str]] = {}
        self.relationships_v1: Set[Tuple] = set()
        self.relationships_v2: Set[Tuple] = set()

    def add_entity(self, version: int, entity_name: str) -> None:
        """Register entity in schema version."""
        if version == 1:
            self.entities_v1.add(entity_name)
        else:
            self.entities_v2.add(entity_name)

    def add_property(self, version: int, entity_name: str,
                    property_name: str) -> None:
        """Register property in schema version."""
        if version == 1:
            if entity_name not in self.properties_v1:
                self.properties_v1[entity_name] = set()
            self.properties_v1[entity_name].add(property_name)
        else:
            if entity_name not in self.properties_v2:
                self.properties_v2[entity_name] = set()
            self.properties_v2[entity_name].add(property_name)

    def add_relationship(self, version: int, source: str,
                        rel_type: str, target: str) -> None:
        """Register relationship in schema version."""
        rel = (source, rel_type, target)
        if version == 1:
            self.relationships_v1.add(rel)
        else:
            self.relationships_v2.add(rel)

    def compute_diff(self) -> None:
        """Compute differences between schemas."""
        self.changes = []

        # Check entity changes
        added_entities = self.entities_v2 - self.entities_v1
        removed_entities = self.entities_v1 - self.entities_v2

        for entity in added_entities:
            self.changes.append(Change(
                change_type=ChangeType.ADDED,
                component_type=ComponentType.ENTITY,
                name=entity,
                risk_level="Low"
            ))

        for entity in removed_entities:
            self.changes.append(Change(
                change_type=ChangeType.REMOVED,
                component_type=ComponentType.ENTITY,
                name=entity,
                risk_level="High"
            ))

        # Check property changes
        for entity in self.entities_v1 & self.entities_v2:
            v1_props = self.properties_v1.get(entity, set())
            v2_props = self.properties_v2.get(entity, set())

            # Added properties
            for prop in v2_props - v1_props:
                self.changes.append(Change(
                    change_type=ChangeType.ADDED,
                    component_type=ComponentType.PROPERTY,
                    name=f"{entity}.{prop}",
                    risk_level="Low"
                ))

            # Removed properties
            for prop in v1_props - v2_props:
                self.changes.append(Change(
                    change_type=ChangeType.REMOVED,
                    component_type=ComponentType.PROPERTY,
                    name=f"{entity}.{prop}",
                    risk_level="High"
                ))

        # Check relationship changes
        added_rels = self.relationships_v2 - self.relationships_v1
        removed_rels = self.relationships_v1 - self.relationships_v2

        for src, rel_type, tgt in added_rels:
            self.changes.append(Change(
                change_type=ChangeType.ADDED,
                component_type=ComponentType.RELATIONSHIP,
                name=f"({src})-[:{rel_type}]->({tgt})",
                risk_level="Low"
            ))

        for src, rel_type, tgt in removed_rels:
            self.changes.append(Change(
                change_type=ChangeType.REMOVED,
                component_type=ComponentType.RELATIONSHIP,
                name=f"({src})-[:{rel_type}]->({tgt})",
                risk_level="High"
            ))

    def get_risk_assessment(self) -> Dict:
        """Assess migration risk."""
        high_risk = sum(1 for c in self.changes if c.risk_level == "High")
        medium_risk = sum(1 for c in self.changes if c.risk_level == "Medium")
        low_risk = sum(1 for c in self.changes if c.risk_level == "Low")

        if high_risk > 0:
            overall_risk = "High"
        elif medium_risk > 0:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"

        return {
            'high_risk_changes': high_risk,
            'medium_risk_changes': medium_risk,
            'low_risk_changes': low_risk,
            'total_changes': len(self.changes),
            'overall_risk': overall_risk
        }

    def print_diff_report(self) -> None:
        """Print schema diff report."""
        print(f"\n{'='*60}")
        print(f"SCHEMA MIGRATION: {self.schema_v1_name} → {self.schema_v2_name}")
        print(f"{'='*60}")

        self.compute_diff()

        if not self.changes:
            print("\nNo differences found")
            return

        # Group by type
        by_type = {}
        for change in self.changes:
            ctype = change.change_type.value
            if ctype not in by_type:
                by_type[ctype] = []
            by_type[ctype].append(change)

        # Print by change type
        for change_type in [ChangeType.ADDED.value, ChangeType.MODIFIED.value,
                           ChangeType.REMOVED.value]:
            if change_type in by_type:
                print(f"\n{change_type}:")
                for change in by_type[change_type]:
                    print(f"  {change}")

        # Print risk assessment
        risk = self.get_risk_assessment()
        print(f"\n{'='*60}")
        print("RISK ASSESSMENT")
        print(f"{'='*60}")
        print(f"Total Changes: {risk['total_changes']}")
        print(f"High Risk: {risk['high_risk_changes']}")
        print(f"Medium Risk: {risk['medium_risk_changes']}")
        print(f"Low Risk: {risk['low_risk_changes']}")
        print(f"Overall Risk: {risk['overall_risk']}")


if __name__ == "__main__":
    # Example: Compare university schemas
    diff = SchemaDiff("University v1", "University v2")

    # Add v1 entities
    diff.add_entity(1, "Student")
    diff.add_entity(1, "Course")
    diff.add_property(1, "Student", "student_id")
    diff.add_property(1, "Student", "name")
    diff.add_property(1, "Student", "email")
    diff.add_property(1, "Course", "course_code")
    diff.add_property(1, "Course", "title")
    diff.add_relationship(1, "Student", "ENROLLED_IN", "Course")

    # Add v2 entities
    diff.add_entity(2, "Student")
    diff.add_entity(2, "Course")
    diff.add_entity(2, "Department")
    diff.add_property(2, "Student", "student_id")
    diff.add_property(2, "Student", "full_name")
    diff.add_property(2, "Student", "email")
    diff.add_property(2, "Student", "gpa")
    diff.add_property(2, "Course", "course_code")
    diff.add_property(2, "Course", "title")
    diff.add_property(2, "Course", "credits")
    diff.add_property(2, "Department", "dept_id")
    diff.add_property(2, "Department", "name")
    diff.add_relationship(2, "Student", "ENROLLED_IN", "Course")
    diff.add_relationship(2, "Course", "BELONGS_TO", "Department")

    # Print diff
    diff.print_diff_report()

