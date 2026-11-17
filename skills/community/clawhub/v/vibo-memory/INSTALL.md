# 📦 ViBo — Installation & Integration Guide

ViBo works with **any AI agent** that can run Python: Hermes, OpenClaw, LangChain, CrewAI, or your own agent.

> **⚠️ Python 3.11 required** — the package ships compiled modules for CPython 3.11.
> On 3.10/3.12+ the import fails with an ImportError; use Python 3.11.

**One skill, six products:**
1. **🧠 Memory** — persistent memory with L1/L2/L3 encryption
2. **🌐 Web Search Savings** — compress articles up to 96%, cache repeats ($0)
3. **💬 Thread Memory** — compress long conversations, keep full history
4. **📦 Living Archive** — pack documents into .vibo, search by meaning
5. **🛡️ Privacy Layer (ViBo Proxy)** — encrypt secrets (AES-256-GCM) and mask them (`🔒[name]`) before prompts reach any LLM — see `vibo-proxy/INSTALL.md`
6. **🟢 Live Handoff (2.0)** — `resume`/`save-state`: after `/new` or a restart the agent continues exactly where it stopped

Everything is driven through the CLI (`vibo_use.py`), so any agent or script that can run shell commands can use ViBo. No Python API needed.

---

## 0. First run — consent-first (granular, no auto-enable)

On first run after activation, the agent asks for consent BEFORE enabling anything and lets the user approve each module individually (memory, web savings, thread memory, archive — **each defaults OFF**). The **Privacy Layer (proxy)** is optional: the agent checks `docker --version` and asks one yes/no question if Docker is present (otherwise it mentions it can be added later — see `vibo-proxy/INSTALL.md`). Nothing is enabled and no data is stored without explicit approval. Full instructions for the agent: **SKILL.md → "First-run setup"**.

---

## 1. CLI (simplest — 2 min)

```bash
# License check (trial: automatic)
python3 check_license.py

# Set your L3 password (ONE TIME — required to store secrets):
python3 vibo_use.py setup "your-secret-password"
#   → saved to ~/.vibo/user.key (chmod 600)
#   → L3 facts (API keys, passwords) are AES-256-GCM-encrypted with THIS password
#   → without it, `vibo add ... --level L3` refuses to run
#   → the password is yours only — never share it, never write it in plaintext

# Memory (file is memory.web by default; override with VIBO_MEM_FILE env)
python3 vibo_use.py add "Anna" "loves coffee without sugar"     # add a fact (L2)
python3 vibo_use.py add "API key" "sk-..." --level L3           # add a SECRET → 🔒 (AES-256-GCM)
python3 vibo_use.py find "what does Anna like?"                 # search by meaning (L3 shows 🔒)
python3 vibo_use.py reveal "API key"                            # show a secret (needs the password)
python3 vibo_use.py forget "Anna"                               # delete ONE fact (by label)
python3 vibo_use.py wipe --yes                                  # delete ALL memory (irreversible)
python3 vibo_use.py stats                                       # how many facts are stored
python3 vibo_use.py usage                                       # see your real savings

# Guardian (Product 7, OPTIONAL) — integrity check of ANY work (3 checks/day on trial; full = $5/mo)
# Optional product outside the core memory scope: runs ONLY on targets the user explicitly approves.
python3 vibo_use.py guardian --url https://my-site.com --check "payment,contacts"
python3 vibo_use.py guardian --file contract.md --check "subject,price"
python3 vibo_use.py guardian --config guardian_config.json      # full checklist
```

---

## 2. Agent instructions (5 min)

Add to your agent's system prompt (see SKILL.md):

> **Memory:** Before answering, search ViBo memory with `vibo find "<topic>"`.
> Save important facts with `vibo add <label> <content>`. Never leak L3
> secrets — use 🔒.
>
> **Web search:** Before searching, check the ViBo cache. After getting
> results, compress each article with `vibo web --compress URL --query "..."`
> before putting it in the context. Save the compressed summary to cache.
>
> **Show savings (IMPORTANT):** after every memory search or web
> compression, tell the user what ViBo saved — right in your reply:
> "💾 ViBo: saved 79,737 tokens (99.4%) — article compressed."
> The user must SEE the savings immediately, no commands needed.

---

## 🌐 Web Search Savings (Product 2)

ViBo compresses web-search results before they reach the LLM:
**measured 96.2% fewer tokens** (12,975 → 489 per article).

```bash
# Compress a URL down to its essence (relevant to your query)
python3 vibo_use.py web --compress https://example.com/article --query "topic"

# Or compress a local file
python3 vibo_use.py web --compress ./article.html --query "topic"

# Show the cache (repeated questions = 0 tokens)
python3 vibo_use.py web --cache
```

### Why it works

| Without ViBo | With ViBo |
|---|---|
| 10 articles × 12,975 tokens = 129,750 tokens | 10 × 489 = 4,890 tokens |
| $0.018/query (DeepSeek) | $0.0007/query |
| repeated questions: paid again | repeated: **$0** (cache) |

---

## 🔄 Migration from old memory (important!)

If you used an older ViBo version with memory in a plain JSON file
(no `VIBO` header), the skill **migrates automatically with a backup**:

1. The first read of an old file creates a copy: `<name>.web.bak-<date>`
   (or `<name>.json.bak-<date>`) right next to the original.
2. Your data is read into the new format. **The original is never deleted.**
3. The next save writes the new `VIBO` format.

**You can always roll back:** copy the `.bak-*` file back over the
current one.

> Example:
> ```
> memory.json          ← legacy file (untouched)
> memory.json.bak-20260813_040005   ← auto-backup (created on read)
> memory.web           ← new format (created on save)
> ```

In the Telegram bot, use `/backup` (snapshot) and `/restore`
(rollback) — owner only.

---

## 📊 How to see YOUR savings (important!)

Every ViBo operation (memory search + web compression) records how many
tokens it saved you. To see the total difference — **without ViBo vs with ViBo**:

### 1. See the summary

```bash
python3 vibo_use.py usage
```

```
📊 ViBo: your real savings
=============================================
📈 Operations via ViBo: 17
💾 Tokens saved: 8,412,584
💰 Savings (DeepSeek): $1.18
=============================================
Without ViBo you'd pay for ALL memory and FULL articles.
With ViBo: only relevant facts + compressed articles.
```

### 2. See the raw log

```bash
cat vibo_usage.jsonl    # one line per operation: tokens saved, %
```

### 3. What counts as savings

| Operation | Without ViBo | With ViBo |
|---|---|---|
| Memory search | ALL memory in the prompt | only relevant facts |
| Web compression | FULL article (50K+ tokens) | essence (300-500 tokens) |

### 4. Daily savings report (optional)

Add to your agent's instructions:

> Once a day, run `vibo usage` and report the savings to the user.
> If savings are zero, explain: memory is still small — savings grow
> as facts accumulate.

---

## 💬 Thread Memory (Product 3)

Long conversations cost a fortune in tokens. ViBo keeps the FULL history
in a `.web` file and sends only a compressed summary to the LLM.

```bash
# Write a message to history
python3 vibo_use.py dialog add "client agreed to new pricing" --role assistant --topic pricing --file thread.web

# Compress old messages (older than 1 day) → summary
python3 vibo_use.py dialog compress --file thread.web
# → 📦 Compressed 8 messages: 188 → 52 tokens (-72%)

# Context for LLM: summary + recent messages
python3 vibo_use.py dialog context --file thread.web

# Find details: "what did we discuss 3 days ago?"
python3 vibo_use.py dialog ask "what was 3 days ago" --file thread.web
```

See **THREAD_MEMORY_GUIDE.md** for the FULL vs SUMMARY modes.

### When to use (agent rule)

> When the conversation gets long (>~50 messages) — compress it:
> 1. Record key points: `vibo dialog add "..." --topic topic`
> 2. Compress old ones: `vibo dialog compress`
> 3. Only compressed context goes to the LLM: `vibo dialog context`
> 4. Full history stays in thread.web — nothing is lost
> 5. "What was 3 days ago?" → `vibo dialog ask "..."`

---

## 📦 Living Archive (Product 4)

Pack documents into a single `.vibo` file, search them by meaning, get
answers in milliseconds.

```bash
python3 vibo_use.py archive pack ./documents -o archive.vibo   # pack a folder
python3 vibo_use.py archive search archive.vibo "company requisites?"
python3 vibo_use.py archive list archive.vibo                  # documents inside
python3 vibo_use.py archive info archive.vibo                  # statistics
python3 vibo_use.py archive unpack archive.vibo -o restored    # restore files
```

---


## 🟢 Live Handoff (Product 6, v2.0)

After `/new`, a crash or a restart, the agent **asks the user first** whether to restore the last snapshot (same user and thread only) and continues only with explicit approval — it never silently reloads prior context into a new session.

```bash
python3 vibo_use.py save-state "summary" [--task --done --next --waiting --files]
python3 vibo_use.py resume              # snapshot: continue where you stopped
python3 vibo_use.py resume --json       # raw JSON for pipelines
python3 vibo_use.py version             # version (2.0.0)
```

**Agent rules:**
- Start of session — **ask the user first** whether to restore the last snapshot; only with explicit approval run `vibo resume` and paste the output into context.
- Every stop — update `vibo save-state`.
- The snapshot is one overwritable snapshot (never grows) — always current.
- Never put secrets into the snapshot (only `🔒[name]`).

## Files

```
vibo_skill.zip
├── SKILL.md                 # agent instructions (what to do)
├── INSTALL.md               # this file
├── THREAD_MEMORY_GUIDE.md   # FULL vs SUMMARY thread modes
├── activate.py              # one-time activation (buyer)
├── check_license.py         # license check on every run
├── vibo_use.py              # CLI (add/find/stats/usage/dialog/archive/web)
├── vibo_web.py              # web search savings (compress + cache)
├── EULA.md                  # end-user license agreement
└── vibo/                    # protected components
```
