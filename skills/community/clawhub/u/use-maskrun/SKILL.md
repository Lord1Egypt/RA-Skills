---
name: use-maskrun
description: Use maskrun instead of executing shell commands directly when commands may print environment variables, API keys, tokens, passwords, secrets, credentials, CI variables, cloud credentials, .env values, or other sensitive values. Trigger this skill before running terminal commands, test commands, build scripts, curl/API calls, package manager scripts, debugging commands, or agent automation where stdout or stderr might contain secret environment variable values.
---

# Use Maskrun

## Core Rule

Run potentially sensitive commands through `maskrun --` instead of executing them directly.

Use this form:

```bash
maskrun -- <command> [args...]
```

Examples:

```bash
maskrun -- cargo test
maskrun -- npm run build
maskrun -- curl "https://api.example.com?key=${API_KEY}"
maskrun -- sh -c 'echo "$API_KEY"'
maskrun -- echo "$API_KEY"
maskrun -- cat openclaw.json
```

## When To Wrap

Wrap commands when any of these are true:

- The command may print environment variables or configuration values.
- The command touches `.env`, credentials, tokens, API keys, cloud config, CI config, auth headers, or debug dumps.
- The command runs tests, build scripts, package scripts, setup scripts, or third-party CLIs that may echo environment state.
- The command sends API requests using credentials from the environment.
- The command is being run by an agent and the output may be saved in logs or transcripts.

## When Direct Execution Is Fine

Direct execution is usually fine for commands that only inspect local source files or repository metadata and do not run project code, read env files, or print environment values.

Examples:

```bash
rg "maskrun" src tests README.md
sed -n '1,120p' Cargo.toml
git diff -- src/main.rs
```

If unsure, use `maskrun --`.

## Command Handling

Keep the wrapped command unchanged after `--`.

Do:

```bash
maskrun -- bash -lc 'echo "$API_KEY"'
maskrun -- env
maskrun -- cargo test -- --nocapture
```

Do not rewrite the child command arguments to make masking work. `maskrun` filters stdout and stderr while preserving the child command's normal inherited environment and exit code.


## Installation

If `maskrun` is not installed, check the latest installation instructions before running sensitive commands.

Start from the GitHub repository or latest release page:

- `https://github.com/ctxinf/agent-env-guard`
- `https://github.com/ctxinf/agent-env-guard/releases/latest`

After installation, verify:

```bash
maskrun --help
```

## Configuration

`maskrun` uses a TOML config to decide which environment variable values should be masked.

Rules match environment variable names, not output text patterns. When a variable name matches `exact`, `glob`, or `regex`, its value is masked by exact string replacement in stdout and stderr.

Default config locations:

- Linux / Unix: `$XDG_CONFIG_HOME/maskrun/config.toml` or `$HOME/.config/maskrun/config.toml`
- macOS: `$HOME/Library/Application Support/maskrun/config.toml`
- Windows: `%APPDATA%\maskrun\config.toml`

Example config:

```toml
[filter]
exact = [
  "API_KEY",
  "SECRET",
  "PASSWORD",
]

glob = [
  "*_KEY",
  "*_TOKEN",
  "*_SECRET",
  "*_PASSWORD",
]

regex = [
  "(?i)^.*password.*$",
]
```

If the user needs to change masking rules, edit the default config file above or pass a project-specific config:

```bash
maskrun --config ./maskrun.toml -- <command> [args...]
```

Use `--verbose` to inspect which environment variable names matched without printing their raw values:

```bash
maskrun --verbose -- <command> [args...]
```

## Safety Boundary

Treat `maskrun` as output masking only.

It does not sandbox the child process, block network access, prevent file writes, manage credentials, or stop the child command from reading environment variables. It reduces accidental exposure in terminal output, logs, and agent transcripts.
