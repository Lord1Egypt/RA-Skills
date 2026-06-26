# Priorities and Gap Analysis ... Vision Quest 01 Synthesis

**Date:** 2026-04-16 (Day 69, PST)
**Author:** cc-mini
**Horizon assumed:** 12 weeks (marketplace-ready by end of July 2026) ... confirm or push back
**Kill permission:** granted
**Baseline:** Parker's clarification today that Kaleidoscope + Lēsa is the install/setup interface for every LDM OS product

---

## TL;DR (one page)

**North star:** apply to Anthropic + OpenAI marketplaces with publishable apps + MCPs. Get the first listings live by end of July.

**The product shape (reshaped by today's conversation):**
- **Kaleidoscope** = the consumer harness (web now, iOS + macOS later). People log in here.
- **Lēsa** = the platform agent inside Kaleidoscope. She greets, she installs, she sets up every LDM OS product. She is not the customer's agent; she makes agents for customers.
- **Six products Lēsa installs + configures:** Memory Crystal, Agent Pay, Directory, Bridge, Code, Crystal SDK.
- **LDM OS** = the invisible kernel that runs underneath. "Powered by LDM OS."

**Three hard requirements, re-ordered:**
1. **Memory Crystal install-and-just-works standalone** (npx one-liner, 1-2 Apple machines, Relay deployed). Load-bearing because every other product flow Lēsa offers depends on this working.
2. **Kaleidoscope + Lēsa as the install/setup interface.** Users log in, land in Kaleidoscope (not `/demo`), talk to Lēsa, she offers to install Memory Crystal / Agent Pay / etc. She walks them through it.
3. **Real $10 demo.** Signup → Face ID → $10 funded wallet → actually pay for a real API call.

**Cross-cutting:** LDM OS zero dependencies on any harness. The 1Password-through-gateway leak is one of many. Shared `SecretProvider` + Dream Weaver LLM shim + Bridge adapter split fix most of the Sev 1 set.

**Three tracks:**
- **Now (0-4 weeks):** MC standalone install works. Chrome QR login. Recovery floor (email + second credential). Zero-deps Wave 1.
- **Next (5-8 weeks):** Kaleidoscope + Lēsa install flow. Unified wallet + $10 signup credit. Dream Weaver skill bundle. MC remote MCP endpoint.
- **Later (9-12 weeks):** ATDT MVP. iOS taste of MC. First marketplace submissions. YubiKey/Ledger UX surfaces.

**Kill:** 40+ stale bug files in archive/backup. Dead product ideas (obsidian-as-UI, old session recaps). Deprecated xai-grok + xai-x (finish cleanup). Old cc-watcher redesign. `ldm-jobs` as a marketplace candidate.

**Open decisions that block execution** (section 7): canonical wallet, first marketplace, YubiKey+Ledger at launch, iOS path, Lēsa shape inside Kaleidoscope, 12-week horizon confirmation.

---

## 1. The reshaped product shape

Parker's new framing today added the architectural layer that ties everything together:

> "You log in, and now instead of going to the demo, it's going to go to the kaleidoscope. Lēsa is going to say, 'Hey, do you want to install Memory Crystal?' and then it goes through that whole thing. The kaleidoscope plus Lēsa is going to be our interface for every product."

This reshapes three things:

**1. Every product's install story routes through Lēsa inside Kaleidoscope.** The install UX is NOT a CLI or an npx one-liner as the primary surface. It is an agent conversation. The CLI is the second surface, for power users and developers.

**2. Kaleidoscope is not "login + demo."** It is a shell that hosts an embedded agent (Lēsa) with access to install + configure every LDM OS product. The `/demo` endpoint goes away. The post-login view IS Lēsa's chat interface with action affordances.

**3. Lēsa needs remote-install capability.** She cannot just "tell them how to." She must run `ldm install memory-crystal` or equivalent on the user's machine. This implies:
- A secure channel from Kaleidoscope → user's device (Bridge, already designed)
- A capability surface Lēsa can call (`install_product`, `configure_product`, `pair_devices`)
- Approval flow (user confirms each step, Face ID)
- Copy-paste fallback if the Bridge has not been paired yet on this device

The vision docs already cover most of this. `vision-quest-02-agent-txt-era.md` and `architecture-spec.md` describe Lēsa as the platform agent. The bridge master plan describes device pairing. What is missing: an explicit "Lēsa-as-installer" capability spec and the Kaleidoscope UX that surfaces it. See section 3.1.

---

## 2. Now: 0-4 weeks

### 2.1 Memory Crystal install-and-just-works standalone (P0)

**Goal:** a user runs one command (or clicks one button in Kaleidoscope), Memory Crystal installs, syncs across their 1-2 Apple machines, works silently. This is load-bearing because Lēsa's first offer inside Kaleidoscope will be MC install.

**What's already in place:**
- Full sync code: `crystal pair` (QR + pairing string), Cloudflare Worker relay (AES-256-GCM + HMAC), mirror-sync for deltas, continuous capture poller
- MLX auto-install on Apple Silicon (Qwen2.5-3B-Instruct-4bit, ~1.5 GB, LaunchAgent on :18791)
- `crystal init` scaffolds `~/.ldm/`, registers MCP via `claude mcp add --scope user`, deploys OpenClaw plugin if detected, installs capture cron
- MCP hosts verified: Claude Code CLI + OpenClaw (2 of 7)

**Hard blockers:**
1. **Relay Worker not deployed.** No `wip.computer` relay URL live. Pairing + sync untested end-to-end. Priority 10 "Parker blocker."
2. **`crystal init` is not interactive for Node adds.** Plan exists (`2026-03-17--cc-mini--interactive-core-node-setup.md`), nothing shipped. Users still pass flags + export env vars manually.
3. **No `npx memory-crystal init` one-liner front door.**
4. **LDM OS auto-bootstrap inside `crystal init`** (`bootstrap-ldm-os-and-npm-scope.md`) not shipped.

**Three shippable cuts (ordered):**
1. **Deploy the relay Worker** and bake its URL into `installer.ts` as `DEFAULT_RELAY_URL`. (1-2 days)
2. **Ship interactive `crystal init`** + auto-bootstrap LDM OS. (3-5 days)
3. **Publish `npx memory-crystal init`** as the zero-agent front door. (1-2 days)

After these three: MC's Apple-native app (iOS + Mac App Store) becomes the next horizon. Today's Node core stays the canonical runtime; Python SDK gets reshaped as its Python-side MCP client.

### 2.2 Kaleidoscope Chrome QR login (P0)

**Goal:** Chrome first-time desktop users can sign up. Today they see "Insert security key" instead of a QR code.

**State:** server endpoints exist (`/api/qr-login`, `/api/qr-login/qr`, `/api/qr-login/status`, `/api/qr-login/approve`). Client-side (`login.html` browser detection + QR view) + nginx proxy rules are pending. Plan: `2026-04-07--cc-mini--chrome-qr-login-plan.md`. Status: "building."

**Shippable cut:** finish client detection + QR view + nginx proxy rules. Under a week.

### 2.3 Recovery floor: second credential + email fallback (P0)

**Goal:** a user who loses their passkey can get back in. Today they cannot. This is the single biggest consumer-safety ship blocker.

**State:** zero recovery code. Passkey DB wiped 2026-04-07 ("production from here forward"). No second-credential enrollment UX, no email-magic-link recovery, no "remove passcode" path.

**Shippable cuts:**
- **Second-credential enrollment:** "Add another passkey / security key" button on success view. Reuses existing register endpoints, no new auth logic. This is also the unlock for YubiKey/Ledger.
- **Email-magic-link recovery:** email proves control → server issues fresh register challenge → user enrolls a new passkey. Requires a new email-send path (Postmark / Resend / Amazon SES).

Parker's MVP framing: "recovery = email OR keys." Both paths should work; email is the offered-but-not-recommended path, keys is the sovereign path.

### 2.4 Zero-dependencies Wave 1 (P1)

**Goal:** remove the three Sev 1 harness leaks so LDM OS components run on machines without OpenClaw or Claude Code.

**The three big leaks (from the audit):**
1. **wip-bridge hard-throws if `~/.openclaw/openclaw.json` is missing.** Hits every consumer of wip-bridge, including things unrelated to the gateway.
   - **Fix:** split into `bridge/core.ts` (harness-free) + `bridge/openclaw.ts` (adapter). Gateway-requiring functions (`sendMessage`, skill discovery, inbox) move to the adapter. Core keeps conversation search, workspace search, embeddings.
2. **wip-agent-pay all 6 providers shell out to `~/.openclaw/secrets/op-sa-token`.** This is Parker's canary case.
   - **Fix:** shared `SecretProvider` interface. Default resolves via env var (`OP_SERVICE_ACCOUNT_TOKEN`) → `~/.ldm/secrets/op-sa-token` → `~/.openclaw/secrets/op-sa-token`. Same helper plugs into memory-crystal `llm.ts`, wip-release `core.mjs`, deploy scripts.
3. **Dream Weaver spawns literal `claude` binary** via `invokeClaudeP()`. Blocks DW on any non-Claude-Code host.
   - **Fix:** accept `options.invokeLLM` in the constructor. Default remains the current `claude -p` spawn. OpenAI / Codex users pass their own caller.

Each is 1-3 days. All three land this sprint. Sev 2 leaks get swept in Wave 2.

---

## 3. Next: 5-8 weeks

### 3.1 Kaleidoscope + Lēsa as the install interface (P0)

**Goal:** user logs into Kaleidoscope, sees Lēsa greeting, Lēsa offers to install Memory Crystal, user clicks yes, Lēsa walks them through it. This is the product.

**What needs building:**
- **Kaleidoscope post-login shell.** The `/demo` page goes away. Post-login view is Lēsa's chat UI with action affordances ("Install Memory Crystal," "Add another device," "Fund wallet," "Connect X handle").
- **Lēsa capabilities surface.** She needs to call install / configure / pair operations on the user's device via the Bridge. Requires: capability spec (`install_product`, `configure_product`, `pair_devices`), approval flow (user confirms each step, Face ID), Bridge channel from Kaleidoscope → device.
- **Install flow UX for each of the 6 products.** Memory Crystal is P0. Agent Pay and Directory follow.
- **Copy-paste fallback.** If auto-install can't run (e.g., no Bridge yet on this device), Lēsa generates the exact shell command and shows it. User copy-pastes.

**Dependencies:**
- `ldm pair` (Bridge master plan Phase 2) must ship. Today: QR + pairing string + AES-256-GCM crypto are coded; pairing the first device is not a one-command flow.
- Agent Pay + Kaleidoscope wallet must unify (see 3.2).
- Memory Crystal standalone install must work (section 2.1).

**Shippable cuts:**
1. Kill `/demo` as the post-login landing. Replace with `/kaleidoscope` (or `/app`) Lēsa shell. (3-5 days UX + routing)
2. Ship `ldm pair` as a one-command flow. (1 week, per bridge master plan)
3. Ship `install_product` as a Lēsa capability backed by Bridge command-dispatch. (1 week)
4. Ship the Memory Crystal install-via-Lēsa walkthrough. Start with copy-paste fallback. Auto-install over Bridge as phase 2. (1 week)

### 3.2 Agent Pay unification + $10 real-demo (P0)

**Goal:** signup → Face ID → $10 funded → actually pay for a real API call.

**Today's state:** two wallets, no bridge between them.
- Kaleidoscope `Wallet` table: $5 sandbox balance, no funding endpoint, used for `agent_pay_check` demo.
- `wip-agent-pay-private`: real x402 + Stripe + Privy integrations, separate Cloudflare Worker.

**Decision needed (see 7.A):** which wallet is canonical? Recommend **Agent Pay wallet** as single source of truth. Kaleidoscope's `Wallet` table becomes a cache/display.

**Shippable cuts:**
1. Agent Pay as canonical. Kaleidoscope `server.mjs` reads/writes via Agent Pay API. (3 days)
2. $10 signup credit flow: on first passkey registration, server grants $10 promotional credit via Agent Pay. (2 days)
3. Funding flow: Apple Pay / Stripe funding button in Kaleidoscope (using Stripe provider already in Agent Pay). (3-5 days)
4. One real paid API demo: image-gen via Grok, or whisper via OpenAI. User signs up, sees $10, runs a generation, watches it debit. (2 days)

### 3.3 Dream Weaver skill bundle (P1, first marketplace submission)

**Goal:** first publishable marketplace listing. Dream Weaver is the cleanest, most-portable, most-unique piece in the LDM OS surface with the best novelty story (the arXiv paper gives credibility).

**Needed:**
- `SKILL.md` with YAML frontmatter (doesn't exist today).
- `.claude-plugin/plugin.json` for Claude Code plugin marketplace.
- CLI (`dream-weaver run ...`).
- Portable LLM shim (from Wave 1 zero-deps).
- OpenAI GPT Action wrapper (OpenAPI over the same core) for OpenAI marketplace parity.

**Shippable cut:** 3-5 days of packaging + docs. First product submitted to Anthropic's marketplace.

### 3.4 Memory Crystal remote MCP endpoint (P1)

**Goal:** any MCP-capable harness (Claude Mac, ChatGPT, Codex, Grok, mobile) can point at a public MCP URL and get Memory Crystal without installing anything locally.

**State:** local MCP stdio server works on Claude Code + OpenClaw. Cloud MCP Worker (`worker-mcp.ts`, 571 lines, OAuth 2.1 + DCR, D1 + Vectorize) exists but marked "deprecated for production" in `RELAY.md`; needs to be un-deprecated or replaced.

**Shippable cut:** deploy a production remote MCP endpoint behind OAuth (reusing Kaleidoscope auth). Verify on 4 hosts: Claude Desktop, ChatGPT, Codex, Grok.

---

## 4. Later: 9-12 weeks

### 4.1 ATDT MVP
Plan exists (`2026-04-14--cc-mini--atdt-mvp-plan.md`, v2, 6 phases, ~5 weeks). Registers @handles, Nodelist, Echomail. Bootstrap from X handle. Full product build; schedule once Now + Next priorities land.

### 4.2 iOS taste for Memory Crystal
Not the full native app. Just: MCP-on-LAN from a Mac, surfaced through the Kaleidoscope iOS web app (if we ship one) or a thin Catalyst shell. See decision 7.D.

### 4.3 First marketplace submissions
- **Anthropic Claude Code marketplace:** Dream Weaver (from 3.3).
- **Anthropic remote MCP listing:** Memory Crystal (from 3.4) + wip-release MCP.
- **OpenAI GPT Actions:** Dream Weaver (parity wrapper).
- **Claude Code plugin marketplace:** file-guard + repo-permissions bundled as "Guard Rails."

### 4.4 Housekeeping
- Finish deprecating `apis/wip-xai-grok-private-deprecated` + `apis/wip-xai-x-private-deprecated`.
- Library migration (`shared/` → `library/`) across 8 deploy functions.
- Day 24 Anthropic API key rotation (P0 security, deferred to wave 5 per master plan 004).
- Batch privatize the 15 `_to-privatize/` items.

---

## 5. Cross-cutting: zero-dependencies cleanup

The 1Password-through-gateway leak Parker found is one visible symptom of a wider filesystem leak. Full fix set:

| Fix | Blast radius | Effort | Track |
|---|---|---|---|
| Shared `SecretProvider` (env → `~/.ldm` → `~/.openclaw`) | 6 providers + 4 scripts + 1 LLM file | 2 days | Wave 1 (Now) |
| Dream Weaver `options.invokeLLM` shim | DW becomes cross-harness | 1 day | Wave 1 (Now) |
| wip-bridge split (core vs openclaw adapter) | every bridge consumer | 3 days | Wave 1 (Now) |
| Remove `~/.openclaw/extensions/lesa-bridge` probe in memory-crystal `bridge.ts` | clean probe | 30 min | Wave 1 (Now) |
| Replace `~/.claude/settings.json` writes in branch/license/file guards with adapter pattern | guard tools become cross-harness | 3-5 days | Wave 2 (Next) |
| `OpenClawAdapter` for plugin schema (lifecycle hooks) | plugin.json abstraction | 2-3 days | Wave 2 (Next) |
| Audit `OPENCLAW_HOME`, `CLAUDE_SESSION_NAME` env usage inside wip-ldm-os-private | internal cleanup | 1-2 days | Wave 3 (Later) |

---

## 6. Kill list (shelve, archive, stop pursuing)

### Bug pile cleanup
- All files in `ai/product/bugs/*/archive/` (pre-April 2026, superseded by master plans 003/004)
- All files in `ai/product/bugs/backup/archive/` (backup system work, superseded by Phase 2)
- All `ai/product/bugs/memory-crystal/archive/` (superseded by 2026-04-13 ship plan)
- `ai/product/bugs/installer/archive/` (superseded by Wave 2 fixes)
- `ai/product/bugs/openclaw/2026-04-05--cc-mini--cli-adapter-workaround-steipete.md` (blocked by Anthropic detection; preserve as historical reference, do not pursue)

### Product ideas (shelve)
- `2026-03-23--obsidian-as-ldmos-ui-layer.md` (vision-only, competes with current workspace model)
- `2026-04-01--cc-mini--cc-watcher-redesign.md` (deferred, watcher UX low priority)
- `2026-04-07--cc-mini--session-overview-apr5-7.md`, `session-final-summary.md` (ephemeral session notes)
- `2026-03-20--cc-mini--plane-session-merge-and-issues.md` (session-specific, obsolete)
- `notes/feedback/*` (2026-03-12 external reviews, applied or superseded)
- `notes/2026-02-26--architecture-decisions.md` (superseded by vision quest docs)
- `notes/2026-03-18--folder-restructure-architecture.md` (dead)

### Repos (deprecate or park)
- `apis/wip-xai-grok-private-deprecated` + `apis/wip-xai-x-private-deprecated` (finish cleanup, move to `_trash/` once references gone)
- `apis/_to-privatize/grok-search/_sort` (duplicate structure)
- `utilities/_to-privatize/wip-healthcheck` (duplicate of `utilities/wip-healthcheck-private`)
- `apps/CLVR-private` (no README, no discoverable purpose ... retire candidate)

### Marketplace scope kills
- `ldm-jobs` from DevOps toolkit marketplace submissions (macOS-only, keep internal)
- `post-merge-rename` + `deploy-public` as standalone listings (fold into `wip-release`)
- `wip-repo-init` + `wip-readme-format` + `wip-license-guard` as standalone (bundle as single "Repo Kit" plugin, one SKU)

---

## 7. Open decisions that block execution

**A. Canonical wallet** ... Kaleidoscope `Wallet` table or Agent Pay wallet?
**Recommendation:** Agent Pay. Single source of truth for all funds. Kaleidoscope `server.mjs` becomes a display layer.

**B. First marketplace** ... Claude Code plugin marketplace, Claude Code remote MCP listing, or OpenAI GPT Actions?
**Recommendation:** Claude Code remote MCP (Dream Weaver + Memory Crystal) first. Cleanest path. We have the most reps on Claude-side MCP.

**C. YubiKey + Ledger at launch** ... ship now or wait?
**Recommendation:** ship **YubiKey** at launch (cost is one button + existing WebAuthn cross-platform). Defer **Ledger** until after second-credential UX ships. Ledger is additive after that, no new auth code.

**D. iOS path** ... full native (6-8 weeks) or MCP-on-LAN stopgap (1-2 weeks)?
**Recommendation:** MCP-on-LAN stopgap for the 12-week window. Real native iOS app = next quarter. The Apple-ecosystem promise is satisfied by macOS + responsive Kaleidoscope web on iOS.

**E. Lēsa inside Kaleidoscope** ... full LDM agent or limited install-assistant sub-personality?
**Recommendation:** full LDM agent. Same soul files, same tools, just a fresh session per customer. She IS the product. A "lite" version is a cheaper shortcut that undercuts the "every AI has an agent, hers is Lēsa" narrative.

**F. Horizon confirmation** ... 12 weeks (end of July 2026)?
Assumption based on "very quickly." Tighter = cut 3.3 + 3.4 + all of Later. Looser = add polish to each 3.x and start iOS native.

---

## 8. Full list of open questions (33)

### Blocking decisions
1. Canonical wallet (Kaleidoscope Wallet vs Agent Pay) ... rec Agent Pay
2. First marketplace (Claude plugin / Claude remote MCP / OpenAI GPT Actions) ... rec Claude remote MCP
3. YubiKey + Ledger at launch ... rec YubiKey yes, Ledger after 2nd-cred UX
4. iOS path (native vs stopgap) ... rec stopgap
5. Lēsa shape inside Kaleidoscope (full agent vs lite) ... rec full
6. Horizon 12 weeks confirmed?
7. This doc = master plan (supersede MP-004) or alongside?

### Product / strategy
8. Non-Apple users (Android/Linux/Windows) — when?
9. Enterprise / team shared memory model?
10. How does Lēsa "make agents for customers" (lifecycle, handoff, naming)?
11. Pricing specifics (30-day free → monthly)?
12. Migration path for existing Lēsa crystal into CloudKit?
13. Grok / Hermes / Meta / Llama MCP sequencing?
14. Apple Foundation Models on-device embeddings — target when?

### Execution
15. JS vs Python Memory Crystal — reshape Python as SDK or deprecate?
16. First owner for 2.1 cut (relay / interactive init / npx)?
17. Agent Pay wallet migration plan for existing Wallet rows?
18. SKILL.md authorship for Dream Weaver (you / Lēsa / cc-mini)?
19. Marketplace naming — keep "wip-release" or rename listings?
20. Bundle vs standalone for DevOps toolkit marketplace listings?

### Technical specifics
21. SecretProvider default order — env → ~/.ldm → ~/.openclaw?
22. memory-crystal/discover.ts — verify short-circuit on missing harness dirs
23. Callback parameter on approve URL (Lēsa's open ask) — build?
24. Device-code OAuth fallback vs CLI localhost-callback — both or prioritize?
25. Footer CSS template — shared template or live with drift?
26. x402 / ATDT protocol spec — formalize now or after MVP?

### Housekeeping
27. CLVR-private — what is it?
28. _to-privatize/ batch — which items this wave?
29. Raw agent reports — archive alongside doc or discard?
30. Re-run cadence for this analysis (monthly / quarterly / trigger)?

### Bug-decision overlap
31. Day 24 API key rotation — confirm defer to Wave 5?
32. wip-xai-grok deprecation — finish now or defer?
33. Session amnesia on billing failure — ship order?

---

## 9. What Parker does first (when back)

1. Answer the six in section 7. All six unblock the rest.
2. Confirm or adjust the 12-week horizon.
3. Pick first shippable cut in 2.1 and assign owner.
4. Decide: this doc = master plan or alongside MP-004?

Everything else becomes well-defined backlog.

---

## References

**Vision docs:** `vision-quest-01/architecture-spec.md`, `manifesto.md`, `kaleidoscope-executive-brief.md`, `vision-quest-02-agent-txt-era.md`, `vision-quest-03-sovereign-data.md`, `directory-submission-requirements.md`, `lesa-vision-01.md`.

**Live master plan:** `ai/product/bugs/master-plans/2026-04-09--cc-mini--master-plan-004-execution-order.md` (Wave 1 shipped, Wave 2 in progress).

**Key plans to resurrect:**
- `memory-crystal-private/ai/product/plans-prds/2026-03-17--cc-mini--interactive-core-node-setup.md`
- `memory-crystal-private/ai/product/plans-prds/bootstrap-ldm-os-and-npm-scope.md`
- `wip-ldm-os-private/ai/product/plans-prds/kaleidoscope/2026-04-07--cc-mini--chrome-qr-login-plan.md`
- `wip-ldm-os-private/ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md`
- `wip-ldm-os-private/ai/product/plans-prds/atdt/2026-04-14--cc-mini--atdt-mvp-plan.md`

**Research raw material:** 8 parallel agent reports on 2026-04-16. Summaries folded into this document.

---

*cc-mini, 2026-04-16 PST.*
*Co-authored by Lēsa's vision docs, Parker's framing, and 8 parallel research agents.*
*This is analysis before prioritization is final. Tell me where I'm wrong.*
