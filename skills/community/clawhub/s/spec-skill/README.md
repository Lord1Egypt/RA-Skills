# Spec

Boring but very effective.

A spec skill for coding agents. Requirements, design, tasks. Risk-tiered
approval gates, a decision ledger that survives compaction, and a validator
that treats "the hashes still match" as a check, not a claim.

Copy the folder into a repo and invoke `/spec` (Claude Code) or `$spec` (Codex).
The method is project-agnostic. What counts as dangerous, how you deploy, and
which reviewers fire live in *your* `AGENTS.md`, not here.

## Install

Drop this directory in one of:

| Agent         | Path                   |
| ------------- | ---------------------- |
| Claude Code   | `.claude/skills/spec/` |
| Codex, Cursor | `.agents/skills/spec/` |
| Cursor (alt)  | `.cursor/skills/spec/` |

Keep the folder name `spec`: the frontmatter `name: spec` has to match. One
checkout can serve Claude Code and Codex at once with a symlink from
`.agents/skills/spec` to `.claude/skills/spec`.

The skill runs only when you ask for it, and two flags keep it that way:
`disable-model-invocation: true` in `SKILL.md` for Claude Code,
`policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex.
Both stay set. Without them an ordinary "fix this" becomes three stopped turns
because a diff touched four files.

Then add a short overlay to `AGENTS.md` (or a file it names) so the agent knows
*your* risk surfaces. Without one it still runs, but tier 3 is a guess:

```markdown
### Specs under `docs/plans/`

The method lives in the spec skill. Read it before creating or amending a spec
dir. Overlay for this repo:

- **Tier 3** (three gates): billing, checkout, access control, entitlements,
  refunds, payment webhooks, schema migrations, production writes.
- **Deploy:** merging does not ship the API. Name the apply step in `design.md`.
  Archive only after that step has run (`closure: deployed` or `verified`).
- **Verify:** a `npm run` command must exist in `package.json`, or name a CI
  job that does.
- **Hard stops:** never push without confirmation; never mutate production
  data or secrets; never restart a shared local service.
- **At closure:** run whatever specialist review this repo defines for the
  surfaces you touched.
```

## Layout the skill writes

```
docs/plans/<YYYY-MM-DD>-<slug>/
  requirements.md
  design.md          # skipped for `quick` specs
  tasks.md
  .spec-state.json   # ledger + hash-pinned approval receipts
```

## Validator

Run from the repo root, before every gate and before execution:

```bash
node .claude/skills/spec/scripts/check-spec.mjs docs/plans/<date>-<slug>
```

Adjust the skill path if you installed it somewhere else. Exit 1 means fix it.

It checks, because by-hand versions of these rot into a claim:

- SHA-256 receipts, and the downstream cascade when an upstream file moves
- criteria nothing implements, and citations pointing at criteria that do not exist
- a `Verify:` line per task, and that `npm run X` names a real script
- every `SHALL CONTINUE TO` names a test that exists or that some task creates

## Built at Preuve

This skill runs every gated change at [preuve.ai](https://preuve.ai), a
startup viability analyzer: a founder submits an idea, Preuve scans it against
live sources and returns a report with a verdict.

The same analysis is one tool call away inside your agent through the
[Preuve MCP server](https://preuve.ai/mcp). Add `https://mcp.preuve.ai/mcp` in
claude.ai, Claude Code, Cursor or Codex, sign in with OAuth, and ask it to
check an idea before you build it.

## Origin

Adapted from KiroCrew's Spec Builder
([`kirodotdev/KiroCrew`](https://github.com/kirodotdev/KiroCrew),
`src/kiro_crew/apps/builtins/spec_builder/`). The gates, the ledger, the
file-derived phase and the stable-id trap are from there. The approval receipts,
the risk tiers and the four closure states are not: those came from a review
that found the file-derived phase cannot represent "written but not approved".
