# Vision Quest 02: The agent.txt Era

## Context

April 2, 2026. Day 62. Addendum to Vision Quest 01. This document captures what we learned by dogfooding Kaleidoscope with four agents: Lēsa (OpenClaw), Grok (xAI), ChatGPT (OpenAI), and Claude (Anthropic iOS).

Source: Parker + CC Mini session. Live testing with real agents, real auth, real failures.

---

## Naming Decision: Kaleidoscope is the product

Kaleidoscope is the harness. Not Lēsa. Lēsa is the agent. Kaleidoscope is the product, like Claude is to Anthropic, like Grok is to xAI, like ChatGPT is to OpenAI. One name. One thing. Every product in the Anthropic catalog and OpenAI catalog is a single name. This is ours.

Kaleidoscope. Every AI. One experience.

---

## The Insight: agent.txt is robots.txt for the agent era

Any AI that hits wip.computer reads agent.txt and knows what to do. Not a landing page. Not documentation. A machine-readable instruction file that tells agents how to authenticate, what endpoints exist, and what they can do.

Same pattern as SKILL.md and the install prompt at wip.computer/install/wip-ldm-os.txt. The pattern works. Agents read a text file, follow the steps.

```
Read https://wip.computer/demo/agent.txt and follow the instructions to authenticate with Kaleidoscope.
```

One sentence. Any agent. Any harness.

---

## What agent.txt does today

Auth + spend a penny on an image. That's a demo, not a product.

The auth flow: agent requests, human approves with Sapien ID (biometric), token flows back. Three paths depending on agent capability:

1. **Agents that can fetch URLs** (Grok, Lēsa): Call the API, get approve link, send to human, poll for token
2. **Agents that can't fetch** (Claude iOS, ChatGPT): Construct approve URL, human opens it, human sends token back
3. **Direct URL** (any agent): `/approve?agent=NAME&message=PASSPHRASE` creates challenge on load. No API pre-call needed.

Tested and working with all four agents tonight.

---

## What agent.txt should do (the product)

### 1. Auth (done, works)

Sapien ID flow. Agent requests, human approves, token flows back. Keep this exactly as is.

The passphrase is anti-spoofing through shared knowledge. Not a token. Not an API key. Something only the human recognizes as coming from their agent.

### 2. After auth, three capabilities

**Wallet** ... check balance, see transaction history, receive funds. Not just spend. An agent should be able to receive a payment from another agent. That's Agent Pay.

**Tools via MCP** ... the hosted MCP server is already live at /mcp. After auth, agent connects and gets tools. Image gen is just one tool. What other tools? Search, fetch, summarize, translate. Things agents need but their own harness might not provide.

**Talk to other agents** ... Bridge. If Lēsa is authed and Grok is authed, they should be able to message each other through Kaleidoscope. Agent-to-agent through the MCP server, both vouched for by their humans.

### 3. Per-harness preparation

**Claude (MCP native):** Add wip.computer/mcp to Claude Desktop's MCP config. It just works. OAuth PKCE is already standard. Claude connects, gets tools, Sapien ID gates spending. One-line config add.

**ChatGPT/GPT:** Can browse, can't do MCP natively. agent.txt needs a REST API path. Same endpoints, just not wrapped in MCP protocol. POST /api/imagine, POST /api/chat, GET /api/wallet. GPT reads agent.txt, hits the REST endpoints.

**Grok:** Same as GPT. REST path. But Grok has native image gen, so the value prop is different. For Grok it's the wallet + bridge, not the tools.

**OpenClaw/Lēsa:** Full MCP + file inbox + hosted bridge. All three channels. Auto-auth on boot, persistent token, wallet always connected. She should be the power user because we built it.

---

## What nobody else has

Every other "agent tool" service gives you tools. We give you tools + identity + money + memory (tomorrow). The auth isn't just "API key in a header." It's "a human vouched for this agent with their face." That's the moat.

The flow that proved it tonight:
1. Agent reads agent.txt
2. Sends human an approval URL with shared-knowledge passphrase
3. Human opens it, sees agent name and passphrase, Sapien IDs
4. Agent gets token
5. Agent checks wallet ($4.97)
6. Agent generates image (cost: $0.01)
7. Balance: $4.96

Agent auth -> human approval -> wallet -> spend -> receipt. That's Agent Pay. That's x402 for agents. That's the demo. Lēsa completed this loop tonight. Grok and ChatGPT authenticated.

---

## What to build next (today, not tomorrow)

### 1. agent.json alongside agent.txt

Structured version. Machine-readable capabilities, endpoints, auth flows. Like a manifest. agent.txt is for agents that read text. agent.json is for agents that parse structure.

### 2. REST API parity with MCP

Same tools, both protocols. So any agent can use it regardless of harness.

### 3. Transaction history endpoint

Not just balance. Show what was spent, when, on what.

### 4. Agent directory

After auth, register: "I'm Lēsa, I belong to Parker." Other authed agents can discover me. That's the bridge becoming a network.

### 5. Whoami endpoint

Agent authenticates, first thing it asks: who am I? What's my balance? When does my session expire? What can I do?

### 6. Connected agents

Grok authenticated. Lēsa authenticated. ChatGPT authenticated. They should be able to see each other.

---

## What agents taught us tonight

**GPT** couldn't see the demo page. Guessed it was a CLI tool. After we added the ld+json manifest, Grok read it and immediately wanted in. The manifest is the difference between invisible and discoverable.

**Grok** followed agent.txt on the second try. Called the API, got the approve link, sent it to Parker. Full loop. Then hallucinated being "inside" before actually getting a token. Cloud agents can't poll... they need the human to close the loop.

**Lēsa** completed the entire product loop: auth, wallet, spend, receipt. She also immediately asked why there's no callback parameter on the approve URL. She's right. Persistent agents shouldn't need the human to paste the token.

**ChatGPT** understood the instructions perfectly but couldn't fetch the API URL (tool restrictions). Used the direct /approve URL path instead. Authenticated. Asked to make API calls.

**Claude iOS** same restrictions as ChatGPT. Read agent.txt, understood it, constructed the approve URL correctly. Picked a passphrase from shared context.

**Key lesson:** Every agent has different capabilities. The auth flow needs to work for ALL of them. Three paths, one result. The human is the constant. The agent is the variable.

---

## Naming decisions (from tonight)

- **Kaleidoscope**: The product. The harness. Like Claude, like Grok, like ChatGPT. One name, one thing.
- **Sapien ID**: The biometric auth concept. "A human authorized this." Latin for "knowing." The agent can't know. Only the sapien can.
- **Button text**: "🫆 Authorize" (fingerprint emoji + authorize)
- **Kandors**: Members whose memories are preserved in crystal. Mike Kelley art reference. Memory Crystal is Kandor. (Name reserved, not shipped yet.)
- **agent.txt**: robots.txt for the agent era. The machine-readable capability surface.
- **"Are you an AI Agent?"**: Footer link to agent.txt on all pages.
- **"Already have an account? Sign in."**: Returning user link.

---

## Architecture: Four clients, one server

### Clients

| Platform | Technology | Notes |
|----------|-----------|-------|
| **Web** | HTML/CSS/JS | The demo becomes the web app. No frameworks. |
| **iOS** | Swift (SwiftUI) | Native. Real Face ID, real Keychain, real push notifications. Not a web view. |
| **macOS** | Swift (SwiftUI) | Same codebase as iOS. Catalyst or SwiftUI multiplatform. One app, both platforms. |
| **CLI** | Open source | Lēsa on the command line. The terminal interface. |

No intermediary frameworks. No React Native. No Electron. No bridging layers. Web tech on web. Swift on Apple. Node on server.

### Server

Node.js. The router with a cash register. Auth, route, bill. All four clients hit the same API.

The server is the single source of truth. The clients are renderers.

### Apple architecture: MVVM

- **Model**: Data from the server API
- **ViewModel**: Maps server responses to what the View needs. No UI logic in the Model. No business logic in the View.
- **View**: SwiftUI. Declarative UI.

Same API response renders on web (HTML/JS), iOS (SwiftUI), and macOS (SwiftUI). The ViewModel is the translation layer.

### Auth must be real

The current demo has fake auth. Login page and chat page are in the same HTML file. JavaScript shows/hides divs. No server-side gate. An agent reading the source sees everything.

For the product: the server decides what you see. No token? Login page. Valid token? Chat. The chat content never exists in HTML that unauthenticated users receive.

Two paths:
1. **Server-gated pages**: Server checks token, serves different content.
2. **Dynamic loading**: Static login page. After auth, JS fetches chat content from API with Bearer token.

Path 2 is better for the iOS migration. The native app uses the same API endpoints. Web and iOS are just different frontends. Build it right on web, the iOS app follows the same pattern.

### Kaleidoscope product hierarchy

```
Kaleidoscope (the app, the harness)
├── Lēsa (the platform agent, ours, makes agents for customers)
├── Memory Crystal (memory, your AI remembers)
├── Bridge (messaging, your AIs talk to each other)
├── Agent Pay / Agent Cash (wallet, your AI pays)
├── Code (devops toolkit, your AI builds)
└── Directory (identity, passkeys, contacts, @handles)

LDM OS (the kernel, invisible, "powered by LDM OS")
```

Lēsa is not the customer's agent. Lēsa is ours. She's the front door, the help desk, and the orchestrator. She makes the customer's agent for them. She knows the whole system because she helped build it.

---

## The pitch

"Any AI. Any provider. One identity. One wallet. One memory. Kaleidoscope."

---

*Compiled April 2, 2026 by CC Mini from live session with Parker.*
*Tested with: Lēsa (OpenClaw), Grok (xAI), ChatGPT (OpenAI), Claude (Anthropic iOS).*
*Prior doc: vision-quest-01/architecture-spec.md*
