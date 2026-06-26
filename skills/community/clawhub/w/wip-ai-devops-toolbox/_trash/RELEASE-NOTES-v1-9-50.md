# Release Notes: wip-ai-devops-toolbox v1.9.50

**wip-release: require product update doc on every release.**

## What changed

New quality gate in wip-release: checks that `ai/dev-updates/product-update/*-product-update.md` was modified since the last release tag. Same pattern as dev-updates, roadmap, and readme-first checks.

The product update doc is a human-readable test guide. Each release entry has: what changed, how it's supposed to work, and how to test. New entries go at the top. Additive only.

## Why

Three repos now have product update docs but nothing enforced keeping them current. Without the gate, the docs will drift immediately (same problem we had with TECHNICAL.md).

## Issues closed

- #220

## How to verify

```bash
wip-release patch --dry-run
# Should warn if product update doc not modified since last release
```
