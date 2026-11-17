---
name: stablepay-agent-bootstrap
version: 1.4.0
author: Bubblevan
description: Install, bootstrap, validate, and optionally connect StablePay MCP on Codex, Claude Code, or Cursor.
tags:
  - stablepay
  - onboarding
  - cli
  - mcp
category: Developer Tools
---

# StablePay Setup Skill

Use this file as the only required entrypoint. Do not ask for extra docs before starting.

## Success Condition

Leave the environment in one of these states:

1. StablePay is installed and `doctor` works.
2. onboarding is complete and at least one follow-up command works.
3. onboarding is paused on a real external step, and the exact resume command is provided.

## Surface Model

- `CLI` is the bootstrap, repair, and release-validation surface.
- `MCP` is the ongoing in-agent runtime surface.
- First-time setup: use `CLI` first.
- After CLI succeeds: optionally add `MCP`.

## First Step: Detect OS

Detect the shell environment before choosing commands.

- Windows PowerShell: prefer `npm.cmd` and `npx.cmd` when `npm` or `npx` are blocked by execution policy.
- Linux/macOS/WSL: use `npm` and `npx`.

## Rules

- Use OS-native commands.
- Prefer published-package flow unless the user explicitly wants local-repo validation.
- For published-package flow, prefer `npx stablepay-agentpay-dev ...`.
- For local-repo flow, prefer `node ./dist/cli.cjs ...`.
- Treat `onboard --interactive` as a loop. Do not stop after the first prompt.
- When onboarding reaches browser-based X verification, stop and wait for the user. This is a human-in-the-loop step.
- Do not try to bypass X verification by searching local source, replaying hidden endpoints, or using mock verification paths.
- Keep user-facing wording focused on meaningful choices, not internal runtime jargon.
- Do not claim MCP is active until config is written or the server is confirmed connected.
- Do not claim the package is release-ready until release verification succeeds.

## Platform Notes

- Windows: the npm package and CLI can work even when the local in-process wallet SDK path is unavailable. Do not assume "installed" means "full local wallet runtime is ready".
- Linux/macOS/WSL: standard CLI bootstrap path is expected to work directly.

## Published-Package Flow

### 1. Install or update

```bash
# Windows
npm.cmd install -g stablepay-agentpay-dev

# Linux/macOS/WSL
npm install -g stablepay-agentpay-dev
```

If global install is unnecessary, skip this and use `npx` directly.

### 2. Verify CLI

```bash
# Windows
npx.cmd stablepay-agentpay-dev doctor

# Linux/macOS/WSL
npx stablepay-agentpay-dev doctor
```

If this fails because the entrypoint is missing or broken, report it as a packaging failure.

### 3. Run onboarding

```bash
# Windows
npx.cmd stablepay-agentpay-dev onboard --interactive

# Linux/macOS/WSL
npx stablepay-agentpay-dev onboard --interactive
```

Expected question types:

- create a new wallet or bind an existing one
- wallet identity details
- payment limits
- X verification
- reward status follow-up

Important:

- If X verification is still pending, treat it as a pause point, not a successful completion.
- If the CLI gives a resume session ID or resume command, preserve it and tell the user exactly how to continue.
- At that point, stop autonomous execution. Wait for the user to complete the browser step and return with the verification result or tweet URL.

### 4. Validate post-onboarding behavior

Run at least one:

```bash
# Windows
npx.cmd stablepay-agentpay-dev status
npx.cmd stablepay-agentpay-dev balance
npx.cmd stablepay-agentpay-dev merchant list

# Linux/macOS/WSL
npx stablepay-agentpay-dev status
npx stablepay-agentpay-dev balance
npx stablepay-agentpay-dev merchant list
```

Balance semantics:

- `balance` is the StablePay gateway balance for the active DID.
- It is not the wallet app's total asset value.
- It is not the native SOL balance.

### 5. Optionally configure MCP

Only after CLI bootstrap works:

```json
{
  "mcpServers": {
    "stablepay": {
      "command": "npx",
      "args": ["stablepay-agentpay-dev", "mcp"]
    }
  }
}
```

## Local-Repo Flow

Use this only when the user wants to validate the working tree before publish.

### 1. Build

```bash
npm.cmd run check
npm.cmd run build
```

### 2. Validate CLI

```bash
node ./dist/cli.cjs doctor
node ./dist/cli.cjs onboard --interactive
node ./dist/cli.cjs status
```

### 3. Release verification

```bash
npm.cmd run release:verify
```

## Publish Flow

```bash
npm.cmd version patch
npm.cmd run release:verify
npm.cmd publish --access public
```

Post-publish smoke test:

```bash
npx stablepay-agentpay-dev doctor
npx stablepay-agentpay-dev onboard --interactive
npx stablepay-agentpay-dev status
```

## Failure Classification

### Packaging failure

Examples:

- `npx` cannot find the command
- `bin` entry is missing
- `dist/cli.cjs` is missing from the package

Report:

- failed command
- concrete packaging symptom
- whether the local repo path still works

### Runtime failure

Examples:

- wallet runtime unavailable
- onboarding cannot continue because no usable wallet path exists

Report:

- CLI is installed or not
- which layer is blocked
- OS context

### Backend or network failure

Examples:

- doctor reaches local runtime but remote APIs fail
- balance, reward, registration, or merchant calls fail

Report:

- local CLI state
- failing remote-facing step
- exact command that failed

### External-verification pause

Examples:

- X verification must be completed in the browser before onboarding can continue
- user must manually open the verification page and finish the external step

Report:

- onboarding reached a real pause point
- what the user must do next
- exact resume command

## Completion Format

Report in compact operator style:

1. OS detected
2. flow used: published package or local repo
3. whether onboarding completed or paused
4. which validation command succeeded
5. whether MCP was configured
6. remaining step, if any

Example:

> OS: Linux / WSL2  
> Flow: published package  
> Onboarding: paused at X verification  
> Validation: `status` works  
> MCP: not configured  
> Next step: complete X verification, then resume onboarding with the saved session
