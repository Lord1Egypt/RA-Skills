# Memory Index

**Source of truth**: `learning/memory_tree/chunks.db` (SQLite).
Query entries via `python3 scripts/learnings.py --root <workspace> status/search/export`.

## Scripts
| Script | Purpose |
|--------|---------|
| `scripts/learnings.py` | CLI for all operations (log, search, promote, maintain, export) |
| `scripts/extract-skill.sh` | Extract a reusable skill from accumulated learnings |
| `scripts/daily-memory.sh` | Generate daily memory entries under `learning/daily/` |

## Evals
| File | Purpose |
|------|---------|
| `evals/trigger-validation.json` | Test: when should the skill trigger? |
| `evals/output-evals.json` | Test: are logged entries well-formed? |

## Lifecycle Tiers
| Tier | SQLite Status | Purpose |
|------|-------------|---------|
| HOT | `admitted` | Active working set |
| WARM | `buffered` | Retained for context search |
| COLD | `sealed` | Archived — explicit query only |
