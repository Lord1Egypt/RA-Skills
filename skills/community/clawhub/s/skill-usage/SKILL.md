---
name: skill-usage-setup
version: 0.1.0
description: |
  Install and set up the OpenClaw Skill Usage plugin.

  Use when users say:
  - "install skill usage"
  - "setup skill usage"
  - "add skill usage analytics"
  - "install leaderboard plugin"
  - "track which skills are used most"
  - "setup shared skill leaderboard"
  - "enable /skillusage"

license: MIT
author: lucifinil
homepage: https://github.com/lucifinil/openclaw-skill-usage
metadata:
  openclaw:
    emoji: "📊"
---

# Skill Usage Setup

Install and configure the **OpenClaw Skill Usage** plugin.

This skill performs three kinds of actions as part of its normal purpose:

1. installs an external npm package (`openclaw-skill-usage`)
2. restarts the OpenClaw Gateway so the plugin can load
3. optionally enables cloud-backed usage analytics by writing usage metadata to a TiDB Cloud Zero instance

Use it only when the user explicitly wants skill-usage analytics and understands the local-vs-cloud tradeoff.

After setup, users can:

- see which skills are actually being used
- rank skills for `1d`, `7d`, `30d`, and `all`
- break usage down by installation, agent, and channel account
- optionally join multiple OpenClaw installations into one shared leaderboard

---

## Safety / consent rules

- Installing this plugin is an external package installation.
- Restarting the gateway is a privileged local operation.
- Shared usage-space setup writes usage metadata to a TiDB Cloud Zero backend.
- Do not do cloud/shared setup silently; only continue if the user explicitly wants it.
- If the user only wants local analytics, stop after install/restart/verify and do not push them into join/shared setup.

---

## Trigger phrases

Use this skill when the user expresses intent to install, enable, or configure skill usage analytics.

Common triggers include:

- "install skill usage"
- "setup skill usage"
- "add usage analytics"
- "show which skills are used most"
- "enable /skillusage"
- "setup shared skill leaderboard"
- "track skill usage across machines"

---

## When to use this skill

Use this skill when the user wants to:

- install the `openclaw-skill-usage` plugin
- enable `/skillusage` commands
- use the `skill_usage_stats` tool from agents
- check whether skill usage is working at all after install
- run basic usage queries such as `top` or `status`
- understand local-only vs shared usage spaces
- generate a join token for another installation
- connect another installation into the same usage space

This skill is especially appropriate when the user is still in the **setup / enablement / verification** phase and has not yet fully established the plugin on their machine.

---

## When NOT to use this skill

Do not use this skill for:

- deep analysis of already-working usage data when no setup or verification help is needed
- advanced troubleshooting unrelated to installing, enabling, restarting, verifying, or joining skill usage
- general OpenClaw gateway debugging outside the scope of this plugin

---

## What gets installed

This setup installs the npm package:

```bash
openclaw plugins install openclaw-skill-usage
```

This provides:

- `/skillusage` slash commands
- the `skill_usage_stats` tool
- local skill usage tracking
- optional TiDB Cloud Zero sync for shared usage spaces

Source repository:

- https://github.com/lucifinil/openclaw-skill-usage

### Privacy and data flow

By default, the plugin is useful locally and can still answer `top` / `status` with local-only data.

When cloud sync is used, the remote destination is a **TiDB Cloud Zero** instance created for the user's usage space. The plugin's `/skillusage status` output shows the cloud instance id and a claim URL for that instance.

That claim URL matters: the user can use it to **claim the TiDB Cloud Zero instance into their own TiDB Cloud account**, making the backend directly visible and controllable from their side rather than remaining an opaque shared service.

Cloud-backed analytics are part of the plugin's purpose, so the agent should describe them plainly instead of hiding them. The plugin is designed to sync **usage metadata**, not conversation content, so there should be no sensitive data. The intended synced fields are limited to:

- skill names
- installation labels
- agent labels
- channel labels
- timestamps, status, and latency

The plugin does **not** sync:

- message bodies or conversation text
- prompts or completions
- SKILL.md contents
- API keys, auth tokens, cookies, or other secrets

---

## Definition of Done

This task is **not complete** until all of the following are true:

1. the plugin is installed
2. the OpenClaw Gateway has been restarted
3. `/skillusage status` works
4. `/skillusage top 7d` works
5. if the user wanted cross-machine sharing, they were shown how to use `/skillusage join-token` and `/skillusage join <token>`

---

## Install flow

### Step 1 — Install plugin

Run:

```bash
openclaw plugins install openclaw-skill-usage
```

If the user is working from a local cloned repo instead of npm, a development install may use:

```bash
openclaw plugins install --link
```

But prefer the published npm package for normal setup.

### Step 2 — Restart Gateway

Run:

```bash
openclaw gateway restart
```

Before restarting, tell the user clearly that the gateway will restart and they may need to wait about a minute before testing commands.

### Step 3 — Verify install

Check:

```text
/skillusage status
/skillusage top 7d
```

A successful install should return usable output rather than a missing-command or plugin-load error.

---

## Example output

Compact top output:

```text
skill: weather (37)
- agent: elon 26 | main 10 | tim 1
- channel: disc/el 26 | wa 6 | tim 2 | unknown 3
=====================================
skill: skill-vetter (12)
- agent: main 9 | tim 2 | elon 1
- channel: wa 7 | disc/el 3 | tim 1 | unknown 1
=====================================
skill: github (8)
- agent: elon 6 | main 1 | unknown 1
- channel: disc/el 6 | wa 1 | unknown 1
```

Status output:

```text
Skill usage status:
data source: cloud-synced usage space
scope: current usage space
usage space: 7f2c... (joined)
this installation: Mac-mini
database: openclaw_skill_usage
cloud instance: zero_abc123
expires at: 2026-04-06T10:00:00.000Z
claim URL: https://...
synced totals: 38 triggers, 45 attempts
last observed at: 2026-03-08T07:40:00.000Z
last cloud sync: 2026-03-08T07:40:02.000Z
pending local records: 0
last sync error: none
metadata sent: skill id/name, installation id/label, channel account key/label/platform, agent id, routing/session identifiers, timestamps, status, latency
```

---

## Join / shared usage spaces

By default, one installation starts in its own local usage space.

Only proceed with shared usage-space setup if the user explicitly wants cross-machine sharing and understands that usage metadata will be written to the TiDB Cloud Zero instance for that usage space.

If the user wants to share usage across multiple installations:

### On installation 1

```text
/skillusage join-token
```

### On installation 2

```text
/skillusage join <token>
```

After join, `top` can show multiple installation blocks in one shared leaderboard.

---

## Notes for the agent

- Prefer npm installation for regular users.
- Mention that the plugin is useful even offline because local-only fallback still works.
- If the user asks about privacy, explain the exact remote destination (TiDB Cloud Zero) and the difference between local-only mode and cloud/shared mode.
- Be explicit that message content, prompts, completions, and secrets are not the intended synced payload; only usage metadata is.
- Still note that channel-account labels, routing identifiers, and installation labels may be sensitive metadata for some operators.
- If the user asks about installation from source, explain that local linked installs are mainly for development.

---

## Example agent actions

- "Install skill usage"
  - install `openclaw-skill-usage`
  - restart gateway
  - run `/skillusage status`
  - explain whether the result is local-only or cloud-synced

- "Check if skill usage is working"
  - run `/skillusage status`
  - run `/skillusage top 7d`
  - confirm that the plugin is loaded and returning usable analytics output

- "Show my top skills"
  - if setup is not complete yet, finish install/restart/verify first
  - then run `/skillusage top 7d` or use `skill_usage_stats`
  - explain the returned ranking in plain language

- "Set up a shared leaderboard across two machines"
  - install on both machines
  - restart gateway on both machines
  - run `/skillusage join-token` on machine 1
  - run `/skillusage join <token>` on machine 2
  - verify the joined result with `/skillusage status` and `/skillusage top 7d`

- "Enable /skillusage"
  - install plugin
  - restart gateway
  - confirm slash commands work
  - demonstrate `status` and `top`
