# Errors

Command failures, exceptions, and non-obvious integration/tool breakages.

Use the `ERR-YYYYMMDD-XXX` format for entries.

## Entry Template

````markdown
## [ERR-YYYYMMDD-XXX] command_or_tool

**Logged**: 2026-04-01T10:00:00Z
**Priority**: medium
**Status**: pending
**Area**: backend | infra | tests | docs | config

### Summary
Short description of the failure.

### Error
```text
Actual error output goes here.
```

### Context
- Command or action attempted
- Relevant inputs
- Environment details if useful

### Suggested Fix
What should be tried next or documented.

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file
- See Also: ERR-20260401-001

---
````
