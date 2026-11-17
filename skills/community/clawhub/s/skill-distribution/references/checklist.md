# Pre-publish checklist

Run `python scripts/check_skill.py <skill-folder>` first; this file explains what it checks and what it cannot.

## Rules every registry shares (Agent Skills spec, agentskills.io)

- The skill is a folder containing `SKILL.md` with YAML frontmatter.
- `name`: 1–64 characters, lowercase letters, digits and hyphens only; no leading, trailing or doubled hyphens; **equal to the folder name**.
- `description`: 1–1024 characters, saying what the skill does and when to use it.
- Optional: `license`, `compatibility` (max 500 chars), `metadata` (string keys to string values), `allowed-tools` (experimental).
- Keep `SKILL.md` under 500 lines and roughly 5,000 tokens; put detail in `references/`, code in `scripts/`, templates in `assets/`.
- Reference other files by relative path from the skill root, one level deep.
- Official validator: `skills-ref validate ./my-skill`.

## Extra rules per registry

| Registry | Extra requirement |
|---|---|
| ClawHub | `version` in semver (first release `1.0.0`). Everything published is licensed **MIT-0**, with no per-skill override — do not publish there if the user needs another license. Bundle max 50 MB. Declare runtime needs under `metadata.openclaw` (`requires.env`, `requires.bins`, `primaryEnv`, `install`). |
| skills CLI / skills.sh | Skills must sit where the CLI looks: `skills/<name>/SKILL.md`, optionally with one or two category folders in between, or an agent folder such as `.claude/skills/`. `metadata.internal: true` hides a skill from normal discovery. |
| Claude Code plugin | Plugin `name` in kebab-case and treated as permanent. `claude plugin validate --strict ./plugin` must pass. Either bump `version` on every release or omit it so the commit SHA is used. |
| Codex / ChatGPT | Optional `agents/openai.yaml` inside the skill for display name, icon, brand colour and `allow_implicit_invocation`. |
| claude.ai upload | A zip of the skill folder, max 50 MB (under 10 MB recommended). Code execution must be enabled for the skill to run. |

## Things a script cannot check

- **Does it work from a clean install?** Install from the published source into an empty environment and run one real task.
- **Does the description trigger?** Try three prompts a real user would type without naming the skill.
- **Secrets.** Search the folder for keys, tokens, internal URLs and personal paths before the first push; git history is public too.
- **Rights.** The user must own or be allowed to redistribute everything bundled, including scripts, fonts and reference text.
- **Security scan triggers.** Instructions to pipe remote scripts into a shell, read credential files, disable safety checks or ignore the user get skills flagged or delisted on ClawHub, agentskill.sh, skills.sh and the Hermes hub.
