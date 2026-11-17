# The ten-stage prompt library

Source: "The call-prep route: ten moves before you dial" (Inference Drift, Eric Gonzalez).
Work top to bottom. Each stage feeds the next. Placeholders in [brackets] come from the intake
(company, contact, solution, deal type) and from earlier stages.

## THE STOP RULE (applies to every stage)

If a source is gated, missing, or unverifiable, SAY SO in the brief and add an entry to `gaps[]`
with an "ask" telling the rep exactly what to paste. A gap the rep can see beats a guess they can't.
Never fill a gap with a plausible-sounding guess: no invented names, quotes, prices, or numbers.

Tagging: every claim gets `"tag": "sourced"` (a specific source says it, listed in `sources[]`)
or `"tag": "inferred"` (your reasoning from sourced facts; say so). Never present inference as fact.

---

## A. Know the account

### 01 One-page account brief  ->  `s1_account_brief`
Prompt: Summarize [company] on one page from their site, news and press releases: business,
customers, current priorities.
Fallback: Can't reach a source? Say so and ask the rep to paste it.
Done = 2 short summary paragraphs, business, customers, 3 priorities, and 3-5 dated "recent changes"
(each with a source id). Prefer items from the last 6 months. Date-stamp every change.

### 02 Pain from earnings calls  ->  `s2_pain_points`
Prompt: From the latest earnings call for [company], find 3 challenges that [my solution] could
address. Attach the exact wording.
Fallback: No transcript? Tell the rep and ask what to use instead (10-K risk factors, investor
letter, CEO interviews, funding announcements for private companies).
Done = exactly 3 challenges, each with a SHORT verbatim quote (at most two sentences), speaker,
call name/date, and one line on where the solution fits. Quotes must be exact. If you cannot get
exact wording, omit the quote and tag the challenge "inferred". Private company: say so, use the
substitute source, and record the substitution in `gaps[]`.

### 03 Your contact's role  ->  `s3_contact`
Prompt: What does a [title] like [name] care about right now? Use their posts and open roles on
their team.
Fallback: Profile locked? Ask the rep to paste it.
Done = 3 things the role cares about, with evidence (public posts, talks, open roles, company
announcements). LinkedIn is usually gated: do not attempt to bypass it; record a gap and ask.
No contact given: describe the likely buyer role for the deal type and tag everything "inferred".

## B. Shape the conversation

### 04 Discovery questions  ->  `s4_discovery`
Prompt: Using the brief, write 5 open questions for [name]'s role and industry, each with one
follow-up.
Fallback: Missing the rep's discovery framework? Ask first (see seller profile).
Done = exactly 5 open questions (no yes/no), each with one follow-up and a one-line "why this"
that traces back to a specific finding from stages 01-03. If the seller profile defines a
framework (MEDDICC, SPICED, etc.), map questions to it.

### 05 A specific opener  ->  `s5_opener`
Prompt: Write a two-sentence opener that references one real, recent thing from [name] or
[company].
Fallback: Can't see their posts? Ask the rep to paste them.
Done = exactly two sentences, one real dated anchor with a source id. No flattery, no "hope you're
well". If no recent anchor exists, say so and anchor on the strongest sourced item from stage 01.

## C. Map the deal

### 06 Buying committee  ->  `s6_committee`
Prompt: For a [deal type] at [company], list likely roles on the committee and how each will judge
us, with names where public.
Fallback: Names unverified? Ask the rep to confirm them.
Done = 4-6 roles (decision-maker, champion candidate, influencer, blocker risk). Names only when a
public source names them; otherwise "Not identified". `verified: true` only with a source.

### 07 Likely objections  ->  `s7_objections`
Prompt: Based on what buyers say about [my product], give the top 3 objections and how I should
respond to each.
Fallback: Need the rep's pricing or lost-deal notes? Ask.
Done = exactly 3 objections with a response and the basis (review sites, forums, seller profile,
account facts). Tag inferred vs sourced. Do not invent buyer quotes.

### 08 Competitor landscape  ->  `s8_competitors`
Prompt: Which 2-3 competitors is [company] likely weighing against [my solution]? Compare pricing
and positioning; highlight gaps.
Fallback: Source gated? Ask the rep to paste it.
Done = 2-3 competitors (the status quo counts as one) with positioning, pricing, and gaps. If
pricing is not public write "Not public" and never estimate. Cite each.

### 09 Objections battle card  ->  `s9_battlecard`
Prompt: Build a battle card for [name] at [company]: the 5 objections most likely to come up, each
with the real concern behind it, my response, one proof point and a question to ask back.
Fallback: Need the rep's pricing, case studies or lost-deal notes? Ask me first.
Done = exactly 5 objections, each with real_concern, response, proof_point, question_back. Proof
points come ONLY from the seller profile or from sourced material. If none exist, write
"Needs rep input: <what>" and add a gap. Never invent customer results.
Optional: set `meta.practice_note` if the seller profile names a practice tool.

## D. Follow through

### 10 Custom follow-up plan  ->  `s10_followup`
Prompt: From everything above, draft a follow-up email and 3 value-adding touches tied to
[company]'s priorities.
Fallback: Anything missing? Ask before you write.
Done = one email (subject + body, under 120 words, one clear ask) and exactly 3 touches with
timing, channel, content, and which finding each is tied to. Drafts only: never send anything.

---

## Snapshot (written LAST, shown FIRST)  ->  `snapshot.takeaways`
3-5 one-sentence takeaways: the things most likely to change how the call goes (a priority, a
risk, a blocker, an opener). Each must trace to a stage above.
