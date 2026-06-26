# Auto-sync product docs version/date on release

**Date:** 2026-03-16
**Closes:** #202

## What changed

wip-release now auto-updates version and date lines in product docs before the release commit. No more stale "Current version: v1.9.1" when you're shipping v1.9.39.

Files updated automatically:
- `ai/product/plans-prds/roadmap.md`: "Current version" and "Last updated"
- `ai/product/readme-first-product.md`: "Last updated" and "What's Built (as of vX.Y.Z)"

Runs between changelog update and git commit (step 3.75). Only touches files that exist. Only updates lines that match the expected patterns.

## Why

These files were stale from v1.9.1 through v1.9.39 (8 days, 38 releases). Nobody remembered to update them. The existing product docs gate warned about it but couldn't fix it. Now it fixes itself.
