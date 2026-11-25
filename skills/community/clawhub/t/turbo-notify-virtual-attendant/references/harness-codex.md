# Codex

Codex can run the attendant **unattended** (recommended) or in session in assisted mode only.

## Install and keep it current

```
codex plugin marketplace add turbo-notify/agent-skills --ref v1
codex plugin add turbo-notify@turbo-notify
```

`--ref v1` keeps you on the 1.x line. Codex does not update plugins on its own. Each cycle checks the version and tells the administrators when a new one exists; to update, run:

```
codex plugin marketplace upgrade
codex plugin add turbo-notify@turbo-notify
```

## Connect Turbo Notify

The plugin already declares the server (`.mcp.json`). Check it with `codex mcp list` and sign in with `codex mcp login turbo-notify`. The unattended mode below uses an API key instead.

## Unattended (recommended)

```
export TURBO_NOTIFY_API_KEY=tn_live_…
export TN_ASSIST_BASE=~/.turbo-notify/attendant TN_ASSIST_ORG=org_… TN_ASSIST_NUMBER=num_…
python3 <skill folder>/scripts/tn_assist run --harness codex
```

- Needs: Codex logged in on this machine, Python 3.9 or newer, the computer on and online.
- Each model turn runs in a fresh `codex exec` process in a read-only sandbox, with no shell, no connectors and no plugins, in an empty folder, and with a **private copy of the Codex home that holds only the login**. This matters: Codex still reads the `AGENTS.md` of its home when it is asked to ignore user configuration, so a customer's process would otherwise see your personal instructions.
- A customer's process has no tools and no key. An administrator's process gets only the read tools of Turbo Notify.
- Idle cycles cost no model tokens. Interval, logs and stopping work as in [harness-claude-code.md](harness-claude-code.md).

## In session

Codex cannot give a conversation with no tools, so work in **assisted mode only**: every answer is a draft that a person approves. Follow [tick.md](tick.md) and [contact-turn.md](contact-turn.md), one customer at a time, and say this limit to the person who set it up.

## What it cannot do

It does not run when the computer is off or Codex is not logged in.
