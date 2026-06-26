---
name: whoop-cli
description: Use when operating the installed `whoop` CLI for agent-friendly WHOOP access, cross-platform secret storage checks, daily briefs, summaries, health flags, activity trends, exports, or installing the bundled WHOOP agent skill into `~/.agents`, Codex, OpenClaw, or another agent skill directory.
metadata:
  openclaw:
    requires:
      bins:
        - whoop
    homepage: https://github.com/andreasnlarsen/whoop-cli
    install:
      - kind: node
        package: "@andreasnlarsen/whoop-cli@0.5.2"
        bins:
          - whoop
        label: Install whoop-cli from npm
---

# whoop-cli

Use the installed `whoop` command.

## Security + Credential Handling

- Never ask users to paste long-lived client secrets or tokens into chat.
- For first-time auth, have the user run login locally in their own shell.
- macOS default secret storage is macOS Keychain.
- Linux/OpenClaw preferred secret storage is 1Password CLI with a service account.
- Linux/OpenClaw simple fallback is explicit `local-vps` storage with `--accept-local-vps-risk`.
- Profile JSON at `~/.whoop-cli/profiles/<profile>.json` stores non-secret metadata only.
- Keychain access uses macOS Security APIs through `/usr/bin/swift`; do not replace this with command-line secret arguments.
- If `/usr/bin/swift` is unavailable, tell the user to install Apple Command Line Tools with `xcode-select --install`.
- If a sandboxed agent shell cannot access macOS Keychain, rerun the `whoop` command with normal user permissions; do not use secret-bearing command-line arguments as a fallback.
- After login, regular read commands should not need passwords or Touch ID.
- If macOS asks for "password data for new item" during login, stop and update or reinstall `whoop`; the CLI should write Keychain items non-interactively.
- On Linux, do not silently fall back to plaintext profile JSON. Use `onepassword` or explicit `local-vps`.
- Do not send long-lived 1Password service-account tokens through Telegram. In simple `local-vps` setup, the expected Telegram handoff is the short-lived WHOOP auth URL and redirected callback URL.
- Prefer read-only operational commands in agent flows: `summary`, `day-brief`, `health`, `trend`, and `sync pull`.
- Do not run `whoop auth login` unless the user explicitly asks for login help.

## Install / Bootstrap

If `whoop` is missing:

```bash
npm install -g @andreasnlarsen/whoop-cli@0.5.2
```

Install this bundled skill for local Codex/agent use:

```bash
whoop skill install --target agents --force
```

That writes `~/.agents/skills/whoop-cli/SKILL.md` and links it into `~/.codex/skills/whoop-cli`.

Install for OpenClaw when needed:

```bash
whoop skill install --target openclaw --force
```

Install to another skill directory:

```bash
whoop skill install --target path --skill-dir /path/to/skills/whoop-cli --force
```

## Core Checks

1. `whoop auth status --json`
2. If unauthenticated, ask the user to run local login:
   - macOS: `whoop auth login`
   - Linux/OpenClaw recommended: `whoop auth login --secret-storage onepassword --op-vault ... --op-item ...`
   - Telegram-only/simple Linux VPS: `whoop auth login --secret-storage local-vps --accept-local-vps-risk`
   - Prefer the interactive hidden client-secret prompt when a human is present.
   - Use one-time env/secret-manager injection only when automation requires it.
3. Validate:
   - `whoop summary --json --pretty`
   - `whoop day-brief --json --pretty`

## Useful Commands

- Daily:
  - `whoop summary --json --pretty`
  - `whoop day-brief --json --pretty`
  - `whoop strain-plan --json --pretty`
  - `whoop health flags --days 7 --json --pretty`
- Activity analysis:
  - `whoop activity list --days 30 --json --pretty`
  - `whoop activity trend --days 30 --json --pretty`
  - `whoop activity types --days 30 --json --pretty`
  - training-only: `whoop activity trend --days 30 --labeled-only --json --pretty`
- Export:
  - `whoop sync pull --start YYYY-MM-DD --end YYYY-MM-DD --out ./whoop.jsonl --json --pretty`

## Activity Interpretation Guardrail

- WHOOP generic `activity` rows, often `sport_id=-1`, are auto-detected and may be unlabeled movement such as housework or incidental activity, not intentional training.
- Do not treat generic `activity` as confirmed training volume by default.
- For coaching or training recommendations, default to `--labeled-only` and report total versus filtered counts.

## Agent Filtering Pattern

- Canonical source: `whoop activity list --json`
- Prefer built-in filters first: `--labeled-only`, `--generic-only`, `--sport-id`, `--sport-name`.
- If custom slicing is needed and `jq` is available, filter shell-side from raw JSON:

```bash
whoop activity list --days 30 --json | jq '.data.records | map(select(.sport_id != -1))'
```

## Experiment Protocol

- Canonical state: `~/.whoop-cli/experiments.json` only.
- Plan experiments with context at creation time:
  - `whoop experiment plan --name ... --behavior ... --start-date YYYY-MM-DD [--end-date YYYY-MM-DD] --description ... --why ... --hypothesis ... --success-criteria ... --protocol ... --json --pretty`
- Update context without creating duplicate state:
  - `whoop experiment context --id ... [--description ... --why ... --hypothesis ... --success-criteria ... --protocol ...] --json --pretty`
- Check lifecycle/status with:
  - `whoop experiment status [--status planned|running|completed] [--id ...] --json --pretty`
- Evaluate outcomes with:
  - `whoop experiment report --id ... --json --pretty`
- Profile scope is strict by default: active `--profile` only.
- Use `--all-profiles` only when cross-profile visibility is explicitly needed.
- Prefer output field `sourceOfTruth`; `experimentsFile` is kept as compatibility alias.
- Avoid duplicating experiment state into other files unless the user explicitly asks for separate notes.

## Safety

- Never print client secrets or raw tokens.
- Treat `local-vps` as a deliberate lower-security mode: it prevents accidental repo/chat/log exposure but not VPS compromise.
- Keep API errors concise and actionable.
- Treat this integration as unofficial and not affiliated with WHOOP.
