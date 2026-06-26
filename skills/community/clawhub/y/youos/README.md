<p align="center">
  <img src="assets/youos-mark.png" width="96" alt="YouOS logo — an envelope whose flap forms a Y">
</p>

<h1 align="center">YouOS</h1>

> **Your email. Your model. Your style.**

> 🧪 **Public beta — [latest release](https://github.com/DrBaher/youos/releases/latest)**

YouOS is a local-first AI email copilot that learns from your sent Gmail history and drafts replies that sound like *you* — not a generic AI. It runs entirely on your Mac. No cloud. No subscriptions. Your data never leaves your machine. **During setup it becomes _your_ OS** — YouOS → BaherOS.

```
Gmail (sent mail)          Your feedback
       │                        │
       ▼                        ▼
  Ingestion pipeline      Review Queue
  (gog CLI + SQLite)      (10 emails/batch)
       │                        │
       ▼                        ▼
  Reply Pairs DB  ──────► LoRA Fine-tuning
  (FTS5 + BM25)           (Qwen, nightly)
       │                        │
       ▼                        ▼
  Draft Generation ◄──── Autoresearch
  (local Qwen MLX)        (80 iterations/night)
       │
       ▼
  Draft Reply ✅
```

**Privacy:** Everything stays local. Your corpus, model, and drafts never leave your Mac.

![YouOS demo](screenshots/demo.gif)

> 🌐 [youos.drbaher.com](https://youos.drbaher.com/)

## What it does

- Ingests your sent Gmail history, Google Docs, WhatsApp exports — including organic pairs you sent without YouOS
- Learns your writing style — richer persona: bullet point rate, directness score, sentence length, paragraph style; EWMA-weighted toward recent emails
- Persona re-analysis is incremental (recent 90 days × 3 weight), with full weekly refresh; confidence intervals (p25/p75) shown in prompts
- Per-sender-type personas: different voice, length, greeting, and closing for internal, external client, and personal contacts
- Sender-type style anchors: explicit prompt slot (`[STYLE ANCHOR — internal|client|personal]`) to stabilize first-draft tone by audience
- Per-account corpus isolation — drafts for work emails draw from work history; personal from personal
- Greets people by first name, closes in your style — greeting and closing injected from persona config per contact type
- Classifies multi-intent (meeting + urgent, etc.), boosts matching exemplars; per-intent reply length calibrated from corpus
- Drafts grounded in score-ranked few-shot exemplars (confidence-annotated, thread-deduplicated); exemplar reply text preserved (600 chars), inbound trimmed (400)
- Exemplar cache by intent+sender-type (TTL + feedback-triggered invalidation) improves consistency and reduces repeated ranking churn
- Prompt token budget enforced — exemplars auto-trimmed if prompt exceeds 2000 tokens
- Confidence thresholds are relative (mean±σ of retrieval scores), not hardcoded
- Subject line + topic-aware retrieval; FTS queries expanded with email vocabulary synonyms
- Same-thread history gets a 2x retrieval boost
- Handles full email threads — paste the whole thread, YouOS focuses on the latest message
- Optional reply instructions — steer a specific draft with explicit guidance even when replying to inbound emails
- Warns you when confidence is low; explain any draft inline via "How was this generated?"
- **Drafts in your voice by default** — your fine-tuned local model is the default drafter (Draft Reply tab + Review Queue), served *warm* (loaded once) so it's fast and fully on-device; Claude is only the cold-start/fallback
- **No silent failures** — see which model actually wrote each draft (your LoRA / base / cloud) in stats, `youos doctor`, and a per-draft badge; a readiness gate holds you back until your model is **trained _and_ benchmarked**
- Subject line generated via smart content analysis — skips greeting/filler lines, extracts the actual topic
- Improves from your feedback via LoRA fine-tuning — quality-filtered, deduplicated, curriculum-ordered, DPO preference pairs supported
- Training export deduplicated by inbound similarity (≥0.95 → keep higher-rated pair)
- Auto-scales training hyperparameters; nightly pipeline skips steps when data is insufficient
- Golden eval runs nightly after fine-tuning — composite score tracked in pipeline log
- Autoresearch benchmarks rotate weekly (seeded re-sample) to prevent overfitting to fixed test cases
- Self-optimizes nightly via autoresearch — configurable composite weights, sender-type boosts, intent signals
- Style drift detection: Stats dashboard flags when your writing patterns shift significantly
- Feedback loop closes: high-rating, low-edit pairs surface higher in future retrievals
- Streak tracking — consecutive daily Review Queue sessions tracked; streak shown in queue UI
- Corpus scan button in Stats — bulk-extracts structured facts from your top reply pairs in one click
- Language-filtered retrieval — retrieval matches language of the inbound email; no cross-language bleed
- Sender profiles track reply-time patterns and topics; notes trigger immediate profile rebuild
- Embedding cache for fast repeated retrieval; corpus health at a glance: `youos corpus`
- Run a golden benchmark anytime (10 curated cases): `youos eval --golden`
- Runs entirely locally on Apple Silicon

## Does it actually sound like you? (measured)

The whole bet behind YouOS is that a small model fine-tuned on *your* mail beats a frontier model that isn't — at sounding like you. So we measured it. `youos compare-models` drafts your held-out messages under each backend and scores every draft against the reply you actually sent — **voice-match**: a blend of semantic similarity, stylometry, phrasing overlap, and length fit.

On the maintainer's ~11,700-email corpus (15 held-out replies):

| | YouOS — local Qwen + your LoRA | Claude — frontier cloud |
|---|---|---|
| **Sounds like you** (voice-match) | **0.80** | 0.70 |
| Reuses your phrasing (lexical overlap) | **0.40** | 0.13 |
| Matches your length | **37 words** | 81 words |
| Speed per draft | **~10s** | ~40s |
| Your email leaves your Mac | **never** | every draft |

The fine-tuning is what wins: the *base* Qwen with no adapter scores just **0.43** — training on your sent mail takes it to **0.80**, past Claude, while staying private and ~4× faster. Reproduce it on your own corpus with `youos compare-models --limit 30 --semantic`.

*(Numbers are from one corpus and will differ for you — the point is the method and the direction, both reproducible.)*

## Requirements

- Apple Silicon Mac (M1/M2/M3/M4) — the local model runs on **MLX**, which `./scripts/install.sh` installs for you (it's the `youos[mlx]` extra; not bundled with macOS)
- 8GB+ RAM (16GB recommended)
- Python 3.11+
- A Google ingestion backend for Gmail/Docs — see [Google ingestion backend](#google-ingestion-backend) below (the [gog CLI](https://github.com/openclaw/gog) works today)
- ~5GB free disk space

## Quick start

YouOS installs and runs standalone — no OpenClaw / clawhub required.

```bash
# 1. Clone + install (creates .venv, installs YouOS, runs the doctor)
git clone https://github.com/DrBaher/youos && cd youos
./scripts/install.sh
source .venv/bin/activate

# 2. Run the server reliably (starts at login, restarts on crash)
youos service install          # or `youos serve` to run in the foreground

# 3. Open the setup wizard in your browser
open http://127.0.0.1:8901/welcome
```

The web wizard walks you through everything:

1. **Who you are** — your name + email addresses
2. **Connect Gmail & Docs** — pick a backend (`gog` / `gws` / `native`) and authenticate
3. **Build your corpus** — pull your sent history (choose how far back; default 1 year)
4. **Learn your voice** — optional local fine-tune
5. **Secure it** — optional API token for the browser extension
6. **Keep it running** — install the background service

Then **draft** in the web UI (`/feedback`) or via the [Gmail extension](extension/).

<details>
<summary>Prefer the terminal? / Manual install</summary>

```bash
youos setup        # the same guided flow, fully in the terminal

# manual install instead of ./scripts/install.sh:
python3 -m venv .venv && source .venv/bin/activate
pip install -e .   # extras: pip install -e ".[reranker]"  or  ".[google]"
```
</details>

## Google ingestion backend

Gmail and Google Docs ingestion fetch through a pluggable backend, selected by
`ingestion.google_backend` in `youos_config.yaml`. You don't need OpenClaw to
run YouOS — pick whichever Google access path you prefer:

| `ingestion.google_backend` | What it uses | Status |
| --- | --- | --- |
| `gog` *(default)* | the [gog CLI](https://github.com/openclaw/gog) | ✅ available |
| `gws` | [Google's own Workspace CLI](https://github.com/googleworkspace/cli) | 🚧 in progress |
| `native` | direct Google API (`youos[google]` extra, OAuth) | 🚧 in progress |

The default is `gog`, so existing setups are unchanged. WhatsApp ingestion needs
no Google backend at all (it parses a local export file).

## Run it reliably (background service)

`youos serve` runs in the foreground and stops when you close the terminal. To
keep YouOS always available — running at login, restarting if it crashes,
surviving reboot — install it as a macOS background service (a launchd
LaunchAgent; no root needed):

```bash
youos service install     # start now + run at every login
youos service status      # not installed | installed | running
youos service uninstall   # stop + remove
```

It serves at your configured host/port (default `127.0.0.1:8901`) and logs to
`var/server.log`. The onboarding wizard offers this too.

## Usage

```bash
# Draft a reply
youos draft "Hi, can we schedule a call next week to discuss the proposal?"

# Draft with sender context
youos draft --sender john@company.com "email text here"

# Open the web UI
youos ui

# Check system status
youos status

# View corpus stats
youos stats

# Full corpus health report (pair count, quality scores, top senders)
youos corpus
youos corpus --json   # raw JSON output

# Add a sender note (immediately rebuilds their profile)
youos note john@company.com "prefers bullet points, decision-maker"

# Submit a feedback pair directly from the terminal
youos feedback --inbound "email text" --reply "your reply" --rating 4
youos feedback --inbound "..." --reply "..." --sender "sarah@co.com" --note "too formal"

# Run nightly pipeline manually (with step-by-step output)
youos improve --verbose

# Check system requirements
youos doctor

# Run golden benchmark evaluation (10 curated cases)
youos eval --golden

# Compare backends (MLX+LoRA / Ollama / Claude) on YOUR mail, ranked by
# how closely each sounds like your real replies (voice-match)
youos compare-models --limit 30          # add --semantic for embedding similarity

# Warm local-model server (loads the model once for fast, on-device drafting)
youos model server status                # start / stop / restart also available

# Start the web server
youos serve

# Ingest a WhatsApp export
youos ingest --whatsapp ~/Downloads/WhatsApp-Chat.txt
```

## Facts & Auto-Extraction

YouOS stores contextual facts about your contacts, projects, and preferences to improve draft quality over time. Facts are injected into generation prompts automatically.

**Auto-extraction from notes:** When you add a sender note (`youos note john@co.com "..."`) or submit feedback with a note, YouOS automatically extracts structured facts using a rule-based extractor with LLM fallback.

**How it works:**
- **Rule-based (primary):** `finditer` over 15+ pattern categories; all matches captured per note
- **Negation awareness:** Detects preceding negation words (`not`, `don't`, `never`, etc.) and skips false positives
- **Confidence scoring:** Each pattern carries a base confidence (0.6–0.9); long/noisy captures are downgraded to 0.4
- **Fact merging:** Duplicate facts (same type + key + text) are deduplicated before upsert
- **LLM fallback:** When rule-based extraction returns nothing, the Claude CLI is invoked to extract facts from unstructured text

**Pattern categories supported:**
- Communication preferences: `prefers short replies`, `prefers bullet points`, `prefers formal tone`
- Dislikes / avoidances: `hates X`, `don't like X`, `never CC X`
- Scheduling: `meetings on Mon/Wed`, `available on Fridays`, `responds within 2 hours`, `unavailable on X`
- Timezone: `UTC+5`, `GMT-8`, `EST`, `America/New_York` (IANA-style)
- Identity: `title/role: X`, `works at X`, `based in X`, `preferred name: X`, `reports to X`
- Sign-offs: `signs off with "Best,"`, `use "Cheers" as sign-off`, `signature: X`
- Language: `writes in Spanish`, `speaks French`
- Contact metadata: `phone: X`, `billing email: X`, `always CC X`, `CC their assistant X`
- Relationship tags: `decision maker`, `gatekeeper`, `VIP client`, `key account`, `referred by X`
- Project facts: `deadline: X`, `budget: $X`, `renewal date: X`, `stakeholder: X`

**API endpoints:**

```
GET    /api/facts          — list all facts (optional ?type= filter: contact | project | user_pref)
POST   /api/facts          — create or upsert a fact
DELETE /api/facts/{id}     — delete a fact by id
```

**Example fact types:**
- `contact` — `key: john@acme.com`, `fact: Prefers Tuesday meetings`
- `project` — `key: project_alpha`, `fact: Uses React 18 with TypeScript`
- `user_pref` — `key: sign_off`, `fact: Always close with "Best,"`

Facts are stored locally in the SQLite `memory` table and surfaced via the web UI.

## Web UI

The web UI provides:
- **Draft Reply**: Paste an inbound email (or full thread), generate a draft grounded in your style. A **confidence reason banner** explains *why* the draft received its confidence score (e.g. "3 strong exemplars found", "low retrieval — new topic"). See the full exemplar trace via "How was this generated?"
- **Review Queue**: Emails appear instantly, drafts stream in one by one as they generate. Automated senders filtered by address and content. Configurable batch size (5/10/20) and draft model (`claude`/`local`/`auto`). Keyboard shortcuts: `j` submit, `k` skip, `e` edit, `1-5` rate, `?` help.
- **History**: Past drafts with intent badges, confidence badges, and edit-distance indicators
- **Stats Dashboard**: Corpus health, model status, pipeline status (with skipped steps), style drift indicator, benchmark trends, edit distance trend chart, per-sender-type accuracy breakdown, and **System Health card** (corpus size, last ingestion, embedding coverage, adapter status)
- **Gmail browser extension** (recommended): A Chrome/Edge/Brave (Manifest V3) extension injects a side panel directly into Gmail — auto-detects sender/subject/body, add an optional instruction or tone, generate a draft, and click "Insert into Gmail" without leaving your inbox. Submit feedback with a star rating from the panel. Works with PIN-protected instances via `youos token-create`. See [extension/README.md](extension/README.md). (A legacy `/bookmarklet` page also exists, but the extension is more robust.)

## Architecture

```
app/
  main.py              # FastAPI application
  api/                 # HTTP endpoints
  core/                # Config, embeddings, sender classification
  db/                  # SQLite bootstrap and migrations
  generation/          # Draft generation (local Qwen + Claude fallback)
  ingestion/           # Gmail, Google Docs, WhatsApp importers
  retrieval/           # FTS5 + semantic search
  evaluation/          # Benchmark scoring
  autoresearch/        # Automated config optimization

scripts/               # CLI tools and pipeline scripts
configs/               # Persona, prompts, retrieval settings
templates/             # Web UI (feedback, stats, bookmarklet)
```

## Privacy

All data stays on your machine. No email content is ever sent to a cloud service unless you explicitly use an external LLM for draft generation (configurable). See [PRIVACY.md](PRIVACY.md).

## Configuration

All settings are in `youos_config.yaml`, created by the setup wizard:

```yaml
user:
  name: "Your Name"
  emails: ["you@company.com", "you@gmail.com"]

ingestion:
  google_backend: "gog"   # gog (default) | gws | native

review:
  draft_model: "auto"     # auto (default) | local | claude

model:
  base: "Qwen/Qwen2.5-1.5B-Instruct"
  fallback: "claude"      # or "none" for fully local
  server:
    enabled: true         # warm mlx_lm.server — loads the local model once
    port: 8088

autoresearch:
  enabled: true
  schedule: "0 1 * * *"
```

**Drafting backend:** by default (`auto`) YouOS drafts on your fine-tuned local model once it's
trained, using the cloud only as a cold-start/fallback. Force it with `review.draft_model: local`
(on-device only — pair with `model.fallback: none` for strict local) or `claude`. You can also
toggle flags without editing YAML: `youos config set review.draft_model local`.

**Troubleshooting:** run `youos doctor` (Python, Google backend, MLX, disk). The Stats page
flags failures inline with "How to fix" steps.

## Running a Personal Instance

You can run multiple independent instances from the same codebase by pointing `YOUOS_DATA_DIR` at an instance directory. Each instance has its own database, config files, and user data.

**Instance directory layout:**
```
instances/myname/
├── youos_config.yaml     # user settings (name, emails, pin, etc.)
├── var/
│   └── youos.db          # SQLite database
├── configs/
│   ├── persona.yaml      # writing style
│   ├── prompts.yaml      # prompt templates
│   └── retrieval.yaml    # retrieval settings
├── data/                 # ingested corpus (raw + feedback)
└── models/adapters/      # fine-tuned LoRA adapter (optional)
```

**Start a named instance:**
```bash
YOUOS_DATA_DIR=instances/myname uvicorn app.main:app --host 127.0.0.1 --port 8901
```

When `YOUOS_DATA_DIR` is set, YouOS derives the canonical DB path as `YOUOS_DATA_DIR/var/youos.db`.
For safety, startup now rejects mismatched DB paths and unsafe paths (for example Trash locations).

### Data Safety Commands

```bash
# Run integrity checks (required tables + regression warnings)
youos health-check --json

# Create snapshot
youos snapshot-create --tier manual

# List snapshots
youos snapshot-list

# Restore snapshot (with confirmation)
youos snapshot-restore /full/path/to/snapshot.db

# Dry-run restore
youos snapshot-restore /full/path/to/snapshot.db --dry-run
```

Instance data directories (`instances/*/var/`, `instances/*/data/`, `instances/*/models/`, `instances/*/youos_config.yaml`) are excluded from git.

## License

Open source. See LICENSE for details.
