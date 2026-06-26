# Evolution Log

> **Convention**: Reverse chronological order (newest on top, oldest at bottom). Prepend new entries.

---

## 2026-04-05: SOTA Audit — Major Update

**Status**: Comprehensive audit against 2025-2026 best practices. All files updated.

### Changes

**SKILL.md**:

- Added security section with loguru redaction filter pattern (regex-based secret scrubbing)
- Added `enqueue=True` OOM warning linking [loguru#1419](https://github.com/Delgan/loguru/issues/1419)
- Added `logger.complete()` shutdown requirement for enqueued messages
- Replaced `json.dumps()` with `orjson.dumps().decode()` in JSONL formatter (2-10x speedup)
- Added OTel trace_id note — production services should use OTel-propagated IDs, not UUID4
- Expanded decision table: loguru, structlog, stdlib, Logfire, with decision heuristic
- Added container vs local distinction (stdout JSON, no rotation for containers)
- Added anti-patterns #6-9 (enqueue without complete, enqueue with slow sinks, json.dumps at volume, UUID4 in OTel services)
- Removed all platformdirs references — log_dir is now a caller-provided `Path | None`

**loguru-patterns.md**:

- Added async enqueue OOM warning with mitigations
- Added `logger.complete()` / `logger.remove()` shutdown patterns (async + sync)
- Added security redaction filter section with regex patterns
- Switched JSONL formatter to orjson
- Added best practices #6-9

**logging-architecture.md**:

- Added structlog as recommended for production services with OTel
- Added Pydantic Logfire for AI/LLM observability
- Added Kern for enterprise compliance
- Added container vs local comparison table
- Added Python 3.14 `LoggerAdapter.merge_extra=True` note
- Added structlog ContextVar reset pattern for async memory leak prevention
- Removed platformdirs references

**migration-guide.md**:

- Replaced platformdirs with simple `Path`-based log directory
- Switched to orjson in JSONL formatter
- Updated PEP 723 dependencies to `["loguru", "orjson"]`

**Deleted**:

- `references/platformdirs-xdg.md` — platformdirs removed from skill

### Sources

- [loguru#1419](https://github.com/Delgan/loguru/issues/1419) — enqueue unbounded memory
- [structlog 25.x releases](https://github.com/hynek/structlog/releases) — ContextVars, exception groups
- [Pydantic Logfire](https://pydantic.dev/logfire) — OTel-based AI observability
- [orjson benchmarks](https://github.com/ijl/orjson) — 2-10x JSON serialization speedup
- [OTel Python logging](https://opentelemetry.io/docs/zero-code/python/logs-example/) — auto-instrumentation
- [pii-redactor](https://pypi.org/project/pii-redactor/) — PII detection library

---

## 2026-02-26: Initial Evolution Log

**Status**: Skill is in use and maintained. Track improvements here.

### Purpose

This evolution log tracks updates to the skill. Each entry should note:

- What changed (content, structure, tooling)
- Why it changed (bug fix, feature request, best practice)
- Files affected

### How to Use

1. When updating SKILL.md or references, add an entry here with the date
2. Keep entries reverse-chronological (newest first)
3. Link to ADRs or GitHub issues when relevant
4. Reference specific line changes when helpful

---
