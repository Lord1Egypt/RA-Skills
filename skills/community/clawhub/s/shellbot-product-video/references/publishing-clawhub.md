# Packaging and Publishing (ClawHub)

Use this checklist to package and publish the skill.

## 1) Validate locally

```bash
python3 /Users/cohnen/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

Run from the skill directory.

## 2) Create a release archive

```bash
./scripts/package_skill.sh
```

Output goes to `dist/` in both formats:

- `shellbot-product-video-<timestamp>.tar.gz`
- `shellbot-product-video-<timestamp>.zip`

## 3) Install/verify ClawHub CLI

```bash
npm i -g clawhub
clawhub --version
```

## 4) Log in and publish

```bash
clawhub login
./scripts/publish_clawhub.sh \
  --version 1.0.0 \
  --changelog "Initial public release" \
  --tags latest,remotion,product-video
```

Manual equivalent:

```bash
clawhub publish . \
  --slug shellbot-product-video \
  --name "Shellbot Product Video" \
  --version 1.0.0 \
  --changelog "Initial public release" \
  --tags latest,remotion,product-video
```

## 5) Publish updates

For new releases:

1. Bump `--version` (semver).
2. Update changelog text.
3. Publish again.

ClawHub also supports sync workflows if you keep the skill in a GitHub repo.
