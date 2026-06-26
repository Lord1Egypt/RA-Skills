# OWL Ontology Design Patterns

This guide provides patterns for designing RDF/OWL ontologies from domain descriptions.

## Class Definition Patterns

### Simple Class

```turtle
@prefix ex: <http://example.org/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Researcher a owl:Class ;
  rdfs:label "Researcher" ;
  rdfs:comment "A person who conducts research" .
```

### Class Hierarchy

```turtle
ex:Person a owl:Class ;
  rdfs:label "Person" .

ex:Researcher a owl:Class ;
  rdfs:subClassOf ex:Person ;
  rdfs:label "Researcher" .

ex:Student a owl:Class ;
  rdfs:subClassOf ex:Person ;
  rdfs:label "Student" .
```

### Equivalent Classes

```turtle
ex:Author owl:equivalentClass ex:Researcher .
```

---

## Property Definition Patterns

### Object Property (Relationships)

```turtle
ex:writes a owl:ObjectProperty ;
  rdfs:label "writes" ;
  rdfs:comment "A researcher writes papers" ;
  rdfs:domain ex:Researcher ;
  rdfs:range ex:Paper .
```

### Datatype Property (Attributes)

```turtle
ex:name a rdf:Property ;
  rdfs:label "name" ;
  rdfs:range xsd:string .

ex:publicationYear a rdf:Property ;
  rdfs:label "publication year" ;
  rdfs:range xsd:integer .
```

### Property Characteristics

**Functional Property** (one value per subject)
```turtle
ex:emailAddress a owl:FunctionalProperty ;
  rdfs:domain ex:Person .
```

**Inverse Properties**
```turtle
ex:writes a owl:ObjectProperty ;
  owl:inverseOf ex:writtenBy .
```

**Transitive Property**
```turtle
ex:locatedIn a owl:ObjectProperty ;
  rdf:type owl:TransitiveProperty .
```

---

## Cardinality Patterns

### Minimum Cardinality

```turtle
ex:Person a owl:Class ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ex:name ;
    owl:minCardinality 1
  ] .
```

### Maximum Cardinality

```turtle
ex:Person a owl:Class ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ex:primaryEmail ;
    owl:maxCardinality 1
  ] .
```

### Exact Cardinality

```turtle
ex:Vehicle a owl:Class ;
  rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty ex:hasWheel ;
    owl:cardinality 4
  ] .
```

---

## Vocabulary Reuse

### FOAF (Friend of a Friend)

```turtle
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

ex:Researcher a owl:Class ;
  rdfs:subClassOf foaf:Person .

ex:name owl:equivalentProperty foaf:name .
```

### Dublin Core (Metadata)

```turtle
@prefix dc: <http://purl.org/dc/elements/1.1/> .

ex:Publication a owl:Class ;
  rdfs:subClassOf dc:BibliographicResource .
```

### Schema.org

```turtle
@prefix schema: <http://schema.org/> .

ex:ResearchPaper a owl:Class ;
  rdfs:subClassOf schema:ScholarlyArticle .
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Ambiguous class names | Use clear URIs with context |
| Over-constrained ontology | Start minimal, add constraints later |
| Unclear relationships | Always define domain & range |
| Inconsistent naming | Use PascalCase for classes, camelCase for properties |
| Missing documentation | Use rdfs:label and rdfs:comment |
| Namespace conflicts | Use distinct prefixes and URIs |

---

## Best Practices

✓ Start with core classes, add complexity gradually  
✓ Always define domain and range for properties  
✓ Use rdfs:label and rdfs:comment for documentation  
✓ Reuse existing vocabularies when applicable  
✓ Keep namespaces clear and consistent  
✓ Separate schema (T-Box) from data (A-Box)  
✓ Validate with SHACL if needed  

---

## Namespace Management

### Recommended Structure

```turtle
@prefix ex: <http://example.org/ontology#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix schema: <http://schema.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

---

See [example-ontologies.md](../examples/example-ontologies.md) for complete domain ontology examples.

