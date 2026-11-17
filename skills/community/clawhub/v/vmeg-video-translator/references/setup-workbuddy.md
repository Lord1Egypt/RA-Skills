# VMEG on WorkBuddy

For **macOS / Windows / Linux** — WorkBuddy.

> MCP settings: WorkBuddy **MCP / Connectors** UI — see official docs.

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Step 1: Install Skill

### In-app (if available)

Search **vmeg-media-translation** in WorkBuddy.

### Manual copy

| System | Skill path |
|--------|-----------|
| macOS / Linux | `~/.workbuddy/skills/vmeg-media-translation/` |
| Windows | `%USERPROFILE%\.workbuddy\skills\vmeg-media-translation\` |

Or via skills.sh:

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -y
```

---

## Step 2: Configure MCP

Add VMEG in WorkBuddy MCP settings; JSON from [setup-common.md](setup-common.md) (OAuth: omit `headers`).

---

## Step 3: Verify

"List VMEG materials" → `vmeg_list_materials`.
