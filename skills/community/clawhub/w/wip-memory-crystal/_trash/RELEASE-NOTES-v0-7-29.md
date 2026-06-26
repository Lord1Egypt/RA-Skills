# Release Notes: memory-crystal v0.7.29

**Doc audit: MLX setup, deep search params, log paths, role clarification.**

## What changed

SKILL.md and TECHNICAL.md updated for 2 weeks of undocumented features:

- **MLX local LLM:** Added as Option A in SKILL.md Step 2. CLI commands (setup, status, stop) added to TECHNICAL.md.
- **Deep search parameters:** `--intent`, `--explain`, `--candidates` documented in both SKILL.md (crystal_search tool) and TECHNICAL.md (CLI reference + new sections for intent, explain, candidate limit, LLM cache).
- **Log paths:** Fixed obsolete `/tmp/ldm-dev-tools/` reference to `~/.ldm/logs/`. Added logs/ to directory structure.
- **Role clarification:** Two-role architecture (Core and Node) explicitly stated. Standalone role was removed in v0.7.22.

## Why

29 releases in 13 days. Docs didn't keep pace. Agents using crystal_search didn't know about --intent (query disambiguation) or --explain (scoring transparency).

## Issues closed

- #57

## How to verify

```bash
grep "intent" SKILL.md TECHNICAL.md
grep "mlx" SKILL.md TECHNICAL.md
grep "ldm/logs" TECHNICAL.md
```
