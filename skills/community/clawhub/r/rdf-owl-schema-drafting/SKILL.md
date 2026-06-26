---
name: rdf_owl_schema_drafting
title: RDF / OWL Ontology Schema Drafting
description: Draft RDF or OWL ontologies and schemas for knowledge graph systems using domain descriptions, entity models, or schema requirements.
category: graph-modeling
tags:
  - knowledge-graph
  - rdf
  - owl
  - ontology
  - semantic-web
  - schema-design
  - linked-data
  - developer-tools
version: 1.0.0
author: community
license: MIT
---

# RDF / OWL Schema Drafting

**Design RDF and OWL ontologies for semantic web and knowledge graph systems.**

This skill translates domain models, entity descriptions, and requirements into machine-readable RDF/OWL schemas with classes, properties, and constraints.

## Quick Start

### Use When
- Designing new RDF/OWL ontologies
- Converting domain models → semantic schemas
- Building linked data systems
- Creating triple store ontologies
- Designing semantic knowledge graphs

### Inputs
- Domain descriptions
- Entity models or ER diagrams
- JSON/CSV structures
- Knowledge graph requirements
- Relational schemas

### Outputs
- RDF classes (rdfs:Class)
- OWL classes (owl:Class)
- Object properties (owl:ObjectProperty)
- Datatype properties (rdf:Property)
- Domain/range constraints
- Turtle/RDF serialization

## Example

**Input:**
```
A research system contains researchers, papers, and institutions.
Researchers write papers and are affiliated with institutions.
Papers have titles and publication years.
```

**Output:**
```turtle
@prefix ex: <http://example.org/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Researcher a owl:Class ;
  rdfs:label "Researcher" .

ex:Paper a owl:Class ;
  rdfs:label "Paper" .

ex:writes a owl:ObjectProperty ;
  rdfs:domain ex:Researcher ;
  rdfs:range ex:Paper ;
  rdfs:label "writes" .

ex:name a rdf:Property ;
  rdfs:label "name" .
```

## Execution Steps

1. **Identify Classes** – Extract core concepts/entities
2. **Identify Properties** – Extract relationships and attributes
3. **Define Domain/Range** – Specify property constraints
4. **Map to OWL** – Convert to OWL/RDF structures
5. **Generate Ontology** – Output Turtle or RDF/XML

## Schema Components

### Classes (Concepts)
```
owl:Class - Core entities
Example: Researcher, Paper, Institution
Naming: PascalCase
```

### Object Properties (Relationships)
```
owl:ObjectProperty - Connect classes
Example: writes, affiliatedWith, publishedIn
Domain: Source class
Range: Target class
Naming: camelCase
```

### Datatype Properties (Attributes)
```
rdf:Property - String/numeric values
Example: name, email, publicationYear
Naming: camelCase
```

## Namespace Structure

```turtle
@prefix ex: <http://example.org/ontology#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
```

## Recommended Libraries

- **Core:** rdflib, owlready2
- **Utilities:** networkx, pyvis
- **Validation:** pyshacl
- **Visualization:** graphviz

## Best Practices

✓ Use clear namespace URIs  
✓ Separate classes from instances  
✓ Define domain/range constraints  
✓ Use camelCase for properties, PascalCase for classes  
✓ Reuse existing vocabularies (FOAF, Dublin Core, Schema.org)  
✓ Keep ontologies modular and maintainable  
✓ Document classes and properties with rdfs:label  

## References

See [ontology-patterns.md](references/ontology-patterns.md) for OWL design patterns and [example-ontologies.md](examples/example-ontologies.md) for domain ontology examples.

---

**Version:** 1.0.0
