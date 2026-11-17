# VMEG on Google Antigravity

For **macOS / Windows / Linux** — Google Antigravity IDE.

> MCP settings: Antigravity Agent / MCP config — see official docs.

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Step 1: Install Skill

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a antigravity -y
```

Manual path:

| System | Skill path |
|--------|-----------|
| macOS / Linux | `~/.gemini/antigravity/skills/vmeg-media-translation/` |
| Windows | `%USERPROFILE%\.gemini\antigravity\skills\vmeg-media-translation\` |

---

## Step 2: Configure MCP

Add Remote Server in Antigravity MCP settings; JSON from [setup-common.md](setup-common.md).

---

## Step 3: Verify

Test `vmeg_list_materials` or `vmeg_list_tasks`.
