#!/usr/bin/env python3
"""
Minimal RDF/OWL ontology generation utilities for rdf-owl-schema-drafting skill.
Provides core functionality for ontology creation.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
from rdflib.namespace import XSD


@dataclass
class OWLClass:
    """Represents an OWL class."""
    name: str
    label: Optional[str] = None
    comment: Optional[str] = None
    parent_class: Optional[str] = None


@dataclass
class OWLProperty:
    """Represents an OWL property."""
    name: str
    prop_type: str  # 'object' or 'datatype'
    label: Optional[str] = None
    domain: Optional[str] = None
    range_class: Optional[str] = None
    functional: bool = False


class OntologyBuilder:
    """Build RDF/OWL ontologies programmatically."""

    def __init__(self, namespace: str, prefix: str = "ex"):
        """
        Initialize ontology builder.

        Args:
            namespace: Base URI for ontology (e.g., http://example.org/ontology#)
            prefix: Prefix for namespace (default: ex)
        """
        self.graph = Graph()
        self.ns = Namespace(namespace)
        self.prefix = prefix

        # Bind common namespaces
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("owl", OWL)
        self.graph.bind("xsd", XSD)
        self.graph.bind(prefix, self.ns)

    def add_class(self, name: str, label: str = None, comment: str = None,
                  parent: str = None) -> None:
        """Add a class to ontology."""
        class_uri = self.ns[name]

        # Define as owl:Class
        self.graph.add((class_uri, RDF.type, OWL.Class))

        # Add label and comment
        if label:
            self.graph.add((class_uri, RDFS.label, Literal(label)))
        if comment:
            self.graph.add((class_uri, RDFS.comment, Literal(comment)))

        # Add parent class if specified
        if parent:
            parent_uri = self.ns[parent]
            self.graph.add((class_uri, RDFS.subClassOf, parent_uri))

    def add_object_property(self, name: str, domain: str, range_class: str,
                           label: str = None, inverse: str = None) -> None:
        """Add an object property to ontology."""
        prop_uri = self.ns[name]
        domain_uri = self.ns[domain]
        range_uri = self.ns[range_class]

        # Define as ObjectProperty
        self.graph.add((prop_uri, RDF.type, OWL.ObjectProperty))
        self.graph.add((prop_uri, RDFS.domain, domain_uri))
        self.graph.add((prop_uri, RDFS.range, range_uri))

        if label:
            self.graph.add((prop_uri, RDFS.label, Literal(label)))

        # Add inverse property if specified
        if inverse:
            inverse_uri = self.ns[inverse]
            self.graph.add((prop_uri, OWL.inverseOf, inverse_uri))

    def add_datatype_property(self, name: str, range_type: str = "xsd:string",
                             label: str = None) -> None:
        """Add a datatype property to ontology."""
        prop_uri = self.ns[name]

        # Define as DatatypeProperty
        self.graph.add((prop_uri, RDF.type, OWL.DatatypeProperty))

        # Add range
        if range_type.startswith("xsd:"):
            range_uri = XSD[range_type.split(":")[1]]
        else:
            range_uri = Literal(range_type)

        self.graph.add((prop_uri, RDFS.range, range_uri))

        if label:
            self.graph.add((prop_uri, RDFS.label, Literal(label)))

    def serialize_turtle(self, file_path: str = None) -> str:
        """
        Serialize ontology to Turtle format.

        Args:
            file_path: Optional path to save to file

        Returns:
            Turtle serialization string
        """
        turtle = self.graph.serialize(format="turtle")

        if file_path:
            with open(file_path, 'w') as f:
                f.write(turtle)

        return turtle

    def serialize_rdfxml(self, file_path: str = None) -> str:
        """Serialize ontology to RDF/XML format."""
        rdfxml = self.graph.serialize(format="xml")

        if file_path:
            with open(file_path, 'w') as f:
                f.write(rdfxml)

        return rdfxml

    def get_statistics(self) -> Dict:
        """Get ontology statistics."""
        classes = list(self.graph.subjects(RDF.type, OWL.Class))
        obj_props = list(self.graph.subjects(RDF.type, OWL.ObjectProperty))
        dt_props = list(self.graph.subjects(RDF.type, OWL.DatatypeProperty))

        return {
            'total_triples': len(self.graph),
            'classes': len(classes),
            'object_properties': len(obj_props),
            'datatype_properties': len(dt_props),
            'total_properties': len(obj_props) + len(dt_props)
        }


if __name__ == "__main__":
    # Example: Build a simple research ontology
    builder = OntologyBuilder("http://example.org/research#")

    # Add classes
    builder.add_class("Researcher", "Researcher", "A person who conducts research")
    builder.add_class("Paper", "Paper", "A research publication")
    builder.add_class("Institution", "Institution", "A research institution")

    # Add object properties
    builder.add_object_property("writes", "Researcher", "Paper", "writes")
    builder.add_object_property("writtenBy", "Paper", "Researcher", "written by",
                               inverse="writes")
    builder.add_object_property("affiliatedWith", "Researcher", "Institution",
                               "affiliated with")

    # Add datatype properties
    builder.add_datatype_property("title", "xsd:string", "title")
    builder.add_datatype_property("name", "xsd:string", "name")
    builder.add_datatype_property("publicationYear", "xsd:integer", "publication year")

    # Print statistics
    stats = builder.get_statistics()
    print("=" * 50)
    print("ONTOLOGY STATISTICS")
    print("=" * 50)
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Serialize to Turtle
    print("\n" + "=" * 50)
    print("TURTLE SERIALIZATION")
    print("=" * 50)
    turtle = builder.serialize_turtle()
    print(turtle)

