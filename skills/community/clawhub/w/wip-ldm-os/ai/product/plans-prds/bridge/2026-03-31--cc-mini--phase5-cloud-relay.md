# Phase 5: Cloud Relay (Cloudflare Workers + CloudKit)

**Added:** 2026-03-31
**Depends on:** Phases 1-4 (file-based inbox, session targeting, boot delivery, cross-agent)

## Two relay services, one inbox

Both services deliver messages to the same `~/.ldm/messages/` directory. The agent doesn't know or care which relay delivered the message. Local, Cloudflare, or CloudKit ... same inbox, same format.

```
LOCAL (same machine):
  Agent A -> write file -> ~/.ldm/messages/ -> Agent B reads

CLOUDFLARE (cross-platform, any device):
  Agent A -> encrypt -> POST relay.wip.computer/drop -> R2 bucket
  Agent B's poller -> GET relay.wip.computer/pickup -> decrypt -> ~/.ldm/messages/

CLOUDKIT (Apple devices only):
  Agent A -> encrypt -> CKRecord write -> CloudKit push notification
  Agent B's app/daemon -> CKQuerySubscription fires -> decrypt -> ~/.ldm/messages/
```

## Service 1: Cloudflare Workers + R2

**For:** Any device. Linux VPS, Android (future), non-Apple machines, cross-platform setups.
**Hosted by:** WIP Computer at `relay.wip.computer`
**Self-hostable:** Yes. Worker code is AGPL. Run your own.

### Architecture

```
Cloudflare Worker (relay.wip.computer)
  POST /drop    ... store encrypted blob in R2, tagged with destination device ID
  GET  /pickup  ... retrieve and delete blobs for a device
  POST /pair    ... exchange device IDs and verify pairing code
  GET  /status  ... health check, pending count
```

R2 bucket stores encrypted blobs. 24-hour TTL. Auto-cleanup. The Worker never sees plaintext.

### Encryption
- AES-256-GCM for message encryption
- HMAC-SHA256 for integrity verification
- Shared key derived during device pairing (Diffie-Hellman key exchange)
- Keys never leave the devices. The relay is blind.

### Poller (on each device)
- LaunchAgent/cron runs every 60 seconds
- Calls `GET relay.wip.computer/pickup?device={id}`
- Decrypts each blob
- Writes to `~/.ldm/messages/{uuid}.json`
- Same format as local messages. The inbox doesn't know the difference.

### Device pairing via Cloudflare
1. Device A calls `POST /pair` with a short pairing code (6 digits, 5 min expiry)
2. Device B enters the code: `POST /pair/verify` with code + device B's public key
3. Worker matches the pair, returns device A's public key to B
4. Both devices derive shared AES key locally (ECDH)
5. Worker stores: `{deviceA, deviceB, pairedAt}`. No keys.

### Pricing (WIP Computer hosted)
- **Free:** 1 Core pair (Mac + Phone) + 1 Node. 1000 messages/day.
- **Pro ($5/month):** Unlimited nodes. 10,000 messages/day. Priority relay.
- **Self-hosted:** Free forever. Deploy the Worker yourself.

### What syncs via Cloudflare
- Messages (chat, system, task delegation)
- Memory Crystal delta chunks (new memories)
- Session state broadcasts (who's active)
- NOT: raw transcripts, databases, large files (use rsync/mirror-sync for those)

### Existing work
- Memory Crystal already has relay Worker code (`worker/` directory)
- Encryption module exists (`src/relay/crypto.ts`)
- R2 bucket pattern proven in Memory Crystal v0.5.0

## Service 2: CloudKit

**For:** Apple devices only. Mac, iPhone, iPad.
**Hosted by:** Apple (iCloud infrastructure)
**Cost:** Free (included with iCloud account, which all Apple users have)

### Why CloudKit alongside Cloudflare

| | Cloudflare | CloudKit |
|---|---|---|
| Platform | Any | Apple only |
| Latency | Polling (60s) | Push (seconds via CKQuerySubscription) |
| Cost | Free tier + paid | Free (Apple provides) |
| Self-hostable | Yes | No |
| Setup | Pair + deploy Worker | Just sign in to iCloud |
| Privacy | Encrypted by us | Encrypted by us + Apple ADP |

CloudKit is faster (push vs poll) and free for Apple users. Cloudflare is universal. Most WIP Computer users have Macs and iPhones, so CloudKit covers the common case. Cloudflare covers everything else.

### Architecture

```
CloudKit Container (iCloud, com.wipcomputer.ldm-relay)
  CKRecord type: "Message"
    - deviceFrom: String
    - deviceTo: String
    - encryptedPayload: Data (AES-256-GCM blob)
    - timestamp: Date
    - ttl: Date (24h from creation)
```

### How it works
1. Device A writes a CKRecord to the shared CloudKit container
2. Device B has a CKQuerySubscription on `deviceTo == myDeviceID`
3. Apple pushes a silent notification to Device B
4. Device B's app/daemon wakes, reads the record, decrypts, writes to `~/.ldm/messages/`
5. Device B deletes the CKRecord (consumed)

### On Mac (daemon)
- `ldm-cloudkit-relay` LaunchAgent
- Uses CloudKit JS (via node) or a small Swift helper binary
- Subscribes to new records on startup
- Writes to `~/.ldm/messages/` on notification

### On iPhone (app)
- The Lesa App registers CKQuerySubscription in app delegate
- Silent push wakes the app
- App reads record, decrypts, writes to local inbox
- Same message format. Same processing.

### Device pairing via CloudKit
- Simpler than Cloudflare. Both devices are signed into the same iCloud account.
- No explicit pairing needed for same-account devices.
- For multi-account (team): use CKShare to share the relay container.

### Existing research
- `ai/product/plans-prds/bridge/2026-03-30--cc-mini--icloud-relay-and-ios-mcp-research.md`
- CKQuerySubscription provides push delivery (seconds, not polling)
- Advanced Data Protection makes CloudKit end-to-end encrypted
- NSMetadataQuery can watch for changes on Mac

## Implementation order

### Phase 5a: Cloudflare relay (builds on existing Memory Crystal worker)
1. Fork the Memory Crystal relay Worker into a standalone `wip-relay` repo
2. Add message endpoints (drop, pickup, pair)
3. Deploy to `relay.wip.computer`
4. Build poller LaunchAgent for Mac (`ldm-relay-poller`)
5. Add `ldm pair` CLI command (generates pairing code, exchanges keys)
6. Test: CC-Air sends message via relay, CC-Mini receives in inbox

### Phase 5b: CloudKit relay (iOS app + Mac daemon)
1. Create CloudKit container in Apple Developer account
2. Build Swift helper for Mac (subscribes, writes to ~/.ldm/messages/)
3. Add CloudKit subscription to Lesa App (iOS)
4. Test: iPhone sends message, Mac receives in seconds
5. Reverse: Mac sends, iPhone receives

### Phase 5c: Transport selection (automatic)
- `lib/messages.mjs` `sendMessage()` gains a transport resolver:
  - Same machine? Write to filesystem directly.
  - Apple device on same iCloud account? Use CloudKit.
  - Everything else? Use Cloudflare relay.
- The sender doesn't choose. The system detects the best path.

## What NOT to build
- No custom protocol. HTTP + JSON + AES-256-GCM. That's it.
- No message broker (RabbitMQ, Redis). Files and HTTP are enough.
- No real-time WebSocket relay. Push notifications (CloudKit) and polling (Cloudflare) cover it.
- No multi-hop routing. Messages go sender -> relay -> receiver. No forwarding chains.
