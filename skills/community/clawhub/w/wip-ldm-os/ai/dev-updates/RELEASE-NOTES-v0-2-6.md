# Release Notes: LDM OS v0.2.6

**Date:** 2026-03-13

## What's new

### Catalog: Memory Crystal npm scoped
- `catalog.json` updated: Memory Crystal npm field now `@wipcomputer/memory-crystal` (was `memory-crystal`)
- Matches the scoping rename in memory-crystal-private

### OpenClaw detection
- `ldm status` and `ldm doctor` now detect OpenClaw as an installed component
- SKILL.md updated with correct OpenClaw link

### Catalog matching and output improvements (v0.2.5)
- Fixed catalog matching for components installed under different names
- Simplified `--dry-run` output for cleaner install previews
- Updated skill descriptions across all components

### Secrets cleanup (v0.2.4)
- Removed secrets directory reference from SKILL.md
- Cleaned up directory descriptions

### System state awareness (v0.2.3)
- System state detection for existing installations
- Trash mechanism for safe removal
- Revert manifests for rollback
- Updated install prompt: four questions, follow-up asks, clearer flow
