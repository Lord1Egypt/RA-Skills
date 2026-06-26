# Entity File Template

Use this for large projects where each major entity gets its own file in `docs/domain/entities/`.
Name the file `[entity-name].md` (lowercase, hyphenated).

Reference it from DOMAIN.md like:
> See `docs/domain/entities/generator.md` for full entity spec.

---

# [EntityName]

**File:** `docs/domain/entities/[entity-name].md`
**Last Updated:** [YYYY-MM-DD]
**Status:** `draft` | `confirmed` | `deprecated`

---

## Definition

[2-4 sentences. What is this entity? What does it represent in the real business?]

## Also Known As

- [internal alias 1]
- [internal alias 2]
- [what a generic system might call this]

---

## Attributes

| Attribute | Type | Description | Required | Example |
|-----------|------|-------------|----------|---------|
| `id` | UUID | Unique identifier | Yes | `gen-00142` |
| `[attr]` | [type] | [description] | Yes/No | [example] |
| `[attr]` | [type] | [description] | Yes/No | [example] |

---

## Status / Lifecycle States

```
[Created] → [Active] → [In Use] → [Returned] → [Maintenance] → [Retired]
               ↓
           [Deleted/Archived]
```

| State | Description | Transitions To |
|-------|-------------|---------------|
| `[state]` | [description] | [valid next states] |

---

## Relationships

| Related Entity | Type | Description |
|---------------|------|-------------|
| `[Entity]` | has many | [description] |
| `[Entity]` | belongs to | [description] |
| `[Entity]` | triggers | [description] |

---

## Business Rules

Rules that specifically govern this entity:

| Rule ID | Rule |
|---------|------|
| BR-XXX | [rule] |

---

## Notes & Edge Cases

- [Any quirk or exception to normal behavior]
- [Things that surprised developers when they first learned this]
- [Historical context for why something works a certain way]

---

## Open Questions

- [ ] [Unresolved question about this entity]

