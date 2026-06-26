# Changelog

All notable changes to the **harness** skill are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows semantic versioning adapted for skills (see [skill-factory](https://github.com/zhelunSun/skill-factory)).

---

## [v1.2.0] — 2026-04-18

**Multi-source integration: beyond OpenAI**

### Added
- `references/extended-sources.md`: curated index of industry sources (Anthropic, GitHub, Aider, Eugene Yan, Chip Huyen, etc.)
- `SKILL.md`: extended trigger word coverage for Chinese and English queries
- `README.md`: updated to reflect multi-source positioning

### Changed
- Repositioned from "OpenAI Harness distillation" → "agent-first engineering knowledge base"
- 10 core principles expanded with cross-source validation

---

## [v1.1.0] — 2026-04-17

**Audit & completion pass**

### Added
- Ralph Wiggum loop principle (self-review cycle)
- Architecture-first principle (Day-1 invariants vs Day-100 luxury)
- `references/core-principles.md`: quick-reference table for all 10 principles

### Fixed
- Coverage gaps identified in initial distillation
- Trigger words expanded to cover more user query patterns

---

## [v1.0.0] — 2026-04-17

**Initial release**

### Added
- `SKILL.md`: triggers + workflow + quick summary of 10 core principles
- `references/harness-engineering.md`: full distillation of OpenAI Harness Engineering post
- Core coverage: context management, architecture constraints, observability, tech debt, merge strategy, human role, tech selection
