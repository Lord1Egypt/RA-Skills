# SCOUTS-AI Search — OpenClaw Skill

Standalone OpenClaw skill that teaches an agent to search the public web
through the public [SCOUTS-AI](https://scouts-ai.com/) `/api/search` HTTP
endpoint via `curl`. No API key, no plugin, no runtime.

The skill is a single `SKILL.md` plus this README, a vendored `LICENSE`, and
a `scripts/` folder (offline validation + smoke test). It follows the
[AgentSkills](https://agentskills.io) spec used by OpenClaw (and other
agents) and the [ClawHub skill format](https://docs.openclaw.ai/clawhub/skill-format).

## Install (local checkout)

```bash
openclaw skills install ./scouts-ai-openclaw-skill --as scouts-ai-search
openclaw skills list
```

Start a new session so the agent sees the refreshed skill list:

```text
/new
```

## Install (ClawHub, once published)

```bash
openclaw skills install scouts-ai-search
```

## What the agent does

When a task needs fresh web context, the agent should:

1. Rewrite the question as a short, specific `q` (1–512 chars).
2. Call SCOUTS-AI. Always capture the HTTP status and headers so rate
   limits and upstream errors can be handled correctly — see `SKILL.md` for
   the full pattern (`mktemp -d`, `umask 077`, `curl -D`, `curl -w '%{http_code}'`,
   `trap … rm -rf` cleanup).
3. Cite the most authoritative results and surface `url` for every factual
   claim. `publishedAt` and `engine` are shown when they help the user judge
   recency or source.

Full rules live in `SKILL.md`.

## Requirements

- `curl` on `PATH` inside the host where the agent's `exec` tool runs.
- The host's `exec` policy must allow HTTPS calls to
  `https://scouts-ai.com/api/search`.
- No API key, no env vars, no other binaries.

## Local validation

```bash
bash scripts/validate.sh
```

Checks SKILL.md frontmatter, that every bash block using the API captures
`-w '%{http_code}'` and uses `mktemp -d`, and that LICENSE/README are
MIT-0 aligned. The script also runs `scripts/smoke.sh`, which boots a
local `python3 -m http.server` on a free port to exercise the curl
pattern (headers, body, status, `mktemp -d` cleanup) end-to-end. No
external network calls.

## Files

| File                  | Purpose                                                         |
| --------------------- | --------------------------------------------------------------- |
| `SKILL.md`            | Required frontmatter + agent instructions.                      |
| `README.md`           | This file — install, usage, publishing notes.                   |
| `LICENSE`             | MIT-0 notice (informational; ClawHub publishes under MIT-0).   |
| `.clawhubignore`      | Excludes the README, scripts, and dotfiles from `clawhub skill publish`. |
| `scripts/validate.sh` | Local sanity check: frontmatter, curl patterns, license.        |
| `scripts/smoke.sh`    | Local smoke test of the curl pattern against an offline server. |

## Publish to ClawHub

```bash
clawhub login
clawhub skill publish ./scouts-ai-openclaw-skill \
  --slug scouts-ai-search \
  --name "SCOUTS-AI Search" \
  --version 0.1.0 \
  --owner <your-clawhub-handle>
```

For a catalog repo, prefer `clawhub sync --dry-run --owner <owner>` first,
then `clawhub sync --all --owner <owner>`.

## License

MIT-0 — see [LICENSE](./LICENSE). ClawHub publishes all skills under MIT-0
regardless of any local license file, so the on-disk license is informational
only and must not add conflicting terms.
