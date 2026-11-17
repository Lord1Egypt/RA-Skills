---
title: "Remote Control OAuth token minting must prove server-side session and PKCE"
status: open
priority: P0
owner: Hardening Cody
repo: wip-ldm-os-private
created: 2026-05-18
source_review: 2026-05-18 security triage of private Remote Control architecture
master_plan_item: 37
---

# Remote Control OAuth Token Minting Must Prove Server-Side Session And PKCE

## Problem

The 2026-05-18 security triage called out the hosted MCP OAuth token issuance path as still too loose from code inspection.

The concern:

- PKCE verification appeared to run only when both `challenge` and `verifier` are present.
- The route can mint a `ck-` bearer token.
- That may be acceptable only if a surrounding passkey-backed server-side session is the real gate.
- The review did not accept that assumption without direct server-side session proof.

The reviewer did not run a live credential-minting exploit against `wip.computer`; only safe unauthorized/default-key probes were run, and those returned Unauthorized.

## Risk

P0 until proven otherwise.

A `ck-` bearer is powerful Remote Control authority. Token mint paths must fail closed. "The page probably gated it" is not enough for production-security review.

## Required analysis

Before changing code, map the current token mint route:

- route path and handler in `src/hosted-mcp/server.mjs`;
- where the passkey or account session is established;
- where the route proves server-side session authority;
- where PKCE challenge and verifier are stored;
- what happens when either PKCE input is missing;
- which token is minted and where it is persisted;
- whether the path is used by Remote Control pairing, app login, generic OAuth, or all of them.

## Fix shape

- Require a server-side authenticated session before any `ck-` or Remote Control bearer can be minted.
- Require PKCE verifier validation when the grant was created with a challenge.
- Fail closed when required PKCE state is missing, expired, mismatched, or already used.
- Do not mint a bearer from only client-supplied identity fields.
- Make the error path generic enough that attackers cannot enumerate account or grant state.
- Add basic rate limiting if the endpoint lacks it, or link to the existing rate-limit ticket that owns it.

## Acceptance

- A test proves unauthenticated requests cannot mint `ck-` tokens.
- A test proves a request with missing verifier cannot mint a token when the grant has a challenge.
- A test proves a request with missing challenge state cannot mint a token.
- A test proves a mismatched verifier cannot mint a token.
- A test proves replaying a used verifier or grant fails.
- A positive test proves a fresh passkey-authenticated session plus correct verifier mints the expected token.
- Code review identifies the exact server-side session proof used by the route.

## Non-goals

- Do not redesign the full account system.
- Do not weaken pair/relink fresh-presence.
- Do not add a client-side-only check and call it authentication.
- Do not run live credential-mint exploit tests against production without Parker explicitly authorizing a safe staging plan.
