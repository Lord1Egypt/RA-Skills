# Text Entity Relation Extractor - Quick Reference

Modular structure for the **text-entity-relation-extractor** skill - extracts entities and relationships from unstructured text to build knowledge graphs.

## 📁 Structure

```
text-entity-relation-extractor/
│
├── SKILL.md                         # Skill definition & overview
│
├── references/                      # Technical guidance
│   └── extraction-patterns.md       # NER and RE extraction patterns
│
├── examples/                        # Domain examples
│   └── example-extractions.md       # Real extraction examples
│
└── scripts/                         # Utility scripts
    └── text_extractor.py            # TextEntityRelationExtractor implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand text extraction
2. **Learn:** `references/extraction-patterns.md` - Extraction patterns
3. **See:** `examples/example-extractions.md` - Real examples

### For Implementation

1. Use `scripts/text_extractor.py` for extracting entities and relationships
2. Supports: NER, Relationship Detection, Triple Generation
3. Generates: Entities, Relationships, Triples, Graphs

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `extraction-patterns.md` | NER and extraction design patterns & best practices |
| `example-extractions.md` | Real-world extraction examples |
| `text_extractor.py` | Python TextEntityRelationExtractor class |

## ⚡ Key Features

✓ Named Entity Recognition (NER) support  
✓ Multiple entity types (Person, Organization, Location, etc.)  
✓ Relationship detection and extraction  
✓ Entity normalization and deduplication  
✓ Multiple output formats (Triples, Graph JSON, RDF, Tabular)  
✓ Dependency parsing for relationship inference  
✓ Pattern-based extraction rules  
✓ Confidence scoring  
✓ Batch text processing  
✓ Multilingual support foundation  

## 🔗 Usage Example

```python
from scripts.text_extractor import TextEntityRelationExtractor

# Create extractor
extractor = TextEntityRelationExtractor(
    model_type="spacy",
    entity_types=["PERSON", "ORG", "LOCATION"]
)

# Extract from text
text = "Alice works at Acme Corporation in New York."
entities = extractor.extract_entities(text)
relationships = extractor.extract_relationships(text, entities)

# Get output formats
triples = extractor.to_triples()
graph_json = extractor.to_graph_json()
rdf_output = extractor.to_rdf()
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Extraction Patterns: `references/extraction-patterns.md`
- Examples: `examples/example-extractions.md`
- Implementation: `scripts/text_extractor.py`

---

**Lean, focused modular structure - only core functionality for text entity and relationship extraction.**


