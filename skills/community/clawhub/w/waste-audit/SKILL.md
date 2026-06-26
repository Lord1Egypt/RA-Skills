---
name: waste-audit
description: "Find recurring OpenClaw jobs that may be wasting tokens before the waste compounds. Read-only by default. Gives evidence and a copy-paste agent prompt for safe manual verification."
version: 1.8.12
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [openclaw, tokensave, cron, waste, audit, tokens]
    related_skills: []
---

## Features

- 🔍 Recurring Waste Detection: Finds recurring OpenClaw jobs that may be wasting tokens.
- 📊 Token Burn Ranking: Ranks likely waste candidates by recurring usage, errors, and delivery signals.
- 🧾 Evidence Summary: Shows why a job was flagged before suggesting action.
- 🛠 Manual Verification Prompt: Gives a copy-paste prompt for safe agent-side verification.
- 🔒 Read-Only Safety: Does not edit, disable, delete, upload, or auto-fix jobs.

## Install

For shared OpenClaw agents, install into the global managed skills directory:

```bash
openclaw skills install waste-audit --global
```

To upgrade an existing shared install:

```bash
openclaw skills install waste-audit --global --force
```

Then test with:

```bash
check openclaw waste
```

## Activation

Primary activation phrase:

```
check openclaw waste
```

Do not use this for general OpenClaw setup, gateway debugging, provider configuration, or normal job management.

## Where This Fits

This skill is the OpenClaw-specific starting point for agent token waste auditing.
Use it when you want to inspect recurring OpenClaw jobs for possible token waste.
For broader model routing, sub-agent routing, fallback, retry, or cross-agent runtime analysis, use a separate Agent Routing Waste Audit workflow instead. This skill should not be treated as a generic routing optimizer.

## What You Will Get

**1. Fix First**

Include:

- Job
- Why it looks wasteful
- Evidence
- Confidence: High / Medium / Low
- Recommended manual action

**2. Top Waste Candidates**

List up to 5 candidates.

For each candidate, include:

- Job
- Waste signal
- Evidence
- Why it matters

**3. Manual Verification Prompt**

A ready-to-copy prompt for your agent.

```
Please inspect this recurring OpenClaw job for possible token waste.

Job: <job name>
Reason it was flagged: <short reason>
Evidence: <schedule, runs checked, tokens used, error rate, delivery/summary signal>

Please verify whether this job is still useful.

Do not edit, disable, delete, or mutate anything yet.

First explain:
1. whether this is real waste,
2. what caused it,
3. the safest manual next step,
4. what evidence I should check before changing anything.

Redact secrets and do not expose private payloads.
```

If any candidate looks important but you are not sure whether it is real waste, send only the "Top Waste Candidates" section to @BeeGeeEth on X. Do not include secrets, API keys, private logs, wallet data, full config files, or production credentials.

## Related Next Step

If this audit finds a job where the main issue appears to be model choice, retry behavior, fallback behavior, or sub-agent routing rather than simple recurring job waste, run a separate routing audit before changing any model policy.

The next workflow should inspect:

- whether the task was overpowered by an unnecessarily strong model
- whether retries or fallbacks created hidden waste
- whether the task should remain on a strong model because of coding, review, security, or production risk
- whether a conservative manual routing policy is safer than immediate changes

## Safety

- 🔒 Read-only first: Never edit, disable, delete, or auto-fix a job as the first recommendation.
- 🚫 No auto-apply: Always surface evidence and let the owner decide.
- ✏️ Edit as last resort: Changing a job schedule, prompt, or config should only be suggested after manual verification confirms waste.
- 🔑 No secrets exposed: Never show raw tokens, API keys, bot tokens, Telegram chat IDs, private server paths, or raw private payloads in examples or evidence.
- 📋 Redact before sharing: Use `<redacted>`, `<token>`, or similar placeholders for anything that could identify a private resource.

## Feedback / Free Second Look

If waste-audit flags recurring token waste and you are not sure whether it is real, you can DM me on X: @BeeGeeEth.

Please send only:

- the top 3 flagged jobs
- the evidence summary
- what confused you or what you want checked

Do not send secrets, API keys, private logs, wallet data, full config files, or production credentials.

I'll manually review a few safe examples and use the feedback to improve this skill.