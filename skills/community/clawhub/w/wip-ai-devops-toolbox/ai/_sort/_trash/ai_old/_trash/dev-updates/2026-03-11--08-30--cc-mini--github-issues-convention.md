# Add GitHub Issues convention to Dev Guide

**Date:** 2026-03-11 08:30 PST
**Author:** Claude Code (cc-mini)
**Version:** v1.7.9

## What changed

Added a GitHub Issues section to both the public and private Dev Guides. We were tracking work in `ai/todos/` markdown files. Items got lost. GitHub Issues gives us tracking, cross-referencing, and visibility across all agents.

### Public Dev Guide (DEV-GUIDE-GENERAL-PUBLIC.md)

- **GitHub Issues section:** when to use issues vs ai/todos/, filing convention with attribution lines and filed-by labels
- **Public vs private issue routing:** public issues are the front door (users file there), private issues are the workshop (we file there), releases connect them
- **Agent ID naming convention:** `[platform]-[agent]-[machine]` format with examples (oc-lesa-mini, cc-mini, cc-air)

### Private Dev Guide (ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md)

- **filed-by label details:** `filed-by:cc-mini` (blue), `filed-by:oc-lesa-mini` (purple)
- **Commands for adding labels** to new agents or repos (single repo and org-wide)
- **Incident note:** Memory Crystal agent ID drift (4 IDs instead of 2), manual merge of 141K chunks, tracked in memory-crystal-private#33

### Org-wide deployment

`filed-by:cc-mini` and `filed-by:oc-lesa-mini` labels created on all wipcomputer repos.

## Files changed

- `DEV-GUIDE-GENERAL-PUBLIC.md` ... +67 lines (GitHub Issues section)
- `ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` ... +31 lines (filed-by details)

Closes #79
