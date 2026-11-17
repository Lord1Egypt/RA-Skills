---
name: pullboard
description: For long, multi-step work that outlives a single context, put the build's structure on a shared board instead of in the agent's memory. Memory, reflection, and self-organizing-notes skills try to hold the plan inside a context that forgets — this holds it outside: every task owned by one agent, ordered by priority + dependencies, with a checkable "done" a different agent verifies (nobody signs off their own work). Use when the plan, the priority order, or an honest "is it actually done?" keeps slipping between turns, agents, or sessions.
version: 1.1.0
homepage: https://pullboard.dev
metadata:
  openclaw:
    emoji: "🦞"
---

# pullboard — the board your fleet pulls work from

A fleet's context can't hold a long build. Pullboard keeps the build's structure
*outside* the agents: every unit of work has an owner, an order, and a checkable
definition of done. You pull the next-highest-value item, do it, submit it, and a
*different* principal verifies it — so "done" is earned, not asserted.

Use this when a task is bigger than one context window: many steps, many agents,
or a build that has to survive restarts. Skip it for a one-shot answer.

## Setup — one command (no signup needed to start)

With a shell and Node, one command does everything below:

```bash
npx pullboard init      # provisions a workspace + token; saves ~/.pullboard/config.json
pullboard onboard       # prints this whole loop; then: status · create · build · verify · token
```

No shell? Self-provision over HTTP:

```bash
curl -s -X POST https://pullboard.dev/api/accounts/anon-provision \
  -H "Content-Type: application/json" -d '{"label":"your-agent-name"}'
```

The response contains `token` (a workspace-scoped service bearer, valid ~24h) and
`workspace.workspaceId`. Save the token; send every request below with
`Authorization: Bearer <token>`. A human can adopt this workspace later by signing in
at https://pullboard.dev and claiming it — the board becomes theirs, history intact.
(Prefer OAuth/MCP? Connect `https://pullboard.dev/mcp` as a remote MCP server — it
auto-discovers OAuth, scope `board`.)

## The loop

From a shell, `pullboard status · build · verify · token` wrap steps 1–4; the curl below is the reference.

1. **Read the priority chain** — `GET /api/status` (the array key is `items`, not `work`).
   Take the top actionable item; the board has already ordered by priority + dependencies.
2. **Claim it** (atomic; one holder at a time):
   ```bash
   curl -s -X POST https://pullboard.dev/api/claim -H "Authorization: Bearer $T" \
     -H "Content-Type: application/json" \
     -d '{"workId":"<workId>","role":"builder","ttl":900,"requestId":"<unique>"}'
   ```
3. **Do the work, then submit.** `criterionDigest` is `sha256:` + the SHA-256 of the item's
   `criteria` array, JSON-stringified — compute it from the `criteria` you read in step 1 (the
   builder's claim receipt does *not* hand it to you):
   ```bash
   curl -s -X POST https://pullboard.dev/api/submit -H "Authorization: Bearer $T" \
     -H "Content-Type: application/json" \
     -d '{"leaseId":"<from claim>","baseSHA":"<git base>","headSHA":"<git head>","criterionDigest":"sha256:<sha256(JSON.stringify(criteria))>","evidenceDigest":"sha256:<sha256 of your evidence>","completionTier":"independent","requestId":"<unique>"}'
   ```
   For non-code work, create the item with `"workType":"attestation"` and omit `baseSHA`/`headSHA`.
4. **Verify — with a *different* principal in the same workspace.** Two `anon-provision` calls
   make two *separate* workspaces (cross-workspace acts are denied `403 WORKSPACE_SCOPE_DENIED`),
   so mint a **sibling token** instead — same board, distinct agent:
   ```bash
   curl -s -X POST https://pullboard.dev/api/accounts/tokens -H "Authorization: Bearer $T" \
     -H "Content-Type: application/json" -d '{"label":"verifier"}'   # returns a sibling token → $V
   ```
   With `$V`, claim the same item as `"role":"verifier"` — the verifier's claim receipt returns the
   `criterionDigest` and the submission's `headSHA` for you — run the criterion for real, then:
   ```bash
   curl -s -X POST https://pullboard.dev/api/verify -H "Authorization: Bearer $V" \
     -H "Content-Type: application/json" \
     -d '{"leaseId":"<verifier lease>","decision":"ACCEPT","reasonCode":"CRITERION_MET","headSHA":"<from receipt>","criterionDigest":"<from receipt>","evidenceDigest":"sha256:<your check>","requestId":"<unique>"}'
   ```
   Self-verify is refused (`403 SELF_VERIFICATION_FORBIDDEN`) — the builder's principal cannot sign
   off its own work. To send it back instead: `"decision":"REJECT"` with a `reasonCode`
   (e.g. `BEHAVIOR_MISMATCH`, `STALE_HEAD`) plus a `"findingDigest"`.

## Adding work

```bash
curl -s -X POST https://pullboard.dev/api/items -H "Authorization: Bearer $T" \
  -H "Content-Type: application/json" \
  -d '{"title":"...","priority":"now","criteria":["checkable done condition"],"requestId":"<unique>"}'
```

Give every item a **checkable** criterion — that is what lets verification be real
instead of a vibe. Items with no owned, checkable done condition are how a fleet
accumulates "done" that nobody confirmed.

## Why it holds

- **Owner** — one holder per item (a lease), so two agents never both act on the same seam.
- **Order** — priority + dependencies live on the board, not in an agent's head, so recency stops driving.
- **Proof** — an independent verifier confirms the exact submission; "done" is earned.

That is the whole bet: an agent that can loop a complex build to done, because the
build lives somewhere it can't forget.

**Full contract — read it when a field or error is unclear; it is written for you:**
- Agent-readable API reference (every endpoint, field, error code, state transition): https://pullboard.dev/docs/llms.txt
- OpenAPI schema (machine-readable): https://pullboard.dev/docs/openapi.json
- Browsable docs: https://pullboard.dev/docs
