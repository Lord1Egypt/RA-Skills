# `skm` JSON contracts

Read this before parsing stdout or writing a script. Human-mode output is
not a stable API; `--json` is.

## Global rules

- Success: one JSON object on stdout, trailing newline.
- Failure: JSON `{"error":"<anyhow message>"}` on **stderr** when the
  command was invoked with `--json`; otherwise `error: ...` on stderr.
  Exit code 1.
- `enable` / `disable` never take `--json`. Their success line is not JSON.
- `fix --yes --json` can print a result object on stdout **and** still
  exit 1 when `failed` is non-empty. Parse stdout, then check the exit
  code (or `failed_count`).
- `doctor --json` always exits 0. Gate on `issues_count`.
- `init --json` always exits 0 on the happy path, including
  `already_initialized: true`.

## `skm init --json`

```json
{
  "already_initialized": false,
  "skills_dir": "/Users/you/.skills-manager/skills",
  "detected_tools": ["claude-code", "codex"],
  "cli_skill": {
    "id": "skills-manager-cli",
    "path": "/Users/you/.skills-manager/skills/skills-manager-cli",
    "enabled_for": ["claude-code", "codex"],
    "failed": []
  }
}
```

`already_initialized: true` still writes/refreshes the companion skill and
enables it for currently active tools — it is not a total no-op. `detected_tools`
is the list of builtin tool ids whose `detected` flag is true in the
loaded config (not a live re-detect of every tool). `cli_skill.failed` lists
tools that could not be linked; `cli_skill.error` is set only if the hub
copy itself could not be written.

Hard errors (exit 1):

- `config.json` exists, is non-empty, and cannot be parsed. Message tells
  the user to move or fix it.
- Another `skm` holds the init lock.

## `skm list --json`

```json
{
  "skills": [
    {
      "instance_id": "global:ab-testing",
      "id": "ab-testing",
      "name": "AB Testing",
      "scope": "global",
      "enabled_for": ["claude-code", "codex"],
      "link_issues": 0
    }
  ]
}
```

- `scope` is `"global"` or `"project"`. Project rows only appear for the
  **active** project binding.
- `enabled_for` is the subset of **active** tools (enabled + detected)
  that currently have a valid link. `--tool <id>` restricts both
  `enabled_for` and `link_issues` to that one tool.
- `link_issues` counts enabled-but-not-`Valid` links for the selected
  tools. Zero does not mean doctor is clean for disabled skills.
- Empty hub: `{"skills":[]}` in JSON; human mode prints
  `no skills found in the configured skills directory`.

## `skm doctor --json`

```json
{
  "config_initialized": true,
  "tools": [
    {
      "id": "claude-code",
      "name": "Claude Code",
      "detected": true,
      "enabled": true
    }
  ],
  "issues_count": 1,
  "issues": [
    {
      "skill": "global:ab-testing",
      "skill_id": "ab-testing",
      "tool": "claude-code",
      "expected": "enabled",
      "status": "Broken"
    }
  ]
}
```

- `tools` includes builtins and custom tools from config, including ones
  that are not detected.
- `status` is `Debug` of `LinkStatus`: `Valid`, `Broken`, `WrongTarget`,
  `NotALink`, `Missing`.
- `issues` is only the rows `should_report_sync_issue` would flag.
  Notably **not** reported: disabled + `Missing`, disabled +
  `WrongTarget`, disabled + `NotALink` (a real directory we did not
  create — never auto-deleted).

## `skm fix --json`

Without `--yes` (report only):

```json
{
  "applied": false,
  "issues_found": 2,
  "hint": "re-run with --yes to apply fixes"
}
```

With `--yes` and nothing to do:

```json
{
  "fixed": [],
  "failed": [],
  "issues_found": 0,
  "failed_count": 0
}
```

With `--yes` after applying:

```json
{
  "applied": true,
  "fixed": [
    {
      "skill": "global:ab-testing",
      "tool": "claude-code",
      "message": "Enabled successfully"
    }
  ],
  "failed": [
    {
      "skill": "global:other",
      "tool": "codex",
      "message": "..."
    }
  ],
  "issues_found": 2,
  "failed_count": 1
}
```

Do not read `issues_count` here — that key is doctor's "problems
detected". On `fix`, use `issues_found` and `failed_count`. Non-empty
`failed` → exit 1, plus `{"error":"N fix(es) could not be applied"}` on
stderr.

## `skm adopt --json`

Only emitted on the apply path (`--yes`, or `--json` without `--dry-run`).
`--dry-run` never prints this object.

```json
{
  "adopted": ["legacy-a"],
  "skipped": [
    {
      "path": "/Users/you/.claude/skills/legacy-b",
      "reason": "'legacy-b' is already in the hub — left in place"
    }
  ]
}
```

No candidates: `{"adopted":[],"skipped":[]}`.

`--json` without `--yes` still applies (the confirmation prompt is
skipped). Always pass `--yes` when applying so the command line records
intent.

## `skm enable` / `skm disable`

No JSON. Success:

```
enabled 'ab-testing' for 'claude-code'
disabled 'ab-testing' for 'claude-code'
```

Typical stderr errors:

- `Skills Manager is not initialized yet.`
- `skill not found: '…'\nrun 'skm list' to see available skills`
- `ambiguous skill reference '…', matches multiple skills:`
- `tool not found: '…'\nrun 'skm doctor' to see detected tools`
- `ambiguous tool reference '…', matches multiple tools:`
- `Tool is disabled: <id>`
- `Cannot disable a project Skill stored directly in the tool directory: …`
- `another skm process is modifying the config; try again later`

## Dry-run / apply matrix (`adopt`, `fix`)

| Command | Mutates? | JSON on stdout? |
| --- | --- | --- |
| `adopt --dry-run` | no | no (human candidate list, or "nothing to adopt") |
| `adopt --json --dry-run` | no | **no** if candidates exist (prints the list only in human mode, then returns). Empty-candidate case still prints `{"adopted":[],"skipped":[]}` because that branch runs before `--dry-run`. |
| `adopt --yes --json` | yes | yes |
| `adopt --json` (no `--yes`) | **yes** (prompt skipped) | yes |
| `fix` / `fix --json` | no | yes if `--json` (`applied: false`) |
| `fix --yes --json` | yes | yes |

## Resolution

Skill lookup (`enable` / `disable`):

1. Exact `instance_id` (`global:ab-testing`, `project:<pid>:ab-testing`).
2. Unique `id` prefix against scanned scoped skills (global + active project).
3. Zero matches → not found. Two or more → ambiguous, lists `id`s.

Tool lookup:

1. Exact id against `config.collect_tool_configs()` (builtins + custom).
2. Unique prefix. Exact match wins, so `trae` is Trae even though
   `trae-cn` shares the prefix.

## Concurrency

Write commands lock `~/.skills-manager/config.json` with
`try_lock_exclusive` (fail fast). Read-only `list`, `doctor`, and `fix`
without `--yes` take no lock. The GUI does not participate — last writer
wins against the app.
