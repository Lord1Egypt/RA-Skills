---
name: truclaw
description: Biometric guardrail for OpenClaw. Intercepts dangerous tool calls and requires Face ID verification via TruClaw iOS app before execution. Biometric processing is on-device only. A relay (Cloudflare Worker, source included) handles push delivery and JWT exchange.
metadata: {"openclaw": {"emoji": "🔐", "homepage": "https://github.com/sanjaymk908/trukyc-openclaw", "requires": {"env": ["ANTHROPIC_API_KEY_TRUKYC", "TRUKYC_RELAY_URL"]}, "install": [{"id": "npm", "kind": "node", "package": "openclaw-truclaw", "bins": [], "label": "Install TruClaw plugin (npm)"}]}}
---

# TruClaw — Biometric AI Guardrail

TruClaw stops your OpenClaw agent from executing dangerous actions without
verified human authorization. When a sensitive tool call is detected — deleting
files, sending messages, running shell commands — TruClaw sends a push
notification to your iPhone. Complete Face ID to authorize. Ignore it to block.

Every authorization is backed by a **Secure Enclave-signed JWT** — hardware
attestation that cryptographically proves a live human authorized the action
on a specific trusted device. No chat account compromise, no prompt injection,
no replay attack can forge this.

---

## Privacy and cloud usage — what runs where

| Component | Where it runs |
|---|---|
| Face matching and biometric processing | On-device only — Apple Vision framework |
| Biometric data (photos, face vectors) | Never leaves your iPhone |
| Danger classification (Claude Haiku) | Anthropic API — tool name and args only, no personal data |
| Push delivery | Cloudflare Worker relay + Firebase Messaging — session token only, no personal data |
| JWT signing | iPhone Secure Enclave — key never leaves device |
| Relay source code | Fully open: https://github.com/sanjaymk908/trukyc-openclaw/tree/main/cloudflare-worker |

The relay handles two things only: forwarding FCM push notifications to your iPhone,
and temporarily storing the signed JWT (auto-deleted after 2 minutes) for the plugin
to pick up. It never sees biometric data, photos, or personal information.

You can self-host the relay on your own Cloudflare account using the included
source code if you prefer not to use the shared relay endpoint.

---

## Security transparency

- Plugin source: https://github.com/sanjaymk908/trukyc-openclaw/tree/main/
- Relay source: https://github.com/sanjaymk908/trukyc-openclaw/tree/main/cloudflare-worker
- The plugin runs in a privileged before_tool_call hook — review the source before installing
- The relay domain is trukyc-relay.trusources.workers.dev (Cloudflare Workers, owned by plugin author)
- Self-hosting the relay is supported and documented in the README

---

## Requirements

- OpenClaw 3.28+
- TruClaw iOS app (search "TruClaw" on App Store)
- Anthropic API key (for Claude Haiku danger classification — tool names and args only)
- TRUKYC_RELAY_URL (default shared relay provided, self-hosting supported)

---

## Setup (3 steps)

### Step 1 — Install TruClaw iOS app

Search "TruClaw" on the App Store. Complete one-time enrollment:
- Take a selfie
- Scan your Driver's License or Passport
- Green badge confirms successful enrollment

Your biometric profile is stored encrypted in your iPhone Secure Enclave.
No photos or biometric data leave your device at any point.

### Step 2 — Install and configure plugin
git clone https://github.com/sanjaymk908/trukyc-openclaw.git
mv trukyc-openclaw truclaw
cd truclaw
npm install && npm run build

Add to ~/.openclaw/openclaw.json plugins section:
"plugins": {
"load": {
"paths": ["/path/to/truclaw"]
},
"entries": {
"truclaw": { "enabled": true, "config": {} }
}
}

Add env vars:
"env": {
"TRUKYC_RELAY_URL": "https://trukyc-relay.trusources.workers.dev",
"ANTHROPIC_API_KEY_TRUKYC": "your-anthropic-api-key"
}

Restart OpenClaw:
openclaw gateway stop && sleep 3 && openclaw gateway install && sleep 5
openclaw plugins list | grep trukyc

### Step 3 — Pair your iPhone

Run in any OpenClaw channel:
/trukyc-pair

A QR code appears. Scan it with the TruClaw iOS app. Done.

---

## How it works

1. OpenClaw Agent detects a tool call
2. TruClaw Plugin intercepts via before_tool_call hook
3. Claude Haiku classifies the tool call as safe or dangerous
4. If dangerous: TruClaw Relay sends push notification via Firebase Messaging
5. TruClaw iOS App receives notification on your iPhone
6. User completes Face ID biometric match
7. iPhone Secure Enclave signs authorization JWT — hardware-bound, tamper-proof
8. Plugin polls relay, receives and verifies JWT
9. isAbove21=true → action proceeds / isAbove21=false → action blocked

---

## TruClaw vs native OpenClaw approval

| | OpenClaw /approve | TruClaw Biometric |
|---|---|---|
| Authorization method | Text command in chat | Face ID on iPhone |
| Proof of human | None | Secure Enclave hardware attestation |
| Spoofable | Yes — compromised account approves | No — requires physical device + live biometric |
| Audit trail | Chat message | Signed JWT with timestamp and device ID |
| Enterprise compliance | No cryptographic proof | Hardware-attested human proof |

---

## What gets flagged as dangerous

- Shell commands that write, delete, or modify (rm, mv, cp)
- Network requests that send data (curl POST, wget)
- Installing software (pip install, npm install)
- Sending messages or emails
- Financial operations, killing processes, modifying permissions

## What passes through safely

- Read-only shell commands (ls, cat, grep, find)
- Querying data or answering questions
- Git read operations (git status, git log, git diff)
- Explicitly safe tools: read, ls, list, session_status, memory_search

---

## Self-hosting the relay

If you prefer not to use the shared relay endpoint, deploy your own:
cd trukyc-openclaw/cloudflare-worker
wrangler deploy worker.js

Then update TRUKYC_RELAY_URL in openclaw.json to your own worker URL.
Full instructions: https://github.com/sanjaymk908/trukyc-openclaw/tree/main/cloudflare-worker

