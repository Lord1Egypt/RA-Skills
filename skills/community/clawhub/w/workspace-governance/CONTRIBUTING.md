# Contributing

Thanks for your interest in improving `workspace-governance`.

## Principles

- Keep `SKILL.md` as the single source of truth for executable rules.
- Keep docs concise and avoid rule duplication across files.
- Prefer safe defaults and explicit confirmation for destructive operations.

## Local Validation

Run all checks before opening a PR:

```bash
make check
```

This runs:

- `scripts/check_skill_contract.sh`
- `scripts/check_docs_sync.sh`
- `scripts/check_adapt_contract.sh`

## Typical Change Flow

1. Update `SKILL.md` first (if rule semantics change).
2. Update `references/` manuals with delta/explanatory changes.
3. Update `SKILL_ADAPT.yaml` examples only if needed.
4. Run `make check`.
5. Open PR with a clear summary of:
   - Why the change is needed
   - What behavior changed
   - Any migration notes

## Pull Request Checklist

- [ ] Rule change is reflected in `SKILL.md`
- [ ] Docs updated and consistent
- [ ] `make check` passes
- [ ] No sensitive data included

## Community Conduct

- Be respectful and specific.
- Prefer actionable feedback with examples.
- For major design proposals, include trade-offs.

## Maintainer

- GitHub: `Mars2003`
