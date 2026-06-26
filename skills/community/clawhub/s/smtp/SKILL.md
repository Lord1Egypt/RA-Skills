---
name: SMTP
slug: smtp
version: 1.0.0
homepage: https://clawic.com/skills/smtp
description: "Send, test, and debug SMTP mail flows with safe dry runs, provider-aware auth, and deliverability checks."
changelog: "Initial release with safe SMTP send flow, provider profiles, auth diagnostics, and deliverability checks."
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/smtp/"]}}
---

## When to Use

Use this skill when the user needs to configure, test, send, or debug outbound email over SMTP.
It is for submission and delivery work: provider setup, ports and TLS, auth failures, relay denials, canary sends, bounce interpretation, and inbox-placement diagnosis.

## Architecture

Memory lives in `~/smtp/`. If `~/smtp/` does not exist, run `setup.md`. Use `memory-template.md`, `memory.md`, `provider-profiles.md`, `send-log.md`, and `deliverability-notes.md` as the local baseline.

```text
~/smtp/
├── memory.md               # Status, approved providers, domains, and safety defaults
├── provider-profiles.md    # Known-good hosts, ports, auth mode, and sender identity notes
├── send-log.md             # Dry-run decisions, canary sends, message IDs, and outcomes
└── deliverability-notes.md # SPF, DKIM, DMARC, bounce, and inbox-placement learnings
```

## Quick Reference

| Topic | File | Use it for |
|-------|------|------------|
| Setup and first-run guardrails | `setup.md` | Initialize `~/smtp/` without storing secrets or sending mail too early |
| Memory structure | `memory-template.md` | Create `~/smtp/memory.md` with status and stable context |
| Baseline memory example | `memory.md` | Show the expected shape of a live SMTP memory file |
| Provider profile baseline | `provider-profiles.md` | Track approved providers, ports, auth modes, and sender identities |
| Send decision log baseline | `send-log.md` | Record dry runs, canaries, queue IDs, and verification evidence |
| Deliverability notes baseline | `deliverability-notes.md` | Capture DNS auth status, spam-folder evidence, and bounce patterns |
| Safe execution workflow | `send-flow.md` | Run draft -> preflight -> canary -> verify -> scale |
| Fault isolation guide | `diagnostic-playbook.md` | Separate DNS, TLS, auth, relay, and placement failures |
| Deliverability rules | `deliverability.md` | Check SPF, DKIM, DMARC, alignment, and inbox placement |
| CLI probe patterns | `swaks-recipes.md` | Use deterministic SMTP tests with placeholder-only examples |

## Requirements

- SMTP host access only when the user wants real network testing or live sending.
- Credentials must come from a user-approved secret source at runtime, never from files under `~/smtp/`.
- Recommended tools: `swaks` for SMTP probes, `openssl` for TLS inspection, and `dig` or `nslookup` for DNS checks.
- Explicit confirmation before any live send, external-recipient test, or multi-recipient action.

## Core Rules

### 1. Separate Draft, Probe, and Live Send
- Decide which mode the task is in before touching the network: draft-only, connectivity probe, auth probe, canary send, or live send.
- Draft and explain first. Do not jump from "help me configure SMTP" to "message sent."

### 2. Match Port, TLS, and Auth Exactly
- Port 465 means implicit TLS. Port 587 usually means STARTTLS. Port 25 is relay transport and is often blocked or policy-limited.
- Treat host, port, TLS mode, and auth mechanism as one contract. A single mismatch can look like a generic timeout or auth error.

### 3. Debug One Layer at a Time
- Validate in order: DNS and hostname, TCP reachability, TLS handshake, EHLO capabilities, auth, submission response, then mailbox placement.
- Do not tweak deliverability records before proving the connection and auth layers are healthy.

### 4. Keep Sender Identity Aligned
- Check whether the authenticated account, envelope sender, visible From address, DKIM domain, and return-path domain actually belong together.
- Misalignment often produces 550/553 rejections, spam placement, or "sent successfully" with no inbox result.

### 5. Canary Before Scale
- The first live test should target one approved canary recipient, ideally on the same org or a controlled inbox.
- Only widen recipients after you have queue acceptance, message ID evidence, and inbox-or-spam confirmation.

### 6. Handle Credentials and Logs Safely
- Never write raw SMTP passwords, API tokens, or full secrets into `~/smtp/`.
- Redact logs and screenshots before storing or sharing them. Keep only the smallest evidence needed to debug.

### 7. Acceptance Is Not Delivery
- A `250 queued` or similar server response means the SMTP server accepted the message, not that the recipient inbox accepted it.
- Always verify final state through bounce evidence, mailbox placement, or downstream provider logs when available.

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Treating port 465 and 587 as interchangeable | TLS handshake breaks or auth never starts | Match implicit TLS vs STARTTLS explicitly |
| Changing SPF before fixing auth | Wrong layer, no effect on login failure | Prove DNS, TLS, and auth separately |
| Assuming `250` means inbox success | Queue acceptance is not mailbox placement | Check spam, bounces, and final recipient evidence |
| Using external recipients as the first test | Increases blast radius and risk | Start with one approved canary inbox |
| Disabling certificate checks to "make it work" | Hides real TLS or hostname issues | Fix hostname, CA trust, or port selection instead |
| Letting From differ wildly from auth identity | Triggers relay denial or spam scoring | Align sender identity or document the relay policy |

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| Configured SMTP submission server, such as `smtp.example.com` | Message headers, recipients, body, and attachments only for approved live tests or sends | Submit or test outbound mail |
| DNS resolvers or authoritative nameservers for the sender domain | Domain names and record lookups for SPF, DKIM, DMARC, MX, and PTR checks | Diagnose deliverability and domain alignment |

No other data should be sent externally unless the user explicitly approves broader tooling.

## Data Storage

Local state in `~/smtp/` includes:

- activation state, approved providers, and safety defaults in `memory.md`
- known-good server profiles and sender-identity notes in `provider-profiles.md`
- dry-run decisions, canary evidence, and message IDs in `send-log.md`
- domain-auth and placement findings in `deliverability-notes.md`

## Security & Privacy

**Data that leaves your machine:**
- SMTP envelope and message content only during approved probes or live sends
- DNS queries needed to validate sender-domain health and routing

**Data that stays local:**
- safe defaults and approved provider context in `~/smtp/memory.md`
- known-good provider settings and debugging evidence in `~/smtp/provider-profiles.md`, `~/smtp/send-log.md`, and `~/smtp/deliverability-notes.md`

**This skill does NOT:**
- send live mail without explicit confirmation
- store raw SMTP passwords or tokens in local memory
- modify DNS records, mailing lists, or provider settings unless the user explicitly asks
- disable TLS verification silently
- modify its own skill definition

## Trust

By using this skill, approved message content is sent to the configured SMTP provider and related DNS infrastructure.
Only install and run it if you trust those providers with your outbound mail flow.

## Scope

This skill ONLY:
- helps configure and diagnose outbound SMTP submission
- maintains small local notes in `~/smtp/`
- runs canary-first send workflows with explicit confirmation gates

This skill NEVER:
- guess live-send approval from vague user intent
- keep credentials in `~/smtp/`
- treat queue acceptance as the final delivery result
- broaden a one-off test into a bulk-send workflow without consent

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `mail` - broader mailbox operations across IMAP, SMTP, and Apple Mail workflows
- `dns` - deeper DNS record work for SPF, DKIM, DMARC, MX, and TTL changes
- `network` - port reachability, TLS, and connection debugging beyond mail workflows
- `newsletter` - message design and campaign structure once SMTP delivery is healthy
- `email-marketing` - deliverability and audience strategy after the send path is stable

## Feedback

- If useful: `clawhub star smtp`
- Stay updated: `clawhub sync`
