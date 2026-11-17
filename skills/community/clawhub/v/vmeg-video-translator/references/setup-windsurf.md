# VMEG on Windsurf

For **macOS / Windows / Linux** — [Windsurf](https://windsurf.com/).

> MCP entry: search MCP in Windsurf Settings / Cascade — see [Windsurf docs](https://docs.windsurf.com/).

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Prerequisites

- Windsurf with Remote HTTP MCP support
- VMEG account: https://www.vmeg.ai
- Skill `vmeg-media-translation/` (see [install.md](install.md))

---

## Step 1: Install Skill

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a windsurf -y
```

Manual paths (version-dependent):

| Scope | Common path |
|-------|-------------|
| User | `~/.windsurf/skills/` or `~/.codeium/windsurf/skills/` |
| Project | `<project>/.windsurf/skills/` |

Windows: `%USERPROFILE%\.windsurf\skills\`

---

## Step 2: Configure MCP

Add Remote Server in Windsurf MCP / Cascade settings, or edit MCP JSON (path per official docs).

Use OAuth / API Key JSON from [setup-common.md](setup-common.md). OAuth: click **Connect** if supported.

---

## Step 3: Verify

Confirm `vmeg_*` in tool list; test "List VMEG materials".

If OAuth discovery unsupported, use **API Key**. See [oauth.md](oauth.md).
