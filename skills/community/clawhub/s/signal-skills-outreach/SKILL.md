---
name: signal-outreach
description: Turn a signal-scout prospect report into the right next action per prospect type — outreach sequences for Individuals, content/GTM briefs for Segments, BD pitch one-pagers for Companies. Use after signal-scout produces its report, or when you already have a qualified prospect list. Never sends anything automatically.
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/signal-skills
    requires:
      bins: [python3]
---

# Signal Outreach

Take the prospect data from `signal-scout` and turn each one into the right next action: an outreach sequence for an Individual, a content/GTM brief for a Segment, or a BD pitch one-pager for a Company. Never send anything automatically.

This skill is the natural companion to `signal-scout`. Use it after signal-scout produces its report, or standalone when you already have a qualified prospect list.

Read [references/outreach-framework.md](references/outreach-framework.md) before writing any output.

## When to use

- After `signal-scout` produces a report and you want ready-to-send outreach, content briefs, or BD pitches.
- When you have a list of prospects with public signals and want personalized next actions.
- When you want A/B variants of an Individual's first touch to test which angle resonates.
- When you need follow-up sequences beyond the first message.
- When you want channel-specific outreach (email, LinkedIn, Twitter/X, community reply).

## Research Tools

- **`webfetch`** — re-read the prospect's source page to extract fresh personalization details.
- **`websearch`** — look for additional public context about the prospect (recent posts, company news).
- **`bash`** — to run `scripts/generate_outreach.py` for the formatted output package.

## Input

This skill accepts either:

1. **A signal-scout report JSON** — the `analysis.json` produced by signal-scout, with its `individuals`, `segments`, and `companies` arrays.
2. **A manual prospect list** — JSON matching one of the three prospect schemas in signal-scout's SKILL.md.

If a manual entry has no `type` field, default it to **Individual** — that's signal-outreach's original schema and the safest assumption for an untagged, one-off entry. Still route Segment- or Company-shaped entries (recognizable by fields like `content_angle` or `execution_path`) to their correct workflow even if `type` is missing.

If nothing is provided, ask the user for a product description and at least one prospect name or URL.

## Workflow

### 1. Load prospect data

- Read the signal-scout report or manual prospect list.
- Group prospects by type: Individual, Segment, Company.
- For Individuals, extract: name, stage, score, pain signal, source URL, source type, suggested channel, opener, follow-up sequence.
- For Segments, extract: name, stage, score, pain signal, content angle, target keywords, suggested channels, proof points.
- For Companies, extract: name, role, stage, score, pain signal, execution path, contact path, BD angle, what to propose.
- Re-fetch the source URL with `webfetch` to pull fresh personalization signals (recent activity, tone, specific language they use) — for all three types, not just Individuals.

### 2. Individuals — select channels and write the sequence

Not every prospect belongs on every channel. Match channel to source type:

| Source type | Primary channel | Backup channel |
|---|---|---|
| Forum post | Reply in-thread | Email (if visible) |
| Twitter/X post | Reply or DM | Email |
| LinkedIn post | Connection + message | InMail |
| GitHub issue | Comment on issue | Email via profile |
| Product review | Email (if contactable) | Social reply |
| Company page | Email to role | LinkedIn |
| Community post | Community reply | Email |
| Job post | Email to hiring manager | LinkedIn |

If the source doesn't suggest a channel, default to email with a LinkedIn backup. If signal-scout marked the Individual as having no public reply/DM channel, do not invent one — drop them from this workflow and say so.

For each Individual, write:

1. **First touch** — grounded in the specific public signal. Under 90 words. One question at the end.
2. **Follow-up 1** (Day 3) — adds a new angle: a relevant insight, a data point, or a brief case study. Under 70 words.
3. **Follow-up 2** (Day 7) — offers something of value with no ask: a relevant article, a template, a benchmark. Under 60 words.
4. **Breakup** (Day 14) — graceful close. Acknowledge they're busy, leave the door open. Under 40 words.

**Personalization rules:**
- Reference the exact public signal by name or topic (not "your recent post" — name the topic).
- Mirror their language style: if they write casually, write casually. If formal, match.
- Never mention that you found them via research. The message should feel natural, like you stumbled into their world.
- Never reference the AI, the research process, or the scoring framework.
- One specific detail from their public content in every touch.

**A/B variants** for the first touch:
- **Variant A (direct)**: Leads with the pain signal, connects to the product immediately.
- **Variant B (curiosity)**: Asks a question about their situation, reveals the product only if they engage.

Recommend a variant per stage: High intent -> A, Problem aware -> B, Trigger present -> A, Potential fit -> B.

### 3. Segments — write the content/GTM brief

A Segment doesn't get a message, it gets a brief a marketer or founder can execute against. For each Segment, write:

- **Angle type** — searchable (captures existing demand) or shareable (creates demand), per signal-scout's classification.
- **Content plan** — 2-3 concrete pieces (e.g., "comparison page: [Product] vs. [Competitor]," "use-case landing page for [job]," "one data-driven blog post on [insight]"), each tagged with the buyer-journey stage it targets.
- **Keywords** — the target keywords from signal-scout, plus any additional long-tail variants found during research, in the segment's own language.
- **Channel plan** — where to publish or promote each piece (SEO/blog, ASO copy, a named subreddit or community, YouTube comparison videos, a specific newsletter).
- **Proof points to use** — the evidence-backed claims from signal-scout, ready to drop into copy.

No opener, no follow-up sequence, no A/B variants — a Segment brief is a plan, not a conversation.

### 4. Companies — write the BD pitch one-pager

A Company doesn't get a drip sequence, it gets a single, specific ask. For each Company, write:

- **Pitch** — one paragraph, under 90 words, stating the combined value proposition and the one specific ask (a self-serve signup, a named program application, a specific intro request). No generic "let's explore synergies."
- **Execution path** — restate honestly from signal-scout: self-serve program, warm BD via a known partnerships function, or cold BD into an org with no visible partner motion.
- **Contact path** — the public contact path only (developer platform docs, partnerships page, published BD contact form). Never a named executive's personal or scraped email, never a gatekeeper/assistant cold-email.
- **Fallback ask** — if the primary ask goes nowhere, a smaller secondary ask (e.g., a newsletter mention instead of a full partnership).

No A/B variants, no multi-touch drip — one pitch, one clear next step.

### 5. Package the output

Produce a JSON artifact and optionally an HTML report. Each top-level array is optional — include only the types present in the input, and omit an array entirely rather than emitting it empty:

```json
{
  "product": "string",
  "generated_at": "string — ISO date",
  "channel_breakdown": {
    "email": "number",
    "linkedin": "number",
    "twitter": "number",
    "community": "number",
    "github": "number"
  },
  "sequences": [
    {
      "prospect_name": "string",
      "prospect_score": "number",
      "primary_channel": "string",
      "backup_channel": "string",
      "variant_recommended": "A | B",
      "touches": [
        {
          "step": "number",
          "day": "number — days from first touch",
          "channel": "string",
          "subject": "string — for email; null for non-email",
          "body": "string — the message",
          "variant": "A | B | null — null for follow-ups (no variants)",
          "personalization_notes": "string — what was referenced and why"
        }
      ],
      "response_handling": {
        "positive_reply": "string — what to send next",
        "question_reply": "string — how to answer common questions",
        "no_reply_after_sequence": "string — what to do after the breakup"
      }
    }
  ],
  "segment_briefs": [
    {
      "segment_name": "string",
      "segment_score": "number",
      "angle_type": "Searchable | Shareable | Both",
      "content_plan": [
        { "piece": "string", "buyer_stage": "Awareness | Consideration | Decision", "format": "string" }
      ],
      "keywords": ["string"],
      "channel_plan": ["string"],
      "proof_points": ["string"]
    }
  ],
  "company_pitches": [
    {
      "company_name": "string",
      "company_score": "number",
      "role": "string",
      "pitch": "string — under 90 words",
      "execution_path": "string",
      "contact_path": "string",
      "fallback_ask": "string"
    }
  ],
  "general_notes": "string — cross-prospect observations"
}
```

Save to `outreach-package.json` and run:

```bash
python3 <skill_dir>/scripts/generate_outreach.py outreach-package.json outputs/signal-outreach-report.html
```

Return a clickable absolute file link.

### 6. Response handling playbook (Individuals and Companies only)

For each Individual sequence, include:

- **Positive reply**: What to say next. Suggest a 15-minute call. Provide a scheduling link template.
- **Question reply**: Answers to the 3 most likely questions ("what is this?", "how much?", "is this relevant to X?").
- **Objection reply**: Handle the top 2 objections for the product type (too expensive, already have a solution, not the right time).
- **No reply after sequence**: Do not re-engage for 90 days. Suggest alternative touchpoints (comment on their content, attend their event, share relevant content publicly).

For each Company pitch, include a lighter version: what a positive reply leads to next, and what to do if there's no reply after 30 days (try the fallback ask once, then stop).

Segments don't need response handling — there's no message to reply to.

## Modes

- **quick**: Individuals get first-touch only; Segments and Companies get a one-line angle only. Up to 5 prospects total.
- **standard**: Full 4-touch Individual sequences, full Segment briefs, full Company pitches, up to 10 prospects total. Default.
- **deep**: Everything in standard, plus A/B variants and response playbooks, up to 20 prospects total.
- **channel-focus**: Individuals only, for one channel (specify: email, linkedin, twitter, community, github). Skips Segments and Companies.

Use `standard` by default.

## Quality bar

- Every Individual message references a specific public signal — no generic outreach.
- Every Individual sequence has at least 3 touches.
- A/B variants are meaningfully different (not just reworded).
- Tone matches the prospect's public communication style.
- No message claims to have been sent.
- No message includes private information not publicly visible.
- Response handling covers positive, question, and no-reply scenarios for Individuals; positive/no-reply for Companies.
- The breakup message is genuinely graceful — no guilt, no pressure.
- Every Segment brief names concrete content pieces and channels — not "write some blog posts."
- Every Company pitch has one specific ask under 90 words and uses only a public contact path — never a scraped or personal executive email.
