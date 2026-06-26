# Dev Update: Publish Prep and Status Markers

**Date:** 2026-03-02 20:00 PST
**Author:** CC-Mini
**Branch:** cc-mini/cloud-mcp

---

## What We Did

### Feature Status Markers

Added per-feature status as the last bullet point on each feature in README.md:

| Feature | Status |
|---------|--------|
| Local Memory | *In production* |
| Multi-Device Sync | *In testing* |
| Cloud Memory | *In testing* |
| Import Memories | *In testing* |
| Memory Consolidation | *In production* |
| AI-to-AI Communication | *In testing* |

Enterprise README also marked *In testing* inline on the subtitle.

### Security Audit

Searched all source code (`src/`, `scripts/`) for hardcoded tokens, API keys, Worker URLs. Result: clean. All secrets are in Wrangler secrets or 1Password. Safe to publish.

### Doc Updates Complete

All four docs now consistent with README naming:
- RELAY.md: Cloud Memory & Search headers, cc-poller in architecture
- TECHNICAL.md: Cloud Memory & Search Architecture header, updated More Info link
- README-ENTERPRISE.md: Integration table shows cc-poller as primary, six interfaces

### Parker Todo Updated

Reorganized around publishing: PR approval, wip-release, testing checklist per feature, relay setup, Air setup.

---

## Files Changed

| File | Change |
|------|--------|
| `README.md` | Status markers on all six features |
| `README-ENTERPRISE.md` | *In testing* on subtitle |
| `ai/todos/Parker-todo.md` | Rewritten for publish flow |
| `ai/dev-updates/2026-03-02--20-00--cc-mini--publish-prep-and-status-markers.md` | This file |
