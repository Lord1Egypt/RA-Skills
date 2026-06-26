# RDF/OWL Schema Drafting - Quick Reference

Modular structure for the **rdf-owl-schema-drafting** skill - designs RDF/OWL ontologies for semantic web systems.

## 📁 Structure

```
rdf-owl-schema-drafting/
│
├── SKILL.md                    # Skill definition & overview
│
├── references/                 # Technical guidance
│   └── ontology-patterns.md    # OWL design patterns & best practices
│
├── examples/                   # Domain examples
│   └── example-ontologies.md   # Research, E-Commerce, Library examples
│
└── scripts/                    # Utility scripts
    └── ontology_builder.py     # OntologyBuilder implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand ontology design
2. **Learn:** `references/ontology-patterns.md` - Design patterns
3. **See:** `examples/example-ontologies.md` - Real domain ontologies

### For Implementation

1. Use `scripts/ontology_builder.py` for building ontologies
2. Supports: Class creation, property definition, constraints
3. Generates: Turtle, RDF/XML output

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `ontology-patterns.md` | OWL design patterns & vocabulary reuse |
| `example-ontologies.md` | 3 domain examples (Research, E-Commerce, Library) |
| `ontology_builder.py` | Python OntologyBuilder class |

## ⚡ Key Features

✓ Class hierarchy definition  
✓ Object property definition  
✓ Datatype property definition  
✓ Domain/range constraints  
✓ Cardinality constraints  
✓ Vocabulary reuse (FOAF, Dublin Core)  
✓ Output in Turtle & RDF/XML  

## 🔗 Usage Example

```python
from scripts.ontology_builder import OntologyBuilder

# Create ontology
builder = OntologyBuilder("http://example.org/research#")

# Add classes
builder.add_class("Researcher", "Researcher", "A research person")
builder.add_class("Paper", "Paper", "A research publication")

# Add properties
builder.add_object_property("writes", "Researcher", "Paper", "writes")
builder.add_datatype_property("title", "xsd:string", "title")

# Export
turtle = builder.serialize_turtle()
print(turtle)
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- OWL Patterns: `references/ontology-patterns.md`
- Domain Examples: `examples/example-ontologies.md`
- Implementation: `scripts/ontology_builder.py`

---

**Lean, focused modular structure - only core functionality for RDF/OWL ontology design.**

