# Features to Preserve from Demo

**Date:** 2026-04-07
**Filed by:** cc-mini
**Status:** reference (do not delete)

## Why this file exists

The demo at `wip.computer/demo/` is the design reference and prototype. As we build production Kaleidoscope, these features from the demo must be carried forward. They are proven, working, and Parker approved the designs.

## 1. Agent Login Flow

**Demo files:** `demo/agent.html`, `demo/agent.txt`, server endpoint `/approve`
**What it does:** Lets AI agents authenticate with Kaleidoscope through their human.

Flow:
1. Agent reads `agent.txt` (instructions for AI agents)
2. Agent calls `/demo/api/agent-auth` to get a challenge ID
3. Agent sends the approve URL to its human (via chat, iMessage, etc.)
4. Human opens `wip.computer/approve?c=CHALLENGE_ID`
5. Human sees agent name + passphrase, authenticates with Face ID
6. Agent polls `/demo/api/agent-auth/status?c=CHALLENGE_ID`
7. Agent receives a bearer token, can now call APIs

Key design elements:
- Agent info cards (agent name, passphrase) on the approve page
- "You can't do Face ID. Your human can." tagline
- 5 minute expiry on challenges
- Polling every 2 seconds
- Copy-paste prompt for humans to send to their agents

**Production location:** needs to be rebuilt at `wip.computer/approve` (not under /demo/)

## 2. QR Code Login (Chrome fallback)

**Status:** not yet built, planned
**What it does:** On Chrome (where WebAuthn cross-platform QR doesn't work), show our own QR code on the login page.

Flow:
1. Desktop (Chrome) clicks "Look Inside"
2. Page generates a session, shows QR code encoding `wip.computer/login?session=XXXXX`
3. Phone scans QR code with camera
4. Phone opens login page, does Face ID, creates passkey
5. Desktop polls, detects registration, logs in

Uses the same challenge/poll pattern as the agent auth flow.

**Note:** Safari handles QR code via native WebAuthn. Chrome on macOS does not (shows "Insert security key" instead). This fallback is Chrome-specific.

## 3. Approve Page Design

**URL pattern:** `wip.computer/approve?c=CHALLENGE_ID`
**Design:** Same Kaleidoscope styling (warm cream background, centered card, colored status bubbles). Parker approved this design on 2026-04-07.

The approve page should:
- Use the same footer as the login page (with local passkeys toggle, agent link, privacy, terms)
- Keep the agent info cards
- Keep the Face ID auth button
- Keep the status bubbles (blue loading, red error, green success)

## 4. Lesa Chat Demo

**Demo file:** `demo/index.html`
**What it does:** Full chat experience with Lesa. Passkey auth, agent permission (Face ID for spending), camera, kaleidoscope image generation.

This is the product vision. The chat UI, the permission flow, the creative generation. All of it needs to eventually live in production Kaleidoscope.

## 5. Auth as SDK / Framework

**Status:** idea (Parker, 2026-04-07)
**What it could be:** Package the entire passkey auth system as a drop-in SDK for other developers.

What we've built:
- Phone-first WebAuthn passkey registration
- Custom QR code fallback for Chrome (server-generated, poll-based)
- Local passkeys toggle (user controls where keys live)
- Agent-to-human authentication (AI agents auth through their human via Face ID)
- Status bubbles, cancel/fade UX, browser detection

How it could ship:
- **Client SDK:** one script tag, handles all the WebAuthn + QR + browser detection
- **Server SDK:** Node.js package for WebAuthn verification + session management
- **Hosted API:** like Clerk/Auth0 but passkey-first. Developer adds one script tag, we handle everything.

Differentiators vs existing auth services (Passage, Corbado, Hanko):
- Phone-first by default (nobody else forces this)
- Custom QR fallback for browsers that don't support native WebAuthn QR
- Agent authentication (unique to Kaleidoscope)
- Local passkeys toggle (user controls their security posture)

This could be Crystal SDK (currently "add memory to your app" in architecture-spec.md) expanded to include auth, or a standalone "Directory SDK" product. The passkey system is the foundation that everything else sits on.

Reference: `ai/product/product-ideas/vision-quest-01/architecture-spec.md` lines 28-30, 413-418

## Cross-references

- `ai/product/plans-prds/kaleidoscope/2026-04-06--cc-mini--kaleidoscope-architecture.md`
- `ai/product/plans-prds/kaleidoscope/2026-04-07--cc-mini--session-final-summary.md`
- `ai/product/product-ideas/vision-quest-01/architecture-spec.md` (Crystal SDK, Directory)
- Demo source: `src/hosted-mcp/demo/` (NEVER MODIFY the demo itself)
