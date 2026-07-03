# Geordi

Geordi is a builder workflow: an installable mission runner for goals, PRD stories, runtime execution across Codex/Droid/Cursor/Claude Code, separate verification, and receipts.

It merges the reusable build-pipeline discipline with a small CLI under the short `geordi` name.

## One-line install

```bash
GEORDI_TARBALL_URL=https://codeload.github.com/OWNER/REPO/tar.gz/refs/tags/v1.2.0 \
  bash <(curl -fsSL https://raw.githubusercontent.com/OWNER/REPO/v1.2.0/geordi/install.sh)
```

## Local install from clone

```bash
git clone https://github.com/OWNER/REPO.git /tmp/geordi-source
bash /tmp/geordi-source/geordi/install.sh
```

## What gets installed

- `~/.geordi/` — the skill bundle and helper scripts.
- `~/.local/bin/geordi` — command wrapper.

No secrets are installed. No shell profile is modified unless `~/.local/bin` is missing from `PATH`; in that case the installer prints the line to add.

On Windows, use WSL or Git Bash for the installer and tarball extraction. PowerShell users can manually download the release archive, then run `install.sh` from inside the extracted `geordi` directory.

## First run

```bash
cd /path/to/git/repo
geordi init --goal "Ship the smallest useful version of X" --mode codex
geordi mission add "Implement the core path" --accept "npm test"
geordi run --mode codex
geordi status
```

## Runtime options

### Codex

Requires `codex` on `PATH`.

```bash
geordi run --mode codex
```

Optional:

```bash
geordi run --mode codex --model "gpt-5"
GEORDI_CODEX_ARGS="exec --full-auto" geordi run --mode codex --model "gpt-5"
```

### Droid

Requires `droid` on `PATH`.

```bash
geordi run --mode droid --model "custom:Your-Model-0"
```

Optional:

```bash
GEORDI_DROID_AUTO=low geordi run --mode droid --model "custom:Your-Model-0"
```

### Cursor

Requires `cursor-agent` on `PATH`. Install from the Cursor docs if it is missing.

```bash
geordi run --mode cursor --model "gpt-5"
```

Optional:

```bash
GEORDI_CURSOR_ARGS="-p --trust --output-format stream-json" geordi run --mode cursor
```

If `cursor-agent` exists but fails before the prompt runs, unlock the OS credential store or refresh Cursor Agent login interactively, then retry.

### Claude Code

Requires `claude` on `PATH`.

```bash
geordi run --mode claude --model "sonnet"
```

Optional:

```bash
GEORDI_CLAUDE_ARGS="-p --permission-mode bypassPermissions --output-format text" geordi run --mode claude
```

## Design

Geordi is deliberately thin:

1. Store the goal.
2. Store missions as JSONL.
3. Load project context.
4. Build a mission prompt.
5. Run Codex, Droid, Cursor, or Claude Code.
6. Run acceptance checks separately.
7. Save logs and git receipts.

That is enough structure to prevent agent work from turning into interpretive dance.
