---
name: sentinel-proxy
title: Sentinel-Proxy AI Firewall
description: AI Firewall for Open Claw agents. Scrubs inbound messages and tool results for prompt injection, jailbreaks, and data exfiltration attempts using Sentinel's multi-layer detection pipeline.
version: 1.0.0
author: skyblue-soft
license: MIT
homepage: https://github.com/c0ri/sentinel-skills 
---

# Sentinel AI Firewall

Protect your Open Claw agent from prompt injection, jailbreaks, malicious skill output, and data exfiltration — automatically, on every message and tool result.

## What It Does

Sentinel intercepts three critical points in the agent lifecycle:

- **`UserPromptSubmit`** — user input is scrubbed before your agent processes it
- **`PreToolUse`** — scans what your agent is about to send to a tool, blocking data exfiltration before it leaves the session
- **`PostToolUse`** — scans tool/skill responses before they reach the agent, catching malicious skills that try to hijack your agent via crafted output

`PreToolUse` is the primary defense against the malicious Clawhub skill attack pattern, where a compromised skill returns a crafted response designed to take over the agent or steal session data.

## Setup

### 1. Get a Sentinel API key

Sign up at [sentinel-proxy.skyblue-soft.com](https://sentinel-proxy.skyblue-soft.com) — free Starter tier available, no credit card required.

### 2. Set environment variables

```bash
export SENTINEL_API_URL=https://sentinel.ircnet.us
export SENTINEL_KEY=sk_live_...
```

Add these to your shell profile or `.env` file so they persist across sessions.

### 3. Install the skill

```bash
openclaw skills install sentinel
```

That's it. The bootstrap hook will verify your credentials on next agent start.

---

## Transparent Proxy Mode (Recommended)

For complete protection — including scanning what your agent sends *to* external tools — route your LLM traffic through Sentinel's transparent proxy. Sentinel sits between Open Claw and the Anthropic API, scanning all content in both directions with zero changes to your agent code.

```bash
export ANTHROPIC_BASE_URL=https://sentinel.ircnet.us/v1
export ANTHROPIC_API_KEY=sk_live_...   # your Sentinel key replaces your Anthropic key here
```

Your agent uses the Anthropic SDK exactly as before. Sentinel proxies the request, scans tool results before they return to your agent, and passes clean traffic through with no overhead.

---

## Detection Layers

Every scrub request runs through three layers:

1. **Text normalization** — strips invisible characters, Unicode homoglyphs, bidi overrides, and Unicode tag blocks before scanning
2. **Fast-path regex** — 22 patterns catch high-confidence attacks (authority hijacks, prompt extraction, persona shifts, tool abuse) with near-zero latency
3. **Deep-path vector similarity** — semantic embedding compared against 30+ attack signatures in pgvector; catches novel attacks that bypass regex

### Actions

| Action | Meaning | Hook behavior |
|--------|---------|---------------|
| `clean` | No threat detected | Content passes through |
| `flagged` | Borderline — above flag threshold | Content passes through, warning logged |
| `neutralized` | Attack detected and rewritten | Safe version used instead |
| `blocked` | High-confidence attack (similarity > 0.82) | Content rejected, agent protected |

---

## Scrub Tier

The hooks use `standard` tier by default. To switch to `strict` mode (lower thresholds, more aggressive):

```bash
export SENTINEL_TIER=strict
```

---

## What Gets Logged

Sentinel does not log or store the content of clean requests. Flagged, neutralized, and blocked events are logged locally by the hook scripts with the threat score and action taken.
