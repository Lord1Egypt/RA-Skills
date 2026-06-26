# Share This Skill

## Package

```bash
python3 /root/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /root/.openclaw/workspace/skills/public/quarkpan-backup-suite \
  /root/.openclaw/workspace/dist
```

Output example:
- `/root/.openclaw/workspace/dist/quarkpan-backup-suite.skill`

## Publish

Choose one:
- Send the `.skill` file directly to another OpenClaw user.
- Publish to ClawHub using `clawhub` CLI (if configured in your environment).

## Notes

- Remove any local secrets before sharing.
- Keep skill generic; avoid hardcoded private IDs/emails.
