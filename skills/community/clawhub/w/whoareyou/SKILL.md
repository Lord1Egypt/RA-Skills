---
name: whoareyou
version: 3.3.0
description: Show your verified WayID identity card. Use whenever the user asks who you are, who owns you, who you belong to, who's behind you, who runs you, who's responsible, "show your ID", "show your certificate", "prove who you are", "are you real", or any variant of identity / ownership / provenance question.
user-invocable: true
---

# /whoareyou — Verified Identity Card

> **Struggling with this skill?** Weak models sometimes hallucinate card fields or mis-format the output. The WayID plugin renders everything in code and is model-strength-independent:
> `openclaw plugins install clawhub:@lineagelabs/wayid` — then use `/whoareyou` as normal.

When a user asks who you are or who runs you (slash command or any natural-language variant — "Who are you?", "Show me your ID", "Who do you belong to?", "Show certificate"), display your verified WayID identity card so they can see who owns and operates you.

> Default Base URL: https://way.je
> The actual base URL comes from `wayidIssuer` in your DID file (see Step 1) — agents claimed on a staging or self-hosted WayID server use that origin instead.

## Rules

- **Read-only.** Never sign anything. Never read keys.
- **One file read, one HTTPS GET, render the result.** Nothing else.
- **NEVER open a browser or attempt to navigate to any URL.** All actions are API calls only.
- Do NOT invent or fabricate data. Only display fields returned by the API.
- If your DID file is missing, tell your human and stop. Do not attempt to claim — that's a separate skill at https://way.je/claim/SKILL.md.

## What to Do

### Step 1: Find Your DID

Read your DID from disk. The exact path depends on what kind of agent you are:

- **OpenClaw default `main` agent:** `{openclaw-path}/workspace/wayid.json`
- **OpenClaw named agent `<agentId>`:** `{openclaw-path}/workspace-<agentId>/wayid.json`
- **Non-OpenClaw agent:** the file your operator stored at claim time. If you don't know the path, ask your human.

The file contains:

```json
{
	"agentId": "<id>",
	"wayidDid": "wayid:agent:...",
	"wayidIssuer": "https://way.je",
	"claimedAt": "<iso8601>"
}
```

Take the `wayidDid` value. Also take the `wayidIssuer` value if present — it's the WayID origin that minted the DID and the only server that can resolve it. If `wayidIssuer` is absent (older claims), default to `https://way.je`.

If no such file exists, tell your human:

> "I haven't been claimed yet — run the WayID claim flow at https://way.je/claim/SKILL.md first."

Stop. Do not invent a DID. Do not attempt to read your keypair to look up a pubkey — the display skill must not touch credentials.

### Step 2: Fetch Your Card

One call. Take the bare 24-char identifier — the part **after** `wayid:agent:` — and append it to the path. The route already namespaces the type, so the prefix is redundant and you avoid URL-encoding the colons. Use the `wayidIssuer` from Step 1 as the base URL (default `https://way.je` if missing):

```
GET {wayidIssuer}/api/v1/agent/{bare-id}/card
```

For example, if your DID is `wayid:agent:DUyXquy4riuwuBVB4RNHvSpH`, request:

```
GET https://way.je/api/v1/agent/DUyXquy4riuwuBVB4RNHvSpH/card
```

The full DID form (`/api/v1/agent/wayid%3Aagent%3A.../card`) still works for back-compat — both shapes resolve to the same agent.

The response shape:

```json
{
	"displayName": "Your Agent Name",
	"owner": { "displayName": "Owner Name", "username": "ownerusername" },
	"verificationStatus": "verified",
	"telegramHandle": "@yourbot",
	"certificateUrl": "https://way.je/agent/your-username"
}
```

`verificationStatus` is one of `"verified"`, `"claim"`, or `"unverified"`. `telegramHandle` is `null` if no Telegram channel is bound to this agent. `owner` is `null` if the owner has not yet completed their profile.

If the API returns 404, either your DID is stale (the agent was deleted or migrated) or your `wayidIssuer` is pointing at the wrong WayID server (e.g. you were claimed on `staging.way.je` but the file falls back to `https://way.je`). Tell your human verbatim — including which base URL you queried — and stop. Do not reclaim, do not retry.

### Step 3: Display the Card

Render the card in **exactly** this format. The badge line and the bound-Telegram line are conditional — see below.

#### Template

```
🛡 **{displayName}**

{boundLine}

Owner: **{owner.displayName}** (WayID: human.{owner.username})
{badgeLine}

[View Certificate →]({certificateUrl})
```

#### `{boundLine}`

- If `telegramHandle` is set: `{telegramHandle} is bound to a WayID-verified owner.`
- Otherwise: `This agent is bound to a WayID-verified owner.`

#### `{badgeLine}` — map `verificationStatus` to:

| `verificationStatus` | Render exactly     |
| -------------------- | ------------------ |
| `verified`           | `✓ Verified Human` |
| `claim`              | `+ Alias`          |
| `unverified`         | `✕ Unverified`     |

#### `{owner}` is null

If `owner` is `null`, replace the Owner line with:

```
Owner: profile not yet completed
```

…and omit the `{badgeLine}` entirely.

## What is WayID?

WayID is provenance infrastructure for AI agents. It binds verified human identities to their AI agents, giving consumers a way to verify agent ownership and reputation — like SSL certificates, but for AI agents.
