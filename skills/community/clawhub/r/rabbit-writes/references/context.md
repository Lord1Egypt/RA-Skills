# Register and voice

Two independent axes. **Register** sets how strict to be. **Voice** sets how the prose should sound. You can write blunt for a blog or warm for docs.

---

## Register profiles

The set is a formality spine plus four genre columns.

**The spine,** loosest first: `chat`, `informal`, `blog`, `formal`. This is the axis a document form maps onto. `references/forms/` holds one file per form, and each names the rung it sits on.

**The genre columns,** `technical-blog`, `docs`, `linkedin`, and `academic`, sit outside the spine because each carries tolerances no formality band captures: the vocabulary exemptions below, parameter lists, hashtags and bold hooks, and the even sentence lengths a research paper genuinely has. A genre column is not stricter or looser than a rung. It is a different kind of document. `academic` is the clearest case, since it is not more formal than `formal`, it is a register where `paradigm` is a term of art.

The split is data, in `scripts/registers.json` under `spine`, so a rung that names nothing fails the build rather than reading as a claim this page makes.

Infer from the text unless the user names one.

| Signal | Register |
|---|---|
| A `Subject:` line, or a salutation with a signoff | `formal`, `informal` in a peer thread. See `forms/email.md` |
| A salutation and a date, no subject line | `formal`. See `forms/letter.md` |
| Under about 100 words, no structure, no greeting | `chat`. A DM, a reply, an issue comment |
| Hashtags or @-mentions, under 300 words | `linkedin` |
| Code blocks, API references, architecture | `technical-blog` |
| Step-by-step instructions, parameter docs, README shape | `docs` |
| Sectioned long-form with a personal frame | `informal` for a newsletter, `formal` for an essay |
| No strong signal | `blog`, the neutral default, all rules at full strength |

If the inference feels wrong, say which register you picked and why. The user can override.

## Tolerance matrix

Rules not listed apply at full strength everywhere.

| Rule | chat | informal | blog | formal | technical-blog | docs | linkedin | academic |
|---|---|---|---|---|---|---|---|---|
| Em dashes | skip | strict | strict | strict | strict | relaxed | relaxed (2/post) | strict |
| Bold overuse | skip | strict | strict | strict | strict | relaxed | relaxed (hooks OK) | strict |
| Emoji in headers | skip | strict | strict | strict | strict | skip | relaxed (1-2, end of line) | strict |
| Excessive bullets | skip | strict | strict | strict | relaxed | skip | skip | strict |
| Hedging | skip | strict | strict | strict | relaxed ("may" is accurate) | relaxed | strict | strict |
| Tier-1 vocabulary | P0 only | strict | strict | strict | **partial**, see below | **partial**, see below | strict | **partial**, see below |
| Promotional language | skip | strict | strict | **extra strict** | strict | strict | relaxed (some sell expected) | **extra strict** |
| Significance inflation | skip | strict | strict | **extra strict** | strict | relaxed | strict | **extra strict** |
| Copula avoidance | skip | relaxed | strict | strict | relaxed | skip | skip | strict |
| Uniform paragraph length | skip | strict | strict | strict | strict | skip | skip | strict |
| Numbered-list inflation | skip | strict | strict | strict | relaxed | skip | relaxed | strict |
| Rhetorical questions | skip | relaxed (1 hook) | strict | strict | strict | skip | relaxed (1 hook) | strict |
| Transition phrases | skip | strict | strict | strict | strict | relaxed | skip | strict |
| Generic conclusions | skip | strict | strict | **extra strict** | strict | skip | skip | **extra strict** |
| Hashtag stuffing | skip | strict | strict | **extra strict** | strict | skip | strict | strict |
| Bullet-NP lists | skip | strict | strict | strict | relaxed | relaxed (parameter lists) | strict | strict |
| Subjectless fragments | skip | relaxed (the register) | strict | strict | relaxed | skip | relaxed (the register) | strict |
| Boilerplate clusters | skip | strict | strict | **extra strict** | strict | relaxed | strict | **extra strict** |
| Future-narrative closers | skip | strict | strict | **extra strict** | strict | skip | strict | **extra strict** |
| Social endorsement closers | relaxed (1 in a DM) | relaxed (1 subscribe line) | strict | strict | strict | skip | strict | strict |
| Wall-of-text replies | strict | skip | skip | skip | skip | skip | strict | strict |
| Curly quotes | relaxed | skip | skip | skip | relaxed (plain-text contexts) | relaxed | skip | skip |
| Tier-2 clusters | skip | strict | strict | strict | **partial**, see below | **partial**, see below | strict | **partial**, see below |
| Tier-3 density | skip | strict | strict | strict | **partial**, see below | **partial**, see below | skip | **partial**, see below |
| Confidence calibration | skip | strict | strict | strict | strict | strict | strict | relaxed (14/19 papers) |
| Signposting | skip | strict | strict | strict | strict | strict | strict | strict |
| Reasoning-chain artifact | skip | skip | strict | strict | strict | strict | strict | strict |
| Acknowledgment loop | skip | skip | strict | strict | strict | strict | strict | strict |
| Diff-anchored writing | strict | strict | strict | strict | skip | skip | strict | strict |
| List-label periods | strict | strict | strict | strict | strict | skip | strict | strict |
| Inline-header bullet | strict | strict | strict | strict | strict | skip | strict | strict |
| Low burstiness | strict | strict | strict | strict | strict | strict | strict | skip |
| Trigram repetition | strict | strict | strict | strict | strict | strict | strict | skip |
| STE sentence length (procedural) | skip | skip | relaxed | strict | relaxed | relaxed | skip | relaxed |
| STE sentence length (descriptive) | skip | skip | relaxed | strict | relaxed | relaxed | skip | skip |
| STE punctuation (semicolons) | skip | skip | relaxed | skip | relaxed | relaxed | skip | skip |
| STE condition order | skip | skip | relaxed | strict | relaxed | relaxed | skip | strict |
| STE paragraph length | skip | skip | relaxed | strict | relaxed | relaxed | skip | relaxed |

**Extra strict** means flag borderline instances. In a `formal` document, an investor email or a letter, one "thriving ecosystem" undermines the message.

**Skip** means do not audit this category here. The rule does not apply.

**Relaxed** means the rule still runs and reports past a tolerance, not that it stops running. `scan.py` holds those tolerances in `PROFILE_RELAX` as hit allowances: `linkedin` reports the third em dash, `docs` the fifth curly quote, either of `technical-blog` and `docs` the third stacked hedge.

One kind of cell has no mechanical form: a rule with no pattern in `lexicon.json`. Bold overuse, excessive bullets, copula avoidance, numbered-list inflation, bullet-NP lists, subjectless fragments, hashtag stuffing, and wall-of-text replies are yours to apply by reading. Every other cell is implemented. This table is not the source: `scripts/registers.json` is, and this block is rendered from it by `python3 scripts/rwlib/registers.py --write`. `scripts/validate.py` fails if the two disagree, so editing the markdown by hand fails the build rather than documenting a tolerance the engine never had.

**Vocabulary exceptions, `technical-blog` and `docs`.** This is what **partial** means in the three vocabulary rows, and it is why those two registers do not take a hit allowance: an allowance would let a second `delve` through, and this does not. These words carry real technical meaning and are not flagged in either register: `robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage` (actual platform leverage), `facilitate`, `underpin`, `streamline`, `scalable`, `dynamic`. Still flagged at full strength: `delve`, `tapestry`, `beacon`, `embark`, `testament to`, `game-changer`, `harness`. The list itself is `technical_exempt` in `lexicon.json`.

P0 fingerprints (chatbot artifacts, cutoff disclaimers, citation leaks, tracking parameters, hidden unicode, placeholders) apply at full strength in **every** register, including `chat`.

---

## Voice personas

A persona is optional. If the writer does not name one, infer from the input's existing register and impose nothing. Each is a set of concrete targets, not a vibe, and the parenthetical says where it belongs.

**`casual`** (*blog, social, community*): Contractions throughout, because their absence reads stiff. Average sentence under 14 words, fragments fine. At least one first-person or concrete-anecdote touch. Near-zero jargon. Keep warm hedges ("I think", "honestly"), cut corporate ones ("it's worth noting").

**`professional`** (*LinkedIn, investor email, pitches*): Active voice for most sentences, varied in length. One concrete claim per paragraph: a number, a name, a date. Never "experts say." Make the ask explicit. Low tolerance for hedging.

**`technical`** (*docs, technical blog*): Plain copulatives ("X is Y") over inflated substitutes. One idea per sentence. Imperative mood for instructions. Jargon is fine, defined on first use. Tables and lists only where content is genuinely list-shaped.

**`warm`** (*mentorship, onboarding, thank-yous*): Address the reader as "you" and acknowledge them at least once. Cut intensifiers ("very", "truly", "incredibly") in favor of stronger verbs. No performative empathy ("I completely understand how you feel"). Medium sentences, 15-20 words, unhurried.

**`blunt`** (*decision memos, hard feedback*): Lead with the claim and cut the windup. Periods for emphasis, not dashes. No padding to reach a rule of three. Near-zero hedging. Short declaratives with the occasional long sentence for contrast.

## How the axes compose

A voice target always applies, even where a register would skip that category: `technical` voice still prefers plain copulatives inside a `chat` register that otherwise ignores copula avoidance.

Where both govern the same rule and agree, they reinforce. Where they disagree, **resolve toward the stricter of the two.** A `warm` voice in `docs` still gets no decorative tables.

A user-supplied writing sample outranks both. See `voice.md`.

Sensible pairings: casual↔chat/informal, professional↔linkedin/formal, technical↔docs/technical-blog.
