# VMEG on QoderWork

For **macOS / Windows / Linux** — QoderWork.

> MCP settings: QoderWork MCP / Connectors UI — see official docs.

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Step 1: Install Skill

### In-app (if available)

Search **vmeg-media-translation** in QoderWork.

### Manual copy

| System | Skill path |
|--------|-----------|
| macOS / Linux | `~/.qoderwork/skills/vmeg-media-translation/` |
| Windows | `%USERPROFILE%\.qoderwork\skills\vmeg-media-translation\` |

Or install via skills.sh:

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -y
```

---

## Step 2: Configure MCP

Add Remote Server in QoderWork MCP settings, URL `https://www.vmeg.ai/api/mcp`.  
OAuth / API Key JSON from [setup-common.md](setup-common.md). Use API Key if OAuth discovery unsupported.

---

## Step 3: Verify

"List VMEG translation tasks" → `vmeg_list_tasks` or `vmeg_list_materials`.
