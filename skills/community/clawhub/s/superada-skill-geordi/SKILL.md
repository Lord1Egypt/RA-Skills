---
name: geordi
description: Use when turning a coding goal or PRD into bounded build missions, running those missions through Codex, Droid, Cursor, or Claude Code, verifying outcomes separately, and preserving receipts. Geordi merges the former build-pipeline discipline with the installable mission runner.
version: 1.2.0
author: SuperAda
license: MIT
metadata:
  tags: [agent-workflow, geordi, codex, droid, cursor, claude, build-pipeline, missions, verification]
---

# Geordi

Geordi is the builder workflow for goal-driven coding work. It combines build-pipeline discipline - context first, implementation second, independent verification, retries, and receipts - with an installable CLI that can run bounded missions through Codex, Droid, Cursor Agent, or Claude Code.

The machinery is intentionally plain: define a goal, add missions, run one runtime at a time, verify with real commands, and leave logs behind. Less mysticism. More receipts.

## What Geordi does

- Defines a **goal**: the operator outcome.
- Breaks work into **missions**: bounded implementation units with acceptance checks.
- Loads project context before building.
- Prepends the shared global `AGENTS.md` context before every mission prompt.
- Runs missions through **Codex**, **Droid**, **Cursor**, or **Claude Code**.
- Keeps state in `.geordi/state/` so runs can be resumed or audited.
- Separates implementation from verification.
- Captures receipts: prompts, command logs, verification logs, and git status before/after.

## Install

From the source repo:

```bash
git clone https://github.com/OWNER/REPO.git /tmp/geordi-source
bash /tmp/geordi-source/geordi/install.sh
```

Or one line, pinned to the public release. Set `GEORDI_TARBALL_URL` to the matching source archive so streamed installs can locate the bundle:

```bash
GEORDI_TARBALL_URL=https://codeload.github.com/OWNER/REPO/tar.gz/refs/tags/v1.2.0 \
  bash <(curl -fsSL https://raw.githubusercontent.com/OWNER/REPO/v1.2.0/geordi/install.sh)
```

The installer copies the bundle into `~/.geordi`, creates `~/.local/bin/geordi`, and prints a verification command.

## Quick start

```bash
cd /path/to/repo
geordi init --goal "Ship dark mode settings" --mode codex
geordi mission add "Add settings toggle" --accept "npm test"
geordi run --mode codex
geordi status
```

Pick any of the four supported runtimes. Use `--model MODEL_ID` where the runtime supports it (Codex, Droid, Cursor, Claude).

## Global AGENTS context

Geordi requires a global `AGENTS.md` file by default. This keeps mission runs aligned with the operator's shared agent rules before project-specific context is applied.

Default path:

```bash
~/.agents/AGENTS.md
```

Override when needed:

```bash
GEORDI_AGENTS_FILE=/path/to/AGENTS.md geordi run --mode codex
```

To intentionally run without a global file:

```bash
GEORDI_REQUIRE_AGENTS=0 geordi run --mode codex
```

`geordi doctor` checks the global file unless `GEORDI_REQUIRE_AGENTS=0` is set.

Project-local defaults can live in `.geordi.env`:

```bash
GEORDI_CODEX_ARGS="exec --full-auto"
GEORDI_DROID_AUTO="medium"
GEORDI_CURSOR_ARGS="-p --trust --output-format text"
GEORDI_CLAUDE_ARGS="-p --dangerously-skip-permissions --output-format text"
```

## Mission contract

Each mission should include:

- **Title** - what to change.
- **Acceptance command** - what proves it worked.
- **Scope note** - what not to touch, if relevant.

Example:

```bash
geordi mission add \
  "Add CSV export to reports page" \
  --accept "npm run test:unit -- reports" \
  --scope "Only reports UI and export helper files. Do not modify auth."
```

Good missions are small enough to verify in one command. If a mission needs five unrelated acceptance commands, split it.

## Runtime modes

Geordi dispatches missions to one of four supported runtimes. Pick the one that fits the task and the model you want to use.

### Codex mode

Uses `codex exec` from the current git repository, with optional `--model`.

Good for:

- feature builds
- refactors
- tests and type fixes
- PR review follow-up

Default command shape:

```bash
codex exec --full-auto "<mission prompt>"
```

With `--model`:

```bash
codex exec --full-auto --model "$MODEL" "<mission prompt>"
```

Override with:

```bash
GEORDI_CODEX_ARGS="exec --full-auto" geordi run --mode codex --model "gpt-5"
```

```bash
cd /path/to/repo
geordi init --goal "Ship dark mode settings" --mode codex
geordi mission add "Add settings toggle" --accept "npm test"
geordi run --mode codex --model "gpt-5"
```

### Droid mode

Uses `droid exec` with optional `--model` and `--auto` settings.

Good for:

- BYOK model routing
- custom OpenAI-compatible endpoints
- Droid mission-style coding passes
- UI/code tasks where Droid is already configured

Default command shape:

```bash
droid exec --auto medium --cwd "$PWD" -m "$MODEL" "<mission prompt>"
```

Override with:

```bash
GEORDI_DROID_AUTO=low geordi run --mode droid --model "custom:Your-Model-0"
```

```bash
cd /path/to/repo
geordi init --goal "Fix checkout form validation" --mode droid
geordi mission add "Repair validation and errors" --accept "npm test"
geordi run --mode droid --model "custom:Your-Model-0"
```

### Cursor mode

Uses the `cursor-agent` CLI in headless print mode.

Good for:

- Cursor editor users who want the same agent in a terminal
- repos where Cursor's model routing is already configured
- UI/code tasks where Cursor's editor-aware context is useful

Default command shape:

```bash
cursor-agent -p --trust --output-format text --model "$MODEL" "<mission prompt>"
```

`-p` runs Cursor in headless print mode. `--trust` auto-accepts the workspace trust dialog so the run is non-interactive. `--output-format text` produces a clean text receipt for the log file.

Override with:

```bash
GEORDI_CURSOR_ARGS="-p --trust --output-format stream-json" geordi run --mode cursor --model "gpt-5"
```

```bash
cd /path/to/repo
geordi init --goal "Refactor settings panel into shared component" --mode cursor
geordi mission add "Extract SettingsPanel and add unit tests" --accept "npm test -- settings"
geordi run --mode cursor --model "gpt-5"
```

### Claude Code mode

Uses the `claude` CLI in non-interactive print mode.

Good for:

- Claude-Code-native repos with a `CLAUDE.md` or `.claude/` config
- missions that benefit from Claude's instruction-following and tool use
- sandboxes where you need a self-contained, non-interactive agent

Default command shape:

```bash
claude -p --dangerously-skip-permissions --output-format text --model "$MODEL" "<mission prompt>"
```

`-p` runs Claude in non-interactive print mode. `--dangerously-skip-permissions` is intended for sandboxed/headless runs where the agent should not be blocked on permission prompts. `--output-format text` produces a clean text receipt for the log file.

Override with:

```bash
GEORDI_CLAUDE_ARGS="-p --permission-mode bypassPermissions --output-format text" geordi run --mode claude --model "sonnet"
```

```bash
cd /path/to/repo
geordi init --goal "Add OAuth refresh-token rotation" --mode claude
geordi mission add "Implement refresh-token rotation and tests" --accept "npm test -- auth"
geordi run --mode claude --model "sonnet"
```

### Choosing a mode

| Mode | Best for | Authentication | Model flag |
|------|----------|----------------|------------|
| `codex` | Codex-default flows | Codex login | `--model` |
| `droid` | BYOK / custom endpoints | Droid login | `--model` |
| `cursor` | Cursor editor workflows | Cursor login | `--model` |
| `claude` | Claude Code workflows | Claude login | `--model` |

If a runtime is missing, install it and re-run `geordi doctor`. The CLI does not bundle any of these agents. Cursor can also fail in unattended shells when its OS credential store is locked or no login exists; run a one-time interactive Cursor Agent login, then retry.

## Context-first build loop

The core build-pipeline rule remains: **load context before implementation**.

Before running a non-trivial mission, collect:

1. `AGENTS.md`, `CLAUDE.md`, or other repo agent instructions.
2. Relevant PRD/story/task text.
3. Existing test/build commands.
4. Recent git status and nearby code conventions.
5. Explicit scope exclusions.

The bundled helper scripts can support this pattern:

```bash
~/.geordi/scripts/load-context.sh /path/to/repo
~/.geordi/scripts/update-context.sh /path/to/repo "Added CSV export with unit tests; npm test passes."
```

If those scripts do not match a repo, do the same manually and put the important context directly into the mission title/scope.

## State layout

Inside the target repo:

```text
.geordi/
  goal.md
  missions.jsonl
  state/
    run-YYYYmmdd-HHMMSS/
      mission-001.prompt.md
      mission-001.log
      mission-001.verify.log
      git-before.txt
      git-after.txt
      summary.md
```

## Operator rules

1. Do not run open-ended prompts when a mission can be bounded.
2. Do not count agent completion as success; run the acceptance command.
3. Do not hide failures. Preserve the log and make the next mission smaller.
4. Do not put secrets in missions, prompts, or logs.
5. Read repo instructions before changing code.
6. Commit only after verification passes and scope is reviewed.
7. If verification fails, retry with the exact failure log and a smaller repair mission.

## When to use Geordi

Use Geordi when the work is larger than a single prompt but smaller than a full project-management system:

- Build a feature across a few files.
- Convert a PRD into a sequence of agent missions.
- Run the same mission through Codex, Droid, Cursor, or Claude Code and compare results.
- Keep receipts for agent work without building a control plane.
- Continue the former build-pipeline workflow under the shorter `geordi` name.

Do not use Geordi for:

- one-line edits where a normal direct change is cleaner
- destructive repo rewrites without explicit operator approval
- secrets, credentials, payment flows, or private data entry
- unbounded "go improve the whole codebase" prompts

## Verification

```bash
geordi doctor
```

Checks:

- bundle installed
- target directory is a git repo
- requested runtime exists (`codex`, `droid`, `cursor-agent`, or `claude`; `--mode cursor` checks `cursor-agent`)
- mission file is parseable
- acceptance command is available for each mission

To check a specific runtime:

```bash
geordi doctor --mode codex
geordi doctor --mode cursor
geordi doctor --mode claude
```

## Common pitfalls

1. **Running the agent before reading repo instructions.** Always load context first.
2. **Over-wide missions.** Split broad PRD stories into smaller missions with one acceptance command each.
3. **Treating agent success as real success.** The acceptance command is the proof.
4. **Committing generated dirt.** Review `git status --short` before committing.
5. **Leaking private environment details.** Keep model IDs, internal hosts, private paths, and secrets out of public missions and docs.
6. **Forgetting to install the runtime.** `cursor-agent` is a separate package from the Cursor editor; install it from the Cursor docs before using `--mode cursor`.
7. **Locked Cursor credentials.** If `cursor-agent` exists but fails before the prompt runs, unlock the OS credential store or refresh Cursor Agent login interactively.
8. **Windows shell mismatch.** Use WSL or Git Bash for the installer and tarball extraction; PowerShell needs an equivalent manual download/copy flow.

## Verification checklist

- [ ] `geordi --version` prints the expected version.
- [ ] `geordi doctor` passes inside a git repo.
- [ ] `geordi init` creates `.geordi/goal.md` and `.geordi/missions.jsonl`.
- [ ] `geordi mission add` appends valid JSONL.
- [ ] `geordi run` writes prompt/log/verification receipts.
- [ ] Acceptance command output is preserved in `.geordi/state/*/*.verify.log`.
- [ ] The chosen runtime (`codex`, `droid`, `cursor-agent`, or `claude`) is on `PATH` before `geordi run`.
