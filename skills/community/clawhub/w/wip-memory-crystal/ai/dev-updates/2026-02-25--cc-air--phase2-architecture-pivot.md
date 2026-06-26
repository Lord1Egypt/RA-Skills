# 2026-02-25 — Phase 2 Architecture Pivot: Cloud Mirror → Ephemeral Relay

**Agent:** cc-air (Claude Code on MacBook Air)
**Repo:** `memory-crystal`
**Branch:** `cc-air/phase2-relay` (new, replaces `cc-mba/phase2-worker`)

## What Happened

Built the Phase 2 Cloudflare Worker as a cloud database mirror (D1 + Vectorize + R2 + FTS5). Full search on the Worker, persistent data in Cloudflare, ~350 lines of Worker code. It worked — built clean, types passed.

Then Parker asked the right questions:
1. What's the security risk of data in transit?
2. What's the security risk of data sitting on Cloudflare?
3. What happens when sync breaks and we lose context?

Read the Dream Weaver Protocol architecture. The entire memory system is designed around sovereignty — "your memory, your machine, your rules." Putting conversation data persistently on Cloudflare violates that principle. And it's not just code conversations — it's everything said to every agent. Personal.

Parker's core requirement: "I gotta be able to leave the house." Take the laptop, talk to cc-air, and have those conversations make it back to the master crystal on the Mini. But the data shouldn't *live* in the cloud. It should pass through.

## The Pivot

**Cloud Mirror (old):** Worker is a searchable database. Data persists on Cloudflare. Air searches the cloud. Cloudflare sees plaintext. OpenAI API key on Cloudflare.

**Ephemeral Relay (new):** Worker is a dead drop. Data passes through encrypted, gets picked up, gets deleted. Nothing persists. Worker can't read what it holds. ~80 lines of code.

### Architecture

```
Any Device → encrypt → Worker (dead drop) → Mini picks up → decrypt → embed → master crystal
                                                                    │
Mini → encrypt mirror snapshot → Worker → Device picks up → decrypt → local read-only mirror
```

- **Mini is the master.** All embedding, indexing, and search intelligence lives there.
- **Devices are read-only.** They capture raw conversations and search against a local mirror. They never write to the crystal.
- **Worker is a mailbox.** Encrypted blobs in, encrypted blobs out. TTL auto-expires everything in 24h. No D1, no Vectorize, no search, no API keys.

### Security Hardening

- **AES-256-GCM** client-side encryption. Key lives only on trusted machines, never on Cloudflare.
- **HMAC-SHA256 drop signing.** Mini verifies every blob came from a trusted device.
- **Random 96-bit nonces.** Prepended to ciphertext, collision-safe for billions of operations.
- **SHA-256 mirror integrity.** Devices verify DB snapshots before replacing their local mirror.
- **Key rotation mechanism.** 24h overlap for in-flight blobs, no re-encryption needed (ephemeral data).
- **Explicit threat model.** Every risk documented with mitigation and residual risk.

## Why This Matters Beyond Us

This isn't just cc-air talking to the Mini. Any device, any agent, any interface can use the same pattern. Phone, laptop, tablet. Every conversation captured, encrypted, relayed, embedded, searchable. One master crystal, many readers. Sovereign memory that travels with you.

Open source. Auditable. No subscription. No cloud lock-in.

## Files

| File | Status |
|------|--------|
| `ai/plan/phase2-ephemeral-relay.md` | NEW — full architecture spec with security model |
| `ai/plan/dev-conventions-note.md` | NEW — documented existing dev conventions |
| `ai/dev-updates/2026-02-25--cc-air--phase2-worker-build.md` | EXISTING — documents the original cloud mirror build |
| `src/worker.ts` | TO BE REBUILT — ephemeral relay (~80 lines replacing ~350) |
| `src/crypto.ts` | TO BE CREATED — AES-256-GCM + HMAC-SHA256 + HKDF |
| `src/cc-hook.ts` | TO BE MODIFIED — encrypt + relay instead of direct ingest |
| `src/poller.ts` | TO BE CREATED — Mini-side pickup + ingest |
| `src/mirror-sync.ts` | TO BE CREATED — Device-side mirror pull |
| `wrangler.toml` | TO BE SIMPLIFIED — R2 only, no D1/Vectorize |
| `schema.sql` | TO BE REMOVED — no database on Worker |

## Previous Branch

`cc-mba/phase2-worker` — contains the cloud mirror build. Preserved so people can see the progression from "persistent cloud DB" to "ephemeral encrypted relay." The thinking is the product.
