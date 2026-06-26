# Archive Schema

## Directory layout

```text
<archive_root>/backups/system-changes/YYYY-MM-DD/HHMM-change-name/
  PRE-RESTART/
    README.md
    meta.json
    plan.md
    backup/
    after/
    diff/
  POST-RESTART/
    restart-result.md
    verify.md
    logs/
```

## PRE-RESTART

### README.md
Human-readable overview:
- change title
- summary
- why this matters
- restart/reload expectation
- risks
- rollback summary

### meta.json
Machine-readable metadata, typically:
- timestamp
- timezone
- change_name
- summary
- archive_root
- persistent_storage
- archive_dir
- restart_required
- operator
- agent
- files
- warnings

### plan.md
Execution plan:
- target files
- exact intended edits
- restart/reload command(s)
- verification points
- rollback steps

### backup/
Before-state copies of files that will be modified.

### after/
Prepared after-state copies of modified files, ideally captured before restart/reload.

### diff/
Unified diffs or notes showing the exact intended change.

## POST-RESTART

### restart-result.md
What happened during restart/reload.

### verify.md
What was checked after restart and what passed/failed.

### logs/
Command outputs, excerpts, or copied logs needed for later diagnosis.

## Daily index

Recommended path:

```text
<archive_root>/backups/system-changes/YYYY-MM-DD/index.md
```

One concise entry per change:
- time
- change name
- directory
- brief purpose
- current status
