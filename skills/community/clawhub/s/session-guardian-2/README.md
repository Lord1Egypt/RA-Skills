# session-guardian

**One skill, every agent: stop paying for context you no longer need.**

[中文说明](README.zh-CN.md)

Session Guardian detects natural boundaries in a conversation and produces a compact handoff summary, so each new topic can start in a fresh session instead of dragging unrelated history along.

## Why you want it: it saves money

Every turn re-sends the entire conversation history to the model. As a session accumulates finished, unrelated topics, you keep paying input tokens for history that contributes nothing to the current answer.

- **Dead weight costs every turn.** A wrapped-up topic that stays in the session is paid for again on every subsequent request — for every subsequent topic.
- **A handoff replaces the history.** At a natural boundary, session-guardian writes a handoff of a few hundred tokens that stands in for tens of thousands of tokens of stale conversation.
- **Hand off before compaction.** Around context limits it pushes a handoff at the first safe stopping point, so you don't pay for auto-compaction of mostly-irrelevant history either.
- **Cheaper *and* better.** Fresh sessions mean lower API bills or less plan-quota burn, faster responses, and answers that aren't diluted by unrelated context.

The skill is deliberately conservative: it never splits active work mid-task, never invents token statistics, and stays silent when staying in the same session is the right call. Its recommendations fire only at meaningful events — a completed task, an explicit topic change, a genuinely unrelated follow-up, or reliable context-pressure telemetry.

## What it does

- **Boundary detection** — identifies the "active work unit" and weighs topic relation, history value, work state, and context pressure to decide: continue silently, defer to the next checkpoint, or recommend a new session.
- **Compact handoffs** — produces a copy-ready summary (topic, status, key decisions, files and commands, blockers, next step, and what *not* to carry forward) that lets the next session start productively without the old transcript.
- **Bilingual out of the box** — skill body in English; user-facing recommendations and handoffs are written in the user's language, with built-in phrasings for English and Chinese.
- **Host-safe** — it never creates, closes, or switches sessions itself; it recommends the boundary and hands you the text. Handoffs never transfer automatically.

## Works with

| Agent | Install (global) | Install (per project) | Notes |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/skills/session-guardian/` | `.claude/skills/session-guardian/` | Copy `versions/claude-code/session-guardian/`; auto-triggers or `/session-guardian` |
| Codex CLI | `~/.codex/skills/session-guardian/` | `.codex/skills/session-guardian/` | Copy `versions/codex/session-guardian/`; includes `agents/openai.yaml` UI metadata |
| OpenCode | `~/.config/opencode/skills/session-guardian/` | `.opencode/skills/session-guardian/` | Copy `versions/opencode/skills/session-guardian/`; optional `/session-guardian` command in `versions/opencode/command/` |
| OpenClaw | `~/.agents/skills/session-guardian/` or `~/.openclaw/skills/session-guardian/` | `<workspace>/skills/session-guardian/` | Copy `versions/openclaw/session-guardian/`; visible from the next session (skills are snapshotted at session start) |
| DeepSeek Harness | depends on preset skill roots | `<workspace>/.agents/skills/session-guardian/` | Copy `versions/deepseek-harness/session-guardian/`; the agent's preset must compose the `skill` tool |
| WorkBuddy | per WorkBuddy docs | — | Copy `versions/workbuddy/session-guardian/`; packaged on the standard SKILL.md layout |

OpenCode also reads `~/.claude/skills/` and `~/.agents/skills/`, so the Claude Code and OpenClaw packages work there too.

## Repository layout

The repo root is the canonical, platform-neutral skill (`SKILL.md` + `references/` + `templates/` + `agents/openai.yaml`). `versions/` contains ready-to-install packages per agent — identical bodies, each with a short "Host notes" section for its platform.

```
session-guardian/
├── SKILL.md                                  # canonical skill
├── agents/openai.yaml                        # Codex-style UI metadata
├── references/topic-boundaries.md            # boundary examples & edge cases
├── templates/handoff.md                      # handoff template
└── versions/
    ├── claude-code/session-guardian/
    ├── codex/session-guardian/
    ├── opencode/{skills,command}/...
    ├── openclaw/session-guardian/
    ├── deepseek-harness/session-guardian/
    └── workbuddy/session-guardian/
```

## Platform notes

- All six packages share the standard `SKILL.md` frontmatter (`name`, `description`). Only OpenCode enforces extra rules: `name` must match the folder name and unknown frontmatter fields are ignored.
- **Codex** auto-compacts long conversations; a compaction notice counts as elevated context pressure. `agents/openai.yaml` is display metadata only.
- **OpenClaw** accepts the optional `metadata.openclaw` display block (emoji) shipped in the package; reference the skill with `$session-guardian` or `/session-guardian`.
- **DeepSeek Harness** is a fast-moving developer preview; re-verify install paths against its docs after upgrading.
- **WorkBuddy** has no published skill spec yet. The package follows the standard SKILL.md layout; if its docs specify a different location, just place the folder accordingly — the body needs no changes. Its Host notes also keep output jargon-free for non-developer office users.

## Maintenance

Edit the canonical files at the root, then sync the changed files into `versions/*/session-guardian/` (bodies are identical; only each package's "Host notes" section is platform-specific). Or just ask an agent to regenerate the version packages.

## License

[MIT](LICENSE)
