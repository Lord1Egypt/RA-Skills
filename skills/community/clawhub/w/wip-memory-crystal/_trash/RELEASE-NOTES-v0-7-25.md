# Release Notes: memory-crystal v0.7.25

Bump SKILL.md version and name to match package branding.

## What changed

- SKILL.md version bumped from 0.4.0 to 0.7.24 (was stuck at the original version)
- SKILL.md name changed from `memory` to `wip-memory-crystal` (matches branded convention)
- Forces deploy to public repo, triggering auto-publish to wip.computer/install/

## Why

The SKILL.md version was out of sync with the package version. The name didn't match the `wip-` branding convention used across all install files on wip.computer.

## Issues closed

- #80

## How to verify

```bash
crystal --version
head -4 ~/.ldm/extensions/memory-crystal/skills/memory/SKILL.md
```
