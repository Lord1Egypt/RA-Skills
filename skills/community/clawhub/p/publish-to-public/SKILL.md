---
name: axiom-rebrand
description: Generic rebrand pipeline. Deterministic, idempotent, byte-to-byte. Strip jargon, fix paths, regenerate manifests, validate. Use when preparing internal code for public release, marketplace publication, or open-sourcing.
---

# axiom-rebrand

Generic rebrand pipeline. Deterministic, idempotent, byte-to-byte.

## Pricing
- **Free tier:** 100 rebrand/months
- **Then:** $0.005 per use

## When to use
- Open-sourcing an internal tool with private codenames
- Marketplace publication (Capafy, GitHub Marketplace)
- Multi-tenant projects — strip org-specific references
- CI/CD gates on jargon leaks

## When NOT to use
- Code logic needs to change (use a real refactor tool)
- One-off case with few files (just sed by hand)
- Need 100% custom rules (this has a configurable jargon list)

## Dependencies
- Pure Python stdlib
- 1 optional dep: PyYAML (for YAML config; falls back to JSON without it)
