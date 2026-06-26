# Anti-patterns — humanization gone wrong

This file catalogs failure modes of over-aggressive humanization. The 5-pass
architecture can do real damage if applied without restraint: legitimate
prose gets flattened, registers get violated, factual specificity gets
"detoxified" alongside the slop. These anti-patterns are the guardrails.

**How to use:** before finalizing any rewrite, scan the output against this
list. If you catch yourself doing any of these, undo and revisit Step 0.
Returning the original unchanged is a valid outcome — returning text that's
measurably worse than the input is the failure mode this file exists to
prevent.

## Contents

- AP01: Manufactured imperfections — typos and comma splices as "humanity"
- AP02: Register violations — contractions and casualness in formal text
- AP03: Vocabulary mutilation — replacing legitimate domain terms
- AP04: Performative asymmetry — variation as an end in itself
- AP05: Synonym-cycling backfire — fixing P15 by introducing new variation
- AP06: Voice ventriloquism — opinions the source author didn't have
- AP07: Genre crossover — applying the wrong playbook
- AP08: Stripping the load-bearing word — when AI tells coincide with meaning
- AP09: Em dash purge — over-correcting deliberate authorial style
- AP10: Detoxing specificity — confusing "structured" with "AI"

---

## AP01: Manufactured imperfections

**The temptation:** Insert typos, comma splices, or run-on sentences to make
text "look human."

**Why it fails:** Humans make errors unevenly and unintentionally.
Deliberately introduced errors read as performance, and detectors
increasingly score for them. A document with one weird typo amid otherwise
clean prose is more suspicious than fully edited writing.

**Wrong:**
> The product was launched in march 2024 and it sold well, the team was happy.

**Right:**
> The product launched in March 2024 and beat projections by 30%.

**Rule:** Never insert errors. Humanness comes from specificity and rhythm,
not from sloppiness.

---

## AP02: Register violations

**The temptation:** Force contractions ("can't", "won't"), add casual
qualifiers ("kinda", "I guess"), or inject first-person doubt into prose
written in a formal register.

**Why it fails:** Casual markers in formal prose don't humanize — they look
like someone ran a "make this casual" prompt over the text. Academic,
encyclopedic, and legal writing have legitimate formal registers.

**Wrong (encyclopedia → forced casual):**
> The temple's not really known for its frescoes, but kinda for its
> architecture I guess.

**Right (encyclopedia, register preserved):**
> The temple is known for its octagonal floor plan rather than its frescoes,
> which were added in the 18th century.

**Rule:** Match the source register. Step 0 captures this constraint — honor it.

---

## AP03: Vocabulary mutilation

**The temptation:** When `vocabulary-by-era.md` flags a Tier-1 word, replace
it everywhere — including in technical or academic contexts where the word
is precise.

**Why it fails:** "Underscore" is slop in blog copy and the exact right word
for a typography article. "Robust" is puffery in marketing and a load-bearing
term in statistics ("robust to outliers"). "Comprehensive" is bloated on a
landing page and standard in literature reviews.

**Wrong (statistics paper, replacing domain term):**
> The model achieved strong performance across conditions.

**Right (term of art preserved):**
> The model achieved robust performance across conditions, with effect sizes
> consistent under bootstrap resampling.

**Rule:** Before replacing flagged vocabulary, ask whether the word is doing
domain-specific work. If yes, keep it. The lexicon is a starting point, not
a search-and-replace list.

---

## AP04: Performative asymmetry

**The temptation:** To push burstiness or sentence-length CoV above "human"
thresholds, insert short fragments or abrupt rhythm shifts.

**Why it fails:** Variation should serve content. Manufactured fragments
mid-paragraph confuse the reader and read as "trying to look human."

**Wrong:**
> The team shipped the feature on Friday. Big release. The metrics climbed.
> Adoption. Three percent of users tried it in the first hour.

**Right (variation that serves the content):**
> The team shipped on Friday. Within an hour, 3% of users had tried it —
> well above the 0.5% pre-launch estimate.

**Rule:** Vary length where content benefits. Don't chase metrics for their
own sake.

---

## AP05: Synonym-cycling backfire

**The temptation:** To avoid P15 (elegant variation), generate new noun
variations within the rewrite instead of fixing the root cause ("the model"
→ "the system" → "the framework").

**Why it fails:** You've swapped one elegant-variation instance for another.
The fix is to repeat the word and use pronouns, not to find new dodges.

**Wrong:**
> The model trained on 1M examples. The system converged in 4 hours. This
> framework achieved 94% accuracy.

**Right:**
> The model trained on 1M examples and converged in 4 hours, hitting 94%
> accuracy.

**Rule:** Repetition is fine. Pronouns are fine. Treat synonym suggestions
with suspicion — they're often the same trap dressed up.

---

## AP06: Voice ventriloquism

**The temptation:** Apply Pass 5b ("acknowledge complexity") by adding doubt,
opinion, or evaluation the original author didn't have.

**Why it fails:** Inserting "the data is thin but suggestive" into a
paragraph where the author never hedged changes the claim. The skill's job
is to remove AI residue, not to add your own analytical voice.

**Wrong (added stance not in original):**
> The trial showed a 12% improvement, though I'm not sure the effect will
> generalize.

**Right (no stance added):**
> The trial showed a 12% improvement in the treatment arm.

**Rule:** Sharpen voice the author already had. Never fabricate one. For
encyclopedic and academic prose, Pass 5b is suppressed per the genre playbook.

---

## AP07: Genre crossover

**The temptation:** Apply your default playbook (often blog/journalistic) to
text from a different genre.

**Why it fails:** Each genre has different baselines. A landing page
rewritten with academic neutrality dies on the page. An encyclopedia article
rewritten with op-ed punch becomes original research.

**Rule:** Run Step 0 honestly. Use the genre's actual playbook even if the
text reads "boring" to you. Boring is correct for some genres.

---

## AP08: Stripping the load-bearing word

**The temptation:** A sentence contains a flagged AI word, so cut it. But
the word was the factual core, not the puffery.

**Why it fails:** "The treaty served as the legal basis for the boundary."
"Served as" is on the copula-avoidance list — but here, "is" loses the
historical aspect. The construction is correct.

**Wrong (over-strip):**
> The treaty defined the boundary.  *(loses "legal basis" meaning)*

**Right (preserve load-bearing structure):**
> The treaty was the legal basis for the boundary.

**Rule:** Before stripping, test whether removal changes meaning. If it does,
find a different fix or leave the construction.

---

## AP09: Em dash purge

**The temptation:** After flagging Pass 5f, replace every em dash in the
document with commas or periods.

**Why it fails:** Some authors use em dashes deliberately and frequently
(David Foster Wallace, Emily Dickinson, Nicholson Baker). A source full of
em dashes may be exhibiting style, not AI residue.

**Rule:** Check em dash density and distribution. If they cluster in
parenthetical insertions or voice shifts, they're likely intentional. Cut
only the formulaic "clause-punch" usage. Genre playbooks specify
register-appropriate thresholds.

---

## AP10: Detoxing specificity

**The temptation:** A paragraph is well-structured, properly transitioned,
and uses formal vocabulary. It "feels" AI even without clear pattern hits,
so you restructure it.

**Why it fails:** Clarity and structure are not AI tells. Well-edited human
writing also has topic sentences, formal vocabulary, and logical
transitions. Mistaking competence for AI is the single most damaging
over-correction.

**Wrong (the original was competent human prose):**
Source:
> The committee considered three proposals. The first emphasized cost
> reduction; the second focused on growth; the third sought a middle path.
> The third was adopted in May.

"Humanized":
> They looked at proposals. The first was about cost. Another was about
> growth. The third one — kind of a compromise — got picked.

**Rule:** Pattern density triggers action, not vibes. Step 0's confidence
question (#6) exists for this. If pattern density is low and the text is
specific, light touch or leave alone.

---

## The default disposition

When you can't confidently identify a pattern, do not "fix" it. The
conservative move is correct more often than the aggressive one. The cost of
leaving some AI residue is small; the cost of mutilating human prose or
inserting fabricated voice is much larger and harder to detect downstream.
