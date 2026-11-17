---
title: "Remote Control start flow should handle relink readiness from inside the TUI"
status: open
priority: P1
owner: Cody
repo: wip-codex-remote-control-private / wip-ldm-os-private
created: 2026-05-06
---

# Remote Control TUI Relink Readiness

## Problem

`start remote control` can generate the correct URL for the current Codex thread, but the browser can still fail with:

```text
daemon has no E2EE key registered. Re-run `codex-daemon link` to upgrade.
```

Today the recovery path is manual:

1. leave the TUI context;
2. open a separate normal terminal;
3. run `codex-daemon link`;
4. open the printed pair URL;
5. return to the browser and refresh the Remote Control page.

That worked during dogfood, but Parker correctly called out that the product should be operable from inside the Codex TUI. The user should not have to remember the daemon CLI, especially when they already asked the correct natural-language command: `start remote control`.

There is a second UX break on mobile: after pairing succeeds, the phone shows a generic completion state such as "your laptop will pick this up in a few seconds." For Remote Control, that page should not be a dead end. It should continue into the intended session URL:

```text
/codex-remote-control/<threadId>
```

The user should not have to send themselves the original Remote Control link or manually reopen it after pairing.

This is related to, but not the same as, the P0 E2EE key persistence ticket. Key persistence should make routine relink unnecessary after hosted reloads. This ticket covers the UX and readiness contract when relink is genuinely required or when the persistence bug has not landed yet.

## Current Evidence

Observed in live dogfood:

- `codex-wip` was running on thread `019dfa1e-0c3d-7f01-86b9-9a22cd452bde`.
- `start remote control` generated the correct current-session URL:

```text
https://wip.computer/login?next=%2Fcodex-remote-control%2F019dfa1e-0c3d-7f01-86b9-9a22cd452bde
```

- The browser showed:

```text
daemon has no E2EE key registered. Re-run `codex-daemon link` to upgrade.
```

- Running `codex-daemon link` in a separate terminal re-registered the daemon key:

```text
codex-daemon: paired as parker-smoke-test
codex-daemon: relay key saved to /Users/lesa/.codex-daemon/relay-key
```

- `codex-daemon status` then showed the daemon still running and relay paired.
- On mobile, pairing completion currently ends at a generic "laptop will pick this up" state instead of redirecting to the original `/codex-remote-control/<threadId>` page.

## Expected Behavior

From inside the WIP Codex TUI, `start remote control` should either:

- return a working Remote Control URL; or
- explain the one missing readiness step and give a direct recovery path.

The ideal flow:

1. User says `start remote control`.
2. MCP checks current thread id, daemon status, relay pairing, and E2EE key availability.
3. If all gates pass, MCP returns the Remote Control URL.
4. If daemon is unpaired or the relay lacks the daemon E2EE public key, MCP starts or proxies relink.
5. MCP prints the pair URL and code directly in the TUI.
6. The pair URL carries the original Remote Control return target.
7. User completes pairing on phone.
8. Phone redirects into `/codex-remote-control/<threadId>`.
9. The page attaches to the live session automatically.

User-facing recovery copy should be direct:

```text
Remote Control needs to relink this daemon before the browser can create an encrypted channel.

Pair URL:
https://wip.computer/login?next=/pair/<CODE>

Code:
<CODE>

After pairing completes, refresh the Remote Control page.
```

If the relink flow includes a return target, the better copy is:

```text
Remote Control needs to relink this daemon before the browser can create an encrypted channel.

Pair URL:
https://wip.computer/login?next=/pair/<CODE>&return_to=/codex-remote-control/<threadId>

Code:
<CODE>

After pairing completes, this device will open the Codex Remote Control session automatically.
```

## Likely Implementation

Short-term:

- Add an MCP tool such as `remote_control_relink`.
- Have `remote_control` detect missing daemon/E2EE readiness when possible and call or suggest the relink tool.
- The relink tool should invoke the installed daemon flow, not repo source code.
- It should return the pair URL and code in the TUI without requiring the user to open a separate terminal.
- The relink flow should preserve the original Remote Control destination through pairing.
- `codex-daemon link` or the MCP relink helper should be able to include a return target, such as `/codex-remote-control/<threadId>`.
- The hosted pair page should redirect to that return target after successful pairing.
- If no return target exists, the pair page can keep the existing generic completion copy.
- If the daemon is not running, the tool should say whether it started it or which command is needed.

Medium-term:

- Add daemon or relay readiness checks so the MCP tool can distinguish:
  - daemon not installed,
  - daemon not running,
  - daemon not paired,
  - daemon paired but relay missing E2EE pubkey,
  - current thread unavailable,
  - WIP Codex App Server unavailable.

Long-term:

- The P0 E2EE key persistence fix should make routine relink after hosted reload unnecessary.
- This relink path remains for first-time setup, device replacement, lost credentials, or explicit re-key.

## Acceptance

- In a WIP Codex TUI, `start remote control` does not leave the user at a browser-only error when relink is needed.
- If E2EE key registration is missing, the TUI output gives a pair URL and code or tells the user exactly why it cannot.
- The relink path uses installed commands or daemon APIs, not repo source paths.
- The relink path does not require guessing the current session or choosing the most recent session.
- The relink path preserves the current thread URL after pairing.
- After pairing from mobile, the phone automatically opens the intended `/codex-remote-control/<threadId>` page.
- The user does not need to send themselves or manually reopen the original Remote Control URL.
- After pairing, the Remote Control page attaches to the same thread.
- If the daemon is already paired and E2EE key is registered, `start remote control` remains the simple URL flow.
- Add tests for the MCP readiness/relink output shape.
- Add tests for pair-success continuation when a return target is present.
- Add a dogfood checklist item: hosted reload or missing relay key produces a TUI-guided relink path.

## Non-Goals

- Do not treat relink as the primary fix for hosted reload key loss. That remains the P0 E2EE key persistence ticket.
- Do not weaken E2EE or allow plaintext fallback.
- Do not make the hosted relay the Codex session authority.
- Do not start a separate Codex runner.
- Do not require relink after normal deploys once key persistence or daemon re-registration is fixed.

## Related Tickets

- `2026-05-05--codex--remote-control-e2ee-key-persistence.md`
- `2026-05-05--codex--remote-control-pair-relink-audit-and-rotation.md`
- `2026-05-06--codex--remote-control-pair-status-poll-token.md`
