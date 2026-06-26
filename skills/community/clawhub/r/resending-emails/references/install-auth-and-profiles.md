# Install, auth, and profiles

This file covers the setup decisions that most often decide whether a Resend CLI flow is smooth or
painful.

## Install methods

Preferred install methods depend on the environment:

| Environment | Good install choice |
| --- | --- |
| Generic macOS/Linux shell | `curl -fsSL https://resend.com/install.sh \| bash` |
| Node-heavy dev machine | `npm install -g resend-cli` |
| Homebrew-managed machine | `brew install resend/cli/resend` |
| Windows PowerShell | `irm https://resend.com/install.ps1 \| iex` |

The published CLI release is currently `v1.4.1`.

## Local development vs operational use

The repo README documents **Node.js 20+** for local development/building the CLI from source.
That is not the same thing as requiring Node for every normal user; native install paths also exist.

## Authentication priority

The CLI resolves credentials in this order:

1. `--api-key`
2. `RESEND_API_KEY`
3. stored config from `resend login`

For agents and CI, prefer:

1. `RESEND_API_KEY` for one-off automation, or
2. a stored named profile plus `--profile` / `RESEND_PROFILE` for multi-account setups.

### Why not default to `--api-key`?

It has highest priority, but environment variables or stored profiles are usually safer than putting
secrets into command-line arguments that may appear in process listings, shell history, or logs.

## `resend login`

Use `resend login` mainly for human setup.

In non-interactive mode, `--key` is required:

```bash
resend login --key re_xxxxxxxxxxxxx
```

The README documents that login validates the key before saving. If you are scripting, still prefer
`RESEND_API_KEY` or pre-seeded profiles so you do not need an interactive auth step at all.

## Profiles

Profiles are the CLI-native way to switch between Resend accounts or teams.

Useful patterns:

```bash
resend auth switch
resend --profile production --json -q domains list
RESEND_PROFILE=staging resend --json -q doctor
```

### Important profile notes

- The config layer prefers `RESEND_PROFILE`.
- `RESEND_TEAM` is legacy compatibility, not the preferred new name.
- Profile names are validated and should stay simple (`letters`, `numbers`, `_`, `-`).

## Config paths and permissions

The CLI stores config under:

- Linux/macOS default: `~/.config/resend/`
- Linux override: `$XDG_CONFIG_HOME/resend`
- Windows: `%APPDATA%/resend`

Credentials go in `credentials.json`. The README and source both indicate restrictive permissions:

- config directory: `0700`
- credentials file: `0600`

## Practical agent guidance

### Single account CI job

```bash
export RESEND_API_KEY=re_xxxxxxxxx
resend --json -q doctor
resend --json -q emails send --from deploy@example.com --to team@example.com --subject "Deploy complete" --text "Done"
```

### Multiple accounts

Use stored profiles and pass `--profile` explicitly on every live mutation that must hit a specific
account. Do not rely on whichever profile was active last unless the user explicitly wants that.

### When auth looks wrong

Run:

```bash
resend --json -q doctor
```

Then check:

- whether a key is resolved at all
- whether it came from the expected source
- whether verified domains exist in that account
