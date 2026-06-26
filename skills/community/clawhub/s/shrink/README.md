# 🦐 Shrink — Multimodal Context Optimizer for AI Agents

**The first tool to solve image context bloat in AI agents.** Every other context compression tool skips images. Shrink doesn't.

Images in your agent's session history consume 15,000–25,000+ tokens each — **every single turn**. Shrink replaces them with rich, three-tier descriptions that preserve conversational context, complete data, AND visual design details. 96-99% token reduction. Zero information loss.

> *"Stop nuking your context with /compact. Shrink your images first."*

---

## The Problem Nobody's Solving

Every AI agent framework stores images as raw base64 in session history. A single screenshot costs ~15,000 tokens. Five images? That's 75,000 tokens of dead weight — **every turn, forever** — until you reset the entire session and lose all your context.

Existing solutions:
- **OpenClaw `/compact`** — summarizes text, **explicitly skips images**
- **Context Gateway** — compresses tool output, **text only**
- **COMPRESSION.md** — defines compression rules, **text only**
- **Agno CompressionManager** — token limits, **text only**

**Nobody touches the images.** Until now.

---

## How Shrink Works

```
Raw Image (~18,000 tokens)
    ↓ Vision model analyzes with conversation context
Three-Tier Description (~500 tokens)
    ↓ Replaces base64 in session JSONL
98.6% savings, zero information loss
```

### Three-Tier Extraction™

Shrink doesn't just describe what an image looks like. It produces three complementary tiers that capture everything an agent could ever need to look back for:

**Tier 1 — CONTEXT:** *Why this image matters in the conversation*
> SSH fingerprint verification dialog on Android, connecting to 192.168.86.194:222. User is setting up first-time SSH access from Samsung S24 phone.

**Tier 2 — DATA:** *Every readable data point in the image*
> Time: 7:24 AM | Battery: 92% | Host: Server | IP:Port: 192.168.86.194:222 | Key Type: ECDSA | Fingerprint: SHA256:D7BJ/VjYo2k6uFn31lm9TKtbF2GuDNNdmuDdrU50w8E | Buttons: Cancel (red), Continue (green)

**Tier 3 — VISUAL:** *Design, layout, and visual details*
> Dark theme interface (#1a1a1a). Dialog box centered with rounded corners, subtle shadow. Cancel button in red, Continue in green. Host entry shows active status with blue indicator. Sans-serif typography, generous vertical spacing (~24px between sections).

The CONTEXT tier captures *why* the image was sent. The DATA tier captures *what's in it* — every value, label, and data point. The VISUAL tier captures *what it looks like* — colors, layout, spacing, design patterns. Together, they eliminate any reason to go back to the raw image.

The VISUAL tier is also **context-aware** — if the conversation is about button spacing, it focuses on layout. If about color scheme, it focuses on colors. The conversation guides what visual details matter most.

---

## Comparison

### vs. Raw Images (no optimization)

| Metric | Raw Image | Shrink |
|--------|-----------|---------|
| Tokens per image | ~15,000-25,000 | ~400-600 |
| Cost per turn (5 images) | ~75,000-125,000 tokens | ~2,000-3,000 tokens |
| Can agent re-examine visual details? | ✅ Yes | ✅ Yes (via VISUAL tier) |
| Can agent recall specific values? | ✅ If readable | ✅ Always (via DATA tier) |
| Can agent recall conversational context? | ⚠️ Must re-interpret | ✅ Always (via CONTEXT tier) |
| Context window impact | 🔴 Massive | 🟢 Negligible |
| Savings | — | **96-98%** |

### vs. /compact (text summarization)

| Metric | /compact | Shrink |
|--------|----------|---------|
| Handles images? | ❌ Explicitly skips | ✅ Primary purpose |
| Preserves conversation text? | ⚠️ Summarizes (lossy) | ✅ Untouched |
| Preserves image data? | ❌ Ignored | ✅ Full extraction |
| Surgical precision? | ❌ Rewrites everything | ✅ Only touches images |
| Use case | Last resort when context is full | **First line of defense** |

### vs. Image Compression (resize/quality reduction)

| Metric | Compress Image | Shrink |
|--------|---------------|---------|
| Token savings | ~80-90% | **98-99%** |
| Text in images readable? | ⚠️ Degraded | ✅ Extracted as text |
| Agent can reference data? | ⚠️ If still legible | ✅ Always |
| Requires Pillow/deps? | Yes | No (stdlib + requests) |
| Information loss | Quality degradation | **None** |

### Approach Comparison at a Glance

| Approach | Token Cost | Info Preserved | Images Handled |
|----------|-----------|----------------|----------------|
| Raw (no optimization) | ~18,000/img | 100% | ✅ |
| Image compression | ~2,000/img | ~85% (quality loss) | ✅ |
| /compact | Varies | ~30-50% (summarized) | ❌ Skipped |
| Context-only description | ~100/img | ~60% (no raw data, no visual) | ✅ |
| Two-tier (context + data) | ~250/img | ~90% (no visual design) | ✅ |
| **Shrink full (three-tier)** | **~500/img** | **~99% (context + data + visual)** | **✅** |

---

## Real Results

Tested on a production OpenClaw fleet (10 agents):

| Agent | Images | Dupes | Tokens Saved | Cost |
|-------|--------|-------|-------------|------|
| Yancy | 121 | 28 | **2,193,034** | $0.049 |
| Wayne | 36 | 18 | 819,614 | $0.11 |
| Abby | 17 | 1 | 248,696 | $0.10 |
| Henry | 5 | 3 | 74,931 | $0.001 |
| **Total** | **179** | **50** | **3,336,275** | **$0.26** |

**$0.26 to free 3.3 million tokens.** ROI breakeven: 0.11 turns.

---

## Features

### Core
- 🧠 **Three-Tier Extraction** — context + data + visual design in every description
- ♻️ **Dedup Detection** — identical images share one API call (saved 28% in our tests)
- 🔄 **Auth Failover** — auto-rotates between API keys and OAuth tokens
- 🔑 **Smart Model Selection** — auto-picks best model based on auth type
- 💾 **Safe by Default** — `.bak` backup before every write, idempotent re-runs
- 💬 **Context-Aware** — reads preceding messages + user text + agent response

### Fleet Management
- 📊 **`--all-sessions`** — shrink every session for an agent in one command
- 🎯 **`--agent <id>`** — target any agent in your fleet
- 🔢 **`--max-images N`** — budget control, process first N only
- 📏 **`--min-tokens N`** — skip tiny images below threshold

### Developer-Friendly
- 📋 **`--json`** — structured output for pipelines, dashboards, and automation
- 🔍 **`--dry-run`** — preview everything before committing
- 💰 **Cost estimates** — see API cost before running, with dedup savings
- 🎛️ **`--context-depth N`** — tune how many preceding messages inform descriptions
- 🎨 **`--detail`** — `full` (default: context + data + visual) or `standard` (context + data only)
- 🔒 **`--redact`** — `pii` (names, DOBs, SSNs), `keys` (API keys, passwords), or `all` (everything sensitive)
- 🤖 **`--model`** — override vision model (auto, sonnet, haiku)

### Interactive UX (Telegram/Discord)
- Inline button menus for scan → shrink → apply workflow
- Per-agent selection with token counts
- Options panel for model/depth/scope
- Gateway restart option to apply changes immediately

---

## Quick Start

### As an OpenClaw Skill
```bash
clawhub install shrink
```
Then in chat:
```
/shrink
```

📦 **ClawHub:** [clawhub.ai/joelovestech/shrink](https://clawhub.ai/joelovestech/shrink)
📂 **GitHub:** [github.com/joelovestech/shrink](https://github.com/joelovestech/shrink)

### CLI Usage
```bash
# Preview what's in your session
python3 shrink.py --agent main --dry-run

# Shrink current session
python3 shrink.py --agent main

# Shrink all sessions for an agent
python3 shrink.py --agent yancy --all-sessions

# Budget-conscious: limit images, use cheaper model
python3 shrink.py --agent main --max-images 10 --model claude-haiku-4-5

# JSON output for automation
python3 shrink.py --agent main --all-sessions --json

# Specific session file
python3 shrink.py --session-file path/to/session.jsonl
```

---

## All Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--session-file` | — | Path to specific JSONL file |
| `--agent <id>` | — | Target agent's sessions directory |
| `--all-sessions` | off | Process all JSONL files for the agent |
| `--dry-run` | off | Preview without modifying |
| `--model` | auto | Vision model (auto-detects from auth type) |
| `--max-images N` | all | Limit to first N images |
| `--min-tokens N` | 500 | Skip images below token threshold |
| `--context-depth N` | 5 | Preceding messages for context-aware descriptions |
| `--detail` | full | `full` (context + data + visual) or `standard` (context + data) |
| `--redact` | off | Redact sensitive data: `pii`, `keys`, or `all` |
| `--no-backup` | off | Skip .bak backup creation |
| `--json` | off | JSON output (suppresses pretty-print) |
| `--no-verbose` | off | Suppress per-image details |

---

## How It Works (Technical)

1. **Scan** — reads session JSONL, finds `{"type":"image","data":"<base64>"}` blocks
2. **Context** — extracts preceding messages, same-message text, and next agent response
3. **Describe** — sends image + context to vision API with three-tier extraction prompt
4. **Dedup** — MD5 fingerprints identical images, reuses descriptions
5. **Replace** — swaps base64 block with `[🖼️ Image deflated: CONTEXT: ... DATA: ...]`
6. **Backup** — creates `.bak` before writing modified JSONL

### Design Decisions

**Why describe-first, never compress-first:** Compressing images (resize/quality reduction) before describing them degrades text readability. Error messages, IP addresses, config values become unreadable. Shrink always describes from the full-quality original, then removes the image. No information loss.

**Why three tiers instead of one:** Every question an agent could ask about an image falls into one of three buckets: "why was this sent?" (CONTEXT), "what was the exact value of X?" (DATA), or "what did it look like?" (VISUAL). Three-tier extraction answers all three. "We captured too much" is never the regret — "we didn't capture enough" always is. At ~500 tokens for full extraction vs ~18,000 for the raw image, the cost of completeness is a rounding error.

**Why VISUAL tier is context-aware:** The VISUAL tier reads the preceding conversation to determine what visual details matter. If the discussion is about button spacing, it focuses on layout metrics. If about color scheme, it captures hex values. This prevents generic visual descriptions and ensures the extracted details are conversationally relevant.

**Why auto model selection:** OAuth tokens (Claude Max/Max Pro) can only use Haiku via direct API. API keys get full Sonnet access. Shrink detects the token type and picks the best available model automatically, with seamless failover if the primary key fails.

---

## Cost Analysis

| Context Depth | One-time Cost/Image | Savings Per Turn | ROI Breakeven |
|---|---|---|---|
| 3 msgs | ~1,600 tokens | ~16,500 tokens | 0.10 turns |
| 5 msgs | ~1,700 tokens | ~16,500 tokens | 0.10 turns |
| 10 msgs (default) | ~1,950 tokens | ~16,500 tokens | 0.12 turns |

Based on production averages: ~17,000 tokens/image in, ~500 tokens/description out (full three-tier).

**Translation:** Spend ~1,950 tokens once → save ~16,500 tokens every turn, forever. Pays for itself before the first response completes.

---

## Roadmap

- [x] Three-tier extraction (context + data + visual)
- [x] Context-aware VISUAL tier (guided by conversation)
- [x] Dedup detection
- [x] Auth failover (API key ↔ OAuth)
- [x] Fleet-wide scanning (`--all-sessions`, `--agent`)
- [x] Interactive button UX
- [x] JSON output for automation
- [x] Detail modes (`full` / `standard`)
- [ ] Auto-shrink on ingest (shrink images as they arrive)
- [ ] Multi-provider vision support (OpenAI, Gemini, local models)
- [ ] OpenClaw core integration (`openclaw shrink` / `/shrink` native)
- [ ] Web dashboard for fleet-wide shrink stats

---

## Redaction — Compliance-Ready Extraction

Shrink can automatically strip sensitive data during extraction using `--redact`:

```bash
# Redact personal information (GDPR/HIPAA compliance)
shrink.py --agent main --redact pii

# Redact secrets and credentials (security hygiene)
shrink.py --agent main --redact keys

# Redact everything sensitive (maximum data minimization)
shrink.py --agent main --redact all
```

| Level | What Gets Redacted | Use Case |
|-------|-------------------|----------|
| `pii` | Names, DOBs, SSNs, phone numbers, emails, physical addresses, account numbers, DL numbers | GDPR, HIPAA, client-facing agents |
| `keys` | API keys, passwords, tokens, connection strings, private keys, webhook URLs with auth | Security hygiene, dev agents |
| `all` | Everything above + IP addresses, financial amounts, internal hostnames, file paths with usernames | Regulated industries, maximum minimization |

**Example output with `--redact pii`:**
```
CONTEXT: Property tax case dashboard showing document checklist status
DATA: Client: [REDACTED-NAME] | DOB: [REDACTED-DOB] | Property: 14533 Wallace Ave |
      Refund: $11,028 | PIN: 29-04-323-017 | Status: Under Review
```

The agent retains enough context to work but PII never persists in session history. Redaction happens at extraction time — zero extra API calls, zero extra cost.

**Why this matters:** Three-tier extraction makes implicit data explicit. A screenshot buried in base64 is hard to grep for PII. A structured text description with names and account numbers is trivially searchable. `--redact` ensures that when you make data accessible, you also make it safe.

## Privacy & Security

**What data leaves your machine:**
- Images (base64) and surrounding conversation context (up to 10 messages) are sent to the **Anthropic vision API** (`api.anthropic.com`) for description generation. No other external services are contacted.

**Credential access:**
- Reads `ANTHROPIC_API_KEY` from environment if set
- When `--agent <id>` is specified, reads credentials **only** from that agent's `auth-profiles.json`
- Without `--agent`, may read credentials from multiple agents for failover
- **Recommendation:** Set `ANTHROPIC_API_KEY` explicitly to control exactly which key is used

**File access:**
- Reads session JSONL files from `~/.openclaw/agents/`
- Writes modified JSONL files (image blocks replaced with text descriptions)
- Creates `.bak` backup before every write (disable with `--no-backup`)

**No telemetry.** No data collection. No external calls beyond the Anthropic API.

Use `--dry-run` to preview all changes before committing.

## License

MIT

---

## Contributing

Issues and PRs welcome. Built by [@joelovestech1](https://x.com/joelovestech1).

*Shrink is the missing piece in AI agent context management. Every framework compresses text. Nobody touches images. We do.*
