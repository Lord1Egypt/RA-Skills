# Text Extraction Design Patterns

This guide provides patterns for named entity recognition and relationship extraction.

## Named Entity Recognition (NER) Patterns

### Spacy-Based NER Pattern

```
Pattern: Use spaCy for entity recognition

Configuration:
  model: en_core_web_sm (small) or en_core_web_lg (large)
  entity_types: PERSON, ORG, GPE, PRODUCT, EVENT, DATE

Example:
  Text: "Alice Johnson works at Google in New York"
  Entities:
    - Alice Johnson → PERSON
    - Google → ORG
    - New York → GPE (Geopolitical)
```

### BERT-Based NER Pattern

```
Pattern: Use BERT transformer for entity recognition

Configuration:
  model: bert-base-cased or distilbert-base-cased
  task: token-classification (NER)
  custom_labels: True/False

Features:
  - Contextual word embeddings
  - Superior accuracy on complex texts
  - Support for custom entity types
  - Bidirectional context
```

### Custom Rule-Based NER Pattern

```
Pattern: Define custom NER rules

Rules:
  - Pattern: [A-Z][a-z]+ [A-Z][a-z]+ → PERSON
    Example: "John Smith" → PERSON
  
  - Pattern: \$[\d,.]+ → MONEY
    Example: "$10,000" → MONEY
  
  - Pattern: [A-Z][A-Za-z ]+ (Inc|Corp|Ltd) → ORGANIZATION
    Example: "Apple Inc" → ORGANIZATION
  
  - Pattern: (Monday|Tuesday|...|January|February|...|2024) → DATE
    Example: "January 2024" → DATE
```

### Dictionary-Based Lookup Pattern

```
Pattern: Use predefined lists of entities

Approach:
  - Maintain dictionary of known entities
  - Match text against dictionary
  - Assign entity type based on match

Example:
  people_dict = ["Alice Johnson", "Bob Smith"]
  orgs_dict = ["Google", "Apple", "Microsoft"]
  
  "Alice Johnson works at Google"
  → "Alice Johnson" in people_dict → PERSON
  → "Google" in orgs_dict → ORGANIZATION
```

---

## Relationship Extraction Patterns

### Dependency Parsing Pattern

```
Pattern: Extract relationships using syntactic dependencies

Approach:
  - Parse sentence syntax
  - Identify subject-verb-object patterns
  - Extract relationships from dependencies

Example:
  Text: "Steve Jobs founded Apple"
  
  Dependency Parse:
    founded(VERB)
      ├─ nsubj: Steve Jobs (PERSON)
      └─ dobj: Apple (ORGANIZATION)
  
  Extracted:
    Steve Jobs -[FOUNDED]-> Apple
```

### Pattern-Matching Extraction Pattern

```
Pattern: Use predefined extraction patterns

Patterns:
  - "[PERSON] works at [ORGANIZATION]"
    Text: "Alice works at Google"
    Extract: Alice -[WORKS_AT]-> Google
  
  - "[ORGANIZATION] is located in [LOCATION]"
    Text: "Google is located in Mountain View"
    Extract: Google -[LOCATED_IN]-> Mountain View
  
  - "[PERSON] is the CEO of [ORGANIZATION]"
    Text: "Tim Cook is the CEO of Apple"
    Extract: Tim Cook -[CEO_OF]-> Apple

Benefits:
  - Transparent rules
  - Easy to maintain
  - Domain-specific patterns
```

### Semantic Role Labeling (SRL) Pattern

```
Pattern: Use semantic roles for relationship extraction

Roles:
  - ARG0: Agent (who performs action)
  - ARG1: Patient (affected by action)
  - ARG2-5: Additional arguments
  - ARGM: Modifiers (time, location, etc.)

Example:
  Text: "John bought a car from David in 2023"
  
  SRL Parse:
    bought(VERB)
      ├─ ARG0 (Agent): John
      ├─ ARG1 (Patient): car
      ├─ ARG2 (Source): David
      └─ ARGM-TMP (Time): in 2023
  
  Extracted Relationships:
    John -[BOUGHT]-> car
    David -[SOLD_TO]-> John
    Transaction -[DATE]-> 2023
```

### Relation Classification Pattern

```
Pattern: Classify relationships between entity pairs

Approach:
  1. Identify entity pairs in sentence
  2. Extract context between entities
  3. Classify relationship type

Example:
  Text: "Microsoft acquired GitHub in 2018"
  
  Entity Pairs:
    (Microsoft, GitHub)
  
  Context: "acquired ... in 2018"
  
  Classification Model:
    Input: (Entity1, Entity2, Context)
    Output: ACQUIRED_BY
```

---

## Entity Normalization Patterns

### Name Normalization Pattern

```
Pattern: Standardize entity names

Operations:
  - Lowercase conversion
  - Whitespace normalization
  - Punctuation removal
  - Accent removal

Example:
  Input: "ALICE JOHNSON", "Alice  Johnson", "Alice-Johnson"
  Output: "alice johnson" (canonical form)
```

### Alias Resolution Pattern

```
Pattern: Map aliases to canonical forms

Aliases:
  USA → United States
  NYC → New York City
  Tesla Inc → Tesla
  Google LLC → Google
  WHO → World Health Organization

Example:
  Text: "The USA government and WHO collaborated"
  Resolved:
    "USA" → "United States"
    "WHO" → "World Health Organization"
```

### Entity Linking Pattern

```
Pattern: Link extracted entities to knowledge bases

Approach:
  1. Extract entity mention
  2. Query knowledge base (Wikipedia, DBpedia, etc.)
  3. Disambiguate if multiple matches
  4. Link to canonical URI

Example:
  Text: "Apple released a new product"
  
  Extracted: Apple (could be company or fruit)
  
  Context Analysis:
    - Mention of "product"
    - Associated with "released"
    - Likely refers to company
  
  Resolution:
    Apple → Q312 (Wikipedia: Apple Inc.)
    URI: https://dbpedia.org/resource/Apple_Inc.
```

### Deduplication Pattern

```
Pattern: Merge equivalent entities

Approach:
  - Calculate similarity between entities
  - Merge if similarity > threshold
  - Keep canonical form

Example:
  Entities:
    - "Apple Inc."
    - "Apple"
    - "APPLE INC"
  
  Similarity:
    - "Apple Inc." vs "Apple": 0.95
    - "Apple Inc." vs "APPLE INC": 0.98
  
  Merge:
    All → "Apple Inc." (canonical)
```

---

## Confidence Scoring Patterns

### Entity Confidence Pattern

```
Pattern: Calculate entity confidence score

Formula:
  Confidence = Model_Score × Boundary_Score × Type_Score
  
  Model_Score: NER model confidence (0.0-1.0)
  Boundary_Score: How clear entity boundaries are
  Type_Score: Confidence in entity type classification

Example:
  Text: "Steve Jobs, CEO of Apple"
  
  "Steve Jobs":
    Model_Score: 0.95
    Boundary_Score: 0.90
    Type_Score: 0.98
    Overall: 0.95 × 0.90 × 0.98 = 0.84
```

### Relationship Confidence Pattern

```
Pattern: Calculate relationship confidence

Formula:
  Confidence = Detection_Score × 
               Entity1_Confidence × 
               Entity2_Confidence × 
               Pattern_Match_Score

Factors:
  - Detection model confidence
  - Quality of entity mentions
  - How well pattern matched
  - Syntactic connection strength
```

---

## Advanced Patterns

### Coreference Resolution Pattern

```
Pattern: Resolve pronoun references

Example:
  Text: "John went to the store. He bought milk."
  
  Pronouns: "He" → John
  
  Unified Entity:
    John -[WENT_TO]-> store
    John -[BOUGHT]-> milk
```

### Temporal Relation Pattern

```
Pattern: Extract temporal relationships

Example:
  Text: "Company X was founded in 2000. After 10 years, it went public."
  
  Temporal Events:
    - Founded: 2000
    - IPO: 2000 + 10 = 2010
    - Relationship: Founded -[PRECEDES_BY 10 YEARS]-> IPO
```

### Knowledge Graph Completion Pattern

```
Pattern: Infer missing relationships

Approach:
  - Extract explicit relationships
  - Use graph structure to infer implicit ones
  - Apply reasoning rules

Example:
  Explicit:
    Alice -[WORKS_AT]-> Company X
    Company X -[LOCATED_IN]-> New York
  
  Inferred:
    Alice -[WORKS_IN]-> New York
```

---

## Domain-Specific Patterns

### Medical NER Pattern

```
Pattern: Extract medical entities

Entities:
  - DISEASE: Diabetes, Heart disease
  - SYMPTOM: Fever, Chest pain
  - MEDICATION: Aspirin, Metformin
  - ANATOMY: Heart, Liver, Brain
  - PROCEDURE: Surgery, CT scan
  - DOSAGE: 500mg, 2x daily

Example:
  Text: "Patient has Type 2 Diabetes. Prescribed Metformin 500mg twice daily."
  
  Extracted:
    Type 2 Diabetes → DISEASE
    Metformin → MEDICATION
    500mg → DOSAGE
    twice daily → FREQUENCY
```

### Legal NER Pattern

```
Pattern: Extract legal entities

Entities:
  - PARTY: People, organizations (plaintiff, defendant)
  - CASE_NUMBER: Case reference numbers
  - STATUTE: Laws, regulations
  - COURT: Court names and jurisdictions
  - DATE: Important dates in case

Example:
  Text: "Smith v. Jones, Case No. 2023-CV-001, decided by Circuit Court"
  
  Extracted:
    Smith → PARTY (Plaintiff)
    Jones → PARTY (Defendant)
    2023-CV-001 → CASE_NUMBER
    Circuit Court → COURT
```

---

## Best Practices

✓ Choose appropriate NER model for domain  
✓ Validate extraction rules with samples  
✓ Handle entity disambiguation  
✓ Use confidence thresholds to filter low-quality extractions  
✓ Document custom patterns and rules  
✓ Test with domain-specific text  
✓ Monitor extraction quality metrics  
✓ Combine multiple extraction methods (ensemble)  
✓ Handle multilingual text when needed  
✓ Validate relationships against domain knowledge  

---

See [example-extractions.md](../examples/example-extractions.md) for complete text extraction examples.


