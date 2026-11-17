# VMEG on Gemini CLI

For **macOS / Windows / Linux** — [Gemini CLI](https://github.com/google-gemini/gemini-cli).

> **Note:** API Key here means **VMEG** `vmeg_sk_`, not Google Gemini API Key.  
> MCP config location: follow **Gemini CLI official docs**.

Common: [setup-common.md](setup-common.md) · [oauth.md](oauth.md) · Install: [install.md](install.md)

## Step 1: Install Skill

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a gemini-cli -y
```

Manual path:

| System | Skill path |
|--------|-----------|
| macOS / Linux | `~/.gemini/skills/vmeg-media-translation/` |
| Windows | `%USERPROFILE%\.gemini\skills\vmeg-media-translation\` |

---

## Step 2: Configure MCP

Edit MCP config per Gemini CLI docs; JSON from [setup-common.md](setup-common.md).

---

## Step 3: Verify

After connecting MCP, ask "What materials are in VMEG?"
