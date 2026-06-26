# Phase 5 Setup Requirements: What Parker Needs to Create

## Cloudflare

### Account setup (one-time)
You already have a Cloudflare account (wip.computer is hosted there). These are the additional resources needed.

1. **R2 bucket**
   - Name: `ldm-relay` (or `wip-relay`)
   - Dashboard: Cloudflare > R2 Object Storage > Create bucket
   - Free tier: 10GB storage, 10M Class A ops/month, 1M Class B ops/month
   - This is where encrypted message blobs are stored (24h TTL, auto-cleanup)

2. **Worker**
   - Name: `relay` (serves at `relay.wip.computer`)
   - Dashboard: Cloudflare > Workers & Pages > Create Worker
   - Bind the R2 bucket to the Worker as `RELAY_BUCKET`
   - Free tier: 100K requests/day. Paid ($5/mo): 10M requests/month.
   - The Worker code lives in our repo. Deploy via `wrangler deploy`.

3. **Custom domain for the Worker**
   - Route: `relay.wip.computer` -> the Worker
   - Dashboard: Cloudflare > Workers > relay > Settings > Domains & Routes
   - Since wip.computer DNS is already on Cloudflare, this is one click.

4. **R2 lifecycle rule**
   - Auto-delete objects older than 24 hours
   - Dashboard: Cloudflare > R2 > ldm-relay > Settings > Object lifecycle
   - Rule: Delete after 1 day

5. **API tokens (for wrangler deploy)**
   - Dashboard: Cloudflare > My Profile > API Tokens > Create Token
   - Permissions: Workers (Edit), R2 (Edit)
   - Store in 1Password as "Cloudflare Wrangler Deploy Token"

### What we already have
- Cloudflare account (wip.computer)
- wrangler CLI (npm install -g wrangler)
- Memory Crystal relay Worker code (can be forked into standalone wip-relay)
- Encryption module (AES-256-GCM)

### Estimated cost
- Free tier covers most usage (1 Core + 2 Nodes, normal message volume)
- R2: free for first 10GB (messages are tiny, well under this)
- Workers: free for 100K req/day (polling every 60s x 3 devices = 4,320 req/day)
- Total: $0 for normal usage. $5/mo Workers paid plan if you exceed free tier.

---

## Apple Developer

### Account setup
You need an Apple Developer account ($99/year). Check if you already have one for the Lesa App.

1. **CloudKit container**
   - Name: `iCloud.com.wipcomputer.ldm-relay`
   - Create in: Xcode > Project > Signing & Capabilities > iCloud > CloudKit
   - Or: developer.apple.com > Certificates, Identifiers & Profiles > CloudKit Dashboard
   - This is the shared container where encrypted messages live

2. **Record type in CloudKit Dashboard**
   - Type name: `RelayMessage`
   - Fields:
     - `deviceFrom` (String) ... sender device ID
     - `deviceTo` (String) ... recipient device ID
     - `encryptedPayload` (Bytes) ... AES-256-GCM blob
     - `timestamp` (Date/Time) ... when sent
     - `expiresAt` (Date/Time) ... 24h TTL
   - Index: `deviceTo` (queryable, for subscriptions)

3. **App ID with CloudKit capability**
   - The Lesa App's App ID needs the CloudKit entitlement
   - Xcode > Signing & Capabilities > + Capability > iCloud > check CloudKit
   - Select the `iCloud.com.wipcomputer.ldm-relay` container

4. **Push notification certificate (for silent pushes)**
   - CloudKit subscriptions use silent push notifications
   - Xcode automatically handles this when you enable CloudKit + Push Notifications capabilities
   - No manual certificate management needed with automatic signing

5. **Mac helper entitlements**
   - The Mac daemon that receives CloudKit notifications needs:
     - `com.apple.developer.icloud-container-identifiers` (same container)
     - `com.apple.developer.icloud-services` (CloudKit)
   - This can be a small Swift CLI tool or a LaunchAgent

### What we already have
- Lesa App (SwiftUI, exists at `team/Lēsa/repos/lesa-app/`)
- Apple Developer account (verify: do you have one?)

### Estimated cost
- Apple Developer Program: $99/year (if not already enrolled)
- CloudKit: free (25GB storage, 250K records, 5M ops/day included)
- iCloud for users: free (5GB, but our encrypted blobs are tiny)
- Total: $99/year for the developer account. Everything else is free.

---

## What I can build without you

Once the accounts and containers exist, I can build everything else:

| Task | Needs Parker | I can do it |
|------|-------------|-------------|
| Create Cloudflare R2 bucket | Yes (dashboard) | No |
| Create Cloudflare Worker | Yes (first deploy) | After first deploy, wrangler handles it |
| Set up relay.wip.computer route | Yes (dashboard) | No |
| Create CloudKit container | Yes (Xcode/dashboard) | No |
| Add CloudKit to Lesa App | No | Yes (code change) |
| Write the relay Worker code | No | Yes |
| Write the poller LaunchAgent | No | Yes |
| Write the Mac CloudKit daemon | No | Yes |
| Write encryption module | No | Yes (already exists in Memory Crystal) |
| Write pairing flow | No | Yes |
| Write `ldm pair` CLI | No | Yes |
| Deploy Worker via wrangler | After token is in 1Password | Yes |

---

## Quick start checklist

Parker does these (15 minutes):
- [ ] Verify Apple Developer account is active
- [ ] Create CloudKit container in Xcode (iCloud.com.wipcomputer.ldm-relay)
- [ ] Add CloudKit + Push capabilities to Lesa App in Xcode
- [ ] Create R2 bucket in Cloudflare dashboard (ldm-relay)
- [ ] Create Workers API token, save to 1Password
- [ ] Set lifecycle rule on R2 bucket (delete after 1 day)

Then I build everything else.
