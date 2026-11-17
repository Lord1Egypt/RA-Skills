# Install VMEG Media Translation Skill

Pick **one** channel. After install, the skill folder name is **`vmeg-media-translation/`** (from `SKILL.md` `name`).

Source: [Pixripple/vmeg-skills](https://github.com/Pixripple/vmeg-skills) → `vmeg-media-translation/`

---

## skills.sh / Vercel CLI — recommended (IDE agents)

Works with Cursor, Claude Code, Codex, Gemini CLI, Windsurf, and 40+ agents.

```bash
npx skills add Pixripple/vmeg-skills --list
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -y
```

Per-agent examples:

```bash
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a cursor -y
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a claude-code -y
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a codex -y
npx skills add Pixripple/vmeg-skills --skill vmeg-media-translation -g -a gemini-cli -y
```

Discover more skills: [skills.sh](https://skills.sh/)

---

## SkillsMP — discovery only

[skillsmp.com](https://skillsmp.com/) indexes skills from GitHub automatically. **No separate publish step.**

Search for `vmeg-media-translation` or `Pixripple/vmeg-skills`, then install with `npx skills add` (above).

---

## GitHub CLI

```bash
gh skill install Pixripple/vmeg-skills vmeg-media-translation --agent cursor --scope user
gh skill install Pixripple/vmeg-skills vmeg-media-translation --agent claude-code --scope user
```

Pin a version: append `@v1.0.0` to the skill name.

---

## ClawHub — OpenClaw ecosystem

Install from the registry (after the maintainer has published):

```bash
clawhub install vmeg-media-translation
```

Or with OpenClaw native commands:

```bash
openclaw skills install vmeg-media-translation
```

Registry: [clawhub.ai](https://clawhub.ai/) · Setup: [setup-openclaw.md](setup-openclaw.md)

---

## LobeHub — marketplace

```bash
npx -y @lobehub/market-cli skills install pixripple-vmeg-skills-vmeg-media-translation -g
```

Per-agent:

```bash
npx -y @lobehub/market-cli skills install pixripple-vmeg-skills-vmeg-media-translation --agent cursor -g
npx -y @lobehub/market-cli skills install pixripple-vmeg-skills-vmeg-media-translation --agent open-claw -g
npx -y @lobehub/market-cli skills install pixripple-vmeg-skills-vmeg-media-translation --agent claude-code -g
```

Marketplace: [lobehub.com/skills](https://lobehub.com/skills)

> Identifier may differ until listed on LobeHub. Check the skill page for the exact install command.

---

## Manual copy

Copy the entire `vmeg-media-translation/` folder (must include `SKILL.md`) to your agent's skills directory:

| Agent | User scope (recommended) |
|-------|--------------------------|
| Cursor | `~/.cursor/skills/vmeg-media-translation/` |
| Claude Code | `~/.claude/skills/vmeg-media-translation/` |
| Codex | `~/.codex/skills/vmeg-media-translation/` |
| Gemini CLI | `~/.gemini/skills/vmeg-media-translation/` |
| Windsurf | `~/.windsurf/skills/vmeg-media-translation/` |
| OpenClaw | `~/.openclaw/skills/vmeg-media-translation/` |

Windows: replace `~` with `%USERPROFILE%`.

Restart the agent client after copying.

---

## After install

1. Configure VMEG Remote MCP — see [setup-common.md](setup-common.md) and your platform's [setup-*.md](setup-cursor.md)
2. Connect OAuth or set API Key — [oauth.md](oauth.md)
3. Verify: ask the agent to "List my VMEG materials"
