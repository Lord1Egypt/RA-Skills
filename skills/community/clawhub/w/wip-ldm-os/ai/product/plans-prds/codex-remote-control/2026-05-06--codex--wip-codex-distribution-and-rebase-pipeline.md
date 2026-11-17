---
title: "WIP Codex Distribution And Auto-Rebase Pipeline"
date: 2026-05-06
author: Codex
status: active-plan
surface: codex-remote-control
priority: P0
---

# WIP Codex Distribution And Auto-Rebase Pipeline

## Decision

Assume there is no upstream acceptance path for Remote Control.

Under that assumption, Codex Remote Control is not only an add-on for stock Codex. It is a WIP distribution:

```text
WIP Codex Remote Control
= WIP-compatible Codex build
+ local daemon
+ Codex MCP entrypoint
+ phone/web Remote Control client
```

Users should not compile Codex, patch Codex, or rebase Codex themselves. WIP owns that maintenance burden.

The user-facing product is:

```text
Run Codex normally if you only need local terminal use.
Run WIP Codex when you want live phone control.
```

WIP Codex installs side by side as `codex-wip` or `wip-codex`. It must not replace the user's normal `codex` binary.

## Why WIP Codex Exists

Remote Control needs live co-presence, not a second runner.

The WIP-compatible Codex build provides the local primitives that stock Codex does not reliably expose for this product:

- a TUI-owned App Server control socket;
- external clients attaching to the live TUI App Server;
- multi-subscriber live thread events;
- MCP stdio servers receiving the current thread id and title;
- Remote Control startup resolving the current active session instead of guessing from recent sessions.

Without those primitives, the daemon can pair and the browser can connect, but the browser risks driving a separate Codex runner instead of the same live TUI session.

## User Experience

The user starts from the install prompt:

```text
Read https://wip.computer/install/wip-codex-remote-control.txt

Use the install document and live local checks as the source of truth. Do not search memory or prior notes for this install.

Check if it's installed. If yes, show me what version I have.

If not, walk me through setup and explain:

1. What is Codex Remote Control?
2. What does it install on my system?
3. How does my phone drive my Codex session?

Then ask:
- Do you have questions?
- Want to see a dry run?

If I say yes, install via `ldm install --alpha wip-codex-remote-control` and walk me through pairing my phone.

Don't install anything until I say "install".
```

The installer flow must explain the WIP Codex requirement clearly:

```text
Codex Remote Control requires WIP Codex for live phone control.
WIP Codex is WIP's compatible Codex build with live App Server co-presence enabled.
It installs side by side as `codex-wip`.
It does not replace your normal `codex` command.
```

After install:

```bash
codex-wip
```

Inside that session:

```text
start remote control
```

Codex returns:

```text
https://wip.computer/login?next=/codex-remote-control/<threadId>
```

The phone opens the URL, signs in, completes E2EE, attaches to the live thread, hydrates history, sends messages, receives streamed Codex output, and can Stop the active turn.

## Install-Session Handoff UX

Most users will discover and install Remote Control from inside a normal stock `codex` session.

That stock session is useful for installation, but it is not the live phone-control runtime. After install, the user must move the current saved thread into `codex-wip`.

The install flow must therefore end with an explicit handoff, not a vague "now run codex-wip" instruction.

Required flow:

1. User is in stock `codex`.
2. User pastes the install prompt.
3. Codex installs Remote Control and WIP Codex after explicit approval.
4. Installer or MCP tool resolves the current thread id and title.
5. It prints the exact resume command for WIP Codex:

```bash
codex-wip resume <thread-uuid>
```

6. It tells the user to exit the current stock Codex session.
7. User pastes the resume command in a new terminal.
8. WIP Codex opens the same saved session.
9. User says:

```text
start remote control
```

10. WIP Codex returns the phone URL for that live WIP Codex session.

User-facing copy should be direct:

```text
Remote Control is installed, but this current session is running in stock Codex.

To use this exact session from your phone:

1. Exit this Codex session.
2. Open a new terminal.
3. Run:

   codex-wip resume <thread-uuid>

4. In the resumed WIP Codex session, say:

   start remote control

Your normal `codex` command is untouched.
```

The handoff command should prefer UUID over title. If the UI also shows a friendly title, show it as context only:

```text
Session: test01
Thread id: 019...
Resume command: codex-wip resume 019...
```

Do not rely on a title if it is missing or not unique.

## Stock Codex Remote Control Invocation

The `start remote control` natural-language path should work inside both stock Codex and WIP Codex, but with different behavior.

If invoked from WIP Codex:

- start live Remote Control;
- return the phone URL;
- attach to the current live WIP Codex session.

If invoked from stock Codex:

- do not pretend live co-presence can start there;
- do not return a phone URL that targets the stock TUI live session;
- detect that the current runtime is not WIP Codex or lacks the required App Server co-presence support;
- return the handoff instructions and exact `codex-wip resume <thread-uuid>` command;
- tell the user to resume in WIP Codex and run `start remote control` again.

Correct stock Codex response:

```text
Remote Control is installed, but this session is running in stock Codex.

To control this same session from your phone, resume it in WIP Codex:

codex-wip resume <thread-uuid>

After it opens, say:

start remote control
```

Incorrect stock Codex response:

```text
Here is your phone URL...
```

That would imply stock Codex can expose the same live TUI co-presence path. Under the no-upstream assumption, it cannot.

## Stock Codex Session Transfer

Stock Codex and WIP Codex should share the normal Codex thread store unless the user explicitly chooses a separate `CODEX_HOME`.

That means this should work:

1. User starts a session in stock `codex`.
2. User names or remembers it as `test01`, or records the UUID.
3. User exits stock `codex`.
4. User opens the same saved session in WIP Codex:

```bash
codex-wip resume test01
```

or:

```bash
codex-wip resume <thread-uuid>
```

Both stock `codex` and `codex-wip` expose the same `resume [SESSION_ID] [PROMPT]` command shape. UUIDs take precedence over names.

Product rule:

- Use UUIDs for unambiguous handoff.
- Thread names are allowed only when unique.
- Do not try to attach Remote Control to a currently active stock Codex TUI. If the user wants phone control, resume that saved thread in `codex-wip`.
- Once the thread is open in `codex-wip`, `start remote control` attaches the phone to that live WIP Codex session.

Compatibility caveat:

- This depends on WIP Codex staying compatible with stock Codex's current thread store format.
- If upstream changes the session format, WIP's rebase pipeline must catch it before publishing a candidate.
- If a saved stock session cannot resume in WIP Codex, the installer or CLI should fail clearly and direct the user to upgrade WIP Codex.

## Packaging Shape

Preferred package split:

```text
wip-codex
  installs the WIP-compatible Codex binary as `codex-wip`

wip-codex-remote-control
  installs `codex-daemon`
  installs `codex-daemon-mcp`
  installs Codex skill trigger
  registers Codex MCP entry
  checks or prompts for `codex-wip`
```

The Remote Control installer may install `wip-codex` as a dependency or prompt for it, but the user-facing story should stay simple:

```text
Install Remote Control.
It installs WIP Codex side by side.
Run `codex-wip` when you want phone control.
```

Required install checks:

```bash
codex-wip --version
codex-daemon --version
codex mcp list
codex-daemon status
```

Do not overwrite:

- `/opt/homebrew/bin/codex`
- the user's stock Codex package;
- unrelated Codex MCP servers;
- existing stock Codex sessions.

## WIP Maintenance Burden

WIP owns:

- tracking upstream `openai/codex`;
- rebasing WIP patches;
- resolving conflicts;
- running Codex tests;
- building binaries;
- signing and notarizing when needed;
- publishing alpha candidates;
- verifying Remote Control dogfood;
- promoting releases only after human approval.

Users own:

- choosing to install;
- pairing their phone;
- running `codex-wip` when they want Remote Control;
- approving upgrades.

## Auto-Rebase And Alpha Candidate Pipeline

Automation should create candidates, not promote them directly to broad users.

Pipeline:

```text
Detect upstream openai/codex update
-> create/update integration branch
-> rebase WIP patches
-> run focused Codex tests
-> build codex-wip artifacts
-> publish alpha candidate
-> install alpha in dogfood environment
-> run Remote Control smoke
-> human approves promotion
```

## Watcher

A scheduled job should:

- fetch upstream `openai/codex`;
- compare upstream commit with the last integrated WIP Codex base;
- open or update a private integration PR when upstream moves;
- do nothing if upstream has not moved.

## Rebase Bot

The bot should apply:

```text
openai/codex@new-upstream
+ WIP Remote Control patches
= WIP Codex candidate
```

If rebase conflicts occur:

- stop;
- leave the integration PR open;
- comment with the conflict paths;
- label the candidate blocked;
- do not publish artifacts.

## Test Gates

Focused gates before any candidate artifact:

- Codex App Server control socket test;
- external WebSocket initialize against embedded App Server;
- multi-subscriber thread event fanout;
- MCP stdio thread environment injection;
- `codex-cli` build;
- app-server thread resume subset;
- Remote Control current-thread URL smoke if feasible.

The test suite should specifically protect stock-to-WIP resume compatibility:

- create or load a stock-compatible thread fixture;
- resume it in WIP Codex;
- start Remote Control from WIP Codex;
- verify thread id and title match.

## Candidate Artifact

If tests pass, publish an alpha candidate:

```text
wip-codex@<version>-alpha.<n>
```

or attach platform binaries to a private GitHub release.

First platform:

- macOS arm64.

Later:

- macOS x64;
- Linux;
- Windows only if product demand justifies it.

## Human Dogfood Gate

Before promotion:

1. Install current alpha candidate.
2. Run `codex-wip`.
3. Say `start remote control`.
4. Open phone URL.
5. Verify:
   - phone attach;
   - browser attach;
   - TUI to phone;
   - phone to TUI;
   - multi-browser fanout;
   - refresh hydration;
   - Stop;
   - stock-to-WIP resume by UUID;
   - stock-to-WIP resume by unique name;
   - no replacement of normal `codex`.

Promotion requires a human to mark the candidate good.

## Installer Messaging

The installer should not frame this as an upstream Codex feature.

Correct:

```text
WIP Codex is required for live phone control.
It installs side by side as `codex-wip`.
Your normal `codex` is untouched.
You can resume saved Codex sessions in `codex-wip` when you want phone control.
```

Incorrect:

```text
This works with any stock Codex session live.
```

Incorrect:

```text
We patch your installed Codex.
```

Incorrect:

```text
You need to compile Codex.
```

## Acceptance

- WIP Codex distribution is documented as the no-upstream product path.
- Users are not asked to compile or patch Codex.
- `codex-wip` installs side by side and never replaces stock `codex`.
- Stock saved sessions can be resumed in WIP Codex by UUID or unique title when thread-store format is compatible.
- Installer checks for `codex-wip` and explains the requirement clearly.
- Auto-rebase pipeline produces alpha candidates only.
- Human dogfood is required before promotion.
- Remote Control install prompt remains honest about what is installed and when phone control requires WIP Codex.

## Non-Goals

- Do not depend on OpenAI accepting upstream changes.
- Do not overwrite stock Codex.
- Do not require users to build Rust or rebase forks.
- Do not publish a candidate if Codex tests or stock-to-WIP resume compatibility fail.
- Do not auto-promote WIP Codex to broad users without human smoke.
