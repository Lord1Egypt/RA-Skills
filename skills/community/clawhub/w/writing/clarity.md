# Clarity — Sentence Surgery and the Readability Math

Scope: the sentence and the paragraph. If the piece's order is wrong, none of this helps (`structure.md`).

**Contents:** [The Two Repairs That Fix Most Sentences](#the-two-repairs-that-fix-most-sentences) · [Topic and Stress Position](#topic-and-stress-position) · [Passive Voice, Correctly](#passive-voice-correctly) · [Cutting Formulas](#cutting-formulas) · [Rhythm](#rhythm) · [Readability Formulas and What They Are For](#readability-formulas-and-what-they-are-for) · [Machine-Written Tells](#machine-written-tells) · [Words That Cost More Than They Pay](#words-that-cost-more-than-they-pay) · [Precision Failures](#precision-failures)

**Before a clarity pass**, read `## Never` in `~/Clawic/data/writing/memory.md` and the `terminology` and `banned` lines of the relevant `style-sheets/<context>.md`. A clarity edit that reintroduces a banned word is worse than no edit: it proves the stored preference is not being read.

## The Two Repairs That Fix Most Sentences

**1. Character in the subject, action in the verb** (Williams). Find who is doing what; make that the grammatical subject and the main verb.

- Before: "The implementation of the new policy resulted in an improvement in response times."
- After: "Support answered faster after the new policy." — 13 words to 7, and now you can see who acted.

**2. Un-nominalise.** A nominalisation is a verb turned into a noun: `make a decision`, `provide support`, `conduct an analysis`, `is a reflection of`. Each one drags in a weak verb and a preposition or two.

- `reach a conclusion` → `conclude` · `perform an evaluation` → `evaluate` · `has a dependency on` → `depends on` · `give consideration to` → `consider`
- Test: scan for `-tion`, `-ment`, `-ance`, `-ity`, `-ness`. If the noun has a verb form and the sentence is limp, the verb form is the sentence.

Applying these two to a bloated paragraph typically removes a fifth of it without touching a single idea — which is where most of the cut target comes from before any content is sacrificed (`revision.md`).

## Topic and Stress Position

Readers place emphasis by position, not by intent (Gopen & Swan).

- **Topic position** (sentence start): what this sentence is *about*. Put old, already-known information here — it is what links the sentence to the last one.
- **Stress position** (sentence end): what the reader will remember. Put the new information, the point, the surprise here.

The known-new chain is why some paragraphs read effortlessly: each sentence starts with something the previous sentence ended on. When a paragraph has to be read twice, check this first — the usual fault is a sentence that opens on new information and buries its point in the middle.

Corollary: never end a sentence on a qualifier ("...in most cases", "...generally"). The stress position is too valuable to spend on a hedge; move it to the front or delete it.

## Passive Voice, Correctly

Passive is a tool, not a fault. Three legitimate uses:

1. The actor is unknown or irrelevant: "The file was corrupted."
2. The receiver is the topic of the paragraph: a paragraph about the invoice says "the invoice was rejected", not "finance rejected the invoice", because the invoice must hold the topic position.
3. Deliberate agent-hiding, when naming the actor would be an accusation you are not making.

The passive worth deleting is the one hiding a responsible actor by accident: "mistakes were made", "it was decided". Fix: name the actor. Hunting every passive produces awkward prose and marks the editor as mechanical (SKILL.md Traps).

Test before deleting a passive: can you add "by zombies" and have it still make sense? That only tells you it *is* passive. The real question is whether the actor matters here — if it does not, leave it.

## Cutting Formulas

Predictable phrases with a shorter exact equivalent. These are safe to apply mechanically because they never change meaning.

| Phrase | Replacement |
|---|---|
| `in order to` | `to` |
| `due to the fact that`, `owing to the fact that` | `because` |
| `at this point in time` | `now` |
| `in the event that` | `if` |
| `has the ability to`, `is able to` | `can` |
| `a large number of` | `many`, or the number |
| `it is important to note that` | delete; the sentence after it is the note |
| `there is / there are ... that` | recast with the real subject |
| `the fact that` | almost always deletable |
| `in terms of` | name the actual relationship |
| `very`, `really`, `quite`, `rather`, `somewhat` | delete, or use a stronger word |
| `basically`, `essentially`, `actually`, `simply` | delete |
| `going forward` | delete, or give the date |

Not on this list and not deletable: `only`, `rarely`, `almost`, `nearly`, `roughly` — these carry truth conditions. Deleting them changes the claim (SKILL.md Where Experts Disagree).

## Rhythm

- Flat rhythm is the loudest machine tell: three or more consecutive sentences within ±3 words of each other (SKILL.md Rule 9).
- The fix is not "add short sentences" but "vary". Break one long sentence in two; fuse two short ones with a semicolon or a conjunction.
- Place the shortest sentence at the point of maximum emphasis — the end of the paragraph or immediately after the hardest idea.
- Read aloud. Every stumble marks a repair site, and stumbles find problems that no formula catches: buried subjects, garden-path openings, unpronounceable clusters of nouns.
- Long is not the same as complex. A 40-word sentence with one main clause and parallel items is easy; a 22-word sentence with three nested clauses is not. `sentence_flag_words` triggers an inspection, not a split.

## Readability Formulas and What They Are For

Flesch Reading Ease = 206.835 − 1.015 × (words ÷ sentences) − 84.6 × (syllables ÷ words)

Bands cover the whole scale with no gap; each one owns its lower bound, so a score of exactly 70 is the 70-80 row and 90 is the 90-100 row.

| Score | Reads like |
|---|---|
| 90-100 | Very easy — short sentences, common words |
| 80-90 | Easy — conversational; consumer email and good newsletters sit here |
| 70-80 | Fairly easy — plain prose carrying a few longer sentences |
| 60-70 | Plain English, standard for general audiences |
| 50-60 | Fairly difficult — trade press: longer clauses, assumed vocabulary |
| 30-50 | Dense; academic and professional prose lives here |
| 0-30 | Very difficult; specialist readers only |

Gunning Fog = 0.4 × ((words ÷ sentences) + 100 × (complex words ÷ words)), where complex = three or more syllables.

Both formulas are functions of exactly two things: sentence length and syllable count. That is their whole diagnostic power and their limit:

- **Legitimate use**: find the outlier paragraph inside one document — the one scoring far below the piece's own average is almost always the one with a buried subject or a stacked clause.
- **Illegitimate use**: comparing two documents on different subjects, or targeting a score. "Use `use` instead of `utilize`" improves the score and the prose; replacing an accurate technical term with a vague common word improves the score and destroys the sentence.
- Plain-language practice puts average sentence length around 20 words for general audiences. Treat it as a check on the *average*, never as a cap on any individual sentence — a document where no sentence exceeds 20 words has flat rhythm by construction.

## Machine-Written Tells

Run this sweep on every generated draft when `ai_tell_sweep` is true. These are structural, not lexical — a word list gets stale, these patterns do not.

| Tell | What it looks like | Fix |
|---|---|---|
| Uniform rhythm | Every sentence 15-20 words | Vary the spread deliberately |
| The tricolon reflex | Three parallel items where two or four would be truer | Use the number the content has |
| Hedge stacking | `may potentially`, `it is worth noting that`, `generally speaking` | One hedge per claim, or state the actual uncertainty |
| Symmetrical paragraphs | Every paragraph the same length, each opening with its topic sentence | Break the pattern where the argument turns |
| The both-sides close | "Ultimately, the right approach depends on your needs" | Give the default and the escape hatch |
| Restating the prompt | An opening paragraph that describes what the piece will do | Delete it; start at the first real move |
| Abstract subjects | `This approach`, `The landscape`, `Organizations` in the subject slot | Put a person or a named thing there |
| Announced structure | "Let's dive in", "First, let's examine" | Delete; the subheads carry the structure |
| Empty intensifiers | `crucial`, `essential`, `vital`, `key insight`, `game-changing` | Cut, or replace with what makes it matter |
| Summary that adds nothing | A closing paragraph restating the subheads | End on the consequence (`structure.md`) |

## Words That Cost More Than They Pay

Not banned — expensive. Each buys less than a plainer alternative in most contexts: `utilize`, `leverage` (as a verb), `facilitate`, `delve`, `robust`, `seamless`, `holistic`, `synergy`, `impactful`, `myriad`, `plethora`, `paradigm`, `ecosystem` (outside biology), `journey` (outside travel), `unlock` (outside locks).

The user's own `## Never` list outranks this one in both directions: a word they like stays, a word they hate goes even if it appears here as acceptable.

## Precision Failures

Clarity failures that survive every readability check because the sentence is short and simple:

- **Ambiguous pronoun**: `this`, `it`, `they` with two candidate referents. Replace with the noun. The most common source of genuine misreading in professional writing.
- **Elegant variation**: renaming the same thing to avoid repetition. The reader assumes a new thing was introduced. One thing, one name.
- **Unquantified comparative**: `faster`, `cheaper`, `better` with no baseline. Faster than what, by how much.
- **Dangling modifier**: "Having reviewed the contract, the terms were unacceptable" — the terms did not review anything.
- **Stacked nouns**: "customer data retention policy review process". Three nouns in a row is the limit; unpack with prepositions.
- **False range**: "5-10 minutes" invented for plausibility. If you do not know, say so or omit it.
- **Scope creep in a negation**: "not all X are Y" vs "all X are not Y" — these mean different things and the second is almost always a mistake.

**When the user rejects a construction, a word, or a rewrite** — not just this once, but as a rule — write it to `## Never` in `memory.md`, and the specific edit to `## Corrections` with the trait it reveals, in the same turn (`memory-template.md`). Three corrections sharing a trait get promoted to `## Voice`.
