# Contributing

Thanks for your interest in improving `sticker-manager`.

## Development setup

```bash
python3 -m pip install -r requirements.txt
make install-hooks
python3 -m pytest -q
```

## Contribution guidelines

- Keep the project generic and public-safe
- Avoid hardcoding personal chat IDs, private paths, or secrets
- Add or update tests for behavior changes
- Prefer environment-variable-based configuration over local-machine assumptions
- Keep bilingual user-facing messages consistent across Chinese and English
- When adding semantic or vision workflows, provide graceful fallback behavior

## Pull request checklist

- [ ] Tests pass locally
- [ ] Documentation updated when behavior changes
- [ ] No secrets, tokens, or personal identifiers added
- [ ] New public APIs/CLI flags documented in README or SKILL.md

## Local safety hooks

This repository uses `.githooks/` as the git hooks path.

Install them once per clone:

```bash
make install-hooks
```

Before every commit/push, it runs:
- `python3 scripts/check_sensitive.py`
- `python3 -m pytest -q`

If sensitive-looking content is found, the operation should fail fast.
