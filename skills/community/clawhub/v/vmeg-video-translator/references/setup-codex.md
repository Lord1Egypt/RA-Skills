# VMEG on Codex

For **macOS / Windows / Linux** — OpenAI Codex CLI / Agent environment.

> MCP config location: follow **Codex official docs**.

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Step 1: Install Skill

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a codex -y
```

Manual path:

| System | Skill path |
|--------|-----------|
| macOS / Linux | `~/.codex/skills/vmeg-media-translation/` |
| Windows | `%USERPROFILE%\.codex\skills\vmeg-media-translation\` |

---

## Step 2: Configure MCP

Edit MCP JSON per Codex docs; content from [setup-common.md](setup-common.md).

---

## Step 3: Verify

"List VMEG materials" → `vmeg_list_materials`.
