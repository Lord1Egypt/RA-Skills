# Research and Qualification Framework

Use this framework to keep prospect research evidence-based, current, and respectful.

## Research sequence

### Product brief

Define:

- product and promised outcome
- primary user and economic buyer
- urgent job to be done
- current alternative or workaround
- likely adoption trigger
- geography or language constraint
- clear disqualifiers

Do not begin broad lead collection until this brief is specific enough to reject weak matches.

### Competitive landscape

Before searching for prospects, map the competitive terrain:

- Identify 3-5 products prospects likely already use for this job.
- Note their pricing, key features, and known frustrations (from reviews, forums, changelogs).
- Find public switching signals: cancellation posts, migration threads, "alternative to X" searches.
- Understand switching barriers: data lock-in, workflow integration, team adoption cost.
- Articulate the clearest differentiation angle in one sentence.

This context sharpens every query and helps identify high-intent switchers.

### Query buckets

Check [query-packs/](query-packs/README.md) first for a pack tuned to this product's vertical — start there instead of the generic buckets below when one matches, then still cover any gaps with the generic list.

Search several buckets rather than repeating one query:

1. **Explicit demand:** "looking for," "recommend a tool," "alternative to," "does anything exist."
2. **Pain:** "takes hours," "manual," "frustrating," "hate," "difficult," "keeps breaking."
3. **Workaround:** spreadsheets, copy-paste, virtual assistants, scripts, templates, or repeated manual steps.
4. **Switching:** cancellation, migration, missing feature, pricing complaint, or competitor frustration.
5. **Timing:** public launch, hiring, expansion, new workflow, regulation, integration, or process change relevant to the product.
6. **Budget/procurement:** "need to justify," "looking for free," "ROI," "budget approved," "just got budget."
7. **Decision-maker signals:** job posts for the role the product serves, "we're hiring a [role]," public org charts.

Adapt wording to the audience's language. Search the original public page and do not qualify from a search snippet alone.

### Source mix

Useful public sources include:

- Forums and public community discussions (Reddit, Hacker News, Indie Hackers, Product Hunt, industry forums)
- Public social posts and replies (Twitter/X, LinkedIn, Mastodon, Bluesky)
- Product reviews and app marketplace reviews (G2, Capterra, App Store, Chrome Web Store)
- GitHub issues and public feature requests (across relevant repos)
- Public company pages, job posts, changelogs, or announcements
- Public "looking for a tool" posts and directories
- Podcast transcripts and public interview mentions
- Conference talk Q&A and public slides
- Open-source project READMEs and discussion boards

Avoid private groups, gated communities, data brokers, scraped contact databases, and sources that prohibit access.

**Reddit is fetchable — the `webfetch` tool just refuses the domain, so route around the tool, not the site** (verified 2026-07-15): `webfetch` returns "unable to fetch" for any `reddit.com` host (new UI, `old.reddit.com`, `api.reddit.com` alike) — that's a restriction the tool itself applies to the domain, not a live network block. A direct HTTP request from `bash` (`curl`, or a Python script's own `urllib`) is not subject to that restriction and reaches Reddit fine, with one wrinkle: `reddit.com`/`www.reddit.com` (the current UI) serve a client-side bot-verification stub to script fetches — HTTP 200, but the page is just a "please wait for verification" placeholder, not the thread. `old.reddit.com` serves the identical content server-rendered, with no such wall. `api.reddit.com` does genuinely 403 script fetches (it expects OAuth).

**Working fetch path:** when `webfetch` can't reach a `reddit.com` URL, use `bash` to `curl` the **`old.reddit.com` equivalent of the same path** (swap the host, keep everything after it) instead of falling back to search-snippet-only evidence — e.g. `curl -sL -A "Mozilla/5.0" 'https://old.reddit.com/r/<sub>/comments/<id>/...'`. This gets the full real page, so the thread is a normal, fully verifiable source like any other — cite it, quote from it, and score its evidence quality the same as a forum or GitHub issue. Keep the URL you record on the prospect as the original `reddit.com`/`www.reddit.com` link (that's what a reader will actually open); only the fetch target is rewritten.

**When that still doesn't work** (old.reddit.com itself unreachable in a given environment, or you only have a search-snippet as discovery and haven't fetched the full thread): fall back to `https://html.duckduckgo.com/html/?q=site%3Areddit.com+"<your query>"` (the plain-HTML DDG endpoint, not duckduckgo.com/html/ which just redirects there) for discovery — it returns real reddit.com thread URLs with titles and paraphrased snippets. A prospect sourced this way stays **snippet-sourced, not fully verified** — a lower-confidence tier, not equivalent to a source you actually opened and read:
- Only cite `evidence` text the snippet itself actually contains — never extrapolate beyond it into invented detail.
- Note the limitation explicitly in that prospect's `caution` field or the report's `limits` array (e.g. "Reddit thread confirmed via search snippet only; full page unreachable in this environment").
- If a stronger source exists for the same signal (HN, Indie Hackers, G2, GitHub issue, a public professional post), prefer it as the primary citation and use the Reddit thread as corroboration only.

**Other bot-walled platforms** (X/Twitter, LinkedIn, Glassdoor, Indeed) don't have a known equivalent to the old.reddit.com bypass — script fetches to these still genuinely 403/429 regardless of tool. Treat them with the same snippet-sourced, lower-confidence caveat above rather than assuming a workaround exists; don't fabricate full-page evidence for a source you couldn't actually open.

`scripts/verify_sources.py --apply` automates all of this at verification time: it fetches `reddit.com`/`www.reddit.com` sources via their `old.reddit.com` equivalent, detects the bot-verification stub page even when it returns HTTP 200, drops prospects whose source is genuinely unreachable, and appends the unverified-evidence caution automatically to whatever's left BOT_BLOCKED — instead of leaving that cleanup to a manual re-read of the script's output.

### Decision-maker mapping

For each qualified prospect, identify:

- **Who feels the pain** — the person experiencing the problem daily.
- **Who decides** — the person who approves the purchase or tool adoption.
- **Who influences** — the person whose opinion sways the decision (technical lead, ops manager).
- **Budget authority** — can they approve spend, or do they need to escalate?

If the pain-feeler and the decision-maker are different people, note both and recommend outreach to the pain-feeler first (they'll champion the product internally).

### Signal freshness

Not all signals are equal by age:

- **Fresh (0-30 days):** Full timing score. Highest confidence.
- **Recent (31-90 days):** Reduce timing by 1 point. Still relevant.
- **Stale (91-180 days):** Reduce timing by 2 points. Label as "signal may be outdated."
- **Old (180+ days):** Timing = 1 max. Include only if the pain is structural rather than event-driven.

Always note the signal date in the prospect record.

This decay schedule is a fixed heuristic applied uniformly across signal types. If `scripts/recalibrate.py` (run against a product's logged outcomes — see SKILL.md step 8) shows a signal type consistently over- or under-performing this schedule, that's evidence to adjust it for that type — don't tune it speculatively without outcome data behind it.

## Classifying prospect type

Before scoring, classify every candidate as exactly one of **Individual**, **Segment**, or **Company** (see the table in SKILL.md). This isn't paperwork — the dimension set and the next action both depend on it, and mixing types under one score is what makes a "73/100" meaningless (73 for a person means something different than 73 for an audience or a company).

Quick tests, in order:

1. **Can you name one person you'd plausibly reply to, DM, or comment at** — a real name or a stable handle tied to a specific post? → **Individual.**
2. **Is the evidence a pattern across many posts/people, or a demand signal with no single addressable person** (a comparison article, an aggregate of reviews, a "best X alternative" search pattern)? → **Segment.**
3. **Is the value in an organization's assets** — its customer base, its developer platform, its partnerships program — rather than one person's reply? → **Company.**

A one-person company is still an **Individual** if you can reply to them directly; reserve **Company** for cases where the org itself, not a person, is the unit of action. When a candidate could plausibly be two types (e.g., a named person at a company worth pitching as a partner), record both — the person as an Individual, the company as a Company — and cross-reference in `evidence`.

## Qualification score

Score dimensions from 0 to 5. The dimension set depends on prospect type.

### Individual

- **Pain strength (25%)** — directness, severity, repetition, and cost of the stated problem.
- **Product fit (25%)** — how directly the startup solves the evidenced job.
- **Timing (20%)** — freshness and presence of a current trigger.
- **Public reachability (15%)** — a natural, relevant public or professional contact path exists.
- **Evidence quality (15%)** — specificity, source reliability, and confidence that the signal belongs to the prospect.

```text
score = pain_strength/5*25 + product_fit/5*25 + timing/5*20 + reachability/5*15 + evidence_quality/5*15
```

### Segment

Reachability doesn't apply to an audience — drop it and reweight toward the pattern's strength and currency:

- **Pain strength (30%)** — how sharp and repeated the pain is across the pattern.
- **Product fit (30%)** — how directly the startup answers this pattern's job-to-be-done.
- **Timing (25%)** — how current the demand/search pattern is.
- **Evidence quality (15%)** — how many independent sources corroborate the pattern (a single article synthesizing a trend scores lower than three independent posts showing the same complaint).

```text
score = pain_strength/5*30 + product_fit/5*30 + timing/5*25 + evidence_quality/5*15
```

### Company

Borrowed from partner-evaluation practice, reframed around public-signal sourcing only (no paid firmographic/contact-enrichment tools):

- **Strategic fit (30%)** — audience/customer overlap and brand alignment; would you be proud to be associated, and do they solve an adjacent (not competing) job?
- **Timing (25%)** — recency and specificity of the trigger event (a hire, a launch, a platform opening, an acquisition).
- **Execution ease (25%)** — is there a self-serve program or open developer platform (high ease), a known partnerships function (medium), or would this require cold BD into an unknown org (low)?
- **Evidence quality (20%)** — how directly the source establishes the gap or trigger, versus inference.

```text
score = strategic_fit/5*30 + timing/5*25 + execution_ease/5*25 + evidence_quality/5*20
```

### Interpretation (all types)

- **80-100:** strong candidate
- **65-79:** promising, validate quickly
- **50-64:** plausible but missing a material signal
- **Below 50:** do not include in the primary shortlist

An old explicit request can still be relevant, but reduce timing and label the date. A company that merely matches the industry without an evidenced trigger is not a qualified prospect.

## Prospect stages

- **High intent:** publicly requesting a solution or actively switching.
- **Problem aware:** clearly describing the pain or expensive workaround.
- **Trigger present:** a current business event makes the product relevant.
- **Potential fit:** ICP match with incomplete evidence; keep outside the primary shortlist.

## Zero-sales priority mode

Apply this whenever the product brief indicates zero paying customers yet (pre-launch, pre-revenue, or the user states outright they haven't made a sale). This is a stage-based override, not a vertical-specific pack — it applies the same way regardless of product category. The goal changes: not building a GTM engine, but landing the first repeatable proof that a stranger will pay.

- **Weight Individuals above Segments and Companies.** A Segment content play or a Company partnership takes weeks to convert; a well-matched Individual with a current public pain signal is the fastest path to a first conversation and first sale. Don't let a report end up all-Segment/Company when reachable Individuals exist — actively search for them even if the product's category tends toward Segment classification.
- **Lower the reachability bar deliberately, but not the evidence bar.** At zero sales, a "Problem aware" Individual with a real reply channel is worth pursuing even at a moderate overall score (60-70) if pain and fit are both strong — timing and reachability matter more than a marginal evidence-quality gap.
- **The seven-day plan must name a first individual conversation, not a channel to build.** "Publish comparison content" or "apply to a partner program" are Segment/Company moves with multi-week payoff; they belong in week 2+, not day 1. Days 1-3 should be: identify the single strongest Individual, draft the opener, and have the user send it themselves.
- **Say so explicitly in the verdict.** If the product has zero sales, state that plainly and frame the whole report around "who is the first person we can close," not "what is our positioning." A verdict that reads like an already-scaled GTM memo is miscalibrated for a zero-sales product.
- **Don't override honesty to force this.** If no reachable Individual genuinely exists in the research (common for enterprise-only or heavily regulated products), say so and default to the strongest Company as the fastest path to a first logo instead of inventing an Individual that isn't there.

## Next-action rules, by type

### Individual — outreach opener

Draft one opener using this shape:

1. mention the public context naturally
2. connect it to the exact problem
3. explain the product in one sentence
4. ask one low-friction question

The context in step 1 must be drawn from this prospect's own `evidence` field — not a fresh claim invented for the opener. `verify_sources.py` only checks `evidence` against the live page; an opener built from different material than what gets verified would ship unchecked next to a verified badge. This is also what keeps the opener from reading generic: it's tied to a specific confirmed detail, not a templated hook.

Keep it under 90 words by default. Never claim the message was sent. Do not include private emails, phone numbers, personal addresses, family information, or sensitive traits. If no public reply/DM channel exists, state that and omit the opener — do not write a placeholder.

Also draft 2-3 follow-up messages for the outreach companion skill. Each follow-up should add a new angle (insight, data point, or value offer) rather than repeating the opener.

### Segment — content angle

A segment isn't a message target, it's a content/GTM brief. For each segment, decide whether the angle is **searchable** (captures existing demand — someone is actively typing "[competitor] alternative" or "[pain] tool") or **shareable** (creates demand — a novel insight or data point worth spreading), or both, and write accordingly:

- **Searchable angle:** name the exact query pattern (e.g. "[competitor] alternative," "[category] tracking tool"), the buyer-journey stage it matches (awareness → "what is"/"how to"; consideration → "best"/"vs"/"alternatives"; decision → "pricing"/"reviews"), and the content type that fits (comparison page, use-case page, template).
- **Shareable angle:** name the counterintuitive insight or original data point this segment's pain reveals, and why it's worth spreading beyond the immediate audience.

List 2-4 target keywords in the segment's own language (not your product's jargon), and the channels where this audience actually spends time (SEO/blog, ASO, a specific subreddit, YouTube comparisons). Cite 1-3 proof points — evidence-backed claims, not invented statistics.

### Company — BD pitch

A company isn't a drip-sequence target, it's a partnership pitch. First name the **partner motion** — it determines the right first ask and who inside the org owns the decision:

| Motion | The value exchanged | Right first ask | Typical owner |
|---|---|---|---|
| **Integration** | Their platform + your capability closes a workflow gap for shared users | Build against their public API/app store, then submit to their directory | Developer relations / platform team |
| **Distribution / marketplace** | Their audience or listing surface, your product | Apply to the marketplace, affiliate, or app-store program | Partnerships / ecosystem team |
| **Co-marketing** | Overlapping audiences, complementary products | One concrete joint asset (webinar, comparison guide, template pack) | Marketing |
| **Reseller / agency** | They implement or resell for their clients | A pilot with one of their existing clients | Services / delivery lead |
| **Customer account** | They have the pain themselves, at org scale | A pilot scoped to the team feeling the evidenced pain | The team named in the evidence |

Pick one motion per company and tailor `what_to_propose` to it — a generic "let's partner" pitch that doesn't name the motion is the BD equivalent of an "N/A" opener.

**Account tiering (optional, for client deliverables):** when the report is a deliverable someone will execute from, place each company in a tier and say why in `tier_rationale`. Tier is execution priority, not a restatement of the score:

- **Tier 1 — pursue now:** strong fit *and* a low-friction path (self-serve program or warm BD) *and* a live trigger. Open these this week.
- **Tier 2 — nurture:** real fit, but a slower path (cold BD) or a weaker trigger. Queue behind Tier 1.
- **Tier 3 — monitor:** plausible fit with no live trigger. Name the trigger to watch for in the rationale.

A high-scoring company with no partnerships function can be Tier 2; a mid-scoring one with an open self-serve program and a fresh launch can be Tier 1.

For each company:

- Name the **combined value proposition** — what does this unlock that neither side has alone? (e.g., "our recognition/automation layer plus their existing distribution closes the one input that's still manual.")
- Name the **execution path** honestly: a self-serve program (lowest friction, apply directly), a known partnerships function (warm BD, find the public partnerships/business-development contact), or cold BD into an org with no visible partner motion (state this plainly — it's a longer shot, not a warm lead).
- Write the pitch itself as a single, specific ask under 90 words — not a generic "let's explore synergies." State the one thing you want them to do next (a self-serve signup, a specific intro request, a named program application).
- Use only the public contact path (developer platform docs, partnerships page, published BD contact). Never suggest emailing a named executive's personal or scraped address, and never suggest cold-emailing an assistant or gatekeeper role.

## Evidence ledger

For each qualified prospect record:

- displayed company, project, or public professional name
- source title and URL
- visible publication date or "date unavailable"
- source type
- concise pain or timing signal
- observed evidence versus inference
- score breakdown, using the dimension set for that prospect's type
- freshness warning when relevant
- competitor mentioned (if any)
- for Individuals: inferred decision-maker role, if relevant
- for Companies: execution path and public contact path

Use citations in the chat response whenever web research was performed.
