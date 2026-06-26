# super_memori — Stable Host Readiness

> ⚠️ ARCHIVED GATE: This equipped-host promotion path was satisfied for the current stable `4.0.1` line. Keep this file as historical validation criteria, not as pending release work.

## Purpose
Define the first equipped-host validation path that was required before promoting the earlier `v4.0.0 candidate` line into the first stable full-hybrid release later published as `4.0.1`.

## Required equipped-host conditions
All must be true on at least one local Ubuntu host:
- `sentence-transformers` installed locally
- `numpy` installed locally
- the configured embedding model is available locally (`local_files_only=True` path succeeds)
- local Qdrant reachable
- vector collection built from current lexical chunks
- `health-check.sh --json` shows `semantic_ready=true` or equivalent fully ready semantic state
- `audit-memory.sh --json` does not show orphan drift

## Required validation sequence
1. `./index-memory.sh --incremental --json`
2. `./index-memory.sh --rebuild-vectors --json`
3. `./query-memory.sh "agent memory" --mode hybrid --json --limit 3`
4. `./validate-release.sh --strict`
5. `./scripts/release-prep.sh`

## Required success signals
- `mode_requested=hybrid`
- `mode_used=hybrid`
- `semantic_ready=true`
- no semantic degradation warning in query output
- temporal/relation-aware result shaping still present in result payloads when relevant
- release gate remains green on the equipped host

## Blocking outcomes
For the archived pre-stable promotion path, do not promote to stable if any of these are true:
- embedding model still unavailable locally
- vector rebuild fails
- `mode_used` falls back to lexical on the equipped host
- audit reports orphan drift
- health reports `FAIL`
- docs claim stable full-hybrid behavior before an equipped host has actually passed this sequence
