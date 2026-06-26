# Dev Update: README Review and Feature Naming

**Date:** 2026-03-02 19:00 PST
**Author:** CC-Mini
**Branch:** cc-mini/cloud-mcp

---

## What We Did

Parker reviewed the README line by line in MDVU. Every change was Parker's call.

### Feature Naming

Old names were inconsistent. Some were product names (Relay, Bridge), some were descriptions (Local Recall, Cloud Search). Parker renamed all of them to plain feature descriptions:

| Old | New |
|-----|-----|
| Local Recall | **Local Memory** |
| Relay | **Multi-Device Sync** |
| Cloud Search | **Cloud Memory** |
| Import | **Import Memories** |
| Memory Consolidation | (unchanged) |
| AI-to-AI Communication | (unchanged) |

These are feature names, not product names. The product names (Relay, Bridge, Total Recall, Dream Weaver Protocol) appear in the body text and "Read more about" links.

### "Read More About" Links

Standardized to show both the product name and what it does:
- Read more about **Relay: Multi-Device Sync**
- Read more about **Cloud Memory & Search**
- Read more about **Bridge: AI-to-AI Communication**

### Other Changes

- Removed "You keep re-explaining yourself." from opening pitch
- Dream Weaver Protocol link goes to repo. Added separate "Read the paper: Dream Weaver Protocol PDF" link to the actual PDF
- AI-to-AI Communication moved below Memory Consolidation (was between Cloud Search and Import)
- Removed redundant "### Memory Crystal" sub-header under "## Features"
- Section renamed from "## Features" to "## Memory Crystal Features"
- Spacing adjustments in the onboarding prompt block

### What's Left

- RELAY.md needs update to match new naming
- TECHNICAL.md needs update to match new naming (Cloud Search references)
- README-ENTERPRISE.md needs update (Claude Code integration table still says "Stop hook" without mentioning poller)

---

## Files Changed

| File | Change |
|------|--------|
| `README.md` | Feature naming, link standardization, section reorg, spacing |
