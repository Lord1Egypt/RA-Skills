---
name: super-memori-session-start
description: "Run Super Memori startup self-check once per new session via agent:bootstrap"
homepage: https://docs.openclaw.ai/automation/hooks
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "events": ["agent:bootstrap"],
        "requires": { "config": ["workspace.dir"] }
      },
  }
---

# Super Memori Session-Start Hook

Runs `startup-self-check.sh` exactly once per new OpenClaw session by listening to the real
internal `agent:bootstrap` event and recording the handled `sessionId` in a local ledger.

## Why

`agent:bootstrap` is a real runtime hook point in OpenClaw's bootstrap-context pipeline.
By itself it is not guaranteed to mean "only the first turn of a session" because bootstrap
context can be rebuilt again later. This hook adds a per-session ledger so the startup self-check
runs only once for each new `sessionId`, making the behavior enforceable at session scope.

## Configuration

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "load": {
        "extraDirs": [
          "/home/irtual/.openclaw/workspace/skills/super_memori/hooks"
        ]
      },
      "entries": {
        "super-memori-session-start": {
          "enabled": true,
          "command": "cd /home/irtual/.openclaw/workspace/skills/super_memori && ./startup-self-check.sh --json --repair --report-file /home/irtual/.openclaw/workspace/memory/index-state/startup-self-check-last.json",
          "ledgerFile": "/home/irtual/.openclaw/workspace/memory/index-state/session-start-hook-ledger.json",
          "reportFile": "/home/irtual/.openclaw/workspace/memory/index-state/startup-self-check-last.json",
          "injectBootstrapReport": true,
          "maxLedgerEntries": 400
        }
      }
    }
  }
}
```

## Notes

- This hook does **not** rely on the model following instructions in `AGENTS.md`.
- It uses a real OpenClaw internal hook event: `agent:bootstrap`.
- The one-shot guarantee is enforced by the ledger keyed by `sessionId`.
- The report is written to `memory/index-state/startup-self-check-last.json`.
- When enabled with `injectBootstrapReport=true`, the latest report summary is appended as an
  extra bootstrap context file for the first handled turn of the session.
