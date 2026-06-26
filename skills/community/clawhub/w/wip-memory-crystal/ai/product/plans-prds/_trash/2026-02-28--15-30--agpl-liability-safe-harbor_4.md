# AGPL, Liability, and Safe Harbor for Memory Crystal Cloud

*Written 2026-02-28 ~15:30 PST by Claude Code*

## Context

Parker asked: if Memory Crystal is open source (AGPL) and he runs the Cloudflare Workers for free/personal use, how does he prevent abuse and protect himself from liability if users store illegal content?

## AGPL and Infrastructure Protection

AGPL protects the code, not the infrastructure. The license requires anyone who deploys a modified version as a network service to share their source. But it doesn't give anyone access to Parker's Workers, D1, R2, or relay keys.

**Protecting the deployed Workers:**

1. **OAuth is the gate.** MCP server requires OAuth. Parker controls who gets tokens. Can be single-user (v1) or allowlisted emails.
2. **Relay key is the second gate.** AES-256-GCM. Key only exists on the Worker (Wrangler secret) and the user's machine. Encrypted blobs in R2 are useless without it.
3. **Rate limiting.** Cloudflare Workers supports rate_limiting in wrangler.toml. Cap per token per minute.
4. **Token revocation.** Delete their row from access_tokens in D1. Instant cutoff.

## Safe Harbor and Liability

### Section 230 + DMCA 512

Safe harbor protects when:
- Storing content at the user's direction
- No actual knowledge of specific illegal content
- Acting on valid takedown/legal requests
- Repeat infringer policy in place

### Tier 1 (Sovereign / Encrypted Relay)

Strongest legal position. Parker literally cannot see user data. Everything is AES-256-GCM encrypted end-to-end. The Worker stores opaque blobs in R2. Only the user has the decryption key.

Comparable to: Signal, ProtonMail.

If law enforcement requests content, Parker hands over encrypted blobs and says "I can't decrypt these, talk to the account holder."

### Tier 2 (Cloud Search / Plaintext in D1)

User explicitly opted in to plaintext cloud storage. Parker is a storage provider, not a publisher. Data is scoped per user_id. Parker doesn't review, curate, or publish it.

Comparable to: Dropbox, Notion, Google Drive.

### Where Safe Harbor Does NOT Protect

- Actual knowledge of specific illegal content + inaction
- Actively promoting illegal use
- CSAM: federal law (18 USC 2258A) requires reporting to NCMEC. For encrypted content (Tier 1), can't scan it... same position as Signal/ProtonMail. For Tier 2, hash-matching (PhotoDNA) is an option but not legally required for small services.

## Signup Flow Implications

When opening to public users:
- Email registration required (identity on file)
- OAuth token issued via MCP consent flow
- User generates their own relay key locally (CLI command)
- Key never touches Parker's servers (Tier 1)

Having an account on file matters: if law enforcement comes with a court order, Parker can identify the account and point to the user, not himself. Shows no knowledge of content.

## Required Before Opening Signups

- [ ] Terms of Service with prohibited use clause
- [ ] Privacy policy (what you can/can't see per tier)
- [ ] DMCA designated agent filing ($6 with US Copyright Office)
- [ ] Ability to terminate accounts and delete their data
- [ ] 30-minute consultation with an actual lawyer

## Summary Table

| Tier | Parker's position | Comparable to |
|------|------------------|---------------|
| Tier 1 (encrypted) | Cannot see content | Signal, ProtonMail |
| Tier 2 (plaintext) | Storage provider | Dropbox, Notion |

## Disclaimer

This is architectural guidance and research notes, not legal advice. Get a real lawyer before opening public registration.
