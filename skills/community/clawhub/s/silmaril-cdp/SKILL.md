---
name: silmaril-cdp
description: Browser automation, DOM inspection, page mutation, wait orchestration, flow execution, and local proxy override work through the Silmaril Chrome DevTools Protocol toolkit. Use when the task requires opening Chrome with CDP, navigating pages, reading DOM or source, extracting structured data, clicking or typing into elements, evaluating JavaScript, waiting for UI state changes, running Silmaril flow JSON files, or managing mitmproxy-backed local overrides.
---

# Silmaril CDP

Use this skill to operate the local Silmaril toolkit from PowerShell.

## Locate the toolkit

- Prefer `D:\silmairl cdp\silmaril.cmd` in this environment.
- If that path is missing, look for `silmaril.cmd` on `PATH` or in a nearby checkout.
- Invoke from PowerShell with `& 'D:\silmairl cdp\silmaril.cmd' ...`.

## Install the toolkit if missing

Use this setup on Windows when the toolkit is not already present:

Only clone or copy the toolkit after the user explicitly approves fetching or installing remote code.

1. Clone or copy the repository:

   `git clone https://github.com/Malac12/CDP-tools.git "D:\silmairl cdp"`

2. Ensure Chrome, Chromium, or Edge is installed.

   The toolkit checks standard Windows install paths and falls back to `chrome.exe` on `PATH`.

3. Run the toolkit from PowerShell:

   `& 'D:\silmairl cdp\silmaril.cmd' openbrowser --json`
   `& 'D:\silmairl cdp\silmaril.cmd' openUrl 'https://example.com' --json`
   `& 'D:\silmairl cdp\silmaril.cmd' get-text 'body' --json`

This is sufficient for the core CDP workflow. No machine-wide PowerShell execution policy change is required because `silmaril.cmd` invokes PowerShell with `ExecutionPolicy Bypass`.

## Default workflow

1. Start or attach a CDP browser with `openbrowser`.
2. Navigate with `openUrl`.
3. Read page state with `exists`, `get-text`, `query`, or `get-dom`.
4. Mutate only after validating selectors.
5. Wait on one clear synchronization signal after each action.
6. Prefer `run` for short repeatable flows.

## Operating rules

- Prefer `--json` for almost every command so later steps can parse structured output.
- Prefer live DOM commands over `get-source` when choosing selectors or checking rendered state.
- Prefer stable selectors such as `data-test`, `data-testid`, semantic IDs, and meaningful attributes.
- Use either `--target-id` or `--url-match` when multiple tabs exist; never use both together.
- Pass `--yes` for page actions and mutations such as `click`, `type`, `set-text`, `set-html`, and `eval-js`.
- Treat `eval-js`, `proxy-override`, `proxy-switch`, and `openurl-proxy` as high-risk commands.
- Use `--allow-unsafe-js` for `eval-js`, or set `SILMARIL_ALLOW_UNSAFE_JS=1` only for a trusted local session.
- Use `--allow-mitm` for proxy commands, or set `SILMARIL_ALLOW_MITM=1` only for a trusted local session.
- Keep proxy listeners on loopback addresses unless the user explicitly requests `--allow-nonlocal-bind`.
- Put long JavaScript in a file and use `eval-js --file` instead of pasting large inline expressions.
- Avoid fixed sleeps when a wait command can express the intended state.

## Command selection

- Use `get-text` for a single text value.
- Use `query` for structured multi-row extraction.
- Use `get-dom` to debug selector or markup issues.
- Use `get-source` only when raw response HTML matters more than the rendered DOM.
- Use `wait-for`, `wait-for-any`, `wait-for-gone`, `wait-until-js`, or `wait-for-mutation` to synchronize.

## References

- Read `references/command-patterns.md` for common command shapes and PowerShell-safe examples.
- Read `references/flows.md` before building or editing a `run` flow.
- Read `references/proxy.md` when working with `openurl-proxy`, `proxy-override`, or `proxy-switch`.
