# Errors Log

{DOMAIN_DESCRIPTION}

**Areas**: {DOMAIN_AREAS}
**Statuses**: pending | in_progress | resolved | wont_fix

## Error Entry Format

Append entries in this format:

```markdown
## [ERR-YYYYMMDD-XXX] operation_or_error_type

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: {DOMAIN_AREAS_EXAMPLE}

### Summary
Brief description of what failed

### Error
```
Actual error message or output
```

### Context
- Operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-YYYYMMDD-XXX (if recurring)

---
```

## Placeholders to Replace

- `{DOMAIN_DESCRIPTION}`: e.g., "Operation failures, exceptions, and unexpected behaviors for [skill-name]."
- `{DOMAIN_AREAS}`: e.g., "文案 | 口播 | 短视频脚本" or "系统优化 | 卡顿 | 报错"
- `{DOMAIN_AREAS_EXAMPLE}`: One example area from the list

---
