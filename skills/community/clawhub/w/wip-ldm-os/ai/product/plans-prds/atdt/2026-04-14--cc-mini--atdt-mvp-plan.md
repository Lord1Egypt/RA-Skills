# ATDT: Identity Primitive for Kaleidoscope

**Date:** 2026-04-14
**Filed by:** cc-mini
**Status:** Plan (pre-implementation, v2 revision)
**Repo (primary):** wip-ldm-os-private (later: its own repo)
**Client target:** Claude Code first, then any MCP-compatible CLI

## Vision

ATDT is the **user driver for Kaleidoscope**. It is the reason someone signs up: to get their `@handle`.

`@handle` is your portable identity: your feed, your inbox, your payment address. Once you have it, the rest of the Kaleidoscope family hangs off it (memory, payments, agent interactions, work-log publishing).

The command is the brand: `/atdt @bcherny`. Self-describing. Retro-modern. Terminal-native.

## Design Principle: Simple Apps, Super UX

ATDT is one simple app in a growing family. Each app does one thing well. Together they compose the Kaleidoscope experience.

- `/atdt register`, `/atdt post`, `/atdt @handle`: identity + work-log
- `/atdt pay`, `/wip pay`, `/kaleidoscope pay`: settlement (same backend, multiple entry points)
- Memory Crystal, Agent Pay, Directory, Bridge, Code, Crystal SDK: the six Kaleidoscope products

Unix philosophy. Each verb is simple. The composition is the magic. "Every AI. One experience" is built out of many small apps, not one monolith.

## The Canonical Use Case

A developer (call him Boris) posts findings, thoughts, fixes, workarounds. Today that work is scattered: replies on HN, comments on GitHub issues, posts on X, messages in Slack. There is no central place for his insight, and his peers and agents cannot find it.

ATDT is that central place.

- Boris: `/atdt post "Fixed the vibes engine."`
- Parker: `/atdt @bcherny` (reads Boris's bulletins)
- Boris's agent: reads Boris's feed to stay in sync with his work

This is the minimum viable workflow. Everything else is in service of making this reliable, addressable, and eventually monetizable.

## Long-term Goal: Payment Is the Endpoint

Identity enables addressing. Addressing enables payment.

The eventual value surface is a universal payment primitive, available from multiple entry points:

- `/wip pay @bcherny 5`
- `/atdt pay @bcherny 5`
- `/kaleidoscope pay @bcherny 5`

All three resolve to the same Agent-Pay backend, using `payment_address` from the Nodelist entry. The entry point depends on context; the behavior is identical. This is not feature creep on ATDT. It is the reason ATDT exists.

The work-log (Boris posting his findings) makes the identity real. The identity makes the payment meaningful. Shipping Boris's use case is the path to shipping payments to everyone.

## Lineage

Honest ancestry. We inherit proven patterns from federated messaging systems that predate platform capture:

- **FidoNet (1984):** the mesh, store-and-forward, Nodelist, zones/nets/nodes
- **Echomail (1986):** topic-based public forums with ORIGIN/PATH/SEENBY headers; loop prevention already solved
- **EchoList (1987):** the topic-registry pattern (separate from the identity registry)
- **The WELL (1985):** "You own your own words" (YOYOW); sovereign voice; conversation as the product
- **Macintosh file sharing:** peer-to-peer by default; every node a server; Chooser-style discovery
- **Hotline (1996):** per-server aesthetic; integrated chat + files + news + boards; trackers as meta-registry
- **KDX (2001):** the cryptographic successor to Hotline; end-to-end encryption, sovereign identity

ATDT is what this architecture looks like with cryptographic keys, modern auth, payment rails, and agent-native ergonomics.

## What It Is

Five concrete pieces:

1. **@handle:** identity address (bootstrapped from an X handle via OAuth for namespace origin)
2. **Keypair:** Ed25519, local to each install. The key is the authority; the handle is a pointer.
3. **Nodelist:** registry mapping `@handle → {public_key, feed_url, payment_address}`. WIP-administered in v1; federation in v0.2.
4. **EchoList** (deferred v0.2): registry of topics (`#music`, `#claudecode`, `#ldm`). Lives here for when cross-account topic discovery is worth building.
5. **Echomail:** the post format. Markdown, signed by your key, served from your node. Mutable with versioning (see Feed Format).

Each person or agent runs or is hosted on a node. Dialing a node reads their Echomail. Following a node pulls their posts into your feed.

## Naming

- **Echomail** = the post/feed system
- **Netmail** (deferred) = private DMs
- **Nodelist** = identity registry
- **EchoList** = topic registry
- **Point** = follower / subscriber (from FidoNet `zone:net/node.point`)
- **Sysop** = the admin of a node
- **Bulletins** = posts on a node

## User Flows (MVP)

### 1. Registration (one-time, ~1 min)

```
/atdt register
```

- Opens browser to Kaleidoscope OAuth (WebAuthn passkey, live at `wip.computer/login`)
- OAuth also links X (PKCE) and reads the user's X handle via `/users/me` ($0.01/registration)
- Ed25519 keypair generated locally at `~/.atdt/key`
- Nodelist entry written: `{@handle, public_key, feed_url, payment_address}`
- `post` and `follow` unlock

### 2. Dialing a node (no auth needed to read)

```
/atdt @bcherny
```

```
*** CONNECTING TO @bcherny ***
Welcome to Boris's node.

Bulletins (3 new):
  1. [04-14] Fixed the vibes engine
  2. [04-13] Thoughts on MCP design
  3. [04-12] Weekend project

[#] Read a post  [Q] Hangup
```

Two actions only: read a post, hang up. No guestbook.

### 3. Posting (sysop mode, no auth)

```
/atdt post "Fixed the vibes engine."       # inline
/atdt post ./today.md                      # from file
```

Signed with your key. Published to your feed (default: `wip.computer/@handle`, self-host later).

### 4. Following

```
/atdt follow @bcherny
```

Writes to `~/.atdt/follows`. His bulletins appear in your feed.

### 5. Home feed

```
/atdt feed          # last 24h (default)
/atdt feed 6h       # last 6 hours
/atdt feed 3d       # last 3 days
```

Chronological across all follows. No algorithm. Single arg: number + unit (`h` or `d`). Caps: 1-24h, 1-30d.

## Commands Summary

**MVP:** `register`, `@<handle>` (dial), `post`, `follow`, `feed`.

**Deferred (v0.2+):**
- `echo #topic` (needs EchoList aggregator)
- `pay @handle <amount>` (wires to Agent-Pay MCP; also available as `/wip pay` and `/kaleidoscope pay`)
- `unfollow`, `following` (list management)
- Netmail / DMs

**Command alias layer:** `/wip`, `/atdt`, and `/kaleidoscope` share the subcommand surface for cross-product verbs like `pay`. The entry point depends on context; the behavior is identical. Parker's call per-verb whether it belongs to the ATDT-only surface or the shared one.

## Feed Format

One file per day, markdown, signed.

**Structure:**
```
wip.computer/@bcherny/2026-04-14.md
wip.computer/@bcherny/2026-04-13.md
```

**Content model:** daily journal. One file, multiple timestamped entries. Respects the BBS "bulletins" framing and doesn't force users to post separate "things." Opens the door to progressive posting throughout the day.

**Mutability:** mutable with versioning. A new signed post supersedes the previous; old versions remain cryptographically reachable by hash; the default feed serves latest. Rationale: humans make mistakes. "I posted a typo and can't fix it" is a rage-quit scenario. Immutable-on-append would be purer but worse UX. Audit trail satisfies the verifiability concern.

## Anti-features (explicit)

ATDT ships without:
- Likes
- Follower counts (or hidden by default)
- Quote-repost
- Trending / algorithmic ranking

Just: follow someone, read what they wrote, chronologically, done. This is a position, not an MVP limitation. Bake it into the pitch.

## Architecture

### Client (MCP server `@wip/atdt`)

Node.js + TypeScript. Ships to npm. Claude Code discovers via MCP config. Any MCP-compatible client (Cursor, Cline, Goose) gets it free.

Tools:
- `atdt_register`, `atdt_dial` (handle), `atdt_post`, `atdt_follow`, `atdt_feed`

Local state in `~/.atdt/`:
- `key` (Ed25519 private key, 600 perms)
- `follows` (one @handle per line)
- `cache/` (cached feeds from dialed nodes)

### Nodelist (WIP-administered in v1, federated in v0.2)

HTTP service at `atdt.wip.computer`:
- `POST /register` (@handle, public_key, feed_url, payment_address)
- `GET /lookup/@handle` → entry
- `POST /update/@handle` (requires key signature)

**v1 is WIP-administered.** One canonical registry. WIP runs the default and can reassign / delist / freeze. Honest and simple.

**v0.2 adds federation** (DNS-style):
- Identity layer (hard): the Ed25519 key controls the record; signatures required; verifiable everywhere.
- Namespace layer (soft): default registry applies policy; clients can choose their own resolvers; `~/.atdt/config` lists one or more Nodelist URLs.
- Multiple roots become possible: `nodelist.anthropic.ai`, community-run registries, etc.

The marketing line is not "owned by no platform." The honest line is: **"Your identity is cryptographic and unstoppable. Your handle is administered like a domain."**

### Handle Policy (UDRP-style)

Since the namespace is governed in v1, a handle policy needs to exist before dogfood:

- **Reserved names:** major brands (`@apple`, `@google`), system names (`@atdt`, `@nodelist`), WIP-reserved seeds.
- **Trademark priority:** verified claim overrides squatter.
- **Impersonation:** confusing similarity triggers reassignment.
- **Inactivity:** optional reclaim after N months of zero posts.
- **Appeals:** human arbitration (Parker for v1; transfer trigger in v1.x, see Governance).

Handles are a leased right, not permanent property. Identity (the key) persists; the handle it points to can change hands under policy.

### Feed hosting

Default: `wip.computer/@handle` serves markdown files with the file structure above.

Self-host by pointing `feed_url` at your own HTTPS endpoint with the same layout. Sign-verify on fetch so readers can confirm posts are from the key on record.

### Auth

Uses existing Kaleidoscope auth (`src/hosted-mcp/server.mjs`):
- WebAuthn passkey (biometric, live at `wip.computer/login`)
- OAuth PKCE (live at `/oauth/authorize`)
- Plus X OAuth 2.0 for namespace bootstrap ($0.01/user)

**Gap:** CLI-native OAuth callback flow not yet implemented. This is **shared Kaleidoscope infrastructure**, not ATDT-specific. The 5-7 days to ship localhost callback + device code benefits every CLI-based WIP product. ATDT is the forcing function, not the sole beneficiary.

### Admin (Kaleidoscope panel)

Nodelist is mutable with admin override:
- Reassign @handle to a different owner / public_key
- Rotate key (lost-key recovery)
- Delist / freeze (abuse)
- Audit log of all changes

Pragmatic over blockchain-immutable. Disputes get arbitrated.

### Governance transfer trigger

WIP-administered does not scale indefinitely. Support load grows with user count (abuse reports, DMCA, handle disputes, lost-key recovery). Trigger for handoff to a foundation or independent org:

- **10k users:** part-time support role emerges. Formalize the policy.
- **100k users:** full-time team. Hand off canonical Nodelist to a non-WIP org.
- **1M users:** federation is mandatory, not optional.

## Dependencies

| Dep | Status | Action needed |
|-----|--------|---------------|
| Kaleidoscope passkey auth | Live at `wip.computer/login` | None (reuse) |
| Kaleidoscope OAuth PKCE | Live at `/oauth/authorize` | None (reuse) |
| CLI localhost callback | **Not implemented** | Build (2-3 days). Shared Kaleidoscope infra. |
| Device code fallback | **Not implemented** | Build (3-4 days). Shared Kaleidoscope infra. |
| X OAuth integration | **Not built** | Register WIP app with X, scopes `users.read` + `tweet.read` |
| Agent-Pay MCP | Live (`agent_pay`, `agent_pay_fund`, `agent_pay_x402`) | None; wire into `/atdt pay` in v0.2 |
| Directory (passkey → @handle) | **TBD** per `architecture-spec.md:27` | Build as part of Nodelist |
| Library migration (`shared/` → `library/`) | Planned (`2026-04-14--cc-mini--library-migration-plus-topology.md`) | Execute first so ATDT docs land in `library/documentation/` |

## Implementation Plan

### Phase 1: Foundations (week 1)
- Land library-migration + deployment-topology doc
- Add CLI localhost callback to Kaleidoscope auth (`src/hosted-mcp/server.mjs`). Shared infra.
- Add device code fallback. Shared infra.
- Register WIP app with X, store credentials via op-secrets plugin

### Phase 2: Nodelist service (week 2)
- HTTP server at `atdt.wip.computer` (Node.js + Prisma + Postgres, reusing the mcp-server stack)
- Endpoints: `register`, `lookup`, `update` (signed)
- Admin endpoints for Kaleidoscope: `reassign`, `rotate`, `delist`
- Write and publish the Handle Policy
- Pre-populate reserved handles: `@anthropic`, `@claude`, `@claudecode`, `@bcherny`, `@lesa`, `@parkertoddbrooks`

### Phase 3: Feed hosting default (week 2-3)
- `wip.computer/@<handle>` serves markdown (daily journal format)
- `/atdt post` uploads to default host if user hasn't set custom `feed_url`
- Sign-verify on fetch
- Mutability: version chain with hash-addressable history

### Phase 4: MCP client (week 3-4)
- `@wip/atdt` npm package
- Tools: `register`, `dial`, `post`, `follow`, `feed`
- Local state under `~/.atdt/`
- ANSI welcome banner, "CARRIER 9600" flavor

### Phase 5: Admin panel (week 4)
- Extend Kaleidoscope web with `/admin/nodelist`
- List, reassign, rotate, delist flows
- Audit log view

### Phase 6: Content commitment + launch (week 5)
- Parker, Lēsa, cc-mini, invited friends post daily for 30 days starting launch day
- Ship `/atdt` as Claude Code slash command
- Reach out to target users (Boris-style work-log use case) for feedback
- Launch post when the feed has enough content to reward a first-time reader

## Public, Federated in v0.2

The protocol is the product. v1 is WIP-administered (one canonical Nodelist). v0.2 adds federation so the "open protocol" claim becomes honest.

- Nodelist server code: public (`wip-ldm-os/library/...` or its own repo)
- `@wip/atdt` MCP client: public npm package
- Deployment topology: public (lands via library-migration plan)
- Handle Policy: public, versioned

## Deferred (v0.2+)

- **Federated Nodelist sync** (DNS-style, multiple roots, eventually consistent)
- **EchoList aggregator** (`/atdt echo #topic`): crawls or push-receives posts by tag
- **Netmail / DMs:** private messaging between @handles
- **Payments (`/atdt pay`, `/wip pay`, `/kaleidoscope pay`):** wire into Agent-Pay MCP. Simple once Nodelist has `payment_address`. This is the long-term endpoint, not a side feature.
- **Agent-to-agent marketplace:** humans have X/Slack/Discord/iMessage; agents have nothing. ATDT becomes the callable address for agents once identity + payment lands. Long-term flywheel.
- **Follower / point notifications** ("@bcherny mentioned you")
- **iOS / macOS native clients:** Kaleidoscope app team's territory. ATDT is CLI-native for v1.

## Open Questions

1. **ATDT in its own repo** (e.g., `wip-atdt`) vs inside `wip-ldm-os-private`? If public-facing protocol, probably own repo after v1 lands.
2. **X-required for v1 registration?** Trade-off: narrative sharpness vs. including developers who never had X. Leaning: X-preferred, not X-required. Revisit at launch.
3. **Nodelist entry schema versioning:** how do we evolve the schema later without breaking old clients? (TTL field + version field in every record.)
4. **Self-hosted feed verification:** require a DNS TXT record or meta tag proving the user controls `feed_url`, or trust-on-first-use?
5. **ANSI art:** who designs the welcome banners? Default template + per-user customization?
6. **Seed content:** what do Parker's / Lēsa's / cc-mini's first posts look like?

## Cross-references

- Library migration plan: `ai/product/bugs/os-level/2026-04-14--cc-mini--library-migration-plus-topology.md`
- Kaleidoscope architecture: `ai/product/product-ideas/vision-quest-01/architecture-spec.md`
- Agent-txt era: `ai/product/product-ideas/vision-quest-01/vision-quest-02-agent-txt-era.md`
- Sovereign data: `ai/product/plans-prds/current/wip-principles/2026-04-11--cc-mini--sovereign-data-principle.md`
- Hosted MCP server: `src/hosted-mcp/server.mjs`
- Agent Pay MCP: `repos/ldm-os/components/wip-agent-pay-private/`
- LYLA settlement: `team/Lēsa/documents/Product Ideas/WIP.computer/lyla/VISION.md`

## Changelog

- **2026-04-14 v1:** initial plan (PR #589)
- **2026-04-14 v2:** reframe as user driver for Kaleidoscope, not Twitter replacement; payment as long-term endpoint; command alias across `/wip`/`/atdt`/`/kaleidoscope`; "simple apps compose a super UX" design principle; feed format clarified (daily journal, mutable with versioning); Handle Policy section; governance transfer trigger; CLI auth flagged as shared Kaleidoscope infra; anti-features made explicit; agent-to-agent preserved as v0.2+ flywheel
