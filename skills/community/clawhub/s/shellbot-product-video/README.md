# Shellbot Product Video Skill

Conversion-focused product marketing video skill for Remotion + React with AIDA structure and ancillary Freepik asset guidance.

- Skill file: `SKILL.md`
- Team: [ShellBot Team](https://getshell.ai)
- Includes official-style Remotion rule snippet assets at: `references/remotion-rules/assets`

## Quick start

```bash
./scripts/bootstrap_template.sh --list
./scripts/bootstrap_template.sh --template cinematic-product-16x9 --include-rule-assets ./my-product-video
cd ./my-product-video
npm install
npm run start
```

## Package and publish

```bash
python3 /Users/cohnen/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
./scripts/package_skill.sh
./scripts/publish_clawhub.sh --version 1.0.0 --changelog "Initial release" --tags latest,remotion,product-video
```

`./scripts/package_skill.sh` now produces both `.tar.gz` and `.zip` in `dist/`.
