# Sapien ID: Agent Login Handoff Through Kaleidoscope

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** open, product spec and implementation ticket
**Master:** [`../kaleidoscope-master-ticket.md`](../kaleidoscope-master-ticket.md)
**Roadmap:** [`../kaleidoscope-roadmap.md`](../kaleidoscope-roadmap.md)
**Priority:** P0
**Product:** Sapien ID, Kaleidoscope, Agent Pay, Bridge
**Surface:** Production design target is Kaleidoscope. First implementation may reuse hosted-mcp primitives if that is still the live path.

## Summary

An AI agent should not be able to bypass login, payment, secrets, or permission boundaries. When the agent reaches a gated WIP surface, it should hit the boundary and ask the human through Kaleidoscope.

The human approves with phone biometrics. Kaleidoscope then creates or releases a scoped token that the agent can use for exactly the approved action.

This is Sapien ID: human-rooted authorization for AI agents.

## Product Statement

Agents cannot Face ID. Their humans can.

When an agent needs access, it should not steal credentials, ask for a long-lived API key, or pretend to be the human. It should explain what it needs and request a token from the human through Kaleidoscope.

The phone becomes the root of trust:

- the human sees the agent name and request
- the human sees the action, scope, cost, and duration
- the human approves with passkey/Face ID
- the agent receives only the scoped token
- the token can be inspected, limited, and revoked

## Why This Exists

The website launch surfaced the exact product requirement. Reviewer agents can read `https://wip.computer/`, GitHub, `agent.txt`, and `llms.txt`, but they cannot enter the gated demo or verify token-backed actions without a real passkey/session.

That is correct. The next product loop is not "let agents bypass login." The next product loop is:

```text
Agent reaches a gate.
Agent asks the human for permission.
Human approves on the phone.
Agent receives a scoped token.
Agent continues.
```

## Current Proven Pieces

The demo already proves the important parts:

- passkey login
- phone-rooted identity
- agent permission flow
- wallet and xAI microtransaction
- API token handoff after authenticated login
- agent auth challenge/poll pattern

Existing reference:

- `2026-04-07--cc-mini--features-to-preserve-from-demo.md`
- `ai/product/product-ideas/vision-quest-01/vision-quest-02-agent-txt-era.md`
- `src/hosted-mcp/demo/agent.html`
- `src/hosted-mcp/demo/agent.txt`
- `src/hosted-mcp/server.mjs`

## User Story

### Human

I want my AI to ask me before it gets access to accounts, tools, money, secrets, or private memory, so I stay in control without having to copy credentials around.

### Agent

I reached a gated action. I need a token, but I cannot authorize myself. I can describe the action, show the human a clear approval URL or QR code, poll for the result, and continue only if the human approves.

### Product

Kaleidoscope becomes the authorization surface that agents route through when they need human-backed identity.

## Core Flow

1. Agent reads `agent.txt`, `llms.txt`, an MCP auth error, or an API response that says Sapien ID approval is required.
2. Agent starts an authorization challenge.
3. Server creates a challenge with:
   - challenge ID
   - agent name
   - requested action
   - requested scopes
   - requested origin/tool
   - optional spend limit
   - expiry timestamp
   - human approval URL
4. Agent presents the approval URL to the human.
5. Human opens the URL on phone or desktop.
6. Human sees the agent identity, request, scope, duration, and spend limit.
7. Human approves with passkey/Face ID.
8. Server mints a scoped token.
9. Agent polls or receives the token through the supported channel.
10. Agent uses the token for the approved action only.
11. Human can inspect and revoke the token in Kaleidoscope.

## Token Rules

Tokens must be scoped. No broad account tokens by default.

Minimum token fields:

```text
token_id
token_prefix
user_id
agent_id
challenge_id
scope
origin
tool_or_action
spend_limit_cents
expires_at
created_at
revoked_at
last_used_at
```

Required constraints:

- short default expiry
- single action or narrow tool scope by default
- optional spend cap
- explicit origin or audience
- revocable
- auditable
- never shown in full after issuance
- never logged in full

## Scope Vocabulary

Start small. Suggested first scopes:

| Scope | Meaning |
|---|---|
| `demo:run` | Enter and run the Kaleidoscope demo |
| `image:generate` | Generate one image through the demo API |
| `wallet:spend:capped` | Spend up to the approved cap |
| `agent:read-profile` | Read the agent/user profile needed for the action |
| `mcp:connect` | Connect to a WIP MCP endpoint |
| `bridge:message` | Send a Bridge message to a named recipient |

Do not start with `account:*`.

## Agent Capability Paths

Different agents have different IO capability. Preserve the three-path design from Vision Quest 02:

### Path A: Agent can fetch URLs

1. Agent calls the challenge endpoint.
2. Agent receives approval URL.
3. Agent sends URL to human.
4. Agent polls status endpoint.
5. Agent receives token if approved.

### Path B: Agent cannot fetch URLs

1. Agent constructs an approval URL from `agent.txt` instructions.
2. Human opens URL.
3. Human approves.
4. Human copies a short one-time result code back to the agent.
5. Agent exchanges result code for a token, or the site shows the exact next command.

### Path C: App-native agent

1. Agent is paired through LDM OS or Kaleidoscope.
2. Approval request appears as a push notification.
3. Human approves.
4. Token is delivered through the paired channel.

## Endpoints, First Draft

Final endpoint names can change, but the contract should be explicit.

```text
POST /api/sapien-id/challenges
GET  /api/sapien-id/challenges/:id/status
POST /api/sapien-id/challenges/:id/approve
POST /api/sapien-id/tokens/exchange
POST /api/sapien-id/tokens/:id/revoke
GET  /api/sapien-id/tokens
```

### Create Challenge

Request:

```json
{
  "agentName": "Claude Code",
  "agentHandle": "claude-code",
  "requestedAction": "Run the Kaleidoscope demo image generation step",
  "requestedScopes": ["image:generate", "wallet:spend:capped"],
  "origin": "https://wip.computer",
  "spendLimitCents": 4,
  "expiresInSeconds": 300,
  "passphrase": "human-readable anti-spoofing phrase"
}
```

Response:

```json
{
  "challengeId": "sid_ch_...",
  "approvalUrl": "https://wip.computer/approve?c=sid_ch_...",
  "expiresAt": "2026-05-18T18:00:00Z",
  "pollUrl": "https://wip.computer/api/sapien-id/challenges/sid_ch_.../status"
}
```

### Poll Status

Pending:

```json
{ "status": "pending" }
```

Approved:

```json
{
  "status": "approved",
  "token": "lesa_...",
  "tokenExpiresAt": "2026-05-18T18:05:00Z",
  "scopes": ["image:generate", "wallet:spend:capped"]
}
```

Rejected:

```json
{
  "status": "rejected",
  "message": "The human denied this request."
}
```

Expired:

```json
{
  "status": "expired",
  "message": "This approval request expired."
}
```

## Approval Page Requirements

Approval page must show:

- agent name
- agent handle or runtime if available
- passphrase or shared anti-spoofing phrase
- requested action in plain language
- requested scopes
- origin/audience
- spend cap if any
- expiry
- approve button
- deny button
- "Agents cannot Face ID. Their humans can." or equivalent product line

The human must be able to understand what they are approving without reading developer docs.

## Security Requirements

1. Challenge IDs must be random and unguessable.
2. Challenges expire quickly, default 5 minutes.
3. Challenge approval requires passkey-authenticated human identity.
4. Agent-provided display fields are untrusted and must be escaped.
5. Tokens are scoped and short-lived.
6. Tokens are never logged in full.
7. Approval result is one-time readable where possible.
8. Polling responses do not reveal private account details before approval.
9. Origin/audience is bound into the token and checked by protected endpoints.
10. Spend scopes must include an explicit cap.
11. Denied and expired challenges cannot be reused.
12. Replays of approval result codes are rejected.

## Product Requirements

- The user should not copy a long API key.
- The agent should not see broad account credentials.
- The action should feel like Apple Pay or passkey approval: quick, explicit, human-controlled.
- The token should be inspectable later.
- The user should be able to revoke active agent tokens.
- If the agent cannot receive tokens automatically, the fallback should still be safe and understandable.

## First Implementation Slice

Do not start with every platform. Start with one loop:

1. `agent.txt` describes Sapien ID challenge creation.
2. Agent starts challenge for a demo or MCP action.
3. Human approves through existing passkey flow.
4. Agent polls and receives scoped token.
5. Token can call one protected endpoint.
6. Token is visible in a simple list for revoke/debug.

Recommended first protected action:

```text
Authorize this agent to call one WIP demo/API action with a small spend cap.
```

This proves identity, authorization, wallet consent, and token handoff without building the full app first.

## Implementation Notes

- Reuse the challenge/poll/approve pattern from existing demo agent auth.
- Do not fork a second identity model.
- Do not create broad API keys for convenience.
- Do not couple this only to image generation. Image generation can be the first proof, not the product boundary.
- Keep Remote Control and existing demo auth behavior unchanged unless a ticket explicitly scopes the migration.
- If implemented in hosted-mcp first, document the intended migration path to Kaleidoscope production surfaces.

## Acceptance Criteria

- Agent can request an approval challenge.
- Human can approve with passkey/Face ID.
- Agent receives a scoped token only after approval.
- Token can call the approved endpoint.
- Token cannot call an unrelated endpoint.
- Token expires.
- Token can be revoked.
- Logs never expose the full token.
- UI shows the human what the agent is asking for.
- Existing login/demo, Remote Control, pair/relink, wallet, and image API flows keep working.

## Out of Scope

- Full native iOS app implementation.
- Full third-party website integration.
- Full OAuth marketplace submission.
- Long-lived account tokens.
- Autonomous spend without human approval.
- Replacing all existing demo tokens in one pass.

## Open Questions

1. What is the first production endpoint to protect with Sapien ID?
2. Should tokens be bearer tokens, structured JWTs, opaque database tokens, or both?
3. Should the approval page live at `wip.computer/approve`, `kaleidoscope.wip.computer/approve`, or both during transition?
4. How should non-fetch agents receive the token safely?
5. Should every token be visible in the user's Kaleidoscope account immediately?
6. How should Agent Pay receipts attach to Sapien ID challenges?

## Review Notes for Coder

Before implementation, review:

- current live hosted-mcp auth code
- current demo agent auth challenge flow
- current passkey/session storage
- current wallet spend authorization
- current `agent.txt` and `llms.txt`
- this spec's security requirements

Stop at a PR. Do not deploy without explicit deploy handoff.

