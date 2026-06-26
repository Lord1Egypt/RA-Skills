# ClawHub skill bundle

This directory is the ClawHub publish target for talk-normal. It contains a copy of `prompt.md` and `install.sh` from the repo root, plus the `SKILL.md` manifest.

**Do not edit `prompt.md` or `install.sh` in this directory directly.** The source of truth for both is the repo root. This directory holds synced copies that get published to ClawHub.

## Publishing

Before running `clawhub skill publish`, re-sync the copies so they match the repo root:

```bash
bash ../scripts/sync-skill.sh
```

Then publish from the repo root:

```bash
clawhub publish ./skill \
  --slug talk-normal \
  --name "talk-normal" \
  --version 0.3.0 \
  --tags latest \
  --changelog "short description of what changed in this version"
```

After publishing, submit a verification request from the skill's ClawHub dashboard. Review takes 3-5 business days.

## Updating the version

When shipping a new release of the ruleset:

1. Edit `prompt.md` at the repo root and commit as usual.
2. Re-run `bash scripts/sync-skill.sh` so the skill bundle picks up the new `prompt.md`.
3. Bump the `version:` field in `skill/SKILL.md`.
4. Re-publish with `clawhub publish ./skill --slug talk-normal --version X.Y.Z --tags latest --changelog "..."`.
