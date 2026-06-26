 Ready to code?
                                                                                                          
 Here is Claude's plan:
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
 Vision Quest 01: Memory Crystal Product Architecture   

 Context

 Parker has been iterating on the Memory Crystal product vision across two sessions: one with Lesa
 (lesa-vision-01.md) and one with CC (cc-mini-01.md). The core ideas are solid but scattered across 1000+
  lines of raw conversation. Key decisions keep getting lost between sessions. This plan extracts and
 consolidates every decision into a buildable spec.

 Source documents:
 - /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/le
 sa-vision-01.md
 - /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/cc
 -mini-01.md

 The Product (One Sentence)

 All your AIs share one memory. Searchable, private, sovereign.

 The Pitch

 "Anthropic sells the thinking. We sell the remembering."

 What Exists Today

 Memory Crystal: sqlite-vec + FTS5 local database. CLI, MCP server, OpenClaw plugin, Claude Code hook.
 83K+ chunks. Works on our machines. Does not work for anyone else yet.

 ---
 No Web App. Agents ARE the Interface.

 There is no web dashboard. No wip.computer/crystal. No browser UI. Everything is agent-based. The user
 interacts with Memory Crystal through MCP tools inside their AI. The AI IS the interface.

 The only native apps are the iOS app (runs on Mac too) for Apple features (Face ID, Keychain, Agent Pay,
  QR auth, settings). The iOS app is NOT where you use memory. It's where you manage auth, billing, and
 sovereignty settings.

 Four Platforms (MVP)

 These are the LLM platforms users connect from. Memory Crystal works across all of them.

 ┌─────┬─────────────────┬───────────────────────────────────┬─────────────────────────┬────────────┐
 │  #  │    Platform     │             Surfaces              │   How Memory Crystal    │   Status   │
 │     │                 │                                   │        Connects         │            │
 ├─────┼─────────────────┼───────────────────────────────────┼─────────────────────────┼────────────┤
 │ 1   │ Anthropic       │ Claude Code CLI, Claude macOS,    │ Remote MCP server (we   │ MVP        │
 │     │ (Claude)        │ Claude iOS, claude.ai             │ host)                   │            │
 ├─────┼─────────────────┼───────────────────────────────────┼─────────────────────────┼────────────┤
 │ 2   │ OpenAI          │ ChatGPT macOS, ChatGPT iOS,       │ Remote MCP server (we   │ MVP        │
 │     │ (ChatGPT)       │ chatgpt.com                       │ host)                   │            │
 ├─────┼─────────────────┼───────────────────────────────────┼─────────────────────────┼────────────┤
 │ 3   │ Grok (xAI)      │ TBD                               │ No MCP support yet      │ Blocked    │
 ├─────┼─────────────────┼───────────────────────────────────┼─────────────────────────┼────────────┤
 │ 4   │ Hermes / Meta / │ TBD                               │ Probably MCP, need to   │ Question   │
 │     │  Llama          │                                   │ investigate             │ mark       │
 └─────┴─────────────────┴───────────────────────────────────┴─────────────────────────┴────────────┘

 MVP is Anthropic + OpenAI. Grok blocked on MCP support. Hermes/Meta/Llama need investigation on how they
  integrate into LDM. May be MCP, may be different.

 MCP tools (what the agent can do):
 - crystal_search ... "I had an idea about X with Claude" (works from ChatGPT)
 - crystal_remember ... save something to memory
 - crystal_forget ... delete a memory
 - crystal_export ... export memories
 - crystal_status ... see what's connected, usage, bucket info
 - More TBD based on what's needed

 Three Customer Types

 Customer 1: Consumer

 "I want my AI to remember across everything."

 Journey:
 1. User is on claude.ai or chatgpt.com (wherever they already are)
 2. Adds Memory Crystal as an MCP connector (remote, we host it)
 3. Uses AI normally. Memory accumulates automatically.
 4. Pays via Agent Pay. No friction.
 5. Optionally installs the iOS/Mac app for Apple features.

 The consumer installs nothing up front. No local MCP server. No CLI. No npm. We host the MCP servers.
 They connect.

 Buckets: Users name their memory spaces whatever they want (like we have cc-mini, cc-air). Multiple
 buckets per account. An agent, a project, a persona.

 The app is the upgrade, not the requirement:
 - Without app: MCP works, memories sync, search works, Agent Pay charges them
 - With app: Face ID, Secure Enclave, Keychain, QR code auth, dashboard, sovereign mode

 Customer 2: Developer (for themselves)

 "I want memory for my own agents and scripts."

 Same as Consumer, plus they can use the SDK to build custom agents that share the same memory. They
 don't need a harness. They build whatever they want and it remembers.

 from crystal import Crystal
 client = Crystal(crystal_key="ck-...")
 client.remember("User prefers dark mode")
 results = client.search("user preferences")

 Customer 3: Platform Developer (for their users)

 "I want to build an app that gives MY users memory."

 Two sub-types (from Lesa's doc):

 ┌───────────────────┬───────────────────────┬─────────────────────────────────────┐
 │                   │ Tier 1: For Yourself  │          Tier 2: Platform           │
 ├───────────────────┼───────────────────────┼─────────────────────────────────────┤
 │ Who signs up      │ You                   │ You (the developer)                 │
 ├───────────────────┼───────────────────────┼─────────────────────────────────────┤
 │ Who owns memories │ You                   │ Your users (managed by you)         │
 ├───────────────────┼───────────────────────┼─────────────────────────────────────┤
 │ Apple ID required │ Yes                   │ Only yours, not your users'         │
 ├───────────────────┼───────────────────────┼─────────────────────────────────────┤
 │ API key type      │ Personal              │ Platform (multi-tenant)             │
 ├───────────────────┼───────────────────────┼─────────────────────────────────────┤
 │ CloudKit          │ Your private database │ Your container, partitioned by user │
 ├───────────────────┼───────────────────────┼─────────────────────────────────────┤
 │ Pricing           │ Per-user plan         │ Per-API-call or per-seat            │
 └───────────────────┴───────────────────────┴─────────────────────────────────────┘

 We're downstream. We don't know what their app does. We store and search memories for their user IDs. We
  charge the developer.

 Customer 4: Enterprise (self-hosted)

 "I want to run this myself on my infrastructure."

 The existing Core/Node architecture. Install Crystal, run it, MIT licensed. No Apple stuff required. No
 dependency on us. This is what we run today.

 ---
 Two Modes of Operation

 Sovereign Mode (app installed, core device available)

 Everything runs on the user's device:
 - Memory extraction
 - Embedding generation
 - Search/retrieval
 - Encryption (CryptoKit + Secure Enclave)

 Our server just routes. Auth, route, bill. Never sees plaintext.

 CloudKit stores encrypted blobs we can't read.

 Cloud Mode (no core device, web only, demo)

 User connected via MCP from a browser. No app. No core device.

 We run the embeddings and extraction on our servers. We briefly have their data. We encrypt it and push
 to CloudKit.

 This is the demo/acquisition funnel. Transparent about it:
 - "Demo mode. Your memories are processed on our servers."
 - "Install the Memory Crystal app to move everything to your device."
 - Limited memories, nag to install app
 - Or: charge significantly more for cloud mode to incentivize sovereign mode

 The system auto-detects: If a core device is registered and online, route to it (sovereign). If not,
 fall back to cloud processing (demo).

 ---
 Architecture

 Claude.ai / ChatGPT / Open Claude / Hermes
     ↓ (MCP connection)
 Our Hosted MCP Server (wip.computer VPS)
     ├── Auth (validate API key / Agent Pay)
     ├── Route traffic
     ├── Billing / usage metering
     ├── IF no core device: run embeddings + extraction here (cloud mode)
     ↓
 CloudKit (Apple infrastructure)
     ├── One container, ours
     ├── Per-user private databases (Apple handles multi-tenancy)
     ├── Enterprise shared zones
     ├── E2E encrypted
     ↓
 User's devices (Mac, iPhone, web)
     ├── Crystal app shows memories, search, manage
     ├── IF sovereign mode: extraction + embeddings run HERE
     ├── CryptoKit + Secure Enclave

 "Our server is a router with a cash register." Auth, route, bill. Three things.

 Why Linode, not Cloudflare Workers: The router is so thin ($5/mo VPS) that Workers is overkill. We're
 only on Linode because Apple doesn't sell compute. If Apple opens Private Cloud Compute, we drop Linode.

 Why not Cloudflare Workers: We don't need global edge. Memory search isn't latency-critical. One VPS is
 simpler, cheaper, and we control it. No vendor-specific code.

 ---
 The App

 One app. iOS app that runs on Mac (Catalyst / iPad on Mac).

 Not two separate apps. One codebase. iOS first because:
 - Keychain integration
 - Face ID / biometric auth
 - Agent Pay (Apple Pay integration)
 - QR code auth: agent shows QR code, user scans with phone, authenticates with built-in keys
 - Push notifications
 - The Mac version is the iOS app running on macOS

 What the app does:
 - Dashboard: see all connected AIs, all buckets, all memories
 - Search: semantic search across all memories
 - Manage: delete, organize, set permissions
 - Auth: Face ID, QR code device pairing
 - Agent Pay: billing, usage, payment methods
 - Secrets: Keychain-based credential storage for agents
 - Settings: core device designation, sovereignty status

 What the app does NOT do:
 - Run an LLM
 - Replace Claude or ChatGPT
 - Require a subscription to use the MCP (MCP works without the app)

 ---
 SDK (OpenAI-Compatible Proxy)

 No special library to install. Crystal is an OpenAI-compatible API proxy with memory. Developers change
 one line: the base_url.

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

 Why OpenAI-compatible:
 - OpenAI's API format is the de facto standard
 - Every language has an OpenAI SDK (Python, Node, Go, Rust, etc.)
 - Works with LiteLLM, OpenRouter, any existing stack
 - Zero SDK to install. Use whatever OpenAI library you already have.
 - One line change to add memory to any existing app.

 The stack:
 Developer's App (standard OpenAI SDK)
     ↓ (base_url = crystal.wip.computer)
 Crystal Proxy (memory layer: search, inject, extract, store)
     ↓
 Anthropic / OpenAI / Google / local models

 Crystal handles memory. Routes to the right provider. One proxy, any model, automatic memory.

 ---
 Enterprise / Self-Hosted (Core + Node)

 The existing architecture. No Apple dependency. MIT licensed.

 - Core: always-on machine, primary Crystal instance
 - Node: mirrors, syncs to Core
 - Permission levels per machine (admin, read/write, read-only)
 - No CloudKit. HTTP sync between nodes.
 - This is what we run today. This is what enterprises who can't use Apple run.

 The Apple features (CloudKit, Face ID, Agent Pay) are what you get when you install the app. Enterprise
 without the app still works. It's just local.

 ---
 Pricing (Draft)

 Consumer (MCP):
 - Free for 30 days (cloud mode, demo)
 - After 30 days: install app + load Agent Pay wallet ($25) for 30 more free days
 - Then: monthly subscription TBD

 SDK Proxy (developers):
 - Crystal memory fee (fixed, per-call or per-month) + model cost (pass-through)
 - We never mark up the model cost. We charge for the memory layer.

 Model cost pass-through:

 ┌────────────────┬────────────────┬─────────────────────────────────────────────────────────────────┐
 │    Provider    │  Relationship  │                          How it works                           │
 ├────────────────┼────────────────┼─────────────────────────────────────────────────────────────────┤
 │ Anthropic      │ Direct (we     │ Pass-through API cost                                           │
 │                │ own)           │                                                                 │
 ├────────────────┼────────────────┼─────────────────────────────────────────────────────────────────┤
 │ OpenAI         │ Direct (we     │ Pass-through API cost                                           │
 │                │ own)           │                                                                 │
 ├────────────────┼────────────────┼─────────────────────────────────────────────────────────────────┤
 │ Grok (xAI)     │ Direct (we     │ Pass-through API cost                                           │
 │                │ own)           │                                                                 │
 ├────────────────┼────────────────┼─────────────────────────────────────────────────────────────────┤
 │ Everything     │ Via OpenRouter │ Pass-through OpenRouter cost, OR user provides their own        │
 │ else           │                │ OpenRouter API key                                              │
 └────────────────┴────────────────┴─────────────────────────────────────────────────────────────────┘

 Three direct integrations. OpenRouter for the long tail. User can always bring their own OpenRouter key
 and just pay us for memory.

 Platform (multi-tenant):
 - Per-seat or per-API-call pricing
 - Same model pass-through structure

 Enterprise (self-hosted):
 - MIT licensed, run it yourself
 - No dependency on us, no Apple required
 - License or support contract

 ---
 What We Build (in order)

 Phase 1: Hosted MCP Server (the product for consumers)

 - Remote MCP server on Linode (wip.computer)
 - MCP tools: search, remember, forget, export, status
 - Auth + Agent Pay integration
 - Cloud-side embedding + extraction (cloud mode for users without app)
 - CloudKit storage (server-to-server API)
 - Buckets (user-named memory spaces)
 - User connects from claude.ai, chatgpt.com, Open Claude, any MCP client
 - Free 30 days. Then Agent Pay wallet.
 - This IS the product. No App Store review needed. No download.

 Phase 2: iOS App (sovereign mode + Apple features)

 - One app: iOS that runs on Mac (Catalyst / iPad on Mac)
 - Apple ID sign-in, CloudKit integration
 - Face ID, Keychain, Secure Enclave
 - QR code auth for device pairing (agent shows QR, phone scans, authenticates)
 - Agent Pay wallet management
 - Core device designation (moves processing off our servers to user's device)
 - Settings: manage connections, buckets, sovereignty status
 - NOT where you use memory. That's the agent. This is auth/billing/settings.

 Phase 3: OpenAI-Compatible Proxy (the product for developers)

 - OpenAI-compatible API at crystal.wip.computer
 - Change base_url, get memory. No SDK to install.
 - Direct integrations: Anthropic, OpenAI, Grok (xAI)
 - Everything else: wrapped OpenRouter (pass-through cost, or bring your own key)
 - Auto-extract memories from responses, auto-inject context into prompts
 - Crystal fee + model pass-through pricing

 Phase 4: Platform API (for developers building apps)

 - Multi-tenant API keys (developer manages their users' memories)
 - Per-user isolation
 - Usage metering, billing per-seat or per-call
 - Developer manages memory, end user never knows Crystal exists

 Phase 5: Swift SDK (native Apple, optional)

 - Native Apple framework for developers building iOS/Mac apps
 - Direct CloudKit integration (no server round-trip)
 - CryptoKit + Secure Enclave
 - For apps that want the deepest Apple integration

 ---
 Key Decisions (extracted from conversations)

 1. Server is just a router. Auth, route, bill. Never sees plaintext in sovereign mode.
 2. One CloudKit container. Ours. Apple handles multi-tenancy. Like WhatsApp.
 3. No Cloudflare Workers. Linode VPS is sufficient. Simpler.
 4. iOS first. One app that runs on Mac. Not two apps.
 5. Consumer installs nothing. MCP connection to our hosted servers. App is optional upgrade.
 6. Demo mode is the funnel. Free, limited, transparent: "your data is on our servers, install the app to
  fix that."
 7. Same version = same code. Version immutability across all releases.
 8. Four-track releases. Alpha, beta, hotfix, stable. Alpha never requires deploy-public.
 9. Hermes is the fourth agent. Not a platform. Integrated. Verifies the architecture.
 10. Enterprise is self-hosted. MIT licensed. No Apple dependency. Core + Node architecture.
 11. "Anthropic sells the thinking. We sell the remembering."
 12. We architecturally CAN'T read their data. Not "we promise not to." The keys never leave their
 device.

 ---
 Auth Model

 No email login. Two methods:

 1. Magic link: Enter email, get a link, click it, you're in.
 2. Passkeys (de facto standard): Set up a passkey. Log in with QR code + Face ID on phone. No password.
 No email. Keys-based.

 Passkeys should be the default. Magic link is the fallback.

 Answered Questions

 - Web app: No. There is no web app. Everything is agent-based. MCP tools inside the AI.
 - SDK model: OpenAI-compatible proxy. Change base_url. No special library.
 - Demo pricing: Free 30 days. Then incentive to install app + load Agent Pay wallet ($25).
 - Model routing: Anthropic, OpenAI direct. Grok blocked (no MCP). Everything else via OpenRouter.
 - App count: One app. iOS that runs on Mac.
 - MVP platforms: Anthropic + OpenAI only. Grok and Hermes/Meta/Llama are future.
 - Auth: Passkeys (Face ID + QR code) as default. Magic link as fallback. No email/password login.
 - MCP tools: Will define later. Core is search/remember/forget/export/status + buckets + instructions.
 - Export: Creates a link (no email attachment).

 Open Questions

 1. Hermes / Meta / Llama integration: How do these agents integrate into LDM? Probably MCP but need to
 investigate.
 2. CloudKit server-to-server API limits: Free tier is generous (1PB assets), but what are the API call
 limits at scale?
 3. Apple Foundation Models SDK (WWDC25): On-device embeddings would eliminate OpenAI embedding API
 dependency. Timeline?
 4. Agent Pay wallet mechanics: How does the 30-day free trial transition? How does wallet loading work?
 5. Passkey implementation: Apple's passkey API for the iOS app. How does the QR code flow work
 technically?
 6. Embedding cost in cloud mode: Included in Crystal fee or separate line item?
 7. OpenRouter relationship: Formal partnership or just use their public API?
 8. Grok MCP timeline: When does xAI add MCP support? Monitor.

 ---
 Files

 - Vision source: ai/product/product-ideas/vision-quest-01/lesa-vision-01.md
 - CC session: ai/product/product-ideas/vision-quest-01/cc-mini-01.md
 - This plan: to be written as ai/product/product-ideas/vision-quest-01/architecture-spec.md
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

 Claude has written up a plan and is ready to execute. Would you like to proceed?

 ❯ 1. Yes, and bypass permissions
   2. Yes, manually approve edits
   3. Tell Claude what to change
      shift+tab to approve with this feedback

 ctrl-g to edit in Vim · ~/.claude/plans/sprightly-watching-nova.md
