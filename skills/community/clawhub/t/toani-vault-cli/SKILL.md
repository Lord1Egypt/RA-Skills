---
name: toani-vault-cli
description: Install, configure, and securely operate the Toani Vault CLI for login, health checks, credential metadata reads, and sandbox browser sessions. Use when the user mentions `toani`, Toani Vault, secure CLI onboarding, credential hygiene, token handling, sandbox automation, defensive security workflows, or needs help installing or using the Vault CLI from a coding agent.
version: 0.0.21
metadata:
  openclaw:
    requires:
      bins:
        - node
      anyBins:
        - npm
        - pnpm
    install:
      - kind: node
        package: "@toani/vault-cli"
        bins:
          - toani
    envVars:
      - name: TOANI_VAULT_TOKEN
        required: false
        description: Optional bearer token for non-interactive CLI auth.
      - name: CREDBRIDGE_TOKEN
        required: false
        description: Legacy-compatible token environment variable.
      - name: TOANI_BASE_URL
        required: false
        description: Optional API base URL override.
      - name: CREDBRIDGE_BASE_URL
        required: false
        description: Legacy-compatible API base URL override.
      - name: TOANI_VAULT_DASHBOARD_BASE_URL
        required: false
        description: Optional dashboard URL used by onboarding and default base URL resolution.
    homepage: https://github.com/credbridge/credbridge/tree/main/cli
---

# Toani Vault CLI

## Purpose

Use this skill to help the user install, verify, and operate the `toani` CLI.

Default priorities:

1. Verify the real CLI surface with `toani --help` before trusting older docs.
2. Prefer `toani login` for onboarding.
3. Treat `credentials` as read-only metadata access.
4. Treat `sandbox` as a remote TEE browser session, not a local browser runtime.
5. Terminate sandbox sessions when finished.

## Install

If `toani` is not available, install it first.

Registry install:

```bash
npm install -g @toani/vault-cli@latest
```

Local dev install:

```bash
cd /path/to/credbridge-public/cli
npm install
npm run build
npm pack
npm install -g ./toani-vault-cli-*.tgz
```

If the user already has the repo checked out and wants the local build, prefer the local dev install path. Otherwise prefer the registry install path.

## Smoke Checks

Run these after install:

```bash
toani --help
toani --version
toani config show
toani sandbox stats
```

## Authentication and Setup

Preferred onboarding:

```bash
toani login
toani doctor
toani --output json config show
toani --output json credentials list
```

`toani login` is the preferred entry path. Do not start with `config init --token` unless the user explicitly needs a legacy-compatible non-interactive flow.

`toani login` semantics:

- interactive onboarding with browser guidance
- supports existing account, sign-up-first, and already-have-token paths
- watches the clipboard for a PASETO token
- validates the token by default
- stores the token in the OS Keychain when possible
- may optionally install the bundled skill into `~/.claude/skills/toani-vault-cli/` or `~/.codex/skills/toani-vault-cli/`

`toani doctor` checks:

1. CLI version
2. Node.js version
3. Token storage
4. Token format
5. Base URL
6. Server reachable
7. Token valid

## Runtime Model

Keep this mental model explicit:

- `toani` is a CLI, not SDK pseudocode.
- `sandbox` is a remote TEE browser session provided by the backend.
- `http_request` is a backend-side direct HTTP operation and does not open the remote browser.
- Credentials and bearer tokens are created in the Dashboard UI; the CLI currently reads existing artifacts.

## Current Command Surface

Trust the current CLI implementation and `toani --help`.

Currently exposed groups:

- `login`
- `doctor`
- `config`
- `credentials`
- `sandbox`

Do not assume these exist unless verified in the installed build:

- `auth`
- `tokens`
- `service-accounts`
- `audit`

`credentials` currently exposes only:

```bash
toani credentials list [--service-id <id>] [--credential-type <type>] [--only-valid true|false]
toani credentials get <credentialId>
```

Do not claim that the CLI can currently do these credential operations unless the user has verified a newer build:

- create
- update
- delete
- decrypt

## Global Flags and Precedence

Global flags must appear before the command group:

```bash
toani --output json credentials list
toani --base-url https://api.example.com sandbox stats
```

Do not write:

```bash
toani credentials list --output json
toani sandbox stats --base-url https://api.example.com
```

Base URL precedence:

1. `--base-url`
2. `TOANI_BASE_URL`
3. `CREDBRIDGE_BASE_URL`
4. config file value
5. default dashboard-derived fallback

Token precedence:

1. `--token`
2. `TOANI_VAULT_TOKEN`
3. `CREDBRIDGE_TOKEN`
4. OS Keychain token
5. legacy config token

Default to `--output json` for automation and agent workflows.

## Recommended Setup

If the user wants explicit environment-variable setup, use:

```bash
export TOANI_VAULT_DASHBOARD_BASE_URL=https://dashboard.example.com
export TOANI_BASE_URL=https://api.example.com/
export TOANI_VAULT_TOKEN=<BEARER_TOKEN>
```

Only use placeholder values in examples. Never log or commit real tokens.

## Sandbox Workflow

Standard browser-session flow:

```bash
toani sandbox create-session --service-id <serviceId> --original-intent <intent> [--credential-id <id>]
toani sandbox get-session <sessionId>
toani sandbox bootstrap-page <sessionId> --mode rocket_loader
toani sandbox execute <sessionId> --operation-type navigate --params '{"url":"https://example.com"}'
toani sandbox execute <sessionId> --operation-type get_text --params '{"selector":"body"}'
toani sandbox terminate <sessionId>
```

Supported operation types to rely on:

- `navigate`
- `click`
- `fill`
- `get_text`
- `execute_script`
- `wait`
- `export`
- `dom_export`
- `http_request`

## Sandbox Safety Rules

When guiding usage, keep these boundaries clear:

- Do not treat the sandbox as local Playwright or a local browser.
- Do not leave long-lived sessions running.
- Inspect page state before secret-backed `fill` steps.
- After credential-backed `fill`, prefer safe post-actions such as `get-session`, `get-operation`, `export-dom`, and `get_text`.
- Do not put secrets into `execute_script.bindings`.

## Credential Handling Rules

- `credentials list/get` return metadata only.
- They do not reveal plaintext secrets.
- They do not perform decryption.
- They still require a token with the right read scope.

If the user gives only a credential nickname instead of a concrete `credential_id`, first inspect metadata with `toani credentials list` or confirm the ID in the Dashboard UI.

## Working Style

When using this skill:

1. Verify the installed CLI surface first.
2. Choose install flow or usage flow based on whether `toani` already exists.
3. Prefer the shortest executable command sequence that answers the user's task.
4. Call out scope limits instead of inventing unpublished commands.
5. If a command fails, check token scope, base URL, and environment before assuming product behavior is broken.

## Common Fast Paths

Install the CLI:

```bash
npm install -g @toani/vault-cli@latest
```

Onboard a new user:

```bash
toani login
toani doctor
```

Inspect credentials:

```bash
toani --output json credentials list
toani --output json credentials get <credentialId>
```

Check sandbox health:

```bash
toani sandbox stats
```
