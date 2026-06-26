---
name: text_entity_relation_extractor
title: Text Entity Relation Extractor
description: Extract entities and relationships from unstructured text and convert them into graph-ready structures such as triples, nodes, and edges.
category: data-ingestion
tags:
  - named-entity-recognition
  - relationship-extraction
  - information-extraction
  - nlp
  - text-mining
  - knowledge-graph
  - entity-extraction
  - semantic-analysis
  - text-processing
  - developer-tools
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🧠","homepage":"https://clawhub.com"}}
---

# Text Entity Relation Extractor

**Extract structured knowledge from unstructured text.**

This skill analyzes natural language text and identifies **entities and relationships** that can be converted into **knowledge graph structures** such as nodes, edges, or semantic triples. It is useful for transforming documents, articles, transcripts, or raw text into **graph-ready data** suitable for knowledge graphs, semantic systems, or graph databases.

## Quick Start

### Use When
- Extracting entities from text
- Identifying relationships between entities
- Converting natural language text into knowledge graphs
- Generating triples from unstructured text
- Building graph datasets from documents
- Performing information extraction from unstructured content
- Mining knowledge from documents

### Inputs
- Unstructured text documents
- Text corpus or collection
- Natural language text strings
- Entity type specifications
- Relationship pattern definitions
- Extraction rules and configurations
- Training data (optional)

### Outputs
- Extracted entities with types
- Detected relationships
- RDF triples or semantic statements
- Graph JSON (nodes and edges)
- Entity-relationship tables
- Confidence scores
- Extracted knowledge base

## Example

**Input Text:**
```
Elon Musk founded SpaceX in 2002. SpaceX is headquartered 
in Hawthorne, California and develops reusable spacecraft. 
The company employs over 9,000 people and has partnerships 
with NASA for space exploration missions.
```

**Extracted Entities:**
```
Elon Musk → PERSON
SpaceX → ORGANIZATION
2002 → DATE
Hawthorne → LOCATION
California → LOCATION
NASA → ORGANIZATION
9,000 → QUANTITY
```

**Extracted Relationships:**
```
Elon Musk -[FOUNDED]-> SpaceX
SpaceX -[HEADQUARTERED_IN]-> Hawthorne
SpaceX -[HEADQUARTERED_IN]-> California
SpaceX -[DEVELOPS]-> Spacecraft
SpaceX -[EMPLOYS]-> 9,000 people
SpaceX -[PARTNERS_WITH]-> NASA
```

**Generated RDF Triples:**
```turtle
:Elon_Musk a foaf:Person ;
  foaf:founded :SpaceX .

:SpaceX a schema:Organization ;
  schema:foundationDate "2002"^^xsd:gYear ;
  schema:headquartersLocation :Hawthorne ;
  schema:numberOfEmployees 9000 ;
  schema:partnerOf :NASA .

:Hawthorne a schema:Place ;
  schema:location :California .
```

## Text Extraction Architecture

### 1. Named Entity Recognition (NER)

**Purpose:** Identify and classify entities in text

**Entity Types Supported:**
- **PERSON** - Individual people
- **ORGANIZATION** - Companies, institutions
- **LOCATION** - Places, geographic regions
- **DATE** - Temporal expressions
- **QUANTITY** - Numbers, measurements
- **PRODUCT** - Items, goods, services
- **EVENT** - Named events, conferences
- **LANGUAGE** - Languages and dialects
- **GPE** - Geopolitical entities
- **FACILITY** - Buildings, infrastructure

**Configuration:**
```yaml
ner:
  model: spacy|bert|custom
  entity_types:
    - PERSON
    - ORGANIZATION
    - LOCATION
  confidence_threshold: 0.7
  case_sensitive: true
```

### 2. Relationship Detection

**Purpose:** Identify and extract relationships between entities

**Relationship Types:**
- **Domain-Specific** - Custom relationships
- **Syntactic** - Based on grammar patterns
- **Semantic** - Based on meaning
- **Knowledge-Based** - Using knowledge bases

**Detection Methods:**
```
Dependency Parsing:
  - Extract based on syntactic dependencies
  - Example: SUBJECT -[verb]-> OBJECT

Pattern Matching:
  - Use predefined patterns
  - Example: [PERSON] works at [ORGANIZATION]

Machine Learning:
  - Train on annotated data
  - Classify relationship types

Knowledge Extraction:
  - Use external knowledge bases
  - Semantic role labeling
```

**Configuration:**
```yaml
relation_extraction:
  method: dependency|pattern|ml|hybrid
  relationship_types:
    - WORKS_AT
    - LOCATED_IN
    - FOUNDED
    - OWNS
  confidence_threshold: 0.6
```

### 3. Entity Normalization

**Purpose:** Standardize and deduplicate entities

**Operations:**
- **Name Normalization** - Standardize spelling and format
- **Alias Resolution** - Map aliases to canonical form
- **Deduplication** - Merge equivalent entities
- **URI Generation** - Create unique identifiers

**Configuration:**
```yaml
normalization:
  lowercase: true
  remove_punctuation: true
  alias_mapping:
    USA: United States
    NYC: New York City
  deduplication:
    similarity_threshold: 0.85
```

### 4. Triple Generation

**Purpose:** Convert extracted knowledge to RDF triples

**Components:**
- **Subject** - Entity or reference
- **Predicate** - Relationship type
- **Object** - Target entity or literal

**Example:**
```
Elon_Musk -[FOUNDED]-> SpaceX
SpaceX -[HEADQUARTERS]-> Hawthorne
SpaceX -[EMPLOYEE_COUNT]-> 9000
```

### 5. Graph Construction

**Purpose:** Build knowledge graph from triples

**Output:**
- Nodes representing entities
- Edges representing relationships
- Attributes on nodes and edges
- Connected graph structure

## Extraction Patterns

### Named Entity Recognition Pattern

```
Pattern: Identify entity boundaries and types

Text: "Apple Inc. was founded in 1976 by Steve Jobs."

Extracted:
  Apple Inc. → ORGANIZATION
  1976 → DATE
  Steve Jobs → PERSON
```

### Relationship Extraction Pattern

```
Pattern: Extract [Entity1] -[Relation]-> [Entity2]

Text: "Steve Jobs founded Apple Inc."

Extracted:
  Steve Jobs -[FOUNDED]-> Apple Inc.
  Type: FOUNDER_OF
  Confidence: 0.92
```

### Dependency Parsing Pattern

```
Pattern: Use syntactic structure to extract relations

Dependency: nsubj(VERB, PERSON), dobj(VERB, ORG)

Example:
  Person → VERB → Organization
  John → founded → Apple
```

### Pattern-Based Extraction

```
Pattern: Use handcrafted extraction rules

Rule: [PERSON] works at [ORGANIZATION]
Match: "Alice works at Acme"
Extract: Alice -[WORKS_AT]-> Acme

Rule: [ORG] is located in [LOCATION]
Match: "Google is located in Mountain View"
Extract: Google -[LOCATED_IN]-> Mountain View
```

## Output Formats

### RDF Triples

```turtle
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .

ex:Elon_Musk a foaf:Person ;
  foaf:name "Elon Musk" ;
  ex:founded ex:SpaceX .

ex:SpaceX a schema:Organization ;
  foaf:name "SpaceX" ;
  schema:foundingDate "2002"^^xsd:gYear ;
  schema:headquartersLocation ex:Hawthorne .
```

### Graph JSON

```json
{
  "nodes": [
    {"id": "Elon Musk", "type": "PERSON", "properties": {"name": "Elon Musk"}},
    {"id": "SpaceX", "type": "ORGANIZATION", "properties": {"name": "SpaceX", "founded": 2002}},
    {"id": "Hawthorne", "type": "LOCATION", "properties": {"name": "Hawthorne"}}
  ],
  "edges": [
    {"source": "Elon Musk", "target": "SpaceX", "type": "FOUNDED", "confidence": 0.92},
    {"source": "SpaceX", "target": "Hawthorne", "type": "HEADQUARTERED_IN", "confidence": 0.88}
  ]
}
```

### Tabular Format

| Entity 1 | Type 1 | Relationship | Entity 2 | Type 2 | Confidence |
|----------|--------|--------------|----------|--------|------------|
| Elon Musk | PERSON | FOUNDED | SpaceX | ORG | 0.92 |
| SpaceX | ORG | HEADQUARTERED_IN | Hawthorne | LOCATION | 0.88 |

## Execution Steps

1. **Preprocess Text** – Tokenize, normalize, split sentences
2. **Apply NER** – Identify and classify entities
3. **Detect Relationships** – Extract entity connections
4. **Normalize Entities** – Standardize names, deduplicate
5. **Generate Triples** – Create RDF statements
6. **Score Confidence** – Calculate extraction confidence
7. **Build Graph** – Construct knowledge graph
8. **Format Output** – Generate requested output format

## Confidence Scoring

**Entity Confidence:**
```
Score = Model_Confidence × Type_Confidence × Normalization_Score
Range: 0.0 - 1.0
Threshold: Usually 0.6-0.8 for filtering
```

**Relationship Confidence:**
```
Score = Detection_Score × Entity_Confidence × Pattern_Match_Score
Factors:
  - Model prediction confidence
  - Dependency strength
  - Pattern specificity
```

## Recommended Libraries

- **NER/NLP:** spaCy, NLTK, Transformers (BERT, RoBERTa)
- **Relation Extraction:** AllenNLP, OpenIE, Stanford CoreNLP
- **Text Processing:** NLTK, TextBlob, Gensim
- **Graph Building:** networkx, rdflib, pyLD
- **Machine Learning:** scikit-learn, TensorFlow, PyTorch
- **Utilities:** pandas, numpy, regex

## Best Practices

✓ Choose appropriate NER models for domain  
✓ Validate extracted relationships  
✓ Normalize entity names consistently  
✓ Remove low-confidence extractions  
✓ Handle entity disambiguation  
✓ Document extraction patterns  
✓ Test with domain-specific text  
✓ Manage performance with long texts  
✓ Validate against domain knowledge  
✓ Monitor confidence scores  

## Integration with Downstream Skills

Extracted knowledge feeds into:

- **Mapping DSL Builder** – Define mappings from extracted data
- **Graph Constraint Generator** – Add constraints to extracted graph
- **Graph Schema Validation** – Validate extracted triples
- **Knowledge Graph Construction** – Build KGs from extractions
- **ETL Pipeline Generator** – Process extractions in pipelines

## References

See [extraction-patterns.md](references/extraction-patterns.md) for detailed NER and relationship extraction patterns and [example-extractions.md](examples/example-extractions.md) for complete real-world examples.

---

**Version:** 1.0.0
