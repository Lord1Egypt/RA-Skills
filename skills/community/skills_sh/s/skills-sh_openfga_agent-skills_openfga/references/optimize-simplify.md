---
title: Simplify Models
---

## Simplify Models

Remove unused types and relations from your model.

**Incorrect (unused relations):**

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user]
    define viewer: [user]
    define commenter: [user]     # Never used in application
    define legacy_admin: [user]  # Deprecated, no tuples exist

    define can_view : owner or editor or viewer
```

**Correct (minimal model):**

```dsl.openfga
type document
  relations
    define owner: [user]
    define editor: [user]
    define viewer: [user]
    define can_view : owner or editor or viewer
```

**Audit checklist:**

1. **Unused types:** Remove types that have no tuples and aren't referenced
2. **Unused relations:** Remove relations that are never checked or written
3. **Unreferenced conditions:** Remove conditions not used in any relation
4. **Dead paths:** Remove `X from Y` paths where Y relation is never used
5. **Downstream relations:** Before deleting relation `r`, verify no relation in this type or child types uses `r from <parent>`
6. **Propagation aliases:** Keep computed aliases (for example, `org_admin`) when they are used to chain permissions across hierarchy levels

**Safety rule:**
- Do not delete a relation only because it is not directly asserted in tests.
- A relation may be required as a transit dependency in inherited paths.
- Always run a dependency scan before removal.

```bash
rg -n "<relation_name>|<relation_name> from" stores/<store>/{model.fga,store.fga.yaml}
```

**After generating models and tests:**


```bash
# Run tests
fga model test --tests store.fga.yaml
```

**Benefits:**
- Easier to understand and maintain
- Faster validation
- Clearer documentation
- Reduced confusion for developers
