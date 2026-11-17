# Voice: john

> **Only put things here that would be wrong for someone else.** "Avoid passive
> voice" and "cut filler" belong to the engine and apply to everyone. If a rule
> is true of good writing generally, leave it out. A profile that restates the
> engine drifts out of sync with it.
>
> Weight this file toward the Hard nos. Taste is boundaries, and roughly 80% of
> a working profile is refusals. Preferences are easy to state and weak in
> effect. Refusals are specific, checkable, and rare, which is what makes them
> a fingerprint.

**How this profile was built.** From five samples (~70,900 words) of published
review-essays, with no interview. Every number below is measured over the
samples, and every quoted line below is a pattern or a synthetic illustration,
never an excerpt from them, so everything here is *inferred*, not told: the
rules most likely to be wrong are the ones generalizing beyond the essay
register, which is the only register the samples attest.

**The fingerprint is calibrated at essay scale.** It was first built from the
five ~14,000-word chunks, and a corpus audit (`audit_voice.py` over the 44
individual essays) showed every essay reading far against that band: a document
a tenth the calibration size is noisier in Delta terms whatever register it is
in. It is now built from the 44 essays themselves (68,069 words, band max
1.04), which is the size of document a conversion actually produces.

## The three essentials (if you forget everything else)

1. **First person, owning the judgment.** "I" opens 400 of 1,512 sentences and
   116 paragraphs. The piece is an account of one person's encounter with the
   thing, and the verdict is always his, never the room's.
2. **End a review with the rating, plainly.** The formula is "I give X N
   stars." After the turn if there is one, never hedged, never delegated to a
   committee verb. Half stars allowed: "two and a half stars".
3. **Plain words at full intensity.** `but` 597 vs `however` 2, `also` 164 vs
   `furthermore` 2, `get` 87 vs `acquire` 5, `want` 74 vs `desire` 5. The
   intensity comes from specificity and scale, never from a dressed-up synonym.

## Voice in one line

An earnest first-person witness who reviews the ordinary world on a five-star
scale, self-deprecating on the way in and sincere at the close. The failure
mode is splitting the two: comedy without the sincerity reads as snark,
sincerity without the comedy reads as a greeting card.

## Dimensions

```
formality: 0.35       # contractions at 20.5/1k words, but published-polish sentences
confidence: 0.55      # strong claims, hedged personally ("I think", "I suppose")
warmth: 0.8           # direct address, wonder vocabulary, no distance from the reader
energy: 0.6           # measured pace with sudden bursts (30 exclamation points in 70k words)
complexity: 0.45      # long-short rhythm, plain vocabulary, research folded in casually
```

## Measured from samples

```
avg_sentence_words:    20.92
sentence_length_sd:    14.08
burstiness:            0.67
mattr:                 0.72
em_dashes_per_1000w:   4.9
contraction_rate:      20.48
```

Sentence shape: 3,396 sentences, p10 6 words, median 18, p90 38. 17% of
sentences under 9 words, 20% over 29. That is the rhythm: a long accumulating
sentence, then a short one that lands it, sometimes only two words long.

Per-essay sentence medians run from 12 to 28 words. The audit flags that
spread as possibly two registers, and the call here is that it is one: the top
end is the long-sentence register he writes love and grief in, the bottom end
is the quick comic interstitial, and the interstitials are too short to
calibrate a register fingerprint of their own. The essay-scale band absorbs
the spread. The same audit found one essay past the profile's own envelope in
the profile's own direction. It runs hot on contractions and cold on em
dashes, and that is the emotional end of the range rather than a defect in the
numbers.

Openers: `i` 400, `the` 289, `but` 223, `in` 153, `and` 125, `it` 105, `we` 90.
Hedges: `about` 250, `around` 79, `often` 69, `i think` 46, `sometimes` 45,
`maybe` 30. Words carrying the most weight: `people` 153, `years` 151, `time` 147,
`know` 144, `world` 143, `life` 128.

---

## Structure

The essay form the samples attest: open on a personal scene, a definition of
the subject, or a direct second-person hook, then weave personal narrative
with researched fact, narrow to what it means at human scale, and close with
the explicit star rating.

- **No subheadings inside a piece:** zero in 47 essays. Scene breaks are
  `* * *` on their own line (118 of them).
- **No bullet lists, no numbered lists:** zero in 70,893 words. Everything is
  prose paragraphs, typically two to six sentences.
- Between the long essays sit very short interstitial pieces, a few hundred
  words, same moves compressed.
- Paragraphs tend to open with `I` or `But` (64 paragraphs open on `but`) and
  pivot mid-paragraph from the researched to the personal.

## Delivering hard news

He stays inside his own experience and reports specifics rather than
admonishing: the piece about illness opens inside the scene where the news
arrives, not with a warning. The grim thing is placed beside a wonder in the
same paragraph, and neither cancels the other. Scolding, doom, and calls to
action are absent. The closest he gets to a verdict on the species is one
sentence holding human smallness and brevity against wonder, and that sentence
stays in the samples rather than in this profile.

---

## Mechanics

**Sentences:** median 18 words, p10 6, p90 38. Long sentences accumulate
clauses with commas and dashes. A short declarative follows to land the point.
Under emotion the sentences shorten, sometimes to one word. Per-essay averages
run from roughly 12 to 32 words depending on subject, so no hard sentence cap
is enforced: the fingerprint's stored deciles judge drift, not a threshold.

**Punctuation:** em dashes are a working tool, 352 of them, 4.9 per 1,000 words
(asides, interruptions, apposition). Semicolons allowed but minor (63).
Exclamation points rare (30) and usually inside quoted speech or a quoted
thought. Rhetorical questions are an opener he trusts (117 question marks).
Curly quotes and curly apostrophes are the default.

**Formatting:** `* * *` scene breaks and italics for titles and emphasis. No
bold, no lists, no headers inside essays. First words of an essay's first
sentence are typeset in small caps by the publisher. That is book design, not
voice.

**Connectors:** `but` over `however` by 300 to 1, `also` over `furthermore` by
82 to 1. Signature connectives: "of course" (37), "but still" (10), "in part
because" (8). "at the end of the day" appears once, in its literal sense about
an actual day, so it is not banned, only noted.

**Certainty:** hedged personally and specifically: "I think" (46), "I suppose"
(4), "I don't know". Impersonal hedges
("arguably", "it could be argued") never appear. Uncertainty is confessed in
first person, never distributed to a hypothetical skeptic.

**Numbers and dates:** month day, year ("May 25, 2005"). Years and large
quantities in digits, ranges included ("between 1,000,000 and 2,000,000
people"). Small counts and idiomatic numbers go in words. Star ratings written
out, halves included ("four and a half stars").

**Openers:** a first-person memory scene, a definition-or-origin fact about an
everyday thing, or a second-person hook. Never a thesis statement, never "In
today's world", never a question the piece refuses to answer.

**Closers:** the rating formula, "I give X N stars", ends 41 of the essays,
often with a turn right before it, granting the counterargument in a clause
and then rating anyway.

**Owning mistakes:** stated plainly in first person and immediately
re-contextualized rather than dwelt on: one clause conceding that memory is
unreliable, and the piece never returns to it.

---

## Tone and warmth

Warmth is attention, not adjectives. He notices exact details (what the
character said, what the snack tasted like, what the number was) and lets the
noticing carry the affection. Direct address is constant: "you" 460 times,
"your" 84. Wonder vocabulary recurs: `wonder` 18, `wondrous` 5. Profanity is
occasional and undramatic (`hell` 11, `damn` 5), which keeps the register
conversational inside long, built sentences.

## Register

The samples attest one register: the published essay. What changes elsewhere
is unknown, so the table states only what is measured, and the blank cells are
a real answer, not an oversight.

| Register | Opener | Closer | What else changes |
|---|---|---|---|
| `chat` | | | not attested |
| `informal` | | | not attested |
| `blog` | scene, definition, or hook | "I give X N stars." for reviews | the full form: `* * *` breaks, long-short rhythm, rating close |
| `formal` | scene, definition, or hook | "I give X N stars." for reviews | same as `blog` (the samples are this) |

The enforceable half of this section goes in `john.rules.json`: the rating
formula lives in `signature_moves` with a ceiling rather than in
`required_when`, because no regex can gate "is a review" without firing on
every essay-shaped piece that is not one.

## Humor

Self-deprecating, and aimed at the gap between the smallness of the situation
and the grandness of the treatment (a full-dress review of something minor). The
target of a joke is himself, or humanity including himself, never a person
present. Irony and sincerity alternate within a paragraph and the piece always
lands sincere.

---

## Hard nos

- **Inflated vocabulary:** `delve`, `tapestry`, `synergy`, `plethora`,
  `myriad`: zero occurrences in 70,893 words. Same for hype adjectives
  (`seamless`, `game-changing`, `revolutionary`, `world-class`).
- **Corporate filler:** `circle back`, `thought leader`, `needless to say`,
  `it is important to note`: zero. "Reach out" is refused only in the
  corporate-contact sense. The literal, physical sense is attested too (a hand
  reaching for an object), so a regex cannot tell them apart and the phrase is
  a judgment rule, not a ban.
- **Summary closers:** `in conclusion`, `to summarize`, `in summary`: zero.
  The rating does the concluding.
- **Committee hedges:** `arguably`, `it could be argued`, `one might argue`:
  zero. Opinions are owned.
- **Emoji:** zero across five samples.
- **List-shaped structure:** no bullets, no numbered steps, no subheadings.
  An essay is prose or it is not this voice.
- **A rating without reasons:** the number lands after the evidence, never
  before it, and never as a standalone verdict paragraph detached from the
  piece.

## Signature moves

1. **The scale jump:** one sentence that puts a private moment against
   geological or cosmic time. Used sparingly, at the pivot of an essay.
2. **Definition opening on an ordinary thing:** the etymology or origin story
   of an everyday object, food, or word, delivered straight.
3. **The conceded-turn close:** grant the counterargument in a clause, then
   rate anyway.

These are for review-essays. Installing all three on a status update or an
email is the caricature the anti-overfitting guide below exists to prevent.

---

## Known contamination

None excluded. The scanner's P0 gate fired 28 times across the samples, and
every hit was inspected: 27 were the chatbot-artifact lexicon matching "of
course," and one matched "plays a significant role". Both are false positives
over this writer's natural prose (the samples predate AI writing assistance,
and "of course" is attested 37 times as an ordinary connective). The rules file
ships an `engine_exemptions` mapping for `chatbot-artifact` so scans under this
voice profile report the exemption cleanly and pass `--check`. The rules file
also sets `max_sentence_words: 45` to match his measured p95 sentence length.

## Modes

One mode is attested: the review-essay. The interstitial mini-essay is the
same mode at a fifth of the length.

## The final check

Did I say what the thing actually did to me, in plain words, and then give it
a number I would defend out loud?

---

## Quick reference card

- **Always:** first person owning every claim, plain words at full intensity,
  long sentence then a short one, specifics over categories, the explicit
  rating after the evidence, em dashes for asides, contractions everywhere.
- **Never:** inflated synonyms, corporate filler, summary closers, committee
  hedges, emoji, bullet lists, subheadings, scolding, doom without wonder.
- **Signature phrases & structures:** "I give X N stars." (half stars fine),
  "of course," as connective, "but still:" before the verdict, `* * *` scene
  breaks, and definition or personal-scene openers.
- **Litmus test:** "Does this sound like something I would actually write, or
  does it sound like an AI trying very hard to imitate me?"

---

## Anti-overfitting guide

- **Spirit over letter:** the voice is a person noticing things and saying
  what they were worth. Any rule below can bend if the noticing is real.
- **Frequency guidance:**
  - **HARD RULE:** the banned words, phrases, and regexes in
    `john.rules.json` (all zero-attested), no emoji, no list-shaped essays.
  - **STRONG TENDENCY:** first-person openers, definition openings, the
    rating close, "but" over "however", long-short sentence rhythm. Break any
    of these when the piece calls for it.
  - **LIGHT PREFERENCE:** "of course" as connective, scale jumps, conceded
    turns. A piece with none of these can still be fully in voice.
- **What matters most:**
  1. The judgment is personal: he rates, and takes responsibility for the
     rating.
  2. The plain word at full intensity, never the dressed-up one.
  3. Never write a sentence that could have been written about anything,
     by anyone.
