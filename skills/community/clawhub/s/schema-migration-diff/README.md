# Schema Migration Diff - Quick Reference

Modular structure for the **schema-migration-diff** skill - detects differences and generates migration plans.

## 📁 Structure

```
schema-migration-diff/
│
├── SKILL.md                    # Skill definition & overview
│
├── references/                 # Technical guidance
│   └── migration-patterns.md   # Schema migration patterns & strategies
│
├── examples/                   # Domain examples
│   └── example-migrations.md   # University, E-Commerce, Research, Social
│
└── scripts/                    # Utility scripts
    └── schema_diff.py          # SchemaDiff implementation
```

## 🎯 Quick Start

### For Using This Skill

1. **Read:** `SKILL.md` - Understand schema migration
2. **Learn:** `references/migration-patterns.md` - Migration patterns
3. **See:** `examples/example-migrations.md` - Real migration examples

### For Implementation

1. Use `scripts/schema_diff.py` for comparing schemas
2. Supports: Entity, property, relationship, constraint diffs
3. Generates: Diff reports, risk assessments

## 📚 Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, overview, use cases |
| `migration-patterns.md` | Migration patterns & best practices |
| `example-migrations.md` | 4 domain migration examples |
| `schema_diff.py` | Python SchemaDiff class |

## ⚡ Key Features

✓ Entity change detection  
✓ Property change detection  
✓ Relationship change detection  
✓ Risk assessment  
✓ Diff categorization  
✓ Migration planning  
✓ Pattern-based migrations  

## 🔗 Usage Example

```python
from scripts.schema_diff import SchemaDiff

# Create diff
diff = SchemaDiff("v1", "v2")

# Add v1 schemas
diff.add_entity(1, "Student")
diff.add_property(1, "Student", "name")

# Add v2 schemas
diff.add_entity(2, "Student")
diff.add_property(2, "Student", "full_name")

# Print diff
diff.print_diff_report()
```

## 📖 See Also

- Skill Definition: `SKILL.md`
- Migration Patterns: `references/migration-patterns.md`
- Examples: `examples/example-migrations.md`
- Implementation: `scripts/schema_diff.py`

---

**Lean, focused modular structure - only core functionality for schema migration diff.**

