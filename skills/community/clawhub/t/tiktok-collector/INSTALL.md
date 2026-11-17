# Installing tiktok-collector

## The fast way (recommended)

Open your AI client and send this in the chat:

> 💬 Install the tiktok-collector skill from https://github.com/monsterget-com/skills

The AI agent will clone, install, and configure itself. If it asks you to confirm anything, say yes.

## What the AI does (for your verification)

1. `git clone` this repository
2. Copies `tiktok-collector/` → `~/.monsterget/skill/`
3. Adds a one-line pointer to your client's custom instructions/rules file

That's it. The actual scripts stay at `~/.monsterget/skill/scripts/` so all your AI clients share the same runtime.

> **Note**: If you use Claude Code natively, you can also symlink directly:
> `ln -s ~/.monsterget/skill ~/.claude/skills/tiktok-collector`

## Manual install

```bash
# Step 1 — clone and copy the runtime (once, shared by all clients)
git clone https://github.com/monsterget-com/skills /tmp/mgs
mkdir -p ~/.monsterget/skill
cp -r /tmp/mgs/tiktok-collector/. ~/.monsterget/skill/

# Step 2 — point your client at it (pick one)
# Claude Code (native, no pointer needed)
cp -r ~/.monsterget/skill ~/.claude/skills/tiktok-collector

# Codex CLI / Cursor / Zed / Windsurf / Copilot / Aider / Gemini CLI
echo 'For TikTok data, read ~/.monsterget/skill/SKILL.md' >> AGENTS.md

# Cline
echo 'For TikTok data, read ~/.monsterget/skill/SKILL.md' >> .clinerules/

# Roo Code
echo 'For TikTok data, read ~/.monsterget/skill/SKILL.md' >> .roo/rules/tiktok-collector.md

# Kilo Code
echo 'For TikTok data, read ~/.monsterget/skill/SKILL.md' >> .kilocode/rules/tiktok-collector.md

# Any other client — paste the content of ~/.monsterget/skill/SKILL.md into
# your client's custom instructions / rules textarea.
```

## Verify the install

```bash
# Quick check that the SKILL.md and scripts are in place
ls ~/.monsterget/skill/SKILL.md && echo "installed"
```
(No automated checks — the AI will guide you manually.)

## First-time user setup (~2 minutes, done once)

The moment the skill is installed, the AI **guides you** through 3 manual steps (no code checks, you just confirm):

You need 3 things, all in the **same browser** (Edge or Chrome — pick one):

| Step | What to do | URL |
|------|-----------|-----|
| ① | Install the MonsterGet browser extension | [monsterget.com/install](https://monsterget.com/install) |
| ② | Log in to monsterget.com (same browser) | [monsterget.com](https://monsterget.com) |
| ③ | Log in to TikTok (same browser) | [tiktok.com](https://www.tiktok.com) |

Tell the AI which browser you used, say "好了", and the AI saves your choice. **No automatic checks — you confirm manually.** Then the AI offers example prompts — e.g. "抓取关于 'mike tyson' 的 TikTok 视频 50 条".

> 💡 This skill uses **pure manual confirmation** — the AI never scans your disk or opens test windows. You know your browser best. If something fails later, the AI will ask you to check the 3 conditions again — still manually.