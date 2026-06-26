# Changelog

All notable changes to this project will be documented in this file.

## v0.1.0 - 2026-04-28

Initial public release.

### Added

- Core governance skill contract in `SKILL.md`
- Project-level adaptation config in `SKILL_ADAPT.yaml`
- Validation scripts:
  - `scripts/check_skill_contract.sh`
  - `scripts/check_docs_sync.sh`
  - `scripts/check_adapt_contract.sh`
- One-command validation via `make check`
- Interoperability capability matrix in `tools/interop-capabilities.yaml`
- Bilingual docs:
  - `README.md`
  - `README.zh-CN.md`
  - `references/Governance-Manual.md`
  - `references/治理手册.zh-CN.md`

### Notes

- `SKILL.md` is the single source of truth for executable governance rules.
- Reference manuals are delta/explanatory docs.
