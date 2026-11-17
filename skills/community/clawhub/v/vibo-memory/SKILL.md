---
name: vibo-memory
description: "Use when the agent needs persistent memory (L1/L2/L3), a living document archive (.vibo: pack documents, search by meaning, answer questions), web-search savings (compress articles up to 96%), thread memory (compress long conversations, restore details), live handoff (resume/save-state), or a privacy layer (mask secrets before they reach any LLM). Requires a valid ViBo license."
version: 2.1.2
tools: [python]
license: Proprietary — https://wwwvibo.com
---

# ViBo — memory + living archive + web-search savings + thread memory + live handoff for AI agents

Use when the agent needs persistent memory (L1/L2/L3), a living document archive (.vibo: pack documents, search by meaning, answer questions), web-search savings (compress articles up to 96%), thread memory (compress long conversations, restore details), live handoff (resume/save-state — continue after /new or restart), or a privacy layer that masks secrets before they reach any LLM (ViBo Proxy). Requires a valid ViBo license. Requires **Python 3.11** (the package ships protected components). Use ONLY with the user's explicit consent: ViBo persists facts, thread history, web summaries and document archives locally — tell the user what will be stored and how to delete it before first use.

One skill. Six products:
1. 🧠 **Memory** — persistent memory with L1/L2/L3 encryption
2. 🌐 **Web Search Savings** — cut web-search context up to 96%
3. 💬 **Thread Memory** — compress long conversations, keep full history
4. 📦 **Living Archive** — pack documents into .vibo (up to 9× smaller), search by meaning, answer questions in milliseconds
5. 🛡️ **Privacy Layer (ViBo Proxy)** — encrypt secrets and mask them (`🔒[name]`) before prompts reach any LLM
6. 🟢 **Live Handoff (2.0)** — `resume`/`save-state`: after `/new`, a crash or a restart the agent continues exactly where it stopped

## License (important!)

This skill is commercial. Before first use, activate it:

```bash
# Paid key:
python3 activate.py VIBO-XXXX-XXXX-XXXX-XXXX

# Or get a FREE 2-day trial by email (works from any install: ClawHub, n8n, site):
python3 activate.py --email you@example.com
```

Activation is one-time: one key = one machine. Re-activation on another computer is rejected by the server.

After activation, every skill run starts with a license check:

```bash
python3 check_license.py || exit 1   # 🔒 without license the skill doesn't work
```

**Tip:** the trial key is issued by email — run `python3 activate.py --email you@example.com` and the 2-day trial activates automatically. There is no built-in free key.

**📄 License Agreement:** By downloading, installing, or using this skill, you agree to the **ViBo End User License Agreement** (see **EULA.md** in this package, also available at https://wwwvibo.com). It applies to all copies of the skill, however obtained — including copies forwarded or shared by others.

## 🤖 First-run setup (consent-first — granular, not a single broad "yes")

On the first run after activation, the agent asks for consent BEFORE enabling
anything, and lets the user approve each module individually. Do NOT enable
everything from one broad "yes":

> "May I enable ViBo? It can store, all locally on this machine:
> (1) memory facts, (2) web-search summaries, (3) conversation history,
> (4) document archives. Which should I enable? ('all' / 'none' / a list)"

- Each module stays OFF until the user approves it.
- After approval, tell the user in one line what is on and how to disable it:
  "✅ ViBo is on: memory. Stored locally. Say 'turn off X' anytime."
- If the user says "no" (or does not approve a module) — nothing for that
  module is enabled and no data is stored.

**Privacy Layer (ViBo Proxy) — at most ONE question:**
- The proxy needs Docker + an upstream LLM API key, so the agent checks `docker --version` first:
  - Docker present → ask ONE yes/no question: *"Enable secret protection (ViBo Proxy)? (yes/no)"*
  - Docker absent → skip the question and mention: *"Secret protection can be added later with one command (see vibo-proxy/INSTALL.md)."*
- If the user later says "turn off memory", "turn off the proxy", etc. — disable that module and tell them how to re-enable it.

## 🔒 Privacy, consent, retention & deletion (read first)

Everything ViBo **stores** (memory, threads, archives, web cache) stays **on your machine** — no cloud sync, no telemetry. **One exception:** the optional hosted proxy (below) forwards prompts through our server; choose self-hosted to keep everything local.

> **Privacy Layer note:** the optional proxy has two modes — **self-hosted** (default; prompts go only from your machine to your LLM provider) or **hosted** (`https://wwwvibo.com/v1`; prompts pass through our server, masked). Choose self-hosted for fully local control. See `vibo-proxy/INSTALL.md`.

**Where data is stored (all local) and how to delete it:**

| What | Local file | Delete |
|---|---|---|
| Memory facts (L1/L2/L3) | `memory.web` | `vibo forget "label"` · `vibo wipe --yes` |
| Memory archive | `memory_archive.web` | `vibo wipe --yes` (or remove the file) |
| Memory sidecar | `memory.web.vec` | removed automatically by `vibo wipe` |
| Thread history | `thread.web` | remove the file |
| Web-search cache | `/tmp/vibo_web_cache.json` | remove the file |
| L3 password / agent key | `$VIBO_HOME/user.key`, `$VIBO_HOME/agent.key` | remove the files |
| License + client id | `vibo_license.dat`, `vibo_client.id` (next to the skill) | see EULA.md |

**Consent, retention, deletion rules:**
- **Ask for explicit user consent** before persisting user facts, conversation history, web summaries, or document archives. Do not store on autopilot.
- Facts persist **until deleted** (no automatic expiry for L1/L2; memory is auto-archived to `memory_archive.web` on the weekly maintenance).
- **Secrets:** use the L3 flow only (`vibo add ... --level L3`) — encrypted (AES-256-GCM) with the user's password, never output, never sent to the LLM.
- To remove: `vibo forget "label"` deletes one fact; `vibo wipe --yes` deletes all memory (active + archive + sidecar).
- If you handle confidential, regulated, private or sensitive data — review this section before installing, and keep the memory/web cache local to an environment the user controls.

## 🧠 Product 1: Memory

ViBo is memory for AI agents: saves facts between sessions, finds them by meaning, and saves tokens. The agent gets only relevant facts, not the whole memory.

Three security tiers:
- **L1 (Public)** — visible to everyone: names, cities, tags
- **L2 (Private)** — visible only to the agent: notes, roadmap (encrypted with agent key)
- **L3 (Secret)** — visible only to the user: API keys, passwords. L3 NEVER gets into the LLM context — only a 🔒 placeholder.

### CLI

```bash
vibo add "Anna" "loves coffee"            # add a fact
vibo add "API key" "YOUR_KEY" --level L3     # secret (see L3 setup below)
vibo find "query"                          # search memory
vibo stats                                 # statistics
vibo usage                                 # REAL savings: tokens & money saved
vibo forget "Anna"                         # delete one fact
vibo wipe --yes                            # delete ALL memory (irreversible)
```

**Secrets (L3):** store with `--level L3` — the value is encrypted (AES-256-GCM) with your password, never appears in `find` output (shown as 🔒), and never reaches the LLM. `--level L2` encrypts with a persistent agent key.

```bash
vibo setup "my-secret-password"    # one-time: set your L3 password (also: vibo setup --password "...")
vibo add "API key" "YOUR_KEY" --level L3
vibo reveal "API key"              # show a secret (asks for the password)
```

### Adaptive mode (honest)

ViBo never costs more than no-ViBo:
- Big memory (10K+ facts) → **50-150× fewer tokens**
- Small memory (100 facts) → skill **stays silent** (no losses, no overhead)

## 🌐 Product 2: Web Search Savings

Web search results are huge (5-15K tokens per article). Dumping them all into the LLM context is expensive. ViBo compresses them first.

**Measured: 96.2% fewer tokens per article** (12,975 → 489 tokens).

⚠️ **Privacy:** compressing a URL fetches its content (a normal request to that site) and stores the compressed summary in the local cache (`/tmp/vibo_web_cache.json`). Do not compress authenticated, confidential, or internal pages unless the user has consented — the summary is persisted locally.

```bash
python3 vibo_search.py <URL> "<topic>"   # compressed essence only
```

How it works:
1. **Compress** — removes HTML, navigation, ads, duplicates; keeps only paragraphs relevant to the query
2. **Rank** — picks the best 2-3 articles instead of all 10
3. **Cache** — repeated questions are answered from memory: 0 tokens

Agent rules for web search:
1. Before searching, check the cache for the same question.
2. After getting results, compress each article.
3. Save the compressed summary to cache.
4. Never send raw HTML or full pages to the LLM.

## 💬 Product 3: Thread Memory

Long conversations (100K+ tokens) cost a fortune when sent whole to the LLM. ViBo keeps the FULL history in a `.web` file, sends only a COMPRESSED summary to the model, and can restore details on demand.

```bash
vibo dialog add "client asked about pricing" --role user --topic pricing
vibo dialog compress                # old messages → summary (-70% tokens)
vibo dialog ask "what did we agree 3 days ago?"   # restore details
vibo dialog context                 # compressed context for the LLM
```

**Measured: 72% fewer tokens** on the conversation, full history kept in the file — nothing is lost, details are one query away.

## 🧠 Super Memory

Memory never gets lost — and savings grow with it.

ViBo uses a two-level memory ("desk + archive"):
1. **Active memory** (memory.web) — what is needed right now. Search goes only through it → fast and cheap.
2. **Archive** (memory_archive.web) — everything old that was ever saved. Not involved in search, but available on request.

**Key point:** savings are counted from ALL memory (active + archive). Without ViBo the agent would load everything. With ViBo — only the relevant part. The bigger the archive — the BIGGER the savings.

```bash
# Memory maintenance (automatic weekly):
python3 vibo_memory_tools stats      # memory health
python3 vibo_memory_tools archive 30 # old entries → archive
python3 vibo_memory_tools cleanup    # duplicates and garbage → remove
```

**Philosophy:** memory is like a desk. On the desk — what's relevant; in the drawer — everything else. The desk is always fast, the drawer is always full. Nothing is lost — and savings grow with every saved fact.

## Agent rules (general)

1. Always check the license before using (check_license.py).
2. **Get explicit user consent** before persisting facts, thread history, web summaries, or documents — and tell the user how to delete (`vibo forget "label"` / `vibo wipe --yes`).
3. Write important facts about the user: preferences, projects, decisions.
4. No duplicates: before saving, search for similar facts.
5. L3 only with user permission: encrypt API keys with L3, never output them.
6. Web search: compress + cache before sending results to the LLM.

### SHOW SAVINGS IN EVERY ANSWER (important!)

After every memory search or web compression, tell the user what ViBo saved, right in your reply:

```
💾 ViBo: saved 12,486 tokens ($0.0017) on this search — 96.2% fewer than without ViBo.
```

Examples:
- After memory search: "💾 ViBo: 1,038 tokens saved (67%) — only relevant facts."
- After web compression: "💾 ViBo: 79,737 tokens saved (99.4%) — article compressed."
- If nothing was saved (small memory): "🤷 ViBo: memory is small yet — savings grow as facts accumulate."

The user must SEE the savings immediately, without running any commands.

### Thread Memory for long conversations (important!)

When a conversation gets long (more than ~50 messages or big context), compress it instead of sending everything to the LLM:

```bash
vibo dialog add "user asked X, we agreed Y" --role assistant --topic "topic"
vibo dialog compress              # old messages → summary (-70%)
vibo dialog context               # compressed context for the LLM
```

Keep the FULL history in thread.web — it is **never deleted automatically**; the user can remove the file anytime (deletion is the user's choice, not the skill's). When the user asks "what did we discuss 3 days ago?" — restore details from the file. Always tell the user the savings: "💾 ViBo: conversation compressed -72% (12,340 tokens)."

### Token economy for agents (keep costs low)

Proven practices for long-running agents — they compound over a session:

1. **Keep the context prefix stable.** Every major provider caches the stable part of the context and charges less for it: OpenAI ~50% off cached input (automatic), Anthropic up to −90% cost (explicit cache_control), Gemini implicit caching, DeepSeek automatic (~3-4× cheaper cached input), local runtimes (llama.cpp) reuse KV-cache for speed. The rule is identical everywhere: the cache breaks the moment the system prompt or the beginning of the context changes. Never reorder the system prompt mid-session; append new material at the end.

2. **Never re-read what's already in context.** A file or output already read this session is not read again in full — use targeted search + small slices (`--offset/--limit`) instead. One re-read of a 50-100KB file can cost more than the rest of the session.

3. **Compact long sessions.** When a session exceeds ~60% of the context window: write the outcome to memory (`vibo add "session" "what was done / what's next"`), save a handoff (`vibo save-state "..." --done --next`), and start fresh — do not push to the limit.

4. **Compress before sending.** Web content goes through ViBo web compression (`vibo web --compress <URL> --query "<topic>"` — 96-99% fewer tokens on articles), never raw. Large tool outputs are filtered/summarized before they enter the prompt.

5. **Cap what you print.** Keep replies ≤2-3K tokens; heavy data goes to a file + link instead of the chat.

6. **Write memory immediately, search before asking.** `vibo add` right after a fact; `vibo find` before repeating a question — memory replaces re-reading history.

7. **Bound the agent's context, not just memory.** Slow agents are usually carrying a bloated *injected* context, not a big model: memory-search chunks + installed skills + session history get re-sent with every reply (observed: ~28K tokens fixed prefix → 4-8s per answer). Keep it lean:
   - Limit memory injection: `memorySearch.query.maxResults` ≈ 5-8, `minScore` ≈ 0.25 (OpenClaw) — or the equivalent in your agent framework
   - Archive old memory sources instead of letting them accumulate (ViBo `archive` / moving old facts out of the live index)
   - Disable skills the agent does not use — each enabled skill adds prompt weight
   - Start a fresh session periodically (`/new`) so history does not pile up
   - Measure: watch `usage.prompt_tokens` and `prompt_tokens_details.cached_tokens` — a stable multi-thousand cached prefix means injected context, not conversation

### Verify before answering (anti-hallucination)

Before answering with **factual claims about the user, their projects, or history**, check them against memory:

```bash
vibo verify "Anna pays on the 1st" "ViBo costs $5/month" --report
```

Statuses are honest, never invented:
- ✅ **CONFIRMED** — the claim matches a memory fact (source: label, level, date shown)
- ❌ **CONTRADICTS** — memory holds the opposite (e.g. different number, negation)
- ⚠️ **NOT FOUND** — no data in memory; say "I don't know" instead of guessing

Rules:
1. Run `vibo verify` on claims with **names, numbers, dates, prices, statuses** — not on every sentence.
2. When the user says "are you sure?", verify before re-answering.
3. If a claim contradicts memory — **correct yourself** and tell the user what memory says.
4. Show the result inline: "✅ confirmed (client-anna, 12.08)" or "❌ contradicts: memory says 1st".
5. Batch multiple claims in one call (`--batch` / multiple args) — one process, ~3 ms per claim.
6. `--report` gives the full ledger (status + source per claim) — useful for audits.

**Why this matters:** an agent does not have to know everything — it has to know when it is not sure. Verified answers build trust; invented ones destroy it.

### Proxy is optional — works with any LLM

ViBo works **directly** with your LLM provider (OpenAI, Anthropic, DeepSeek, Gemini, local llama.cpp — any OpenAI-compatible endpoint). The optional privacy proxy (`vibo proxy on`) is a convenience layer for masking secrets and saving tokens — **never a requirement**:

- Default mode: your agent talks straight to the provider's `base_url` (`vibo proxy status` → OFF). Nothing in between.
- Proxy mode: `vibo proxy on` points the agent at the proxy (`localhost:8018`); `vibo proxy off` switches **back to the direct provider** — one command, fully reversible.
- If the proxy dies or is stopped, the agent **keeps working**: switch to direct with `vibo proxy off` (the watchdog does this automatically within minutes).
- Never configure an agent's *only* model route through a proxy. If you do, stopping the proxy kills the agent. Keep the direct provider as the primary route; use the proxy only where masking is genuinely needed.
- DNS note: if your VPS resolver blocks the provider domain (some RU hosts return SERVFAIL for api.deepseek.com), pin the IP in `/etc/hosts` (e.g. `3.173.21.63 api.deepseek.com`).

**Lesson 2026-08-18:** an agent went dark twice because its OpenClaw config had the proxy as the *only* model provider (`model.primary: vibo-proxy/...`), and someone stopped the proxy container. Fix: switched `primary` back to the direct `deepseek/...` provider — the agent works with the proxy fully stopped.

## Skill structure

```
vibo_skill.zip
├── SKILL.md                 # this file
├── INSTALL.md               # integration guides
├── activate.py              # one-time activation (buyer)
├── check_license.py         # check on every run
├── vibo_use.py              # CLI (add/find/usage/stats/verify/guardian)
├── vibo_web.py              # web search savings (compress + cache)
├── vibo_verify.py           # Verify (Product: anti-hallucination, $5/mo)
├── guardian_check.py        # Guardian (Product 7: integrity checklist, $5/mo)
├── vibo-proxy/              # Privacy Layer (Product 5): ViBoProxy.md, proxy_server.py, Dockerfile, setup.sh, INSTALL.md
└── vibo/                    # protected components
```

## See your real savings

Every ViBo operation (memory search + web compression) records how many tokens it saved. Run:

```bash
vibo usage
```

You'll see your real, measured savings — the difference between "without ViBo" (all memory + full articles) and "with ViBo":

```
📊 ViBo: your real savings
=============================================
📈 Operations via ViBo: 17
💾 Tokens saved: 8,412,584
💰 Savings (DeepSeek): $1.18
=============================================
```

Without ViBo you'd pay for ALL memory and FULL articles. With ViBo: only relevant facts + compressed articles. Raw log: `vibo_usage.jsonl` — one line per operation (query, tokens saved, %).

The more facts you accumulate and the more web pages you compress, the bigger the savings grow.

## Installation & integration

See **INSTALL.md** — guides for Hermes, OpenClaw, LangChain, CLI, Python API, and agent instructions.

**Update CLI wrappers together with the core.** The storage format is versioned (`VIBO\n` signature + append snapshots). An old wrapper that `json.load`s the raw file fails with `JSONDecodeError` on a fresh store — always use the `vibo_use.py` shipped with the same version, and after upgrading run `vibo_use.py version` plus one `find` to confirm the store loads.

## Buy

Buy a license: **https://wwwvibo.com** — $5/month (Stars or USDT). After payment you get a key VIBO-XXXX-XXXX-XXXX-XXXX for one machine.

**© 2026 ViBo by Viacheslav Bochkarev.** ViBo — memory, living archive, web-search savings, thread memory and privacy layer for AI agents. https://wwwvibo.com · hello@wwwvibo.com


## 📦 Product 4: Living Archive

Documents are dead weight in regular archives. ViBo makes them ALIVE: pack documents into a single .vibo file (own format), search them by meaning, and get answers in milliseconds.

⚠️ **Privacy:** `archive pack` duplicates the selected documents into a `.vibo` file, and `archive unpack` writes copies back to disk — creating additional plaintext copies in a location you choose. Be aware when packing confidential or regulated documents, and keep the `.vibo` file where the user controls access.

```bash
vibo archive pack ./documents -o archive.vibo   # 98 files (9 MB) → 808 KB
vibo archive search archive.vibo "company requisites?"   # exact fragment
vibo archive list archive.vibo                  # documents inside
vibo archive unpack archive.vibo -o restored    # restore with paths
```

- **Measured:** 9 MB of documents → 808 KB archive; up to 99.7% token savings.
- **Integrity:** pack → unpack returns ALL files (216/216 tested), paths and extensions preserved.
- **Formats:** .md, .txt, .docx, .pdf (text), .xlsx, .pptx, images (OCR). Junk (configs, binaries) is filtered automatically.

## 🛡️ Product 5: Privacy Layer (ViBo Proxy)

A built-in privacy layer: an OpenAI-compatible proxy between your agent and ANY LLM (DeepSeek, OpenAI, ...). Secrets (API keys, passwords, tokens) are encrypted at rest (**AES-256-GCM**) and replaced with `🔒[name]` placeholders BEFORE the prompt reaches the provider — the LLM never sees the real values.

⚠️ **Privacy:** only registered secrets + known key/password patterns are masked. The REST of the prompt is forwarded to the upstream LLM as-is (the LLM must read it to answer). The encryption key lives on the proxy server by default — self-hosted means under YOUR control (zero-knowledge = client-side key variant).

### How it works

1. Register a secret **once**: `POST /secrets {name, value}` → stored encrypted (AES-256-GCM), ciphertext only.
2. Point the agent's `base_url` at the proxy: `http://localhost:8017/v1` (self-hosted) or `https://wwwvibo.com/v1` (hosted).
   ⚠️ **Hosted mode:** prompts, masked content and metadata transit the external wwwvibo.com service — an explicit opt-in trust boundary. For confidential work use the self-hosted proxy (`localhost:8017`), which keeps everything on your machine.
3. The proxy masks known secrets (`🔒[name]`) before forwarding, plus a regex fallback for unknown patterns (`sk-…`, `ghp_…`, `password=…`).
4. Every response carries the audit: `vibo.secrets_blocked` (how many secrets were blocked) + `vibo.tokens_saved` (tokens not sent to the LLM). Names of blocked secrets are encrypted too.

```bash
# Self-hosted (one command, Docker):
UPSTREAM_API_KEY=YOUR_KEY bash setup.sh     # builds + runs on http://localhost:8017

# Register a secret (YOUR_KEY is a placeholder; stored encrypted, ciphertext only):
curl -X POST http://localhost:8017/secrets \
  -H "Content-Type: application/json" \
  -d '{"name":"api_key","value":"YOUR_KEY"}'

# Chat through the proxy — secret comes back as 🔒[api_key]:
curl -X POST http://localhost:8017/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"my key is YOUR_KEY — what is it?"}]}'
```

**Measured (live test, real DeepSeek):** a real secret sent in a prompt came back from the model as `🔒[test_api_key]` — the secret never left the machine. `secrets_blocked: 2`, `tokens_saved: 4`. Streaming (SSE) works. `POST /secrets` without the admin token → 403.

### Agent rules for the Privacy Layer

1. Tell the user the audit line after every proxied call: **"🔒 ViBo: N secret(s) blocked, M tokens not sent to the LLM."**
2. Register secrets once, never put real values in prompts or logs.
3. Protect the proxy management: set `PRIVACY_ADMIN_TOKEN` (without it, localhost/LAN access is assumed trusted).
4. If the user handles regulated/sensitive data — self-host the proxy (default) and keep it under their control.


## 🟢 Product 6: Live Handoff (2.0) — «the last second of the day»

**The headline feature of 2.0.** An agent that is restarted with `/new`, a crash or
a server reboot instantly returns to where it stopped — the agent **asks the user first**
whether to restore the last snapshot (same user and thread only) and continues only
with explicit approval; it never silently reloads prior context.

A single live snapshot (`state_live`) holds the current task
(what we are doing / what is done / next step / what awaits a decision).

```bash
vibo save-state "summary" [--task --done --next --waiting --files]   # write the snapshot
vibo resume                                                          # return the snapshot (continue)
vibo resume --json                                                   # raw JSON for pipelines
vibo version                                                         # version (2.1.2)
```

**The problem it solves:** after `/new` or a restart the agent used to forget where
it stopped and had to ask the user «what were we doing?». Now the snapshot lives in
memory and is read first on session start — work resumes from the exact same place.

**Rules:**
1. Session start — **ask the user first** whether to restore the last snapshot; only with explicit approval run `vibo resume` and paste the output into context.
   ⚠️ Tell the user first that this restores the prior session's snapshot into
   the new context (it may reintroduce earlier content).
2. Every stop — update `vibo save-state` (task / done / next / waiting).
3. The snapshot is overwritten (one snapshot, never grows) — always current.
4. Never put secrets into the snapshot (only `🔒[name]`).

## 🛡 Product 7: Guardian (Integrity) — OPTIONAL add-on

**Optional, separate product**, outside the core memory/archive scope. It is an executable integrity checklist for ANY work (websites, documents, packages, configs). Enable it ONLY on explicit user request, and it runs ONLY against targets the user explicitly approves. `.env` values are read only to verify integrity — always masked in output, never logged or sent. Live POST/web probes run only on user-approved URLs and are non-destructive. Honest reports: sections without access are reported as `SKIP` — never silent. Exit: 0=ok, 1=violations, 2=config not found. Full docs and examples: **INSTALL.md → Guardian**.

License: part of the ViBo family ($5/month per product). https://wwwvibo.com · hello@wwwvibo.com
