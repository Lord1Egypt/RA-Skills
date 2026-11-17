# VMEG on OpenClaw

For **macOS / Windows / Linux** — [OpenClaw](https://docs.openclaw.ai/) agents via [ClawHub](https://clawhub.ai/).

> **MCP settings**: OpenClaw Control UI `/settings/mcp` (alias `/mcp`), or `openclaw mcp` CLI. See [OpenClaw MCP docs](https://docs.openclaw.ai/cli/mcp).

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Prerequisites

- OpenClaw installed and gateway running
- VMEG account: https://www.vmeg.ai
- This skill installed (see [install.md](install.md))

---

## Step 1: Install Skill

### ClawHub (recommended)

```bash
clawhub install vmeg-media-translation
```

Or:

```bash
openclaw skills install vmeg-media-translation
```

### skills.sh / Vercel CLI

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a open-claw -y
```

### Manual copy

| Scope | Path |
|-------|------|
| User / workspace | `~/.openclaw/skills/vmeg-media-translation/` or `<workspace>/skills/vmeg-media-translation/` |

ClawHub CLI installs to `./skills` under current workdir by default. Restart or reload OpenClaw after install.

---

## Step 2: Configure MCP

OpenClaw MCP config is typically in `~/.openclaw/openclaw.json` (or workspace config).

Add VMEG Remote MCP:

### OAuth

```json
{
  "mcpServers": {
    "vmeg": {
      "url": "https://www.vmeg.ai/api/mcp"
    }
  }
}
```

### API Key

```json
{
  "mcpServers": {
    "vmeg": {
      "url": "https://www.vmeg.ai/api/mcp",
      "headers": {
        "Authorization": "Bearer vmeg_sk_YOUR_KEY"
      }
    }
  }
}
```

In Control UI `/settings/mcp`: OAuth → **Connect** → browser login → **select project**.

---

## Step 3: Verify

Ask "List my VMEG materials" → `vmeg_list_materials`.

Confirm `vmeg` shows connected in `/settings/mcp`.

---

## Troubleshooting (OpenClaw + VMEG)

| Symptom | Fix |
|---------|-----|
| Skill not loaded | Run `openclaw skills list`; reinstall from ClawHub |
| MCP not connected | Check `openclaw.json`; restart gateway |
| OAuth failed | Re-Connect in Control UI; confirm project selected |

More: [oauth.md](oauth.md) · [tools.md](tools.md)
