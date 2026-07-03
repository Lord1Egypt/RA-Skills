# Geordi build loop

This is the sanitized public form of the former Geordi build-pipeline workflow.

## Loop

1. Load global agent context first from `~/.agents/AGENTS.md` or `GEORDI_AGENTS_FILE`.
2. Load project context before editing: repo instructions, PRD/story text, tests, current git status, and relevant files.
3. Create one bounded mission with a single acceptance command.
4. Run the mission through one of the supported runtimes: Codex, Droid, Cursor, or Claude Code.
5. Verify separately with the acceptance command.
6. If verification fails, preserve the log and create a smaller repair mission.
7. Commit only after the acceptance command passes and the diff is reviewed.
8. Update project context or notes with what changed and any follow-up risks.

## Runtime selection

| Runtime | Use when | Default invocation |
|---------|----------|-------------------|
| Codex | Default OpenAI-Codex flows, refactors, type fixes | `codex exec --full-auto` |
| Droid | BYOK routing, custom OpenAI-compatible endpoints, Droid-mission flows | `droid exec --auto medium -m <model>` |
| Cursor | Repos where Cursor editor or `cursor-agent` is the primary tool | `cursor-agent -p --trust --output-format text` |
| Claude Code | Repos with `CLAUDE.md`/`.claude/` configs, sandboxes needing a self-contained non-interactive agent | `claude -p --dangerously-skip-permissions --output-format text` |

Pick the runtime before defining the mission so the prompt and acceptance command target the right tool.

## Retry rule

Retry a failed mission at most three times. Each retry should include the exact failure log and a narrower instruction. After three failures, mark it blocked and ask for operator input.

## Receipt rule

Every completed mission should leave:

- mission prompt
- agent output log
- verification log
- git status before and after
- concise summary of files changed
