# TODO: Align wip-agent-pay with Universal Installer Spec

**Date:** 2026-02-24
**Source:** External feedback on mini/wire-coinbase branch
**Ref:** https://github.com/wipcomputer/wip-universal-installer

## What Already Aligns

- CLI interface exists (agent-pay)
- Worker server endpoints exist (POST /pool/pay, /pool/confirm, etc.)
- SPEC.md is present
- Skill concepts exist

## What Needs Work

### 1. Add a Machine-Readable Interface Spec (JSON/YAML)

Create a manifest file (`universal.json` or `AGENT-PAY.SPEC.json`) that enumerates:

```yaml
actions:
  pay-url:
    entrypoints:
      - cli: agent-pay pay
      - server: POST /pool/pay
    parameters:
      - name: targetUrl
        type: string
        required: true
  quote-url:
    entrypoints:
      - cli: agent-pay quote
      - server: POST /pool/pay (step 1)
    parameters:
      - name: targetUrl
        type: string
        required: true
```

### 2. Explicitly List Entry Points in a Manifest

Enumerate all agent-native operations:

```
command: agent-pay pay
server-route: POST /pool/pay
server-route: POST /pool/confirm
server-route: POST /wallet/create
server-route: POST /wallet/pay
purpose: unlock paywalled content
payment-model: "quote -> pay -> fulfill"
```

### 3. Map CLI Commands to SPEC Semantics

Link CLI commands directly to SPEC.md actions:

```
SPEC:
  ACTION pay-url:
    description: "pay for a URL via AGENT CASH"
    parameters:
      - targetUrl: string
```

### 4. Use Universal Installer Vocabulary in README

Add a section like:

> This repo exposes the following agent-native operations:
> - pay-url: pay for a URL via AGENT CASH
> - quote-url: fetch a quote for a paywalled URL

### 5. Clarify Types and Parameters in Structured Form

Each operation needs:
- targetUrl (string, required)
- quoteId (string, matched to a quote)
- payment authorization (signed with user consent)

## What This Unlocks

- AI agents can auto-discover what the repo does
- They can auto-invoke operations reliably
- They can integrate payment flows into workflows without ambiguous prompts
- They can compose wip-agent-pay into broader agent tasks (e.g., "agent pay for PDF, then summarize")

## Decision Needed

- JSON or YAML for the manifest?
- Embedded in repo (universal.json) or sidecar (AGENT-PAY.SPEC.json)?
