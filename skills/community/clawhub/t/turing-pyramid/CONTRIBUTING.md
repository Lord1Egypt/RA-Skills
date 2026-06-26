# Contributing to Turing Pyramid

## Branch Strategy

- **main** — stable releases, tagged versions. Protected.
- **develop** — integration branch. All feature branches merge here first.

## Workflow

### 1. Start from develop
```bash
git checkout develop
git pull origin develop
# If develop is behind main:
git merge main --no-edit
```

### 2. Create a feature branch
```bash
git checkout -b feat/short-description   # new feature
git checkout -b fix/short-description    # bug fix
git checkout -b docs/short-description   # documentation
git checkout -b chore/short-description  # maintenance
git checkout -b test/short-description   # test changes
```

### 3. Make changes
- Work in `~/.openclaw/workspace/skills/turing-pyramid/` (live copy)
- Run tests: `WORKSPACE=~/.openclaw/workspace bash tests/run-tests.sh`
- Copy changes to git repo: sync only modified files

### 4. Commit (conventional commits)
```bash
git commit -m "feat: add new scanner for X"
git commit -m "fix: prevent audit.log race condition"
git commit -m "docs: update TUNING.md with new parameters"
git commit -m "chore: bump version to X.Y.Z"
git commit -m "test: add regression test for gate timeout"
```

### 5. Push and create PR
```bash
git push origin feat/short-description
# Create PR: feat/short-description → develop
# Add a maintainer as reviewer
```

### 6. Review → Merge
- Steward reviews the PR
- Fix requested changes or merge
- After merge to develop: test in live environment
- When ready for release: merge develop → main, tag version

## Release Checklist

1. [ ] All tests pass (27+ unit, 4 integration)
2. [ ] Version bumped in `assets/needs-config.json` and `SKILL.md`
3. [ ] CHANGELOG.md updated
4. [ ] No PII in any file (steward/agent/formalization partner only)
5. [ ] PR merged to main, tag created (`git tag vX.Y.Z`)
6. [ ] ClawHub publish (one attempt, ignore timeout)

## File Ownership

| File | Who edits | Committed? |
|---|---|---|
| scripts/*.sh | Both | Yes |
| assets/needs-config.json | Both | Yes (config only) |
| assets/needs-state.json | Agent (runtime) | No (.gitignore) |
| assets/audit.log | Agent (runtime) | No |
| assets/decisions.log | Agent (runtime) | No |
| assets/mindstate-config.json | Agent (local override) | No |
| docs/*.md | Both | Yes |
| tests/**/*.sh | Both | Yes |

## Local Overrides (not committed)

These files intentionally differ between git and local install:
- `assets/mindstate-config.json` — local `allow_kill=true`
- All runtime state files (see `.gitignore`)
