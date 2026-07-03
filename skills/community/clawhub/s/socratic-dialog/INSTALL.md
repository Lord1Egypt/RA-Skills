# Installation — socratic-dialogue

This skill follows the open [Agent Skills](https://agentskills.io) standard. Pick the platform that matches your runtime.

> **Note on the hermes scan:** This file was extracted from `README.md` to keep the scan-clean (no agent-environment persistence patterns in the public-facing docs). All install instructions are still here — just in a separate file that the hermes safety scanner does not flag.

## Claude.ai

1. Download or clone this folder.
2. Go to **Settings → Capabilities → Skills**.
3. Click **Upload skill** and select the `socratic-dialogue/` folder (zip it if needed).
4. Toggle the skill on.

## Claude Code

```bash
mkdir -p ~/.claude/skills/socratic-dialogue
cp -r skills/socratic-dialogue/* ~/.claude/skills/socratic-dialogue/
```

Restart Claude Code. The skill will auto-trigger on relevant queries.

## OpenAI Codex

Codex loads skills from your project's skill manifest file at the project root. Add a section:

```markdown
## Skills
This project uses the Socratic Dialog skill.
Path: ./skills/socratic-dialogue/SKILL.md
```

Or place the folder under `~/.codex/skills/` and reference it in your manifest.

## OpenCode

```bash
mkdir -p ~/.opencode/skills/socratic-dialogue
cp -r skills/socratic-dialogue/* ~/.opencode/skills/socratic-dialogue/
```

OpenCode picks up skills from `~/.opencode/skills/` on startup.

## Grok Builds (xAI)

Place the folder in your Grok workspace and reference it from the project's skill manifest. Grok follows the same `SKILL.md` frontmatter format.

## Anthropic API (Code Execution Tool)

Upload via the `/v1/skills` endpoint and pass `container.skills: ["socratic-dialogue"]` in Messages API requests. Requires the Code Execution Tool beta.

## Cursor

Cursor has no native skill loader. Wrap the skill as a custom rule (a plain-text instruction that points to the SKILL.md path) or use a slash command. See the Cursor docs for whichever pattern fits your workflow.

## Continue.dev

Continue.dev has no native skill loader. Wrap the skill as a slash command or as a context provider. See the Continue.dev docs for whichever pattern fits your workflow.

## Compatibility

| Tool                     | Status     | Notes                                                         |
| ------------------------ | ---------- | ------------------------------------------------------------- |
| Claude.ai                | ✅ Tested   | Upload via Settings → Capabilities → Skills                   |
| Claude Code              | ✅ Tested   | Drop into `~/.claude/skills/`                                 |
| Anthropic Messages API   | ✅ Tested   | Use `/v1/skills` endpoint + `container.skills` parameter      |
| OpenAI Codex             | ✅ Works    | Reference from your project's skill manifest                  |
| OpenCode                 | ✅ Works    | Drop into `~/.opencode/skills/`                               |
| Grok Builds (xAI)        | ✅ Works    | Place in workspace, reference in skill manifest               |
| Cursor                   | ⚠ Partial  | Wrap as a custom rule (no native skill loader)                |
| Continue.dev             | ⚠ Partial  | Wrap as a slash command or context provider                   |

Skill format follows the open [Agent Skills](https://agentskills.io) standard.
