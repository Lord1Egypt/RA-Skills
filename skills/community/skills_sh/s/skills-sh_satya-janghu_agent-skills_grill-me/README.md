# grill-me

A relentless interviewer skill for any AI coding assistant that supports the [open agent skills](https://github.com/vercel-labs/skills) format — Claude Code, Cursor, Codex, OpenCode, Continue, Windsurf, and 40+ others.

`/grill-me` does not hunt for bugs. It expands your understanding of what you actually want by surfacing intent, constraints, hidden assumptions, and unstated alternatives — across coding, marketing, personal branding, SOPs, systems thinking, process design, and tough business decisions.

## Install

```bash
# Project-local install (default) — committed with your project
npx skills@latest add satya-janghu/agent-skills/skills/grill-me

# Global install — available across all your projects
npx skills@latest add satya-janghu/agent-skills/skills/grill-me -g

# Non-interactive, Claude Code only, global
npx skills@latest add satya-janghu/agent-skills/skills/grill-me -g -a claude-code -y
```

The `skills` CLI prompts you for which AI agent to install for (Claude Code, Cursor, Codex, etc.) and whether to install project-locally or user-globally.

If you don't want to use the CLI, see [Manual install](#manual-install) below.

## Usage

Inside any AI agent that supports skills:

```
/grill-me <what you want grilled on>
```

Or trigger by phrase: "grill me on…", "interview me about…", "pressure-test this…", "help me think through…".

The skill ends when the next concrete action becomes possible (writing code, drafting a brief, editing an SOP, making a commit). Before that action, it writes a distilled session log to `<cwd>/.grill/<slug>.md`.

## What makes it different

Most AI assistants ask too few questions and declare "I have enough to start" too early. `grill-me` is engineered to fight that:

- **One question at a time, with a recommended answer attached** — gives you something to react to instead of a blank prompt.
- **Drills the last answer before moving sideways** — the depth comes from following one thread to the bottom, not from breadth.
- **Pulls from a menu of lenses** without naming them — first-principles, pre-mortem, steelman, reversibility, five-whys, audience, hidden-assumption excavation, second-best, sustainability, plus established mental-model frames (Naval permissionless leverage, Thiel "what do you believe…", Hormozi value equation, Christensen JTBD, Munger inversion, Bezos regret minimization). The conversation feels natural; the structure is hidden.
- **Pushes back on vague answers, deflections, and contradictions** rather than accepting fog.
- **Strawmans half-answers by default** — easier to disagree with a draft than invent from blank.
- **Adapts the lens to the domain** (coding vs. marketing vs. SOPs vs. business decisions), but does not bug-hunt. The goal is expanding the user's understanding of what they want, not finding flaws in execution.
- **Writes a session log to `<cwd>/.grill/<slug>.md`** — Intent, Constraints, Key decisions, Surfaced assumptions, Open questions, Out of scope. The log is the distilled output, not a transcript.

See [SKILL.md](SKILL.md) for the full instruction set.

## Manual install

If you prefer not to use the `skills` CLI, drop `SKILL.md` directly into the right location for your agent:

| Agent | Location |
|---|---|
| Claude Code (global) | `~/.claude/skills/grill-me/SKILL.md` |
| Claude Code (project) | `<project>/.claude/skills/grill-me/SKILL.md` |
| Cursor | `<project>/.cursor/skills/grill-me/SKILL.md` |
| Codex | `<project>/.codex/skills/grill-me/SKILL.md` |

A one-liner using `curl`:

```bash
mkdir -p ~/.claude/skills/grill-me && \
  curl -fsSL https://raw.githubusercontent.com/satya-janghu/agent-skills/main/skills/grill-me/SKILL.md \
  -o ~/.claude/skills/grill-me/SKILL.md
```

## License

MIT — see [LICENSE](../../LICENSE).
