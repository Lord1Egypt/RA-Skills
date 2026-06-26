# Vision Quest 01: Memory Crystal Product Architecture

## Context

Parker has been iterating on the Memory Crystal product vision across two sessions: one with Lesa (lesa-vision-01.md) and one with CC (cc-mini-01.md). The core ideas are solid but scattered across 1000+ lines of raw conversation. Key decisions keep getting lost between sessions. This spec extracts and consolidates every decision into a buildable reference.

Source documents:
- `lesa-vision-01.md` (Parker + Lesa brainstorm: SDK, CloudKit, Apple architecture, enterprise)
- `cc-mini-01.md` (Parker + CC: platforms, MCP, routing, pricing, auth, cloud vs sovereign mode)

---

## The Product (One Sentence)

All your AIs share one memory. Searchable, private, sovereign.

## The Pitch

"Anthropic sells the thinking. We sell the remembering."

## Six Products

| Product | What it does | Repo |
|---------|-------------|------|
| **Memory Crystal** | Your AI remembers | memory-crystal-private |
| **Pay** | Your AI pays | wip-agent-pay-private |
| **Directory** | Identity, contacts, namespace resolution | TBD (the passkey + directory system) |
| **Bridge** | Your AIs talk to each other | wip-ldm-os-private (src/bridge/) |
| **Code** | Your AI builds | wip-ai-devops-toolbox-private (renaming) |
| **Crystal SDK** | Add memory to your app | TBD (the OpenAI-compatible proxy) |

LDM OS is the kernel. Invisible. Users never see it. "Powered by LDM OS."

Directory is its own product. Not part of Agent Pay. Identity (passkeys), contacts (bidirectional consent), namespace resolution (@handles). The foundation everything else sits on.

## What Exists Today

Memory Crystal: sqlite-vec + FTS5 local database. CLI, MCP server, OpenClaw plugin, Claude Code hook. 83K+ chunks. Works on our machines. Does not work for anyone else yet.

---

## No Web App. Agents ARE the Interface.

There is no web dashboard. No wip.computer/crystal. No browser UI. Everything is agent-based. The user interacts with Memory Crystal through MCP tools inside their AI. The AI IS the interface.

The only native apps are the iOS app (runs on Mac too) for Apple features (Face ID, Keychain, Agent Pay, QR auth, settings). The iOS app is NOT where you use memory. It's where you manage auth, billing, and sovereignty settings.

## Platforms (MVP)

These are the LLM platforms users connect from. Memory Crystal works across all of them.

| # | Platform | Surfaces | How Memory Crystal Connects | Status |
|---|----------|----------|-----------------------------|--------|
| 1 | **Anthropic (Claude)** | Claude Code CLI, Claude macOS, Claude iOS, claude.ai | Remote MCP server (we host) | MVP |
| 2 | **OpenAI (ChatGPT)** | ChatGPT macOS, ChatGPT iOS, chatgpt.com | Remote MCP server (we host) | MVP |
| 3 | **Grok (xAI)** | TBD | No MCP support yet | Blocked |
| 4 | **Hermes / Meta / Llama** | TBD | Probably MCP, need to investigate | Question mark |

MVP is Anthropic + OpenAI. Grok blocked on MCP support. Hermes/Meta/Llama need investigation on how they integrate into LDM. May be MCP, may be different.

**MCP tools (what the agent can do):**
- `crystal_search` ... "I had an idea about X with Claude" (works from ChatGPT)
- `crystal_remember` ... save something to memory
- `crystal_forget` ... delete a memory
- `crystal_export` ... export memories (creates a link, no email)
- `crystal_status` ... see what's connected, usage, bucket info
- Buckets: user-named memory spaces, instructions per bucket
- More TBD based on what's needed

---

## Customer Types

### Customer 1: Consumer

"I want my AI to remember across everything."

**Journey:**
1. User is on claude.ai or chatgpt.com (wherever they already are)
2. Adds Memory Crystal as an MCP connector (remote, we host it)
3. Uses AI normally. Memory accumulates automatically.
4. Pays via Agent Pay. No friction.
5. Optionally installs the iOS/Mac app for Apple features.

**The consumer installs nothing up front.** No local MCP server. No CLI. No npm. We host the MCP servers. They connect.

**Buckets:** Users name their memory spaces whatever they want (like we have cc-mini, cc-air). Multiple buckets per account. An agent, a project, a persona.

**The app is the upgrade, not the requirement:**
- Without app: MCP works, memories sync, search works, Agent Pay charges them
- With app: Face ID, Secure Enclave, Keychain, QR code auth, dashboard, sovereign mode

### Customer 2: Developer (for themselves)

"I want memory for my own agents and scripts."

Same as Consumer, plus they can use the SDK to build custom agents that share the same memory. They don't need a harness. They build whatever they want and it remembers.

```python
from crystal import Crystal
client = Crystal(crystal_key="ck-...")
client.remember("User prefers dark mode")
results = client.search("user preferences")
```

### Customer 3: Platform Developer (for their users)

"I want to build an app that gives MY users memory."

Two sub-types (from Lesa's doc):

| | Tier 1: For Yourself | Tier 2: Platform |
|---|---|---|
| Who signs up | You | You (the developer) |
| Who owns memories | You | Your users (managed by you) |
| Apple ID required | Yes | Only yours, not your users' |
| API key type | Personal | Platform (multi-tenant) |
| CloudKit | Your private database | Your container, partitioned by user |
| Pricing | Per-user plan | Per-API-call or per-seat |

We're downstream. We don't know what their app does. We store and search memories for their user IDs. We charge the developer.

### Customer 4: Enterprise (self-hosted)

"I want to run this myself on my infrastructure."

The existing Core/Node architecture. Install Crystal, run it, MIT licensed. No Apple stuff required. No dependency on us. This is what we run today.

---

## Two Modes of Operation

### Sovereign Mode (app installed, core device available)

Everything runs on the user's device:
- Memory extraction
- Embedding generation
- Search/retrieval
- Encryption (CryptoKit + Secure Enclave)

Our server just routes. Auth, route, bill. Never sees plaintext.

CloudKit stores encrypted blobs we can't read.

### Cloud Mode (no core device, demo)

User connected via MCP. No app. No core device.

We run the embeddings and extraction on our servers. We briefly have their data. We encrypt it and push to CloudKit.

**This is the demo/acquisition funnel.** Transparent about it:
- "Demo mode. Your memories are processed on our servers."
- "Install the Memory Crystal app to move everything to your device."
- Free for 30 days, then Agent Pay wallet

**The system auto-detects:** If a core device is registered and online, route to it (sovereign). If not, fall back to cloud processing (demo).

---

## Architecture

```
Claude.ai / ChatGPT / Open Claude / Hermes
    | (MCP connection)
Our Hosted MCP Server (wip.computer VPS)
    |-- Auth (validate API key / Agent Pay)
    |-- Route traffic
    |-- Billing / usage metering
    |-- IF no core device: run embeddings + extraction here (cloud mode)
    |
CloudKit (Apple infrastructure)
    |-- One container, ours
    |-- Per-user private databases (Apple handles multi-tenancy)
    |-- Enterprise shared zones
    |-- E2E encrypted
    |
User's devices (Mac, iPhone)
    |-- Crystal app: auth, billing, settings, sovereignty
    |-- IF sovereign mode: extraction + embeddings run HERE
    |-- CryptoKit + Secure Enclave
```

**"Our server is a router with a cash register."** Auth, route, bill. Three things.

**Why Linode, not Cloudflare Workers:** The router is so thin ($5/mo VPS) that Workers is overkill. We're only on Linode because Apple doesn't sell compute. If Apple opens Private Cloud Compute, we drop Linode.

**Why not Cloudflare Workers:** We don't need global edge. Memory search isn't latency-critical. One VPS is simpler, cheaper, and we control it. No vendor-specific code.

---

## The App

**One app. iOS app that runs on Mac (Catalyst / iPad on Mac).**

Not two separate apps. One codebase. iOS first because:
- Keychain integration
- Face ID / biometric auth
- Agent Pay (Apple Pay integration)
- QR code auth: agent shows QR code, user scans with phone, authenticates with built-in keys
- Push notifications
- The Mac version is the iOS app running on macOS

**What the app does:**
- See all connected AIs, all buckets, all memories
- Search: semantic search across all memories
- Manage: delete, organize, set permissions
- Auth: Face ID, QR code device pairing
- Agent Pay: billing, usage, payment methods
- Secrets: Keychain-based credential storage for agents
- Settings: core device designation, sovereignty status

**What the app does NOT do:**
- Run an LLM
- Replace Claude or ChatGPT
- Require a subscription to use the MCP (MCP works without the app)

---

## SDK (OpenAI-Compatible Proxy)

No special library to install. Crystal is an OpenAI-compatible API proxy with memory. Developers change one line: the `base_url`.

```python
# Before (no memory)
client = OpenAI(api_key="sk-...", base_url="https://api.openai.com")

# After (memory, one line change)
client = OpenAI(api_key="ck-...", base_url="https://crystal.wip.computer")
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4-20250514",  # any model
    messages=[{"role": "user", "content": "What about Q3?"}]
)
# Crystal: searches memory, injects context, forwards to Anthropic,
# extracts memories from response, returns response. Transparent.
```

**Why OpenAI-compatible:**
- OpenAI's API format is the de facto standard
- Every language has an OpenAI SDK (Python, Node, Go, Rust, etc.)
- Works with LiteLLM, OpenRouter, any existing stack
- Zero SDK to install. Use whatever OpenAI library you already have.
- One line change to add memory to any existing app.

**The stack:**
```
Developer's App (standard OpenAI SDK)
    | (base_url = crystal.wip.computer)
Crystal Proxy (memory layer: search, inject, extract, store)
    |
Anthropic / OpenAI / Google / local models
```

Crystal handles memory. Routes to the right provider. One proxy, any model, automatic memory.

---

## Model Routing and Pricing

**Three direct integrations (we own the relationship):**
- Anthropic
- OpenAI
- Grok (xAI)

**Everything else via OpenRouter** (pass-through cost, or user provides their own OpenRouter API key).

**Pricing structure:**
- Crystal memory fee (fixed) + model cost (pass-through)
- We never mark up the model cost. We charge for the memory layer.
- User can bring their own OpenRouter key for non-direct models.

| Provider | Relationship | How it works |
|----------|-------------|--------------|
| Anthropic | Direct (we own) | Pass-through API cost |
| OpenAI | Direct (we own) | Pass-through API cost |
| Grok (xAI) | Direct (we own) | Pass-through API cost |
| Everything else | Via OpenRouter | Pass-through OpenRouter cost, OR user provides own key |

---

## Enterprise / Self-Hosted (Core + Node)

The existing architecture. No Apple dependency. MIT licensed.

- Core: always-on machine, primary Crystal instance
- Node: mirrors, syncs to Core
- Permission levels per machine (admin, read/write, read-only)
- No CloudKit. HTTP sync between nodes.
- This is what we run today. This is what enterprises who can't use Apple run.

**The Apple features (CloudKit, Face ID, Agent Pay) are what you get when you install the app.** Enterprise without the app still works. It's just local.

---

## Pricing (Draft)

**Consumer (MCP):**
- Free for 30 days (cloud mode, demo)
- After 30 days: install app + load Agent Pay wallet ($25) for 30 more free days
- Then: monthly subscription TBD

**SDK Proxy (developers):**
- Crystal memory fee (fixed, per-call or per-month) + model cost (pass-through)

**Platform (multi-tenant):**
- Per-seat or per-API-call pricing
- Same model pass-through structure

**Enterprise (self-hosted):**
- MIT licensed, run it yourself
- No dependency on us, no Apple required
- License or support contract

---

## Auth Model

**No passwords. Ever. In anything we build.**

Passkeys only. No email/password forms. No stored passwords. This applies to every auth flow: signup, login, agent permissions, payments, secrets, device pairing.

### Primary flow (push notification + Face ID):
1. Agent needs permission (or user is logging in)
2. Push notification hits your phone: "Memory Crystal: approve this action?"
3. Tap notification. App opens.
4. Face ID. Done.

No QR code. No scanning. No camera. No typing. Push + biometric. That's it.

### First-time setup (QR code, one time only):
1. No app installed yet, no push notifications registered
2. QR code displayed on screen
3. Scan with phone, install app, register passkey
4. From this point forward, everything is push + Face ID

### OAuth (required by Claude/ChatGPT directories):
OAuth is the PROTOCOL that Claude/ChatGPT use to talk to us. It's the handshake, not the login. Inside the OAuth redirect, our login page shows "Sign in with passkey" or sends a push notification. The user never sees an email/password form. Claude and ChatGPT just see a standard OAuth flow.

### Agent permission pattern:
Every agent action that needs approval uses the same flow:
- Agent wants to spend money? Push + Face ID.
- Agent needs a secret from Keychain? Push + Face ID.
- Agent wants to send a message? Push + Face ID.
- New device connecting? Push + Face ID.

One pattern. Every permission. No passwords. The phone is the auth device.

---

## Identity and Directory (Resolution Layer)

Identity and Directory sit beneath everything else. They answer two questions: who are you, and who do you know. Everything in the system builds on those answers.

**The stack:**
```
Identity (passkeys)     ... who you are
Directory (contacts)    ... who you know
Bridge (messaging)      ... how it travels
Memory Crystal          ... what you remember
Agent Pay               ... how you pay
```

### Identity

The passkey IS the account. Face ID (Apple) or fingerprint (Android). No email. No password.

**What the server stores:** credential ID + public key. Never biometric data.

**What stays on the device:** private key, locked in the Secure Enclave. Hardware-locked. Never leaves.

**Verification flow:**
1. Server sends a challenge (random bytes)
2. Device signs the challenge with the private key (Face ID unlocks it)
3. Server verifies the signature with the stored public key
4. If valid, you're authenticated

Same model as Apple Pay. We can prove it's you without having your biometric data. We can verify, not impersonate.

### Directory (the resolution layer)

The directory maps human names to agent endpoints. Like DNS resolves domains to IPs.

**Example:** "Send a note to Jimmy Iovine" -> directory lookup -> jimmy@wip.computer -> Bridge routes it.

**Bidirectional consent:** Jimmy adds you, you add Jimmy. Both authenticated by passkey. Both opted in. No unsolicited messages. Both sides must be in each other's directory before a message can travel.

This is the resolution layer. Bridge handles transport. Directory handles "who is this person and where do they live in the system."

### Signup Flow

1. Tap a link (wip.computer/signup)
2. Webpage calls WebAuthn
3. Face ID creates passkey
4. Account exists. No email. No password. No form.

Optional later: add email (recovery), phone (recovery), 2FA. These are fallbacks, not requirements.

### As an SDK

One function: `createAccount()`. Developer drops it in. User sees Face ID. Done.

What developers don't have to build:
- No signup form
- No email verification
- No password reset
- No "forgot password" flow

Passkeys first. Passkeys only. Email is the optional add-on, not the default.

### How Identity Connects to the Six Products

Identity is the FOUNDATION. Everything else sits on top.

| Product | How it uses Identity |
|---------|---------------------|
| **Agent Pay** | Same passkey for payment authorization. Face ID to approve a charge. |
| **Bridge** | Directory resolves recipients. "Send to Jimmy" -> directory lookup -> route. |
| **Memory Crystal** | Identity isolates per-user memories. Your passkey = your memory space. |
| **Crystal SDK** | Identity for API authentication. Passkey-derived credentials. |
| **Code** | Identity for repo access, deploy permissions, agent authorization. |

---

## Build Order

### Phase 1: Hosted MCP Server (the product for consumers)
- Remote MCP server on Linode (wip.computer)
- MCP tools: search, remember, forget, export, status
- Auth + Agent Pay integration
- Cloud-side embedding + extraction (cloud mode for users without app)
- CloudKit storage (server-to-server API)
- Buckets (user-named memory spaces)
- User connects from claude.ai, chatgpt.com, any MCP client
- Free 30 days. Then Agent Pay wallet.
- This IS the product. No App Store review needed. No download.

### Phase 2: iOS App (sovereign mode + Apple features)
- One app: iOS that runs on Mac (Catalyst / iPad on Mac)
- Apple ID sign-in, CloudKit integration
- Face ID, Keychain, Secure Enclave
- QR code auth for device pairing (agent shows QR, phone scans, authenticates)
- Agent Pay wallet management
- Core device designation (moves processing off our servers to user's device)
- Settings: manage connections, buckets, sovereignty status
- NOT where you use memory. That's the agent. This is auth/billing/settings.

### Phase 3: OpenAI-Compatible Proxy (the product for developers)
- OpenAI-compatible API at crystal.wip.computer
- Change base_url, get memory. No SDK to install.
- Direct integrations: Anthropic, OpenAI
- Everything else: wrapped OpenRouter (pass-through cost, or bring your own key)
- Auto-extract memories from responses, auto-inject context into prompts
- Crystal fee + model pass-through pricing

### Phase 4: Platform API (for developers building apps)
- Multi-tenant API keys (developer manages their users' memories)
- Per-user isolation
- Usage metering, billing per-seat or per-call
- Developer manages memory, end user never knows Crystal exists

### Phase 5: Swift SDK (native Apple, optional)
- Native Apple framework for developers building iOS/Mac apps
- Direct CloudKit integration (no server round-trip)
- CryptoKit + Secure Enclave
- For apps that want the deepest Apple integration

---

## Key Decisions (extracted from conversations)

1. **Server is just a router.** Auth, route, bill. Never sees plaintext in sovereign mode.
2. **One CloudKit container.** Ours. Apple handles multi-tenancy. Like WhatsApp.
3. **No Cloudflare Workers.** Linode VPS is sufficient. Simpler.
4. **iOS first.** One app that runs on Mac. Not two apps.
5. **Consumer installs nothing.** MCP connection to our hosted servers. App is optional upgrade.
6. **Demo mode is the funnel.** Free 30 days, transparent: "your data is on our servers, install the app to fix that."
7. **Same version = same code.** Version immutability across all releases.
8. **Four-track releases.** Alpha, beta, hotfix, stable. Alpha never requires deploy-public.
9. **Hermes / Meta / Llama are question marks.** MVP is Anthropic + OpenAI only.
10. **Enterprise is self-hosted.** MIT licensed. No Apple dependency. Core + Node architecture.
11. **"Anthropic sells the thinking. We sell the remembering."**
12. **We architecturally CAN'T read their data.** Not "we promise not to." The keys never leave their device.
13. **OpenAI-compatible proxy, not custom SDK.** Change base_url. Works with any OpenAI SDK in any language.
14. **Three direct model integrations** (Anthropic, OpenAI, Grok). OpenRouter for everything else.
15. **Passkeys as default auth.** Magic link as fallback. No email/password.
16. **No web app.** Agents are the interface. MCP tools only.
17. **Identity is the foundation.** Passkeys create the account. Directory resolves contacts. Everything else builds on "I know who you are because you Face ID'd."
18. **No biometric data stored.** Public key only. Private key in Secure Enclave. We can verify, not impersonate.
19. **Directory is bidirectional consent.** Both sides opt in. No unsolicited messages.

---

## Open Questions (to spec in future sessions)

1. **Hermes / Meta / Llama integration:** How do these agents integrate into LDM? Probably MCP but need to investigate.
2. **CloudKit server-to-server API limits:** Free tier is generous (1PB assets), but what are the API call limits at scale?
3. **Apple Foundation Models SDK (WWDC25):** On-device embeddings would eliminate OpenAI embedding API dependency. Timeline?
4. **Agent Pay wallet mechanics:** How does the 30-day free trial transition? How does wallet loading work?
5. **Passkey implementation:** Apple's passkey API for the iOS app. How does the QR code flow work technically?
6. **Embedding cost in cloud mode:** Included in Crystal fee or separate line item?
7. **OpenRouter relationship:** Formal partnership or just use their public API?
8. **Grok MCP timeline:** When does xAI add MCP support? Monitor.
9. **MCP tool list:** Full tool surface beyond search/remember/forget/export/status.
10. **Bucket spec:** Instructions per bucket, naming, sharing, permissions.

---

## Prior Art and Larger Vision: The Settlement Layer

Parker built the DJ Mixes system at Apple. First functionally compulsory licensing system for master recordings. Infrastructure that identified tracks within continuous mixes, generated precise attribution, and routed pro-rata payments to every rights holder. Over 200 million streams. The industry thought it was impossible. It shipped.

That was the prototype. Memory Crystal is the scale.

### The Insight: The Prompt IS the Attribution

When a user types "remix @aphextwin with @jayz," the AI knows exactly whose work influenced the output because the user declared it. This is cleaner attribution than any sample ever had. The data exists. The payment rail doesn't. Until now.

### The Framework

**WHY money flows (attribution layers):**

| Layer | Why you get paid |
|-------|-----------------|
| Training | Your work was used to train the model |
| Prompt | You were named/invoked by the user |
| Recording | Your actual recording was used (played, sampled, stems) |
| Curation | You assembled/mixed/sequenced the output |
| Creation | You crafted the prompt / made the new work |
| Distribution | Your work was released/published |
| Stream | Your work was consumed |
| Remix | Your work became source material for a new work |

**WHO gets paid (rights buckets):**

| Bucket | Why you have a claim |
|--------|---------------------|
| Masters | You own the recording |
| Publishing | You own the composition |
| Name/likeness | Your identity was invoked |
| Creator | You made the new work (DJ, prompter, mashup artist, producer) |

**WHAT happened (output types):**

| Output | Description |
|--------|-------------|
| Passthrough | Existing recording played via connected streaming service |
| Generation | New output created by AI |
| Transformation | Existing recording modified by AI |
| Mix | Multiple recordings/generations assembled together |

### How Our Stack Maps to the Framework

```
Our system                     The attribution framework
-----------                    -------------------------
Identity (passkeys)        =   Namespace (@handles, verified creator identities)
Directory (contacts)       =   Resolution (who referenced -> who gets paid)
Bridge (messaging)         =   Attribution routing (trace the influence)
Agent Pay                  =   Payment rails (compensation flows automatically)
Memory Crystal             =   The ledger (what happened, lineage, searchable, sovereign)
Crystal SDK (proxy)        =   The interception point (every API call traced)
```

"Remix @aphextwin with @jayz" -> both handles resolve via the directory -> attribution traced via Memory Crystal -> payment routed via Agent Pay.

The passkey IS the verified @handle. The directory IS the namespace. The bridge IS the routing. Agent Pay IS the payment rail. Memory Crystal IS the ledger.

### The Bigger Picture

Music is the proving ground. Highest litigation exposure. Clearest identity mapping. Precedent already exists (DJ Mixes at Apple).

Solve creative attribution for music, you've prototyped how value flows in post-scarcity. The same logic extends to visual arts, writing, code, any domain where human work trains the models.

The company that solves attribution for AI prompts becomes the platform artists trust.

Parker's words: "I've built this infrastructure before. I can build it again."

References:
- Parker's full framework: https://parkertoddbrooks.bearblog.dev/move-human-why-innovation-in-music-rights-will-shape-our-creative-future-ptii/
- Peter Diamandis + David Blundin + Elon Musk UHI discussion (context for the post)

---

*Compiled April 1, 2026 by CC Mini from conversations with Parker and Lesa.*
*Each open question above is a future spec session: read the architecture-spec, then spec out one topic in depth.*
