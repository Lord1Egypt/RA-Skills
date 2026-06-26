# Publishing to ClawHub

## Prerequisites

1. **ClawHub CLI** — `npm install -g clawhub`
2. **ClawHub account** — Sign up at [clawhub.ai](https://clawhub.ai)
3. **GitHub account** — Must be at least 1 week old to publish

## Publish Steps

### 1. Authenticate

```bash
clawhub login
clawhub whoami   # verify
```

### 2. Prepare Bundle (exclude .git)

ClawHub may fail if `.git` is present. Copy to a clean directory:

```bash
rsync -av --exclude=.git --exclude=node_modules \
  packages/clawhub-tolstoy-skill/ /tmp/tolstoy-mcp-skill/
```

### 3. Publish

```bash
clawhub publish /tmp/tolstoy-mcp-skill \
  --slug tolstoy-mcp \
  --name "Tolstoy MCP" \
  --version 1.0.0 \
  --changelog "Initial release - connect OpenClaw to Tolstoy's video commerce platform"
```

### 4. Known Issues

- **CLI v0.7.0** — May fail with `acceptLicenseTerms invalid value`. Try a newer CLI version or check [clawhub#660](https://github.com/openclaw/clawhub/issues/660).
- **SKILL.md required** — Ensure SKILL.md is in the root of the published directory.

## What Gets Published

The skill bundle includes:
- `SKILL.md` — AI instructions and setup (automatic + manual options)
- `setup.js` — One-command config: `node setup.js` adds Tolstoy MCP to openclaw.json
- `claw.json`, `clawhub.json`, `README.md`

## Version Updates

For subsequent releases, bump version in `claw.json`, `clawhub.json`, and `package.json`, then:

```bash
clawhub publish /tmp/tolstoy-mcp-skill \
  --slug tolstoy-mcp \
  --name "Tolstoy MCP" \
  --version 1.1.0 \
  --changelog "Describe changes"
```
