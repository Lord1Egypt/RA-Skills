# Publish viralnote-skill to ClawHub

ClawHub is OpenClaw's public skill registry (https://clawhub.ai). Publishing makes the skill discoverable via `clawhub search viralnote` and installable with `clawhub install @howdy7/viralnote`.

## Prerequisites

- GitHub account at least one week old (ClawHub requirement for publishers)
- This folder contains `SKILL.md` with `name`, `description`, and `homepage` in the frontmatter

## 1. Log in (device flow)

Browser callback login is deprecated. Use device-code auth:

```bash
npm i -g clawhub
clawhub login --device
```

1. CLI prints a one-time code and URL `https://clawhub.ai/cli/device`
2. Open the URL in a browser (signed in to GitHub / ClawHub)
3. Enter the code → **Authorize**
4. Terminal should confirm login

Verify:

```bash
clawhub whoami
```

**If device approve fails:** create a token in the ClawHub web UI and run `clawhub login --token clh_...`

## 2. Dry run

From this directory (`tools/viralnote-skill` in vndash, or the root of `github.com/viralnote/viralnote-skill`):

```bash
clawhub skill publish . --slug viralnote --name "ViralNote" --version 1.0.0 --dry-run
```

Fix any validation errors before publishing.

## 3. Publish

```bash
clawhub skill publish . \
  --slug viralnote \
  --name "ViralNote" \
  --version 1.0.0 \
  --changelog "Initial ClawHub release: schedule, publish, and manage social posts via the ViralNote REST API."
```

## 4. Verify

```bash
clawhub search viralnote
clawhub inspect @howdy7/viralnote
```

Open https://clawhub.ai and confirm the skill page is public.

## OpenClaw install (for users)

After publish:

```bash
clawhub install @howdy7/viralnote
# or
openclaw skills install @howdy7/viralnote
export VIRALNOTE_API_KEY="vnd_..."
```

For native MCP (15 tools), users should use OpenClaw MCP instead — see https://www.viralnote.app/agents#openclaw

## Updating

Bump `--version` (semver) and add `--changelog` on each publish:

```bash
clawhub skill publish . --slug viralnote --name "ViralNote" --version 1.0.1 --changelog "..."
```
