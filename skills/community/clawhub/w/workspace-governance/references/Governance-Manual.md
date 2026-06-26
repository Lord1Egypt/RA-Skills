# Workspace Governance Manual (Delta)

- Author: Mars
- GitHub: Mars2003
- Date: 2026-04-28

## Positioning

This manual is a supplement to `SKILL.md`, not a duplicate rulebook.  
Executable semantics live in `SKILL.md`; this file focuses on onboarding, operations, and troubleshooting.

## Source-of-Truth Policy

- Single source of truth: `SKILL.md`
- This manual contains only delta content (examples, operations, FAQ)
- In case of conflict, `SKILL.md` wins

## Quick Integration

1. Place `SKILL.md` in your agent-readable skill directory
2. Keep `SKILL_ADAPT.yaml` at project root
3. Run contract validation: `bash scripts/check_skill_contract.sh`
4. Optionally run docs-sync validation: `bash scripts/check_docs_sync.sh`

## Practical File Roles

- `SKILL.md`: executable governance contract
- `SKILL_ADAPT.yaml`: project-level policy parameters
- `scripts/`: automated validation scripts
- `tools/`: interoperability capability maps and tool mappings
- `references/`: explanatory, non-normative docs

## Agent Profile Merge (New)

When a platform profile exists (for example `tools/adapt-profiles/openclaw.yaml`), use base + overlay:

- base: `SKILL_ADAPT.yaml`
- overlay: platform profile

Merge semantics:

- `immutable_dirs`: union (security list only grows)
- `protected_files`: union (protection list only grows)
- `destructive_guard`: override is allowed only if strictness is not reduced

## Common Ops Playbook

### 1) Rule update release

Update `SKILL.md` first, then sync manuals, then run:

```bash
bash scripts/check_skill_contract.sh
bash scripts/check_docs_sync.sh
```

### 2) Preflight for non-interactive jobs

- Confirm `Non-Interactive Safety Policy` exists in `SKILL.md`
- Confirm `ask-user` items cause `blocked` status
- Confirm `SKILL_ADAPT.yaml` is present and parseable

### 3) Missing dependency diagnosis

- Check `tools/interop-capabilities.yaml`
- If user intent requires unavailable capability (for example git/github), return `blocked` with dependency details

## FAQ (Delta)

**Q1: Why not keep a full detailed manual here?**  
To avoid long-term drift between duplicated documents.

**Q2: Where should I fix validation failures first?**  
Start with section headers and mandatory policies in `SKILL.md`, then sync reference docs.

**Q3: Where should Chinese users start?**  
`README.zh-CN.md` first, then `references/治理手册.zh-CN.md`; execution semantics still come from `SKILL.md`.
