# ClawHub CLI Reference

Use this file when managing the WhiteBIT skill on `clawhub.ai`.

## Install and Auth
```bash
npm i -g clawhub
clawhub login
clawhub whoami
```

## Discovery and Install
```bash
clawhub search "whitebit"
clawhub install <skill-slug>
clawhub list
```

## Updates
```bash
clawhub update <skill-slug>
clawhub update --all
```

## Publish This Skill
```bash
clawhub publish ./clawhub-whitebit-trading \
  --slug whitebit \
  --name "whitebit" \
  --version 1.0.0 \
  --tags latest
```

## Bulk Backup/Sync
```bash
clawhub sync --dry-run
clawhub sync --all
```

## Useful Global Options
- `--workdir <dir>` set workspace root.
- `--dir <dir>` set skills directory relative to workdir.
- `--no-input` disable interactive prompts.
- `--site <url>` override site URL.
- `--registry <url>` override registry API URL.

## Safety Notes
- Run `clawhub sync --dry-run` before large publish operations.
- Review `SKILL.md` and supporting files before install/update.
- Never publish tokens, API secrets, or local environment files.
