# openclaw-quire-skill

An [OpenClaw](https://openclaw.dev) skill that lets chat agents read tasks,
projects, and task trees from [Quire](https://quire.io) — and update
existing tasks — by shelling out to the
[`quire`](https://github.com/quire-io/quire-cli) CLI.

v0.3 adds six gap-filler tools — four reads (`list_subtasks`,
`list_task_comments`, `list_statuses`, `list_tags`) and two writes
(`set_task_dates`, `uncomplete_task`) — bringing the curated surface to
13 reads and 6 writes. Heavier writes (delete, attach, move/transfer,
comment edit, approval workflows) stay deferred; full CLI coverage is
the future `quire mcp` server's job, not this skill's.

## Install

```bash
openclaw skills install quire
```

View on ClawHub: [clawhub.ai/quire/quire](https://clawhub.ai/quire/quire)

## Prerequisites

- [`quire` CLI](https://github.com/quire-io/quire-cli) on `$PATH`.
- One-time auth: run `quire login` in a terminal — it opens a browser for
  OAuth. After that, every host using the skill reuses the same token store.

The skill declares `quire` in `requires.bins`, so OpenClaw will refuse to
load it until the binary is present.

No environment variables, no API keys to paste.

## What the skill exposes

Nineteen tools (thirteen reads, six writes), all backed by
`quire <command> --json`:

| Tool | Wraps | Kind |
|---|---|---|
| `whoami` | `quire whoami` | read |
| `list_my_tasks` | `quire mine` | read |
| `list_project_tasks` | `quire task list` | read |
| `get_task` | `quire task get` | read |
| `list_subtasks` | `quire task subtasks` | read |
| `get_task_tree` | `quire task tree` | read |
| `search_tasks` | `quire task search` | read |
| `list_task_comments` | `quire comment list` | read |
| `list_projects` | `quire project list` | read |
| `get_project` | `quire project get` | read |
| `list_statuses` | `quire status list` | read |
| `list_tags` | `quire tag list` | read |
| `resolve_url` | `quire resolve` | read |
| `create_task` | `quire task create` | **write** |
| `update_task` | `quire task update` | **write** |
| `set_task_dates` | `quire task dates` | **write** |
| `complete_task` | `quire task complete` | **write** |
| `uncomplete_task` | `quire task uncomplete` | **write** |
| `add_comment` | `quire comment add` | **write** |

See [`SKILL.md`](SKILL.md) for the full manifest the model reads at install
time — including when-to-use guidance, common pitfalls, and example prompts.

## Why a skill and not a hosted integration?

Because `quire-cli` already exists, already handles auth, and already speaks
JSON. The skill is ~one Markdown file telling the model which command to
run for which question. There is nothing to host, nothing to scale, nothing
to keep secret.

The strategic plan is for `quire-cli` itself to expose an MCP server in a
future version (`quire mcp`). When that lands, this skill stays useful for
OpenClaw-specific contexts but new MCP-aware clients can talk to Quire
directly.

## Development

The skill is plain Markdown — no build step, no tests beyond manifest
validation. CI runs the validator on every PR (see
[`.github/workflows/validate.yml`](.github/workflows/validate.yml)); run
it locally with:

```bash
bash .github/scripts/validate.sh
```

The validator parses every `quire ...` invocation out of SKILL.md's bash
code fences and asserts each one resolves against the installed CLI's
`--help` output. If you add a new tool section, the CI catches it
automatically — no separate manifest to keep in sync.

Publishing to ClawHub (requires `clawhub login` first):

```bash
clawhub skill publish . --slug quire --owner quire --version <semver>
```

Bump `<semver>` for each release — the registry rejects republishing an
existing version. Add `--changelog "..."` to annotate the release; the
narrative changelog lives in [`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT-0](LICENSE) — no attribution required.
