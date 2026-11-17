---
name: psyseal-scan
description: "Offline, read-only scan of your AI agent (OpenClaw, Hermes Agent, nanobot, PicoClaw, ZeroClaw, NanoClaw or any agent folder): what loads on every message, what heartbeats and scheduled tasks cost, plaintext secrets, and planted or bloated memory. No network, no dependencies."
version: 0.3.3
metadata:
  openclaw:
    emoji: "🩺"
    homepage: https://github.com/psyseal/psyseal-scan
    requires:
      bins:
        - node
    envVars:
      - name: OPENCLAW_CONFIG_PATH
        required: false
        description: "Alternative path to openclaw.json (read only)."
      - name: OPENCLAW_STATE_DIR
        required: false
        description: "Alternative OpenClaw state directory (read only)."
      - name: OPENCLAW_PROFILE
        required: false
        description: "Profile name; selects the ~/.openclaw-<profile> state directory (read only)."
      - name: OPENCLAW_WORKSPACE_DIR
        required: false
        description: "Alternative workspace directory (read only)."
      - name: OPENCLAW_INCLUDE_ROOTS
        required: false
        description: "Extra directories allowed for $include files in the config (read only)."
      - name: OPENCLAW_CACHE_RETENTION
        required: false
        description: "If set to long, the heartbeat estimate assumes a 1-hour prompt cache."
      - name: HERMES_HOME
        required: false
        description: "Alternative Hermes Agent home (read only)."
      - name: PICOCLAW_HOME
        required: false
        description: "Alternative PicoClaw home (read only)."
      - name: PICOCLAW_CONFIG
        required: false
        description: "Alternative PicoClaw config file (read only)."
      - name: PICOCLAW_AGENTS_DEFAULTS_WORKSPACE
        required: false
        description: "PicoClaw workspace override, read the same way PicoClaw reads it."
      - name: PICOCLAW_HEARTBEAT_ENABLED
        required: false
        description: "PicoClaw heartbeat switch, read to estimate heartbeat cost."
      - name: PICOCLAW_HEARTBEAT_INTERVAL
        required: false
        description: "PicoClaw heartbeat interval, read to estimate heartbeat cost."
      - name: ZEROCLAW_CONFIG_DIR
        required: false
        description: "Alternative ZeroClaw config directory (read only)."
      - name: ZEROCLAW_WORKSPACE
        required: false
        description: "ZeroClaw workspace override (read only)."
      - name: NANOCLAW_DIR
        required: false
        description: "Folder of a NanoClaw install (read only)."
      - name: PSYSEAL_LANG
        required: false
        description: "Report language, es or en."
      - name: PSYSEAL_ASCII
        required: false
        description: "Set to 1 for plain ASCII output."
      - name: LANG
        required: false
        description: "Only read to pick the report language."
      - name: LC_ALL
        required: false
        description: "Only read to pick the report language."
      - name: LC_MESSAGES
        required: false
        description: "Only read to pick the report language."
---

# psyseal-scan

Offline, read-only review of the AI agents on this machine. Every finding comes with a concrete fix. It checks:

1. **What loads on every message** - size of the instruction and memory files, and which ones get cut silently.
2. **Scheduled tasks and heartbeats** - runs per day and monthly cost (tokens, and dollars when the model price is known).
3. **Plaintext secrets** in memory, instructions and skills, plus credential files other users can read - reported as type, file and line only, never the value.
4. **Planted or bloated memory** - text that looks like a planted instruction, invisible characters, repeated lines and giant blobs.

## When to use it

The owner asks to check the agent's memory, to understand a high bill, to check for leaked keys, or to check whether memory was tampered with.

## Run

```bash
node {baseDir}/scripts/psyseal-scan.mjs --lang en --exit-zero
```

Optional flags: `--path <folder>`, `--platform <id>`, `--agent <id>`, `--json`, `--no-cta`. See `--help`.

## Rules for the agent

- Show the owner the report as printed. Do not restate the figures from memory: they are estimates.
- The report never contains secret values or memory text, on purpose. Do not open the flagged lines and paste them into the chat; give the owner the file and line so they open it themselves.
- Do not edit config, delete or rewrite memory, or rotate keys on your own. Offer each fix and wait for the owner's explicit OK.
- Exit codes: 0 no high-severity findings, 1 high-severity findings (`--exit-zero` turns this into 0), 2 usage error.

## What it touches

The scanner reads only the agents' config, instruction, memory and skill files. It does not use the network, write files, start other programs or follow symlinks. It has no dependencies: plain Node.js 20 or newer.

## About the maker

This skill is the free Psyseal scanner (MIT-0). Psyseal also sells a cleanup that fixes the findings (with a backup and the owner's OK on each change) and a signed seal, at https://psyseal.com. Those are separate programs, they are not part of this skill, and the scan is free and complete without them. The report ends with one line linking to psyseal.com; the scanner only prints that link and never opens it, and `--no-cta` removes it.

Full source of the scanner: https://github.com/psyseal/scanner
