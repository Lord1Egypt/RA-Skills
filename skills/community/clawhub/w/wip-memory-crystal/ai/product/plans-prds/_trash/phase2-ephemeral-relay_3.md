# Phase 2 — Ephemeral Relay Architecture

**Date:** 2026-02-25
**Agent:** cc-air
**Status:** Approved direction, replacing the cloud-mirror design

## Vision

Any device, any agent, any interface — laptop, phone, tablet, whatever comes next — captures conversations, encrypts them, and drops them at a relay. The Mini pulls everything in, embeds it, indexes it, and pushes the searchable mirror back out to every device. One master crystal, many readers. Every conversation you've ever had with any agent, fully searchable from anywhere.

And it's yours. Not behind a subscription. Not in someone else's cloud. Sovereign.

## Core Principle

The Mini is the master. Every other device is read-only. The Worker is a dead drop.
Nothing persists in the cloud. Data is there, then it's gone.

## Two One-Way Roads

### Road 1: Device → Mini (raw conversation chunks)

```
Device captures turn (cc-hook / any agent hook)
  → encrypts payload (AES-256-GCM, key on local machines only)
  → signs payload (HMAC-SHA256, proving origin)
  → POST /drop/conversations (bearer token auth)
  → Worker stores encrypted+signed blob (R2 or KV, TTL 24h safety net)

Mini polls (cron, every few minutes)
  → GET /pickup/conversations (bearer token auth)
  → receives encrypted blob
  → verifies signature (HMAC-SHA256 — confirms this came from a trusted device)
  → decrypts locally
  → chunks, embeds, ingests into master crystal
  → DELETE /confirm/conversations (tells Worker to delete)
  → Worker deletes blob
```

### Road 2: Mini → Devices (search-ready DB snapshot)

```
Mini's master crystal updated (after ingesting new chunks)
  → exports crystal.db snapshot
  → computes integrity hash (SHA-256 of plaintext DB)
  → encrypts snapshot + hash (AES-256-GCM)
  → POST /drop/mirror (bearer token auth)
  → Worker stores encrypted blob in R2 (TTL 24h safety net)

Device polls (on startup, or periodic)
  → GET /pickup/mirror (bearer token auth)
  → receives encrypted blob
  → decrypts locally
  → verifies integrity hash (SHA-256 matches — DB not corrupted or tampered)
  → replaces local read-only crystal mirror
  → DELETE /confirm/mirror (tells Worker to delete)
  → Worker deletes blob
```

## What Lives Where

| Location | What | Role |
|----------|------|------|
| Any device | Read-only crystal mirror (sqlite-vec + FTS5) | Search only, never writes |
| Any device | Raw JSONL transcripts (Claude Code native) | Source of truth for that device's conversations |
| Any device | Hook captures turns → encrypts → signs → sends to Worker | Capture + relay |
| Mini | Master crystal (sqlite-vec + FTS5 + LanceDB) | All embedding, indexing, search |
| Mini | Poller pulls from Worker → verifies → decrypts → ingests | Ingestion pipeline |
| Mini | Exports DB snapshot → hashes → encrypts → sends to Worker | Mirror distribution |
| Worker | Encrypted blobs only | Dead drop, no intelligence |

## Worker API (minimal)

```
POST   /drop/:channel        — deposit encrypted+signed blob
GET    /pickup/:channel      — retrieve encrypted blob(s)
DELETE /confirm/:channel/:id — confirm receipt, Worker deletes

GET    /health               — returns { ok: true }
```

Channels: `conversations` (devices→mini), `mirror` (mini→devices)

Auth: Bearer token per agent. Worker maps token → agent_id.

The Worker has no concept of what's inside the blobs. It's a dumb mailbox.

## Security Architecture

### Encryption

- **Algorithm:** AES-256-GCM (authenticated encryption)
- **Key:** Shared symmetric key, lives only on trusted machines (never on Cloudflare)
- **Key storage:** `~/.openclaw/secrets/crystal-relay-key` on each machine
- **Key generation:** `openssl rand -base64 32` once, copy to all trusted machines
- **What's encrypted:** Everything. The Worker sees only ciphertext.
- **Embeddings:** Created on Mini only, included in the encrypted DB snapshot

### Nonce Management (critical)

AES-256-GCM requires a unique nonce for every encryption. Reusing a nonce with the same key is catastrophic — it breaks confidentiality and authentication.

- **Nonce size:** 96 bits (12 bytes), per NIST recommendation
- **Generation:** Random (`crypto.getRandomValues(new Uint8Array(12))`)
- **Storage:** Prepended to ciphertext: `[12-byte nonce][ciphertext][16-byte auth tag]`
- **Uniqueness guarantee:** Random 96-bit nonces have negligible collision probability for fewer than 2^32 encryptions per key. At 1 drop per minute, that's ~8,000 years before rotation is needed for nonce safety. We rotate far more often for other reasons.

### Drop Signing (authenticity)

Even with bearer token auth, a stolen token could let an attacker drop malicious blobs. The Mini must verify that drops actually came from a trusted device.

- **Algorithm:** HMAC-SHA256
- **Key:** Derived from the encryption key (HKDF with context "crystal-relay-sign")
- **What's signed:** The encrypted blob (sign-then-MAC over ciphertext)
- **Verification:** Mini checks HMAC before decrypting. If it fails, the blob is discarded and logged.
- **Why not just rely on GCM's auth tag?** GCM proves the blob wasn't tampered with *after* encryption, but it doesn't prove *who* encrypted it. HMAC over the ciphertext proves the sender had the signing key, which only trusted devices have.

### Mirror Integrity Verification

When the Air (or any device) receives a new DB snapshot, it must verify the contents before replacing its local mirror.

- **Hash:** SHA-256 of the plaintext DB file
- **Included in payload:** `{ hash: "<sha256>", db: "<encrypted blob>" }`
- **Verification flow:**
  1. Decrypt the blob
  2. Compute SHA-256 of the decrypted DB
  3. Compare to the included hash
  4. If mismatch: reject, keep existing mirror, log error
  5. If match: replace local mirror

### Key Rotation

- **Mechanism:** Generate new key, distribute to all trusted machines, re-encrypt any in-transit blobs
- **Trigger:** Manual (Parker decides), or on suspected compromise
- **Process:**
  1. Generate new key: `openssl rand -base64 32`
  2. Copy to all machines: `~/.openclaw/secrets/crystal-relay-key`
  3. Both sides start using new key immediately
  4. Old key kept in `crystal-relay-key.prev` for 24h to decrypt any in-flight blobs from before rotation
  5. After 24h, delete old key
- **No re-encryption of historical data needed** — there is no historical data. Everything is ephemeral. The only data that matters is the master crystal on the Mini, which is never encrypted with the relay key.

### Threat Model Summary

| Threat | Mitigation | Residual Risk |
|--------|-----------|---------------|
| Data read in transit | TLS 1.3 + AES-256-GCM payload encryption | Cloudflare sees TLS-terminated headers (timing, size) |
| Data read at rest (Cloudflare) | Client-side AES-256-GCM, Cloudflare sees ciphertext only | Key compromise would expose in-flight blobs (max 24h window) |
| Data read at rest (device) | macOS FileVault full-disk encryption | Unlocked laptop = readable disk |
| Stolen bearer token | HMAC-SHA256 drop signing; attacker can't forge valid blobs without encryption key | Attacker could DELETE blobs (denial of service) |
| Tampered blobs | GCM auth tag (in-transit) + HMAC (origin) + SHA-256 (mirror integrity) | None — tampered data is rejected |
| Nonce reuse | Random 96-bit nonces, collision-safe for billions of operations | Theoretical at 2^48 operations; we rotate keys long before |
| Metadata/traffic analysis | Not mitigated | Cloudflare sees when/how much you talk to agents |
| Mini offline >24h | TTL expires blobs; `crystal replay` re-sends from raw JSONL | Must manually replay; those turns aren't auto-recovered |
| Key compromise | Rotation mechanism, ephemeral data (nothing to decrypt retroactively) | Active session blobs (minutes of data) exposed until rotation |
| Cloudflare account breach | Attacker sees ciphertext only; no keys, no OpenAI key, no secrets | Could delete blobs (DoS) or observe metadata |

## What the Worker Does NOT Have

- No D1 database
- No Vectorize index
- No FTS5
- No search capability
- No OpenAI API key
- No encryption keys
- No signing keys
- No ability to read the data it holds
- No knowledge of what's inside the blobs

## What Changes from the Cloud-Mirror Design

| Cloud Mirror (old) | Ephemeral Relay (new) |
|--------------------|-----------------------|
| D1 + Vectorize + R2 | R2 only (or KV with TTL) |
| Search on Worker | No search on Worker |
| Data persists in cloud | Data deleted after pickup |
| Worker creates embeddings | Mini creates embeddings |
| Device writes to remote crystal | Device sends raw chunks, never writes to crystal |
| Device searches remote crystal | Device searches local read-only mirror |
| Worker needs OpenAI key | Worker needs nothing but auth tokens |
| No client-side encryption | AES-256-GCM + HMAC-SHA256 + SHA-256 integrity |
| ~350 lines of Worker code | ~80 lines of Worker code |

## TTL Safety Net

All blobs get a 24-hour TTL. Even if the Mini is offline for a day and never confirms receipt, the data auto-expires from Cloudflare. This means:

- If Mini is offline >24h, those conversation chunks are lost from the relay
- But they still exist as raw JSONL on the originating device
- Recovery: `crystal replay` tool re-reads JSONL and re-sends

## Recovery Tool: `crystal replay`

Re-reads raw JSONL transcripts and re-sends through the relay:

```bash
crystal replay                          # replay all un-synced turns
crystal replay --since 2026-02-20      # replay from date
crystal replay --file <path.jsonl>     # replay specific file
crystal replay --dry-run               # show what would be sent
```

Uses the same watermark system as cc-hook but can reset/ignore watermarks.
Dedup happens on the Mini side (SHA-256 hash check before ingest).

## Multi-Device Future

This architecture scales to any number of devices:

```
Phone       ──┐
Laptop      ──┤── encrypt → drop → Worker (dead drop) → pickup → Mini (master)
Tablet      ──┤                                              │
Desktop     ──┘                                              │
                                                             ▼
Phone       ←─┐                                    embed, index, search
Laptop      ←─┤── decrypt ← pickup ← Worker ← drop ← encrypt (mirror snapshot)
Tablet      ←─┤
Desktop     ←─┘
```

Each device gets:
- Its own bearer token (revocable independently)
- The shared encryption key (for E2E encryption)
- A read-only mirror of the master crystal
- Full local search (keyword + semantic)

Adding a new device: generate a bearer token, copy the encryption key, done.
Removing a device: revoke its bearer token, rotate the encryption key.

## Open Questions

- Should the mirror snapshot be the full DB or incremental deltas?
  - Full DB is simpler but larger (~50MB+ as crystal grows)
  - Deltas are smaller but need conflict-free merge logic
  - Start with full DB, optimize later if needed
- How often should Mini push a new mirror? After every ingestion? Hourly? On-demand?
- Should devices poll for mirror updates on MCP server startup?
- Should we add a version counter to mirrors so devices know if they're stale without downloading?
