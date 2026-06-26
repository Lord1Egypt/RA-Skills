---
name: superthink
version: 1.0.0
description: >
  Deep-dive research and analysis engine. Triggered by /superthink. Runs an interrogate flow
  to narrow topic and scope, then executes a 4-stage fully automatic pipeline: (1) master
  reasoning brief via Opus, (2) parallel deep-dive sections via Sonnet batch, (3) synthesis
  pass producing ~60,000 word document via Sonnet batch, (4) executive brief ~3,000 words via
  Sonnet batch. Fully hands-off after scope confirmation. Each stage uses an idempotent
  self-terminating cron poller. Requires the interrogate skill.
requires:
  skills:
    - interrogate
  env:
    - name: ANTHROPIC_API_KEY
      description: Anthropic API key — required for all batch API calls (stages 2-4)
      required: true
      sensitive: true
    - name: BATCH_JOBS_DIR
      description: Directory for batch job state files. Defaults to ./batch-jobs/ if not set.
      required: false
      sensitive: false
    - name: NOTIFY_WEBHOOK_URL
      description: Optional webhook URL for job completion notifications
      required: false
      sensitive: false
    - name: TELEGRAM_BOT_TOKEN
      description: Optional Telegram bot token for job completion notifications
      required: false
      sensitive: true
    - name: TELEGRAM_CHAT_ID
      description: Optional Telegram chat ID for job completion notifications
      required: false
      sensitive: false
    - name: NOTIFY_LOG_FILE
      description: Optional path to a log file for job completion notifications
      required: false
      sensitive: false
  dependencies:
    - name: python-docx
      install: pip install python-docx
      reason: Required by md2docx.py to generate .docx output in Stage 4
      required: false
      note: Only needed if you want .docx output. brief.md is always written regardless.
  filesystem:
    - path: /data/superthink/
      access: read-write
      reason: Persistent storage for all pipeline output (master brief, sections, synthesis, final brief)
    - path: ./batch-jobs/
      access: read-write
      reason: Batch job state files, results JSONL, job registry
  network:
    - host: api.anthropic.com
      reason: Anthropic Batch API — used for stages 2, 3, and 4
    - host: configurable
      reason: Optional notification endpoints (webhook, Telegram) — only if env vars are set
  autonomy:
    confirmation: single — user confirms scope once, pipeline runs fully unattended after that
    duration: 6-12 hours typical (dominated by Anthropic batch queue times)
    checkpoints: none after scope confirmation — by design
    note: >-
      If you want approval checkpoints between stages, modify the cron poller payloads
      to pause and notify before submitting the next stage.
---

# /superthink

Deep research + synthesis engine. Triggered by `/superthink`.

## ⚠️ Prerequisites

This skill requires the **interrogate** skill to be installed.
If it's not present, prompt the user:

> "The superthink skill requires the **interrogate** skill.

Check by looking for an `interrogate` skill in your skills directory before proceeding.

---

## Pipeline Overview

4 stages, fully hands-off after scope confirmation:

| Stage | What | How | Output | Max tokens |
|---|---|---|---|---|
| 1 | Master Reasoning Brief | Opus subagent (realtime) | `master-brief.md` | 12,000 |
| 2 | Parallel Deep-Dives (10-12 sections) | Sonnet batch + Cron 2 | `sections/NN-title.md` | 24,000 each |
| 3 | Full Synthesis Document | Sonnet batch + Cron 3 | `synthesis.md` | 60,000 |
| 4 | Executive Brief | Sonnet batch + Cron 4 | `brief.md` + `brief.docx` | 4,000 |

**Estimated cost per run:** ~$15-20 (batch discount applied to stages 2-4)
**Estimated time:** 6-12 hours end-to-end (dominated by batch queue times)
**Final delivery:** `brief.docx` delivered via your configured channel when complete

---

## Model Configuration

This skill prefers **Opus** for Stage 1 and **Sonnet** for stages 2-4, but adapts to whatever models your OpenClaw instance has available.

**Resolution order:**
- Stage 1: try `anthropic/claude-opus-4-7` → fall back to your default model if blocked
- Stages 2-4: try `claude-sonnet-4-6` → fall back to your default model if blocked

Check your model whitelist before running. Note in `pipeline-state.json` which model was actually used.

---

## Storage

All output is written to a persistent directory. **Create these directories before running:**

```
/data/superthink/
  [topic-slug]/
    sections/        ← Stage 2 section files go here
```

Create with:
```bash
mkdir -p /data/superthink/[slug]/sections
```

Full structure after a completed run:
```
/data/superthink/[topic-slug]/
  pipeline-state.json    # Source of truth — stage tracking + all job IDs
  master-brief.md        # Stage 1 output
  sections/
    01-[title].md        # Stage 2 sections (10-12 files)
    02-[title].md
    ...
  synthesis.md           # Stage 3 full synthesis (~40-60k words)
  brief.md               # Stage 4 executive brief (~3,000 words)
  [slug]-BRIEF.docx      # Final deliverable
  stage2-job.json        # Batch job definitions (kept for reference)
  stage3-job.json
  stage4-job.json
```

Store under `/data/` if your setup persists that path across restarts (e.g. Railway volume mounts). Adjust the base path to match your environment.

---

## Trigger Flow

When user sends `/superthink [optional topic]`:

1. Check interrogate skill is installed — prompt to install if missing
2. Create output directories: `mkdir -p /data/superthink/[slug]/sections`
3. Run **interrogate flow** — ask 4-10 questions in batches of 2 to narrow scope
4. Confirm scope summary — wait for explicit "yes"
5. From here: **fully hands-off** — no more checkpoints, no approvals needed

---

## Interrogate Flow

Ask in batches of 2, adapt based on answers. Minimum 4, maximum 10 questions.

Always cover:
- What is the core subject/concept?
- Primary goal: build it / understand it / evaluate it / compare options?
- Domain/context: tech, business, product, finance, legal, other?
- Depth on "how to do it": conceptual overview vs step-by-step implementation?
- Known constraints: budget, tech stack, market, regulatory?
- Output focus: new project foundation / feature for existing product / investment thesis / other?

After answers → confirm scope summary → wait for "yes" → proceed to Stage 1.

---

## Topic Slug Rules

Lowercase, hyphens only, max 40 chars.
- "staking platform for LatAm" → `staking-platform-latam`
- "crypto exchange compliance UAE" → `crypto-exchange-compliance-uae`

If slug already exists in `/data/superthink/`, append `-v2`, `-v3`.

---

## Stage 1 — Master Reasoning Brief

**Model: Opus (fall back to default model if blocked)**
**Method: `sessions_spawn` with `model: "anthropic/claude-opus-4-7"` or your configured Opus alias**
**No checkpoint after Stage 1 — proceed immediately to Stage 2**

### Subagent task:
```
Write the master reasoning brief for this research topic.

Topic: [TOPIC]
Scope: [SCOPE FROM INTERROGATE]
Goal: [GOAL]
Constraints: [CONSTRAINTS]

The brief must contain:

1. THESIS — Central claim (5-8 sentences). Specific, testable.

2. CORE ASSUMPTIONS — All assumptions (tech, market, feasibility, regulatory).
   Label each: (a) established fact, (b) reasonable assumption, (c) uncertain bet.

3. KEY FACTS — 15-20 most important facts, figures, data points.
   Include sources/indicators where possible.

4. OPEN QUESTIONS — 8-12 genuinely unknown or debated questions.
   These are what the deep-dive sections must attempt to answer.

5. SECTION PLAN — Exactly 10-12 sections. For each:
   - Title
   - Precise scope (what it covers, what it excludes)
   - 5-7 key questions it must answer
   - How it connects to the thesis
   - What evidence or examples it should engage with
   - Which other sections it relates to

6. REASONING ANCHORS — 8-10 shared principles ALL sections must respect.
   These ensure internal consistency across the document.

7. KNOWN RISKS & FAILURE MODES — 5-8 ways this could go wrong.

This brief will be passed verbatim to 10-12 parallel research agents.
Write so each agent can reason independently but consistently.
No filler. No hedging without substance.

IMPORTANT: Write the brief to /data/superthink/[SLUG]/master-brief.md using the write tool.
After writing, return ONLY: "Master brief saved — ~[word count] words"
Do NOT return the content as a message.
```

### After Stage 1 subagent returns:
1. `read` the file to verify it exists and has content
2. Write `pipeline-state.json` → `{"stage": "2-pending", "slug": "[slug]"}`
3. Build `stage2-job.json` (see Stage 2 below)
4. Submit batch job via your batch submission method (see Batch Submission below)
5. Capture Job ID + Batch ID from output
6. Update `pipeline-state.json` → `{"stage": "2", "stage2_job_id": "...", "stage2_batch_id": "..."}`
7. Create Cron 2 with payload referencing its own cron ID (see Cron Pattern below)
8. Notify user via their configured channel: "⚙️ Stage 1 done. Stage 2 (10-12 deep-dives) running — ~2-4h."

---

## Stage 2 — Parallel Deep-Dives

**One batch request per section. `max_tokens: 24,000` each.**
**Include `"project": "superthink"` in job JSON for API dashboard tagging.**

### Job JSON structure:
```json
{
  "description": "Superthink Stage 2 — [TOPIC] — [N] deep-dive sections",
  "model": "claude-sonnet-4-6",
  "max_tokens": 24000,
  "project": "superthink",
  "system": "You are a senior domain expert and researcher. Write with depth, specificity, and precision. No filler. Every paragraph must add information not in the previous one.",
  "requests": [
    {
      "id": "s01",
      "max_tokens": 24000,
      "messages": [{"role": "user", "content": "[FULL PROMPT — see template below]"}]
    }
  ]
}
```

### Per-section prompt template:
```
MASTER BRIEF (do not deviate from thesis, assumptions, or reasoning anchors):
[FULL CONTENT OF master-brief.md]

---

YOUR ASSIGNMENT: Write Section [N] of [TOTAL]: [SECTION TITLE]

Scope for this section:
[SCOPE FROM MASTER BRIEF]

Key questions you must answer (all of them):
[QUESTIONS FROM MASTER BRIEF]

Related sections (do not duplicate their content):
[LIST OF OTHER SECTION TITLES]

Requirements:
- 8,000-12,000 words
- H2 and H3 headers throughout — no walls of text
- Structure: Introduction → [3-5 major subsections] → Synthesis → Key Takeaways
- Include: real examples, step-by-step breakdowns, alternatives/trade-offs, edge cases,
  quantitative data, real company/tool/framework names, forward-looking implications
- Do NOT contradict master thesis or reasoning anchors
- Do NOT repeat content from other sections
- End with "Key Takeaways" block: 7-10 specific, actionable bullets
- End with "Open Threads" block: 3-5 questions this section raises but doesn't resolve

Write with the depth of a senior domain expert. No generic observations.
If uncertain, say what IS known and what the uncertainty is.
```

### Cron 2 — Stage 2 Poller
See **Cron Poller Pattern** section below.
When Stage 2 completes: write sections → build stage3-job.json → submit Stage 3 → create Cron 3 → self-delete.

---

## Stage 3 — Full Synthesis Document

**One batch request. `max_tokens: 60,000`.**
**Input: master brief + all Stage 2 sections concatenated.**
**Target output: ~40,000-60,000 words.**

### Job JSON structure:
```json
{
  "description": "Superthink Stage 3 — [TOPIC] — synthesis",
  "model": "claude-sonnet-4-6",
  "max_tokens": 60000,
  "project": "superthink",
  "system": "You are the editor and synthesizer for a major deep research report. Produce a unified, authoritative document. No filler. Every sentence must earn its place.",
  "requests": [
    {
      "id": "synthesis",
      "max_tokens": 60000,
      "messages": [{"role": "user", "content": "[FULL PROMPT — see template below]"}]
    }
  ]
}
```

### Synthesis prompt template:
```
MASTER BRIEF:
[FULL CONTENT OF master-brief.md]

SECTION 1: [TITLE]
[FULL CONTENT OF sections/01-title.md]

[... all sections ...]

---

YOUR TASK — produce a single unified document:

1. TITLE PAGE — topic title, date, word count estimate.

2. TABLE OF CONTENTS — all section titles + major subsections.

3. EXECUTIVE SUMMARY (1,000-1,500 words)
   - What this is and why it matters now
   - Central thesis restated with confidence level
   - Top 7 findings across all sections
   - Top 5 actionable insights
   - Top 3 risks or unresolved questions

4. SYNTHESIS NARRATIVE (4,000-6,000 words)
   Connect all sections into one coherent argument:
   - How sections relate to and reinforce each other
   - Cross-section patterns and tensions
   - Contradictions resolved or explicitly flagged
   - Argument arc: foundations → implications → action

5. FULL SECTIONS
   For each section, write a 200-300 word contextualizing introduction,
   then include the full section content verbatim.

6. CONCLUSION (800-1,000 words)
   - What all of this adds up to
   - 5-7 concrete, prioritized next steps
   - What to validate or research further

7. OPEN QUESTIONS REGISTRY
   All "Open Threads" from all sections, grouped by theme.

Word target: 40,000-60,000 words total.
Format: clean markdown, H1/H2/H3 throughout.
```

### Cron 3 — Stage 3 Poller
See **Cron Poller Pattern** section below.
When Stage 3 completes: save `synthesis.md` → build stage4-job.json → submit Stage 4 → create Cron 4 → self-delete.

---

## Stage 4 — Executive Brief

**One batch request. `max_tokens: 4,000`.**
**Input: synthesis.md. Target: 3,000-3,500 words.**

### Job JSON structure:
```json
{
  "description": "Superthink Stage 4 — [TOPIC] — executive brief",
  "model": "claude-sonnet-4-6",
  "max_tokens": 4000,
  "project": "superthink",
  "system": "You are writing an executive brief for a decision-maker. Direct, specific, no filler. Every sentence must be actionable or informative.",
  "requests": [
    {
      "id": "brief",
      "max_tokens": 4000,
      "messages": [{"role": "user", "content": "[FULL PROMPT — see template below]"}]
    }
  ]
}
```

### Brief prompt template:
```
SYNTHESIS DOCUMENT:
[FULL CONTENT OF synthesis.md]

---

Write an executive brief of 3,000-3,500 words. Structure:

## TL;DR (100-150 words)
Core problem, proposed solution, single most important takeaway. No hedging.

## The Problem Being Solved (200-300 words)
What is broken, inefficient, or underexploited? Be concrete. Use numbers.
Why now — not in theory, but in this specific context?

## The Recommended Approach (300-400 words)
What to do. Clear enough for a non-expert in 2 minutes.

## Top 10 Findings (250-350 words)
10 numbered findings. Each 2-3 sentences. Concrete and specific.

## Top 5 Actions (Priority Order) (500-600 words)
5 sequenced actions. For each: what, why, effort estimate, expected outcome.

## Top 3 Risks (150-200 words)
Top 3 failure modes. Direct. No softening.

## If You Do Nothing (50-75 words)
What happens in 6 months? Make it real.
```

### Cron 4 — Stage 4 Poller
See **Cron Poller Pattern** section below.
When Stage 4 completes:
1. Save `brief.md`
2. Generate `brief.docx` from `brief.md` (use your environment's markdown-to-docx converter)
3. Update `pipeline-state.json` → `{"stage": "complete", ...}`
4. Self-delete cron
5. Deliver `brief.docx` via your configured channel (Telegram, Discord, email, etc.)

---

## Batch Submission

This skill assumes you have a way to submit Anthropic Batch API jobs and poll for results.
The job JSON format above is compatible with the OpenClaw batch infrastructure.

If you're using OpenClaw's built-in batch system:
```bash
python3 /path/to/batch-worker.py submit --job-file stage2-job.json
python3 /path/to/batch-worker.py poll
```

If not, implement equivalent: POST to `https://api.anthropic.com/v1/messages/batches`, poll until `processing_status == "ended"`, fetch JSONL results.

JSONL result format:
```jsonl
{"custom_id": "s01", "result": {"type": "succeeded", "message": {"content": [{"type": "text", "text": "..."}]}}}
```
Extract text via: `result.message.content[0].text`

---

## Cron Poller Pattern (Mandatory for all stages)

Every stage uses an **idempotent, self-terminating** cron poller.

### Two-step cron creation:
1. Create cron with `CRON_ID=PENDING` in payload
2. Immediately `cron update` with actual cron ID injected into payload

### Poller payload — exact 9-step sequence:

```
You are a superthink pipeline poller. Run these steps exactly.

━━━ STEP 0 — IDEMPOTENCY GUARD (always first) ━━━
Read: /data/superthink/[SLUG]/pipeline-state.json
If "stage" field is NOT "[CURRENT_STAGE]" → EXIT immediately. Do nothing.

━━━ STEP 1 — CHECK LOCAL STATE ━━━
Read: /data/batch-jobs/[JOB_ID]/state.json
If status == "complete" AND [OUTPUT_FLAG] == true → skip to STEP 4.
If status == "complete" AND [OUTPUT_FLAG] == false → go to STEP 3.
If status == "processing" or "pending" → go to STEP 2.

━━━ STEP 2 — POLL BATCH ━━━
Run your batch poll command.
Re-read state.json. If still not complete → EXIT silently.

━━━ STEP 3 — EXTRACT OUTPUT ━━━
Read results file (JSONL). Extract text from each result.
Write output files to /data/superthink/[SLUG]/.
Mark [OUTPUT_FLAG] = true in state.json.

━━━ STEP 4 — WRITE IDEMPOTENCY FLAG ━━━
Write pipeline-state.json: {"stage": "[NEXT_STAGE]-pending", ...}
Do this BEFORE submitting the next batch.

━━━ STEP 5 — BUILD + SUBMIT NEXT STAGE ━━━
Check if [NEXT_JOB_FILE].json already exists — if so, skip building.
Submit batch. Capture Job ID + Batch ID.

━━━ STEP 6 — UPDATE PIPELINE STATE ━━━
Write pipeline-state.json: {"stage": "[NEXT_STAGE]", "job_id": "...", ...}

━━━ STEP 7 — SELF-DELETE THIS CRON ━━━
Call: cron action=remove jobId=[CRON_ID]
Cron ID: [CRON_ID]

━━━ STEP 8 — CREATE NEXT CRON ━━━
Create poller cron for stage [NEXT_STAGE].
Immediately update it with its own ID.

━━━ STEP 9 — NOTIFY ━━━
Send completion message via your configured channel.
```

### Invariants:
- `pipeline-state.json` stage transition written **before** next batch submission — always
- `pipeline-state.json` checked as **STEP 0** — hard gate on exact stage string
- `state.json status == "complete"` verified before touching the API
- Job file never rebuilt if it already exists on disk
- Cron always self-deletes — if it fails, notify user with the cron ID to remove manually

---

## pipeline-state.json Schema

```json
{
  "stage": "2 | 3-pending | 3 | 4-pending | 4 | complete",
  "slug": "topic-slug",
  "topic": "Full topic name",
  "created_at": "ISO timestamp",
  "stage2_job_id": "...",
  "stage2_batch_id": "...",
  "stage2_complete": true,
  "stage2_sections": 11,
  "stage2_completed_at": "...",
  "stage3_job_id": "...",
  "stage3_batch_id": "...",
  "stage3_complete": true,
  "stage3_word_count": 52000,
  "stage3_completed_at": "...",
  "stage4_job_id": "...",
  "stage4_batch_id": "...",
  "stage4_complete": true,
  "stage4_word_count": 3200,
  "completed_at": "...",
  "last_error": "..."
}
```

---

## Token & Cost Reference

| Stage | Requests | max_tokens out | Est. input tokens | Est. cost (batch discount) |
|---|---|---|---|---|
| 1 | 1 | 12,000 | ~3,000 | ~$1.50 (realtime) |
| 2 | 10-12 | 24,000 each | ~15,000 each | ~$8-12 |
| 3 | 1 | 60,000 | ~180,000 | ~$4-6 |
| 4 | 1 | 4,000 | ~80,000 | ~$1-2 |
| **Total** | | | | **~$15-22/run** |

Batch discount (50%) applies to stages 2-4. Stage 1 is realtime.

---

## Error Handling

- Any batch failure → notify user immediately with stage + error message
- Stage 2 partial failure → notify, ask whether to retry failed sections or proceed
- Never silently swallow errors
- Save all partial results even on failure — work is never lost
- All errors written to `pipeline-state.json` → `last_error` field

---

## Notes

- `/superthink` is for deep foundation work — not quick lookups
- Full pipeline: up to 12 hours end-to-end (dominated by batch queue times)
- The `.docx` is the primary deliverable
- Update your memory/notes after each run with topic slug + date + key findings

---

## Supporting Scripts

This skill requires two supporting scripts. Spec files are included in `scripts/` — have your AI implement them for your environment before running the pipeline.

### `scripts/batch-worker-spec.md` → implement as `batch-worker.py`
Handles Anthropic Batch API submission, polling, and result fetching.
- `submit` — send a batch job, save state locally
- `poll` — check pending jobs, download results when done, notify user
- `status` — print a summary table of all jobs
- stdlib only (no third-party packages except your notification layer)
- See spec for full API call sequences, storage layout, and state.json schema

### `scripts/md2docx-spec.md` → implement as `md2docx.py`
Converts Markdown to .docx — used to generate the final executive brief.
- Requires: `pip install python-docx`
- Handles all superthink output elements: H1-H4, bold/italic/code, bullets, numbered lists, code blocks, horizontal rules
- See spec for exact styling, colours, fonts, and parsing logic

**First-time setup:**
1. Read `scripts/batch-worker-spec.md` → implement `batch-worker.py` in your workspace
2. Read `scripts/md2docx-spec.md` → implement `md2docx.py` in your workspace
3. Install python-docx: `pip install python-docx`
4. Update the `Batch Submission` section paths above to match where you saved the scripts
5. Run `/superthink` — the skill handles the rest
