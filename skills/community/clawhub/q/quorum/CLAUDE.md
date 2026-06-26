# CLAUDE.md — Agent Instructions for Quorum

This file provides context for Claude Code and other AI agents working on this repository.

## Project Overview

Quorum is a multi-critic quality assurance framework. The reference implementation lives in `reference-implementation/` and is published on PyPI as `quorum-validator`.

## Current State

- **6 of 9 critics shipped**: Correctness, Completeness, Security, Code Hygiene, Cross-Consistency (`--relationships` flag required), Tester (L1 + L2)
- **3 planned**: Architecture, Delegation, Style
- **Version**: See `critic-status.yaml` for the canonical version and critic status
- **Tests**: `cd reference-implementation && pytest tests/ -v` (exclude `test_e2e_smoke.py` and `test_performance.py` for offline runs)

## Shipping Checklist — MANDATORY

**When shipping any feature or critic to main, follow `SHIPPING.md` in the repo root.**

Key steps:
1. Update `critic-status.yaml` (the single source of truth for critic/feature status)
2. Bump version in `critic-status.yaml` AND `reference-implementation/pyproject.toml`
3. Run `python tools/validate-docs.py` — fix all findings before merging
4. Run `tools/boundary-scan.sh` (located in the workspace, not this repo) — ensure no private paths leak
5. Update `docs/CHANGELOG.md` with a full release entry
6. All doc files that reference critic counts or status markers must match the manifest

**Why this matters:** We've shipped features with 10+ doc files still claiming old critic counts. The manifest + validation script + CI gate exists to prevent that. Don't skip it.

## Key Files

| File | Purpose |
|------|---------|
| `critic-status.yaml` | Single source of truth for shipped critics and features |
| `SHIPPING.md` | Full shipping checklist |
| `tools/validate-docs.py` | Automated doc validation (reads manifest, flags stale references) |
| `SPEC.md` | Framework specification |
| `reference-implementation/` | Python CLI implementation |
| `docs/CHANGELOG.md` | Release history |

## Conventions

- **Evidence grounding**: Every critic finding must cite specific locus (file, line, excerpt). No hand-waving.
- **Test coverage**: New critics need both unit tests and integration tests. Target: 20+ tests per critic.
- **Status markers**: Use ✅ Shipped or 🔜 Planned in docs. Update `critic-status.yaml` first, then docs.
- **Boundary scan**: No private file paths, internal names, or credentials in public files. `quorum-runs/` is gitignored.
