#!/usr/bin/env python3
"""
Text Entity Relation Extractor implementation for text-entity-relation-extractor skill.
Provides core functionality for extracting entities and relationships from text.
"""

from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import json
import re
from datetime import datetime


class EntityType(Enum):
    """Entity types for NER."""
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    DATE = "DATE"
    QUANTITY = "QUANTITY"
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"
    LANGUAGE = "LANGUAGE"
    GPE = "GPE"
    FACILITY = "FACILITY"


class RelationshipType(Enum):
    """Common relationship types."""
    WORKS_AT = "WORKS_AT"
    LOCATED_IN = "LOCATED_IN"
    FOUNDED = "FOUNDED"
    OWNS = "OWNS"
    AFFILIATED_WITH = "AFFILIATED_WITH"
    HAS_CEO = "HAS_CEO"
    PARTNERS_WITH = "PARTNERS_WITH"
    EMPLOYS = "EMPLOYS"
    DEVELOPS = "DEVELOPS"
    MANUFACTURES = "MANUFACTURES"


class OutputFormat(Enum):
    """Output formats for extractions."""
    RDF = "rdf"
    GRAPH_JSON = "graph_json"
    TRIPLES = "triples"
    TABULAR = "tabular"


@dataclass
class Entity:
    """Extracted entity."""
    text: str
    entity_type: EntityType
    start_char: int
    end_char: int
    confidence: float = 1.0


@dataclass
class Relationship:
    """Extracted relationship."""
    entity1: Entity
    entity2: Entity
    relationship_type: str
    confidence: float = 1.0
    sentence: Optional[str] = None


@dataclass
class ExtractionResult:
    """Result of text extraction."""
    entities: List[Entity] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    text: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


class TextEntityRelationExtractor:
    """Main text extraction class."""

    def __init__(self, model_type: str = "rule-based"):
        """Initialize text extractor."""
        self.model_type = model_type
        self.extraction_result = ExtractionResult()
        self.patterns = self._init_patterns()
        self.errors: List[str] = []

    def _init_patterns(self) -> Dict[str, str]:
        """Initialize extraction patterns."""
        return {
            "person": r"[A-Z][a-z]+ (?:[A-Z]\.? )?[A-Z][a-z]+",
            "organization": r"[A-Z][a-zA-Z\s&]*(?:Inc|Corp|Ltd|Company|Co|Corporation|LLC|Organization)",
            "location": r"[A-Z][a-z]+ (?:City|County|State|Region|District|Province|Country)?",
            "date": r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}|\d{4}",
            "money": r"\$[\d,\.]+(?:\s*(?:million|billion|trillion))?",
            "percentage": r"\d+(?:\.\d+)?%",
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "url": r"https?://[^\s]+"
        }

    def extract(self, text: str) -> ExtractionResult:
        """Extract entities and relationships from text."""
        self.extraction_result = ExtractionResult(text=text)
        self.errors.clear()

        # Extract entities
        self._extract_entities(text)

        # Extract relationships
        self._extract_relationships(text)

        return self.extraction_result

    def _extract_entities(self, text: str) -> None:
        """Extract entities from text."""
        # Simple rule-based extraction

        # Extract people (name pattern)
        people_pattern = r"[A-Z][a-z]+ (?:Dr\.|Prof\.|Mr\.|Ms\. )?[A-Z][a-z]+"
        for match in re.finditer(people_pattern, text):
            entity = Entity(
                text=match.group(),
                entity_type=EntityType.PERSON,
                start_char=match.start(),
                end_char=match.end(),
                confidence=0.85
            )
            if entity not in self.extraction_result.entities:
                self.extraction_result.entities.append(entity)

        # Extract organizations
        org_pattern = r"[A-Z][a-zA-Z\s&]*(?:Inc|Corp|Ltd|Company|Co|Corporation|LLC|Organization|University)"
        for match in re.finditer(org_pattern, text):
            entity = Entity(
                text=match.group(),
                entity_type=EntityType.ORGANIZATION,
                start_char=match.start(),
                end_char=match.end(),
                confidence=0.80
            )
            if entity not in self.extraction_result.entities:
                self.extraction_result.entities.append(entity)

        # Extract dates
        date_pattern = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}|\d{4}"
        for match in re.finditer(date_pattern, text):
            entity = Entity(
                text=match.group(),
                entity_type=EntityType.DATE,
                start_char=match.start(),
                end_char=match.end(),
                confidence=0.90
            )
            if entity not in self.extraction_result.entities:
                self.extraction_result.entities.append(entity)

        # Extract money amounts
        money_pattern = r"\$[\d,\.]+(?:\s*(?:million|billion|trillion))?"
        for match in re.finditer(money_pattern, text):
            entity = Entity(
                text=match.group(),
                entity_type=EntityType.QUANTITY,
                start_char=match.start(),
                end_char=match.end(),
                confidence=0.88
            )
            if entity not in self.extraction_result.entities:
                self.extraction_result.entities.append(entity)

    def _extract_relationships(self, text: str) -> None:
        """Extract relationships from text."""
        # Simple pattern-based relationship extraction

        # Pattern: [PERSON] works at [ORGANIZATION]
        pattern1 = r"([A-Z][a-z]+ [A-Z][a-z]+) works at ([A-Z][a-zA-Z\s&]*(?:Inc|Corp|Ltd|Company))"
        for match in re.finditer(pattern1, text):
            entity1_text = match.group(1)
            entity2_text = match.group(2)
            entity1 = Entity(entity1_text, EntityType.PERSON, match.start(1), match.end(1))
            entity2 = Entity(entity2_text, EntityType.ORGANIZATION, match.start(2), match.end(2))
            rel = Relationship(entity1, entity2, "WORKS_AT", confidence=0.85, sentence=text)
            self.extraction_result.relationships.append(rel)

        # Pattern: [PERSON] founded [ORGANIZATION]
        pattern2 = r"([A-Z][a-z]+ [A-Z][a-z]+) founded ([A-Z][a-zA-Z\s&]*(?:Inc|Corp|Ltd|Company))"
        for match in re.finditer(pattern2, text):
            entity1_text = match.group(1)
            entity2_text = match.group(2)
            entity1 = Entity(entity1_text, EntityType.PERSON, match.start(1), match.end(1))
            entity2 = Entity(entity2_text, EntityType.ORGANIZATION, match.start(2), match.end(2))
            rel = Relationship(entity1, entity2, "FOUNDED", confidence=0.88, sentence=text)
            self.extraction_result.relationships.append(rel)

        # Pattern: [ORGANIZATION] is located in [LOCATION]
        pattern3 = r"([A-Z][a-zA-Z\s&]*(?:Inc|Corp|Ltd|Company)) (?:is )?located in ([A-Z][a-z]+(?:\s*,?\s*[A-Z][a-z]+)?)"
        for match in re.finditer(pattern3, text):
            entity1_text = match.group(1)
            entity2_text = match.group(2)
            entity1 = Entity(entity1_text, EntityType.ORGANIZATION, match.start(1), match.end(1))
            entity2 = Entity(entity2_text, EntityType.LOCATION, match.start(2), match.end(2))
            rel = Relationship(entity1, entity2, "LOCATED_IN", confidence=0.82, sentence=text)
            self.extraction_result.relationships.append(rel)

    def to_triples(self) -> List[Tuple[str, str, str]]:
        """Convert to simple triples format."""
        triples = []
        for rel in self.extraction_result.relationships:
            triple = (
                rel.entity1.text,
                rel.relationship_type,
                rel.entity2.text
            )
            triples.append(triple)
        return triples

    def to_graph_json(self) -> Dict:
        """Convert to graph JSON format."""
        # Create nodes from entities
        nodes = []
        entity_set = set()

        for entity in self.extraction_result.entities:
            if entity.text not in entity_set:
                nodes.append({
                    "id": entity.text,
                    "type": entity.entity_type.value,
                    "confidence": entity.confidence
                })
                entity_set.add(entity.text)

        # Create edges from relationships
        edges = []
        for rel in self.extraction_result.relationships:
            edges.append({
                "source": rel.entity1.text,
                "target": rel.entity2.text,
                "type": rel.relationship_type,
                "confidence": rel.confidence
            })

        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_entities": len(nodes),
                "total_relationships": len(edges),
                "extraction_timestamp": self.extraction_result.timestamp.isoformat()
            }
        }

    def to_rdf(self) -> str:
        """Convert to RDF Turtle format."""
        output = """@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

"""

        # Create RDF triples
        for rel in self.extraction_result.relationships:
            entity1_id = rel.entity1.text.replace(" ", "_").lower()
            entity2_id = rel.entity2.text.replace(" ", "_").lower()

            output += f"ex:{entity1_id} a {self._get_rdf_type(rel.entity1.entity_type)} ;\n"
            output += f"  foaf:name \"{rel.entity1.text}\" ;\n"
            output += f"  ex:{rel.relationship_type.lower()} ex:{entity2_id} .\n\n"

            output += f"ex:{entity2_id} a {self._get_rdf_type(rel.entity2.entity_type)} ;\n"
            output += f"  foaf:name \"{rel.entity2.text}\" .\n\n"

        return output

    def to_tabular(self) -> List[Dict[str, str]]:
        """Convert to tabular format."""
        rows = []
        for rel in self.extraction_result.relationships:
            rows.append({
                "Entity 1": rel.entity1.text,
                "Type 1": rel.entity1.entity_type.value,
                "Relationship": rel.relationship_type,
                "Entity 2": rel.entity2.text,
                "Type 2": rel.entity2.entity_type.value,
                "Confidence": f"{rel.confidence:.2f}"
            })
        return rows

    def get_entities_by_type(self, entity_type: EntityType) -> List[Entity]:
        """Get entities by type."""
        return [e for e in self.extraction_result.entities if e.entity_type == entity_type]

    def get_relationships_by_type(self, rel_type: str) -> List[Relationship]:
        """Get relationships by type."""
        return [r for r in self.extraction_result.relationships if r.relationship_type == rel_type]

    def get_summary(self) -> Dict:
        """Get extraction summary."""
        return {
            "total_entities": len(self.extraction_result.entities),
            "total_relationships": len(self.extraction_result.relationships),
            "entity_types": list(set(e.entity_type.value for e in self.extraction_result.entities)),
            "relationship_types": list(set(r.relationship_type for r in self.extraction_result.relationships)),
            "avg_entity_confidence": sum(e.confidence for e in self.extraction_result.entities) / len(self.extraction_result.entities) if self.extraction_result.entities else 0,
            "avg_rel_confidence": sum(r.confidence for r in self.extraction_result.relationships) / len(self.extraction_result.relationships) if self.extraction_result.relationships else 0
        }

    def print_summary(self) -> None:
        """Print extraction summary."""
        print(f"\n{'='*60}")
        print(f"TEXT EXTRACTION SUMMARY")
        print(f"{'='*60}")

        summary = self.get_summary()
        print(f"Total Entities: {summary['total_entities']}")
        print(f"Total Relationships: {summary['total_relationships']}")
        print(f"Entity Types: {', '.join(summary['entity_types'])}")
        print(f"Relationship Types: {', '.join(summary['relationship_types'])}")
        print(f"Avg Entity Confidence: {summary['avg_entity_confidence']:.2f}")
        print(f"Avg Relationship Confidence: {summary['avg_rel_confidence']:.2f}")

        print(f"\nExtracted Entities:")
        for entity in self.extraction_result.entities[:10]:
            print(f"  {entity.text:30} {entity.entity_type.value:15} {entity.confidence:.2f}")

        print(f"\nExtracted Relationships:")
        for rel in self.extraction_result.relationships[:10]:
            print(f"  {rel.entity1.text:20} -[{rel.relationship_type:15}]-> {rel.entity2.text:20} {rel.confidence:.2f}")

    @staticmethod
    def _get_rdf_type(entity_type: EntityType) -> str:
        """Get RDF type for entity type."""
        mapping = {
            EntityType.PERSON: "foaf:Person",
            EntityType.ORGANIZATION: "schema:Organization",
            EntityType.LOCATION: "schema:Place",
            EntityType.PRODUCT: "schema:Product",
            EntityType.EVENT: "schema:Event"
        }
        return mapping.get(entity_type, "rdf:Resource")


if __name__ == "__main__":
    # Example 1: Simple text extraction
    print("Example 1: News Article Text Extraction")

    extractor = TextEntityRelationExtractor(model_type="rule-based")

    text = """
    Elon Musk founded SpaceX in 2002. SpaceX is located in Hawthorne, California.
    Tim Cook works at Apple Inc. The company is headquartered in Cupertino.
    """

    result = extractor.extract(text)
    extractor.print_summary()

    print("\n\nGenerated Triples:")
    for triple in extractor.to_triples():
        print(f"  {triple[0]} -[{triple[1]}]-> {triple[2]}")

    print("\n\nGenerated Graph JSON:")
    print(json.dumps(extractor.to_graph_json(), indent=2))

    print("\n\nGenerated RDF Triples:")
    print(extractor.to_rdf())

    print("\n\nTabular Format:")
    tabular = extractor.to_tabular()
    for row in tabular:
        print(f"  {row['Entity 1']:25} {row['Relationship']:15} {row['Entity 2']:25} {row['Confidence']}")


