# Changelog

## 3.0.0 — 2026-03-14

This is a **CLI-first** rewrite of the skill.

### What changed

- Reoriented the skill around the official `resend` CLI rather than raw API calls.
- Added an explicit **agent subprocess contract** for deterministic invocation and parsing.
- Added a **coverage-gap model** so agents know when to fall back to MCP/API instead of guessing.
- Added a new `scripts/resend_cli.py` wrapper for:
  - CLI probing
  - task routing
  - command lookup
  - scaffold generation
  - batch linting
  - static diagnosis
  - safe subprocess execution with stdout/stderr JSON tolerance
- Added richer machine-readable assets:
  - `command-catalog.json`
  - `task-router.json`
  - `coverage-gaps.json`
  - `subprocess-contract.json`
  - `source-manifest.json`
- Added CLI-native playbooks for:
  - transactional sends
  - batch sends
  - domains and DNS
  - webhooks and local listeners
  - inbound receiving
  - contacts, topics, segments, broadcasts
  - templates and current template-send caveats
  - multi-profile usage
  - CI/CD usage

### Important behavioural changes from v2

- The skill now defaults to **CLI → MCP/API fallback**, not SDK/API-first.
- The skill treats long-running `listen` commands as **event streams**, not ordinary request/response commands.
- The skill now explicitly models the current `stderr` JSON discrepancy, the template-send gap, and the domains capability-toggle ambiguity.
