# Release Channel

## Author release flow

1. Bump `metadata.version` in `SKILL.md`.
2. Package skill:

```bash
python3 /Users/raymond/.codex/skills/fs-skill-creator/scripts/package_skill.py /path/to/weex-trader-skill ./dist
```

3. Create GitHub Release with tag like `v1.1.0`.
4. Upload `weex-trader-skill.skill` as release asset.

Agent client update behavior is handled outside this skill. This repository no longer ships a dedicated update script.
