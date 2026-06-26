---
name: eve-web-ui-testing-agent-browser
description: Web UI testing and browser automation. Use Vercel agent-browser for general apps, or the repo-pinned Playwright wrapper inside Eve Horizon. Use when tasks require opening pages, interacting with forms, validating UI flows, taking screenshots, extracting page data, or running repeatable browser-based checks locally or in CI.
---

# Web UI Testing with agent-browser

Use `agent-browser` as the default CLI for deterministic UI checks in app repos. Inside the Eve Horizon repo itself, prefer the repo-pinned Playwright wrapper (see "Eve Horizon Repo Wrapper" below).

## Install agent-browser

```bash
# macOS/Linux (recommended)
npm install -g agent-browser
agent-browser install

# Linux containers/VMs that need extra browser libs
agent-browser install --with-deps
```

Alternative install on macOS:

```bash
brew install agent-browser
agent-browser install
```

## Configure for Reliable Runs

Use isolated state for each test target:

```bash
# one session per test flow
agent-browser --session login-flow open https://example.com

# persistent auth/session state per app
agent-browser --profile ~/.agent-browser/myapp open https://example.com
```

Set environment variables for CI:

```bash
export AGENT_BROWSER_SESSION=ci
export AGENT_BROWSER_PROFILE="$PWD/.tmp/agent-browser-profile"
export AGENT_BROWSER_PROVIDER=local
```

Optional cloud providers:

- Browserbase: set `AGENT_BROWSER_PROVIDER=browserbase`, `BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID`
- Browser Use: set `AGENT_BROWSER_PROVIDER=browseruse`, `BROWSER_USE_API_KEY`
- Kernel: set `AGENT_BROWSER_PROVIDER=kernel`, `KERNEL_API_KEY`

For proxy testing:

```bash
export AGENT_BROWSER_PROXY="http://user:pass@proxy-host:port"
```

## Install the Upstream Skill (Optional)

If your runtime supports skill installation, add the upstream skill:

```bash
eve skill install https://github.com/vercel-labs/agent-browser
```

## Core Workflow

Run every flow in this sequence:

1. Navigate: `agent-browser open <url>`
2. Snapshot interactive refs: `agent-browser snapshot -i`
3. Interact with refs: `agent-browser click @e1`, `agent-browser fill @e2 "value"`
4. Re-snapshot after page changes: `agent-browser snapshot -i`
5. Assert output: `agent-browser get text <selector-or-ref>`
6. Capture artifacts: `agent-browser screenshot <path>`

## Minimal Test Template

```bash
agent-browser --session smoke open https://example.com/login
agent-browser --session smoke snapshot -i
agent-browser --session smoke fill @e1 "user@example.com"
agent-browser --session smoke fill @e2 "password"
agent-browser --session smoke click @e3
agent-browser --session smoke wait --url "**/dashboard"
agent-browser --session smoke screenshot ./artifacts/login-dashboard.png
agent-browser --session smoke close
```

## Guardrails

- Re-snapshot after every navigation or dynamic UI update; refs become stale.
- Prefer `snapshot -i` refs over brittle CSS selectors.
- Use `--json` for machine-readable assertions in scripts.
- Keep one session/profile per environment to avoid cross-test leakage.
- Save screenshots and logs as artifacts for failed runs.

## Eve Horizon Repo Wrapper

When working inside the Eve Horizon source repo, use the repo-pinned Playwright wrapper instead of installing `agent-browser` separately. It ships with the repo and targets the local dashboard out of the box:

```bash
./bin/eh browser install        # one-time per machine / Playwright upgrade
./bin/eh browser dashboard      # headed Chromium with Eve token injected
./bin/eh browser open <url>
./bin/eh browser codegen <url>  # capture a draft Playwright spec
./bin/eh browser screenshot <url> [file]
./bin/eh browser test -g "<name>"  # run the dashboard Playwright suite
```

Defaults: `chromium` browser, persistent profile under `tmp/playwright-browser/profile`, screenshots in `tmp/playwright-browser/screenshots`, codegen output in `tmp/playwright-browser/codegen`, dashboard URL `http://dashboard.eve.lvh.me`, API URL `http://api.eve.lvh.me`. Set `EVE_API_URL=https://api.eve.example.com` to point at staging.

`./bin/eh browser dashboard` mints a token via `eve auth token --raw` and injects it as `sessionStorage.eve_access_token`. If minting fails, run `eve auth login` first.

Escalate exploratory repros into committed Playwright specs under `apps/dashboard/e2e/` when you need assertion coverage, CI protection, or a regression suite.

## References and Templates

- Full commands: `references/commands.md`
- Ref lifecycle: `references/snapshot-refs.md`
- Session strategy: `references/session-management.md`
- Authentication flows: `references/authentication.md`
- Proxy setup: `references/proxy-support.md`
- Video capture: `references/video-recording.md`
- Reusable scripts: `templates/*.sh`
