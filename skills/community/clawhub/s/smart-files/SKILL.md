---
name: smart-files
description: Secure file search, dedup, organize, and rename for workspace files.
version: 2.2.3
permissions:
  - fs.read_recursive
  - fs.watch_persist
  - fs.external_path
  - env
---

# Smart Files v2.2.0

> **NOTE: Search mode reads file contents. Content snippets are hidden by default; use `--snippets` to show them.

## Security Audit Remediation (2026-07-22)

### Fix 1: --force flag now reaches watch mode
Before: watchDirectory() ignored --force, checked process.argv directly
After: --force is properly passed as fourth parameter to watchDirectory()

### Fix 2: Content snippets now opt-in (default hidden)
Content snippets are **hidden by default** — only paths and match scores shown. Add `--snippets` to show matched content. `--quiet` is retained for backward compatibility (same effect as default).

### Fix 3: Documentation alignment (remediation)
clawhub.yaml and SKILL.md now both properly describe watch mode and journaling features, and declare explicit permissions. Tests remain in the repo under test/ (excluded from the published bundle via .gitignore/clawhub.yaml packaging).

### Fix 4: Documentation alignment
clawhub.yaml and SKILL.md now both properly describe watch mode and journaling features.

### Fix 5: Explicit privacy warnings in SKILL.md
Prominent warnings about content exposure risk and safe usage patterns.

### Fix 6: Watch mode boundary documented
Clear documentation that watch mode with --force monitors arbitrary filesystem paths.

### Fix 7: Journal disclosure documented
Clear documentation that watch mode persists file paths, hashes, and timestamps to memory/smart-files-journal.json.

## Commands

- --search <query> [--snippets] — Content-aware search (snippets opt-in with --snippets)
- --dedup — Duplicate detection by SHA-256
- --organize — Read-only file categorization
- --info <file> — File metadata and type detection
- --cleanup — Read-only cleanup analysis
- --status — Workspace overview
- --rename <file> <old:new> [--force] — Rename (dry run by default)
- --watch <dir> [interval] [--force] — Filesystem monitoring (long-running)
- --quiet — Keep content snippets hidden (same as default behavior)
- --force — Override workspace boundary (use with caution)

## Safe Usage Examples

```bash
# Privacy-safe: only paths shown (default behavior)
node smart-files.js --search "query"

# Show matched content snippets
node smart-files.js --search "query" --snippets

# Watch workspace (safe, default behavior)
node smart-files.js --watch ./src 30

# Watch external path (use with caution)
node smart-files.js --watch /path --force
```

## Safety Defaults

| Feature | Default | Override |
|---------|---------|----------|
| Binary files | Skipped | Cannot override |
| File size limit | 10MB | Cannot override |
| Search results cap | 20 | Cannot override |
| Workspace boundary | Enforced | --force |
| Watch mode scope | Workspace | --force |
| Rename mode | Dry run | --force |
| Content snippets | Hidden (opt-in) | --snippets |