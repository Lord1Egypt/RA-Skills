<div align="center">

# 🧠 Self-Evolving Agent

**A 5-stage multi-agent pipeline that reads your AI's logs, finds what's actually broken, measures whether fixes worked, and proposes evidence-based rule changes — for your review.**

![Dashboard](demo/dashboard-preview-sm.png)

![Demo](demo/demo.gif)

![Version](https://img.shields.io/badge/version-5.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-orange)
![Cost](https://img.shields.io/badge/cost-%240.00%2Fweek%20(Ollama)-brightgreen)
![Ollama](https://img.shields.io/badge/Ollama-embeddings%20%2B%20LLM-purple)
![FP Rate](https://img.shields.io/badge/false%20positives-~8%25-green)

*Not magic. Six specialized agents + your approval. Semantic embeddings. Real-time monitoring. Fleet analysis. And it still measures whether fixes actually worked.*

</div>

---

## 🆕 What's New in v5.0

> Three new pillars. Same zero-cost local-first philosophy. Same human-approval guarantee.

### Pillar 1: Semantic Embeddings (False Positives: ~15% → ~8%)

v4 used keyword matching: "다시", "wrong again", etc. Good but blunt. "다시 확인해줘" (normal request) and "또 다시?? 진짜??" (frustration) both triggered the same keyword.

v5 uses **Ollama `nomic-embed-text`** — a local embedding model (274MB, free, no API). Every user message gets a 384-dimension vector. Cosine similarity against pre-built frustration anchors. Threshold 0.78. Result: *semantic* distinction between identical surface forms.

```
"다시 해줘"        → similarity 0.41 → normal request (no trigger)
"또 다시?? 진짜?"  → similarity 0.89 → frustration signal ✓
```

Ollama offline? **Auto-fallback to v4 heuristics.** Zero impact on weekly reporting.

### Pillar 2: Streaming Monitor (<30s Real-Time Alerts)

v4 caught 119 exec retries — but on Sunday. The 119 retries happened on Thursday.

v5's `stream-monitor.sh` watches logs continuously with `tail -F`. Exec retries ≥5 consecutive → Discord alert in under 30 seconds. No more waiting 6 days to find out something broke.

```bash
sea monitor          # Start real-time watching
sea monitor --poll   # 30s polling mode (CI / non-interactive)
sea alerts           # See triggered alerts from this week
```

### Pillar 3: Fleet Analysis (Multi-Instance)

If you run opus + sonnet + haiku, v4 only analyzed the one you pointed it at. v5 analyzes **all of them** and finds cross-instance patterns.

Pattern in all 3 instances → system-level AGENTS.md issue.  
Pattern in only haiku → haiku-specific tuning needed.

```bash
sea fleet                      # Analyze all agent instances
sea fleet --agents opus,sonnet # Specific instances only
```

### Upgrade from v4

```bash
# Optional but recommended: install Ollama for semantic embeddings
brew install ollama && ollama pull nomic-embed-text && ollama serve &

# Add v5 config sections to config.yaml (existing sections unchanged)
# See: docs/migration-v4-to-v5.md

# Switch cron to v5 orchestrator
bash scripts/register-cron.sh --v5 --update

# v4 still works unchanged — no forced migration
bash scripts/v4/orchestrator.sh   # still runs fine
```

Full migration guide: [`docs/migration-v4-to-v5.md`](docs/migration-v4-to-v5.md)

---

## The Problem

Your AI assistant makes mistakes. You correct it. It makes the same mistake next week.

Why? Because corrections die with the conversation. They never become rules.

```
Monday:   "Stop splitting messages!"  → AI: "Sorry!"
Tuesday:  Split messages again.
Monday:   "STOP SPLITTING—"
```

Manually updating AGENTS.md works. But it requires you to notice the pattern, remember to fix it, write the rule clearly, and then… somehow know whether it actually helped.

**This skill automates the entire loop. Including the part nobody else does: measuring whether it worked.**

---

## Pipeline Overview

### v5.0 (Recommended)

```
Real-time:  [stream-monitor.sh] ──── threshold breach ──▶ instant Discord alert

Batch (Sunday 22:00):
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌───────────┐  ┌──────────┐
│ Collect │─▶│ Embed    │─▶│  Trend   │─▶│ Fleet  │─▶│ Benchmark │─▶│Synthesize│
│  Logs   │  │ Analyze  │  │ Analyze  │  │Analyze │  │  Compare  │  │ Proposal │
└─────────┘  └──────────┘  └──────────┘  └────────┘  └───────────┘  └──────────┘
  7d logs +   Ollama emb.   4-week        multi-       past fixes     Claude/
  stream       → semantic   trend         instance     worked? ✓/✗    Ollama/none
  alerts       similarity   comparison    cross-view
               ↓ offline?
               v4 fallback
```

Each box is a separate script. Each produces a structured JSON artifact.  
**Only the final Synthesize stage optionally calls the Claude API** (or Ollama/none).

### v4.x (Still works, unchanged)

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Collect  │───▶│ Analyze  │───▶│Benchmark │───▶│ Measure  │───▶│Synthesize│
│  Logs    │    │ Patterns │    │ Compare  │    │ Effects  │    │ Proposal │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
  7d logs        Heuristic       AGENTS.md       Past fixes      Markdown
  30 sessions    analysis        structure       worked? ✓/✗     with diffs
```

---

---

## 🆓 Zero-Cost Mode — Run for $0.00/week with Ollama

> **v4.2 new.** Self-evolving AI self-improvement, completely free. No API keys. No internet. No cloud. Just your machine.

Stages 1–4 already run 100% locally. v4.2 adds **Ollama support** so Stage 5 (synthesis) can too.

```bash
# 1. Install Ollama (one-time)
brew install ollama
ollama pull llama3.1:8b   # ~4.7 GB, one-time download

# 2. Start Ollama server
ollama serve &

# 3. Switch to Ollama in config.yaml
#    llm:
#      provider: "ollama"
#      ollama:
#        model: "llama3.1:8b"
#        url: "http://localhost:11434"

# That's it. Zero API cost from now on.
```

### LLM Provider Comparison (synthesis stage)

| Provider | Cost/week | API Key | Internet | Quality |
|----------|:---------:|:-------:|:--------:|:-------:|
| **Anthropic** | ~$0.05 | Required | Required | ⭐⭐⭐⭐⭐ |
| **OpenAI** | ~$0.05 | Required | Required | ⭐⭐⭐⭐⭐ |
| **Ollama** 🆓 | **$0.00** | **None** | **None** | ⭐⭐⭐⭐ |
| **none** 🆓 | **$0.00** | **None** | **None** | Heuristic only |

### Ollama Usage (v5.0 — Embedding + LLM)

```bash
# Embeddings model (v5.0 new — Stage 2 semantic analysis)
ollama pull nomic-embed-text   # 274MB, free, local

# LLM model (synthesis stage — same as v4.2+)
ollama pull llama3.1:8b        # 4.7GB, free, local

# Run both
ollama serve &

# Config: use Ollama for both embedding and synthesis
# embedding:
#   model: "nomic-embed-text"
# llm:
#   provider: "ollama"
#   ollama:
#     model: "llama3.1:8b"
```

Total Ollama cost: **$0.00** — embeddings + synthesis both local.

**Ollama-recommended models:**
- `llama3.1:8b` — Best balance of speed/quality (default)
- `mistral:7b` — Fastest, good for quick iterations
- `gemma3:9b` — Google's model, strong reasoning
- `qwen2.5:7b` — Excellent multilingual (great for Korean sessions)

### Pure Heuristic Mode (provider: none)

If you don't want any LLM involvement at all:

```yaml
llm:
  provider: "none"
```

Stages 1–4 produce the analysis. Stage 5 synthesizes it into markdown using shell scripts only. No API, no Ollama, no network. Pure pattern-matching → proposal generation.

**Use case:** Air-gapped machines, maximum privacy, or when you trust the heuristic output as-is.

---

## Why v4.0? The Journey

> "Each version was born from a real failure of the previous one."

### v1.0 — Complaint Detection
The first version. A single script that keyword-searched chat logs for user frustration signals: `"다시"`, `"반복"`, `"기억"`. It found complaints and dumped them into a file.

**Problem:** ~40% false positive rate. The assistant itself says `"다시"` constantly. No way to tell who's frustrated.

### v2.0 — Exec Retry Detection
Added a new signal: consecutive exec retries. Found 119 consecutive retries in one session that no one had noticed. Added cron error log parsing too.

**Problem:** Still one flat script, one Claude call with everything thrown in. Output was noisy. And after applying a proposal, there was no way to know if it helped.

### v3.0 — Session Health Metrics
Introduced compaction counting, per-session dedup, and a cleaner proposal template. Made the reports more readable.

**Problem:** Still ~40% FP. Still no feedback loop. Applied a fix? You'd never know if it worked unless you manually went back and checked weeks later. Nobody does that.

### v4.0 — Closed Feedback Loop + Multi-Agent Pipeline
Split the monolith into 5 specialized stages. Added `role_filter` to separate user vs assistant messages (killed most false positives). Added the Benchmark Agent to measure whether last week's proposals actually helped.

**What changed:**
- False positive rate: ~40% → ~15%
- Feedback loop: None → closed (you see `"Proposal #2: −45% ✅"` next week)
- Cost: Still < $0.05/run (only Stage 5 hits the API)
- Runtime: < 3 minutes end-to-end

```
v1.0  ──▶  keyword grep + dump
v2.0  ──▶  + exec retry detection
v3.0  ──▶  + session health + cleaner output
v4.0  ──▶  5-stage pipeline + role filter + effect measurement ✅
```

---

## The Key Differentiator: Closed Feedback Loop

Every other tool in this space proposes changes. None of them measure whether the changes actually helped.

v4.0's Benchmark Agent does:

```
Week 1: Proposal #2 — "Add exec retry limit rule"
        → You apply it.

Week 2: Benchmark Agent checks:
        "다시" pattern: 22× → 12× (−45%)
        → Verdict: ✅ Effective

        Report includes:
        📈 Last week's proposals:
           #2 Exec retry rule: Effective (−45%) ✅
           #3 Log check rule:  Neutral (+2%)  — observe more
```

If a rule made things worse (Regressed), the Benchmark Agent flags it for re-review. If it had no effect, it stays on the watchlist. You always know what's working.

---

## vs. Alternatives

| Feature | Self-Evolving Agent v5 | CrewAI / Autogen | LangChain loops | Custom crons |
|---------|:------------------:|:----------------:|:---------------:|:------------:|
| Reads actual chat logs | ✅ | ❌ | ❌ | Manual |
| Multi-agent pipeline | ✅ 6 stages | ✅ Complex | ✅ Complex | ❌ |
| **Semantic embeddings** | ✅ Ollama local | ❌ | ❌ (optional) | ❌ |
| **Real-time streaming** | ✅ <30s alerts | ❌ | ❌ | ❌ |
| **Fleet / multi-instance** | ✅ Cross-agent analysis | ❌ | ❌ | ❌ |
| Setup complexity | **Low** (3 commands) | High | High | Medium |
| Effect measurement | ✅ Benchmark agent | ❌ | ❌ | ❌ |
| False positive rate | **~8%** (semantic+structured) | N/A | N/A | ~40%+ |
| Human approval gate | ✅ Hard constraint | Optional | Optional | Optional |
| AGENTS.md targeting | ✅ Native | ❌ | ❌ | ❌ |
| Cost per run | **$0.00 (Ollama)** | $0.50+ | $0.50+ | $0 (no LLM) |
| Runtime | **< 5 min** (w/ embed) | 5–20 min | 5–20 min | < 1 min |
| OpenClaw native | ✅ | ❌ | ❌ | ❌ |
| Graceful degradation | ✅ v4 fallback | ❌ | ❌ | N/A |

**Honest take:** CrewAI and LangChain are powerful general-purpose frameworks. If you need complex agent coordination for arbitrary tasks, use them. Self-Evolving Agent is purpose-built for one thing: improving your AI's AGENTS.md based on real log evidence — and then measuring whether it worked. v5.0 adds semantic understanding and real-time awareness without losing the simplicity that makes it auditable in 15 minutes.

---

## Example: What You See in Discord

Every Sunday at 22:00, this lands in your Discord channel:

```
🧠 Self-Evolving Agent v4.0 — Week of Feb 17

📈 Benchmark (last week's proposals):
   #2 Exec retry limit:  ✅ Effective (−45%, "다시" 22× → 12×)
   #3 Log check rule:    ⏳ Neutral   (+2%) — observe one more week

📊 This week's analysis:
   Sessions: 30 analyzed (of 964 total)
   exec retries: 405 events, max 119 consecutive
   Cron errors: 3 active
   Role-filtered false positives removed: ~18

📝 3 new proposals:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proposal #1 — HIGH
Evidence: 405 retry events, max 119 consecutive in one session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before: No rule for consecutive exec failures (infinite loop possible)

After:
  If same exec fails 3× in a row:
  1. Report error immediately
  2. Second attempt must use different approach
  3. Third failure → STOP, request manual confirmation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Apply:  "apply proposal #1"
❌ Reject: "reject: [reason]"
```

No vague suggestions. Real numbers. Diff format. Your decision.

---

## Real Numbers (v3.0 Live Test — v4.0 improves on this)

Deployed on a personal OpenClaw instance. These are actual numbers from the system that triggered the v4.0 rewrite:

| Metric | Value |
|--------|-------|
| Sessions analyzed (7-day sample) | **30** (of 964 total) |
| exec retry events detected | **405** |
| Max consecutive retries (one session) | **119** |
| Cron errors detected | **3 active** |
| Repeating log errors (same error) | **18×** (heartbeat bug) |
| Heavy sessions (20+ compactions) | **3** |
| Proposals generated | **3** |
| Proposals accepted | **2 / 3** |
| v3.0 false positive rate | ~40% |
| **v4.0 estimated false positive rate** | **~15%** |

**What triggered v4.0:** After applying the v3.0 proposals, we had no way to know if they helped. That's the problem the Benchmark Agent was built to solve.

---

## 📊 Local Dashboard

Visualize your agent's self-improvement history in a browser — no npm, no build step.

```bash
# Start the dashboard server (auto-builds the data index)
bash dashboard/serve.sh
# → Open http://localhost:8420/dashboard/
```

| Panel | What it shows |
|---|---|
| 📈 Quality Trend | `quality_score` line chart over time |
| 🏥 AGENTS.md Health | Benchmark score ring (0–100) + history sparkline |
| 🔍 Pattern Frequency | Complaint patterns stacked bar chart by week |
| 📋 Proposal History | All proposals with severity, status, effect badges |
| ⚡ Rules Effectiveness | Green = reduced patterns, Red = regressed, Blue = neutral |

> See [`dashboard/README.md`](dashboard/README.md) for full docs.

---

## Install

```bash
# 1. Clone the repository
git clone https://github.com/Ramsbaby/self-evolving-agent ~/openclaw/skills/self-evolving-agent

# 2. Run the setup wizard (interactive)
bash ~/openclaw/skills/self-evolving-agent/scripts/setup-wizard.sh

# Done. Every Sunday at 22:00, 5 agents analyze your AI.
```

### sea CLI (optional but recommended)

Add `bin/` to your PATH to use the `sea` command anywhere:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/openclaw/skills/self-evolving-agent/bin:$PATH"

# Enable tab completion (bash only)
source ~/openclaw/skills/self-evolving-agent/bin/sea-completion.bash
```

Then reload your shell and use `sea` directly:

```bash
sea status                     # Last run: 2026-02-17 22:00 | Score: 6.8/10 | Proposals: 3
sea proposals                  # List pending proposals
sea approve proposal-20260217  # Review diff → patch AGENTS.md → git commit
sea reject proposal-20260217 "Already handled"
sea run                        # Trigger pipeline manually
sea run --stage 2              # Run only the analyze stage
sea health                     # AGENTS.md health score
sea config set analysis.days 14
sea help                       # Full command reference
```

Use `--json` on any command for machine-readable output:

```bash
sea status --json
sea history --json | jq '.[].title'
```

**Non-interactive install** (CI/automation):

```bash
bash ~/openclaw/skills/self-evolving-agent/scripts/setup-wizard.sh \
  --platform discord \
  --channel YOUR_CHANNEL_ID \
  --lang auto \
  --days 7 \
  --yes
```

The wizard will:
- Ask where your OpenClaw workspace is
- Ask which delivery platform (discord / slack / telegram / webhook)
- Collect the required credentials for your platform
- Ask for analysis period, max sessions, and primary language
- Write `config.yaml`
- Optionally register the weekly cron

**Validate config at any time:**

```bash
bash ~/openclaw/skills/self-evolving-agent/scripts/validate-config.sh --fix
```

Want v3.0 compatibility? Use `--v3` flag (legacy scripts are preserved).

**Optional — edit `config.yaml`:**

```yaml
# LLM provider (v4.2) — set "ollama" for zero-cost local AI
llm:
  provider: "ollama"          # anthropic | openai | ollama | none
  ollama:
    model: "llama3.1:8b"      # or mistral:7b, gemma3:9b, qwen2.5:7b
    url: "http://localhost:11434"

analysis:
  days: 14                    # 2 weeks instead of 1
  complaint_patterns:         # v4.1: language-separated (ko/en) with auto-detection
    ko:                       # Korean session patterns
      - "말했잖아"
      - "왜 또"
      - "전부 다 해줘"        # Add your own Korean frustration signals
    en:                       # English session patterns
      - "stop asking me"      # Add your own English frustration signals
      - "you forgot again"
      - "how many times"
    auto_detect: true         # Auto-detect language from session content
                              # >50% Korean chars → ko patterns, else → en
  heuristic:
    role_filter: true         # User messages only (default: on)
    context_window: 3         # Lines of context around keyword
    dedup_per_session: true   # One count per pattern per session
  benchmark:
    enabled: true             # Measure previous proposals (default: on)
    effective_threshold: 0.30 # 30% reduction = "Effective"

cron:
  schedule: "0 9 * * 1"      # Monday 9AM instead of Sunday 22:00
```

---

## Architecture

```
scripts/v4/
├── orchestrator.sh         ← Orchestrator (start here)
├── collect-logs.sh         ← Stage 1: Reads logs → structured JSON
├── semantic-analyze.sh     ← Stage 2: Keyword + heuristic analysis
├── benchmark.sh            ← Stage 3: Compares AGENTS.md structure vs patterns
├── measure-effects.sh      ← Stage 4: Before/after effect measurement ✓/✗
└── synthesize-proposal.sh  ← Stage 5: Claude call → Markdown with diffs

data/
├── proposals/              ← Generated proposal JSONs
├── benchmarks/             ← Stage 4 effectiveness results (v4.0 new)
├── undelivered/            ← Failed deliveries (auto-saved for retry)
└── rejected-proposals.json ← Rejection log (fed back next cycle)
```

Full architecture details: [`docs/v4-architecture.md`](docs/v4-architecture.md)

---

## Multi-Platform Support

By default, proposals are delivered via Discord using OpenClaw's native cron delivery. v4.1 adds native support for **Slack**, **Telegram**, and **generic webhooks**.

Set your platform in `config.yaml`:

```yaml
delivery:
  platform: "slack"   # discord | slack | telegram | webhook
```

| Platform | How it works | What to set |
|----------|-------------|-------------|
| **Discord** | OpenClaw cron native delivery (default) | `cron.discord_channel` + cron `delivery.to` |
| **Slack** | `curl` to Incoming Webhook, markdown→mrkdwn | `delivery.slack.webhook_url` |
| **Telegram** | `curl` to Bot API, markdown→HTML | `delivery.telegram.bot_token` + `chat_id` |
| **Webhook** | `curl` JSON POST to any endpoint | `delivery.webhook.url` |

### Slack

```yaml
delivery:
  platform: "slack"
  slack:
    webhook_url: "https://hooks.slack.com/services/T.../B.../..."
```

→ [Create a Slack Incoming Webhook](https://api.slack.com/messaging/webhooks)

### Telegram

```yaml
delivery:
  platform: "telegram"
  telegram:
    bot_token: "123456:ABC-DEF..."   # from @BotFather
    chat_id: "-1001234567890"        # channel ID (starts with -100)
```

### Generic Webhook

```yaml
delivery:
  platform: "webhook"
  webhook:
    url: "https://your-server.example.com/proposals"
    method: "POST"
```

Payload delivered as:
```json
{
  "source": "self-evolving-agent",
  "version": "4.0",
  "timestamp": "2026-02-18T00:00:00Z",
  "proposal": "## 🧠 SEA v4.0 ...(full markdown)..."
}
```

**Fallback:** If delivery fails for any reason, the proposal is saved to `data/undelivered/` so nothing is lost. Retry manually:

```bash
PLATFORM=slack bash scripts/v4/deliver.sh data/undelivered/<file>.md
```

---

## What It Doesn't Do

Being explicit here:

- ⚠️ **Semantic embeddings require Ollama** — if Ollama is offline, auto-falls back to v4 heuristics (~15% FP). With Ollama: ~8% FP.
- ⚠️ **~8% false positive rate (embedding) / ~15% (heuristic fallback)** — improved from v3.0's ~40%, but still imperfect
- ⚠️ **Streaming monitor needs persistent process** — `sea monitor` or a LaunchAgent; not a fire-and-forget cron
- ⚠️ **Trend analysis needs 4+ weeks** — first month shows sparse trends
- ❌ **Benchmark ≠ causal analysis** — frequency-based correlation, not causation
- ❌ **Generic output on quiet weeks** — if no complaint data, proposals will be vague
- ❌ **Cold start** — first 2–4 weeks have little data
- ❌ **Mixed-language sessions** — embedding helps, but code-switching edge cases remain

**v5.0:** Semantic embeddings (Ollama `nomic-embed-text`) now handle the patterns that keyword lists can't. Auto-fallback to v4 heuristics if Ollama is offline. The analysis mechanism is now: 6 shell scripts + one optional Claude/Ollama call + your approval.

The name "self-evolving" describes the goal, not the mechanism. Useful? Yes. Magic? No.

---

## FAQ

**Q: How is this different from self-improving-agent?**

> `self-improving-agent` scores individual sessions in real-time — per-session microscope. `self-evolving-agent` looks across 7+ days and finds systemic patterns — system-level telescope. v4.0 integrates self-improving-agent's quality scores as input weights to the analysis stage.

**Q: Will it modify my AGENTS.md automatically?**

> Never. Hard design constraint. Every proposal requires explicit approval from you. The word "modify" doesn't appear in the same code path as "AGENTS.md" without a user confirmation gate.

**Q: How does the Benchmark Agent work?**

> It compares pattern frequency between the week before a proposal was applied and the week after. If "다시" appeared 22 times before and 12 times after, that's −45% → Effective. The comparison uses the same analysis methodology across both periods for consistency.

**Q: What if I reject a proposal?**

> Logged to `data/rejected-proposals.json`. The next week's Synthesize Agent reads this and won't re-propose the same change. After 3 similar rejections, it flags the pattern as "user preference — do not suggest."

**Q: How much does it cost?**

> **$0.00/week with Ollama** (v4.2). Set `llm.provider: "ollama"` in config.yaml and run `ollama serve`. All 5 stages run locally — zero API cost, zero internet required.
>
> With cloud APIs: < $0.05/week using Claude Sonnet 4.5 or GPT-4.1. Only Stage 5 (Synthesize) hits the API. Stages 1–4 always run locally regardless of provider.
>
> With `provider: "none"`: also $0.00/week — pure heuristic mode, no LLM at all.

**Q: Can I run one stage at a time?**

> Yes. Each stage is an independent script:
> ```bash
> bash scripts/v4/collect-logs.sh        # Run collection only
> bash scripts/v4/semantic-analyze.sh    # Run analysis only
> bash scripts/v4/benchmark.sh           # Run benchmark only
> bash scripts/v4/measure-effects.sh     # Run effect measurement only
> bash scripts/v4/synthesize-proposal.sh # Run synthesis only
> ```

**Q: Is this actually "self-evolving"?**

> It's 5 shell scripts + one Claude call + your approval. "Self-reviewing with effect measurement" would be more accurate. The name communicates the goal. We're not pretending it's more than it is.

---

## 🤖 Fleet Analysis (v5.0)

**SEA v5.0 introduces multi-agent fleet analysis** — instead of analyzing one agent, it analyzes ALL agents simultaneously and finds shared patterns, benchmark leaders, and cross-agent improvement opportunities.

### Fleet Commands

```bash
# Show all agents' status at a glance
sea fleet

# Run full fleet analysis (all agents in ~/.openclaw/agents/)
sea fleet run

# Side-by-side comparison table
sea fleet compare
sea fleet compare --focus exec_safety   # Focus on one metric

# Generate cross-agent improvement proposals
sea fleet proposals

# Copy a validated rule from one agent to another
sea fleet sync exec_safety --from opus --to sonnet
sea fleet sync core_rules --from opus --to-all

# Fleet-wide health score
sea fleet health
```

### Fleet Report Schema

```json
{
  "agents_analyzed": 5,
  "fleet_health": 8.1,
  "agent_scores": {
    "opus":   {"quality": 8.2, "exec_safety": 9.0, "frustration": 1},
    "sonnet": {"quality": 7.8, "exec_safety": 7.5, "frustration": 4},
    "haiku":  {"quality": 7.1, "exec_safety": 8.5, "frustration": 0}
  },
  "shared_patterns": [
    {
      "pattern": "git_direct_cmd",
      "agents_affected": ["opus", "sonnet"],
      "is_systemic": false
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "type": "transfer_rule",
      "target": "sonnet",
      "source": "opus",
      "proposal": "Copy exec safety rule from opus → sonnet",
      "action": "sea fleet sync exec_safety --from opus --to sonnet"
    }
  ]
}
```

### Cross-Agent Proposal Types

| Type | When | Example |
|------|------|---------|
| `systemic` | Same violation in 2+ agents | "git 직접 명령 — opus, sonnet 모두 발생" |
| `transfer` | Agent A's rule works well → copy to B | "opus exec_safety(9.0) → sonnet(7.5)" |
| `all_agents` | Fleet-wide health below target | "공통 WAL 프로토콜 강화" |
| `improvement` | Single agent high frustration | "sonnet 좌절 4건 — 컨텍스트 관리 개선" |

**Architecture details:** [`docs/v5-architecture.md`](docs/v5-architecture.md)

---

## Roadmap

| Version | Feature | Status |
|---------|---------|--------|
| **v1.0** | Complaint detection (keyword grep) | ✅ Done |
| **v2.0** | exec retry detection (119× real case) | ✅ Done |
| **v3.0** | Session health metrics + cleaner proposals | ✅ Done |
| **v4.0** | 5-stage pipeline + effect measurement + role filter | ✅ Done |
| **v4.1** | Multi-platform delivery (Slack/Telegram) + ko/en patterns | ✅ Done |
| **v4.2** | Ollama/local LLM — zero-cost AI self-improvement | ✅ Done |
| **v4.3** | Interactive approval (sea watch) + export + GitHub Issues | ✅ Done |
| **v5.0** | Semantic embeddings + streaming monitor + fleet analysis | ✅ **Live** |
| **v5.1** | Multi-language embedding anchors (JP, ES, ZH) | 🔨 Next |
| **v5.2** | Causal inference for effect measurement (interrupted time series) | 📋 Planned |
| **v5.3** | Dashboard v2 — embedding cluster visualization, fleet heatmap | 📋 Planned |
| **v6.0** | Active learning — flag low-confidence predictions for user feedback | 💡 Concept |

---

## Safety Principles

- ✅ **Propose only** — no code path modifies AGENTS.md without explicit approval
- ✅ **Evidence required** — every proposal cites measured data + semantic confidence score
- ✅ **Diff format** — before/after always shown; never vague "you should improve X"
- ✅ **Rejection learning** — rejected proposals logged and respected
- ✅ **Transparent code** — ~500 lines of shell scripts you can audit in 20 minutes
- ✅ **Local-first** — all analysis runs on your machine; embeddings are local too (Ollama)
- ✅ **Human in the loop** — always. The AI proposes, you decide.
- ✅ **Effect measurement** — tracks whether previous proposals actually helped
- ✅ **Embedding privacy** — cache stores vectors only, never raw message text
- ✅ **Graceful degradation** — Ollama offline → heuristic fallback, not crash

---

## Contributing

Most useful contributions right now:

1. **Embedding anchor patterns** — more frustration anchor texts for `sea patterns add` (all languages welcome)
2. **Multi-language embedding anchors** — Japanese, Spanish, Chinese (v5.1 target)
3. **Stream monitor thresholds** — better heuristics for what counts as "anomalous"
4. **Causal inference for effect measurement** — interrupted time series analysis (v5.2 target)
5. **Dashboard v2** — embedding cluster visualization, fleet heatmap (v5.3 target)

---

## License

MIT — use freely, modify freely, ship freely.

---

<div align="center">

*Honest tool. Imperfect. But it caught 119 exec retries I never noticed — and now it tells me whether the fix actually worked. And with Ollama, it costs exactly $0.00.*

*Made with ❤️ on [OpenClaw](https://openclaw.ai)*

**[⭐ Star this skill](#) · [🐛 Report a bug](#) · [💡 Suggest a pattern](#) · [📖 Architecture docs](docs/v4-architecture.md)**

</div>
