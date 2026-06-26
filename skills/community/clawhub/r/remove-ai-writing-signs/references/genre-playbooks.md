# Genre playbooks — calibrating the rewrite to context

The 5-pass architecture is universal. Its aggressiveness is not. The same
sentence can be slop in encyclopedic prose, brand voice in marketing copy,
and authentic style in a personal essay. This file calibrates each pass to
the genre identified in Step 0.

**How to use:** in Step 0, pick a playbook below. While running Passes 1–5,
refer back to the **prioritize**, **tolerate**, and **suppress** notes for
that genre. When in doubt, undertreat — restoring a deleted phrase is harder
than removing one the second time.

## Contents

- **Encyclopedic / reference** — Wikipedia, knowledge-base, glossaries
- **Marketing / landing page** — SaaS, product copy, ad copy, sales emails
- **Academic / scientific** — journal articles, theses, grant applications
- **Blog / op-ed / personal essay** — Substack, opinion columns, newsletters
- **Technical documentation** — API references, READMEs, runbooks, tutorials
- **Fiction / creative** — stories, scripts, poetry, creative nonfiction
- **Cross-cutting notes** — multi-genre documents, author overrides, lexicon interaction

---

## Encyclopedic / reference

**Examples:** Wikipedia articles, internal knowledge-base pages, glossaries,
reference handbooks.

**Voice expectations:** Neutral, third-person, no authorial opinion, no
future speculation, no promotional adjectives, no first-person.

**Prioritize (most common AI failures here):**
- Significance inflation (P05) — "marks a pivotal moment in the evolution
  of" almost always belongs in the bin
- Notability assertion (P09) — listing media outlets without saying what
  they reported
- Promotional language (P10) — "nestled," "vibrant," "renowned" have no
  encyclopedic home
- Trailing -ing analyses (P06) — they fake depth that encyclopedic prose
  shouldn't claim
- Formulaic challenges/future (P07) — encyclopedias describe, they don't
  forecast

**Tolerate (don't strip these reflexively):**
- Passive voice — common and acceptable in reference prose
- Sentence-initial "Also," / "Additionally," in moderation
- Formal copulas if they're factually load-bearing ("Mount Everest stands
  as the tallest peak above sea level" — the "stands" is fine; it's literal)
- Lower burstiness — uniform paragraph length is normal in reference work

**Suppress (do not apply these passes here):**
- Pass 5b "acknowledge complexity" with authorial doubt — encyclopedias
  don't hedge with opinion, they cite or omit
- Pass 5c "vary register" — register should stay flat and neutral
- Pass 5d adding rhetorical asymmetry — section structure should follow
  conventions

**Statistical baselines:**
- Burstiness: 0.30–0.55 acceptable (don't push higher artificially)
- Sentence CoV: 0.30–0.50
- Transition density: low; ~2–4% sentence-initial
- Em dashes: rare, mostly avoided

**Watch for false positives:** Words like "underscore," "intricate," and
"comprehensive" CAN appear here legitimately, but in encyclopedic prose
they're still usually puffery. Lean toward replacing unless the word is
factually load-bearing.

---

## Marketing / landing page

**Examples:** SaaS landing pages, product descriptions, ad copy, brand
announcements, sales emails.

**Voice expectations:** Brand-consistent. Can be upbeat, opinionated, even
promotional — but every claim should be earned by specifics.

**Prioritize:**
- Vague benefit claims ("transform your workflow," "next-level results")
- False specificity ("enterprise-grade," "world-class") without evidence
- Notability flexing without proof
- Rule-of-three triplets ("faster, smarter, simpler")
- "Not just X, it's Y" framing
- Filler phrases inflating short content

**Tolerate:**
- Some "boasts/features/offers" language if the brand voice supports it
- Em dashes used as punch — landing-page copy uses them deliberately
- Sentence fragments for emphasis
- Higher imperative-mood density ("Get started," "See it in action")
- Upbeat register

**Calibration per pass:**
- Pass 3: do not deflate ALL promotional language. Cut only the parts
  unsupported by evidence. "Best-in-class workflow tool" → cut. "Used by
  Stripe and Notion" → keep, that's specific.
- Pass 5: register can stay upbeat. Don't impose neutrality.

**Statistical baselines:**
- Burstiness: 0.50+ (landing pages mix headlines, paragraphs, fragments)
- Sentence CoV: high (0.55+)
- Average sentence length: shorter (~12–18 words)
- Em dashes: more permissive — up to 1 per 200 words if author style fits

**Watch for false positives:** Promotional adjectives are not automatically
AI in marketing copy. The test is whether they're earned by a specific fact
nearby. "World-class engineering team led by ex-Stripe principals" is
acceptable; "world-class team" alone is not.

---

## Academic / scientific

**Examples:** Journal articles, thesis chapters, conference papers,
grant applications, literature reviews.

**Voice expectations:** Formal, third-person, appropriately hedged,
citation-dense. Passive voice common.

**Prioritize:**
- Trailing -ing analyses (P06) that don't add information
- Vague attributions (P08) — "studies show" without citation
- False balance (P23) — inserting "on the other hand" when evidence is
  one-sided
- Notability inflation around author or work
- Stock phrases that survived ESL editing ("plays a crucial role in,"
  "it is worth noting that")

**Tolerate (large false-positive zone):**
- Formal vocabulary: "underscore," "highlight," "robust," "comprehensive,"
  "elucidate," "demonstrate" — all have legitimate academic homes
- Passive voice (10–25% ratio normal in many fields)
- Formal transitions: "Moreover," "Furthermore," "Consequently" — used
  more often than in journalism but appropriate
- Sentence-initial nominalizations
- Longer average sentence length

**Calibration per pass:**
- Pass 2: only flag Tier-1 dead giveaways AND only when clustered. A single
  "underscore" in 800 words of methods section is not a problem.
- Pass 4a: leave sentence rhythm closer to uniform — academic prose CoV is
  legitimately lower than journalism
- Pass 4b: do not force copula restoration in technical descriptions where
  "is" would be imprecise ("the model exhibits convergence" is not "the
  model is convergent")
- Pass 5b–5c: do NOT add casual register or authorial doubt expressions
  that don't belong in the field's conventions

**Statistical baselines:**
- Burstiness: 0.30–0.55
- Sentence CoV: 0.30–0.50
- Passive voice: 15–30% acceptable
- Trigram repetition: methods sections legitimately repeat phrases

**Watch for false positives:** This is the highest-false-positive genre.
Many fields have stylistic conventions that overlap with AI tells. When in
doubt, preserve.

---

## Blog / op-ed / personal essay

**Examples:** Substack posts, opinion columns, personal essays, newsletter
issues, long-form magazine pieces.

**Voice expectations:** First-person allowed and often expected.
Opinionated. Register varies within a piece. Specific lived detail.

**Prioritize:**
- ALL pattern families — this is the genre AI fakes worst
- Generic openers and stale hooks ("In today's fast-paced world...")
- The conclusion that summarizes what was just said
- Fake-vulnerable hedging that's actually filler ("I've been thinking a
  lot about...")
- Stock metaphors ("a journey," "a tapestry," "a dance")

**Tolerate (genre-appropriate):**
- First-person ("I think," "in my experience")
- Sentence fragments for rhythm
- Long-then-short rhythm shifts
- Em dashes if the author actually uses them (verify against any prior work)
- Asymmetric structure — paragraphs of wildly different length

**Calibration per pass:**
- Pass 5: lean in heavily. Add specifics, lived detail, opinions with
  stakes. This is the genre where texture injection matters most.
- Pass 4a: maximum sentence rhythm variation. Target CoV well above 0.5.
- Pass 4d: break triplet patterns aggressively — they're a tell here.
- Pass 5e: kill false balance harder than anywhere else. Op-eds with a
  spine read more human than op-eds that hedge.

**Statistical baselines:**
- Burstiness: 0.60+ expected
- Sentence CoV: 0.55+
- Em dashes: more permissive if author voice supports it
- Transition density: low; transitions should be implicit

**Watch for false positives:** Few. If text feels AI in this genre, it
almost certainly is. The remaining risk is mistaking competent but plain
writing for AI — flag rather than rewrite if you're unsure.

---

## Technical documentation

**Examples:** API references, README files, developer guides, runbooks,
configuration docs, tutorials.

**Voice expectations:** Instructional, often second-person ("you can"),
imperative mood common ("Run the command"), precision over personality.

**Prioritize:**
- Filler phrases ("it is important to note that")
- Vague hedging ("you may want to consider possibly...")
- Redundant overviews and conclusions
- Promotional language ("powerful," "robust," "elegant") — never belongs
  in reference docs even when applied to tools
- "Boasts" / "features" used to describe APIs
- Rule-of-three when not genuinely enumerable

**Tolerate:**
- Lists and tables — appropriate; do not force into prose
- Lower burstiness — consistent structure aids scanning
- Repeated sentence patterns ("To do X, run Y. To do A, run B.")
- Imperative mood throughout
- Code blocks adjacent to short explanatory sentences

**Calibration per pass:**
- Pass 4g (list-to-prose): suppress. Lists are correct here when the
  content is genuinely enumerable.
- Pass 4h (table audit): keep tables that aid lookup, even small ones.
- Pass 5: minimal texture injection. Technical docs should be clear, not
  literary. Don't add asymmetry or authorial voice.
- Pass 5a (specificity): apply hard. "Configure the database" → "Set
  `DB_HOST` and `DB_PORT` in `.env`."

**Statistical baselines:**
- Burstiness: 0.25–0.45 acceptable
- Sentence CoV: 0.30–0.45
- Average sentence length: shorter (12–18 words)
- Em dashes: rare

**Watch for false positives:** Uniformity is a feature here, not a bug.
Don't manufacture variation that hurts scanability.

---

## Fiction / creative

**Examples:** Short stories, novel chapters, poetry, scripts, creative
nonfiction, song lyrics.

**Voice expectations:** Whatever the author chose. Stylistic anomalies are
intentional more often than not.

**Prioritize:**
- Cliché phrases and stock metaphors
- Show-vs-tell failures ("she was sad" instead of behavior)
- Predictable arc beats and resolution
- Workshop-safe "good writing" that sounds like every MFA workshop
- AI-typical sensory clusters ("the sun cast golden light across...")
- Generic dialogue tags and dialogue that all sounds like the same person

**Tolerate (high false-positive zone — possibly the highest):**
- Em dash overuse (could be deliberate style — verify)
- Sentence fragments
- Unconventional grammar
- Repeated words for rhythm
- Long winding sentences without breaks
- First-person idiosyncrasies
- Vocabulary choices that look "AI" but are author signature

**Calibration per pass:**
- Pass 2: almost never apply mechanically. Author word choice may be
  deliberate. Flag suspicious vocabulary; do not auto-replace.
- Pass 4a (rhythm): respect deliberate rhythm. Some authors write
  intentionally metronomic prose for effect.
- Pass 5: minimal. Imposing your aesthetic on an author is worse than
  leaving some AI residue.

**Default disposition:** prefer flagging to rewriting. If you can't
distinguish AI from deliberate authorial style, flag the passage and let
the author decide.

**Statistical baselines:** Highly variable. Defer to author voice rather
than to numerical targets.

**Watch for false positives:** This is the genre where the skill should be
most conservative. Any rewriting should be sentence-level at most, not
structural reconstruction.

---

## Cross-cutting notes

**Multi-genre documents.** A blog post embedding an academic citation, or a
landing page with a technical section, should switch playbook by section.
Run Step 0 separately on each section if they differ materially in genre.

**When the genre is unclear.** Default to the more conservative playbook of
the two candidates. Over-rewriting destroys voice; under-rewriting leaves
some AI residue. The first error is harder to recover from.

**Author overrides.** If the user names a target author or style ("write
like Joan Didion," "match our brand voice doc"), that override beats the
genre playbook. Note the override explicitly in your Step 0 plan.

**Genre-vocabulary interaction.** The `vocabulary-by-era.md` lexicon is
written from an encyclopedic / journalistic baseline. Words it flags as
"dead giveaways" can be legitimate in academic or fiction contexts —
always cross-check against this file before applying Pass 2 mechanically.
