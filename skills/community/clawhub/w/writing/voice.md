# Voice — Capturing It, Reproducing It, Proving It

A voice is not a mood. It is a set of choices a writer makes repeatedly, most of them unconsciously, all of them observable in a page of their prose. Reproducing it is a measurement problem before it is an art problem.

**Before any draft**, read `## Voice`, `## Never` and `## Formats` in `~/Clawic/data/writing/memory.md`, plus `voice_file` if `config.yaml` sets one, plus any `samples/` file the `## Boxes` index points at for this format. Voice work done from memory of the conversation instead of the stored fingerprint is how a trait the user already stated gets violated twice.

**Contents:** [The Four Dimensions That Carry a Voice](#the-four-dimensions-that-carry-a-voice) · [The Full Detection Sweep](#the-full-detection-sweep) · [Eliciting a Voice Without Interrogating](#eliciting-a-voice-without-interrogating) · [Measuring a Sample in Five Minutes](#measuring-a-sample-in-five-minutes) · [Reproducing It](#reproducing-it) · [Which Voice Wins](#which-voice-wins) · [Voice Drift](#voice-drift) · [Ghostwriting and Brand Voices](#ghostwriting-and-brand-voices) · [What to Record and When](#what-to-record-and-when)

## The Four Dimensions That Carry a Voice

Most of the recognisable signal lives here. Get these right and readers accept the text as the person's, even when the vocabulary is unremarkable.

| Dimension | How to measure it in a sample | What imitating it looks like |
|---|---|---|
| **Sentence-length distribution** | Count words per sentence for 20 sentences: the min, the max, and whether short ones cluster at paragraph ends | Reproduce the *spread* and the placement, not the average |
| **Who occupies the subject slot** | Tally subjects: people, named things, abstractions, or dummy `it`/`there` | A writer whose subjects are people reads completely differently from one whose subjects are processes |
| **Concreteness ratio** | Per 100 words, count nouns you could photograph | Match the ratio; inventing concrete details they did not have is fabrication, not voice |
| **The never-list** | What is conspicuously absent: exclamation marks, semicolons, rhetorical questions, hedges, emoji, second person | The absences are the most reliable signature, because they persist when the topic changes |

Everything else — favourite words, a signature closing, a joke pattern — is a tic. Tics decorate a voice; they cannot carry one (SKILL.md Rule 4).

## The Full Detection Sweep

Run this against a sample when the four dimensions are already captured and the draft still reads wrong. Record only what is actually observable in their writing — a dimension with no evidence stays unrecorded.

**Register and stance**
- Formality: contractions, sentence fragments, slang, profanity tolerance
- Distance: first person singular, "we", second person, impersonal
- Confidence: bare assertions vs hedged claims; whether they admit uncertainty in text
- Humour: none, dry, self-deprecating, absurd — and whether it appears in serious pieces

**Structure**
- Opening move: scene, number, claim, question, anecdote, context
- Closing move: consequence, call to action, callback, summary, open end
- Paragraph length and whether it varies with tension
- Lists vs prose; headings vs a continuous run
- Whether they signpost ("three reasons") or let structure be implicit

**Language**
- Vocabulary register and whether it shifts by audience
- Latinate vs Germanic preference (`purchase` vs `buy`, `utilize` vs `use`)
- Active/passive balance and *which* things they leave passive
- Metaphor density and where the metaphors come from (sport, cooking, engineering, war)
- Jargon: which fields they will use unglossed, and for whom

**Mechanics as style**
- Em-dash, parentheses, colon, semicolon — most writers strongly prefer one
- Emoji, bold, italics, ALL CAPS for emphasis
- Oxford comma, serial punctuation, ellipsis habits
- Numerals vs spelled-out numbers
- Capitalisation of headings and job titles

**Social moves**
- Greetings and sign-offs, by relationship
- How they disagree, deliver bad news, decline, apologise, chase
- How they credit others and how they handle being wrong
- What they never put in writing at all

**Context splits** — a person has several voices, not one. Split by: channel (email vs chat vs post), relationship (manager, peer, client, stranger), byline (their own vs a company's), and language. Record each split under `## Formats` with its condition, never as a global trait.

## Eliciting a Voice Without Interrogating

Never open a session with a questionnaire. Voice arrives three ways, in order of value:

1. **Samples they already have.** One request, once: "if you have two or three things you've written that felt right, they're worth more than any description." Store what arrives in `samples/`.
2. **Their edits of your draft.** The highest-signal source in the domain, because it is a preference stated against a concrete alternative. Every edit goes to `## Corrections` with the trait extracted.
3. **Forced choice.** Offer two variants differing on exactly one dimension — sentence length, or person, or opening move — and let the pick be the data. Never offer three: with three, the pick tells you nothing about which dimension decided it.

What not to do: ask "what's your writing style?" Almost nobody can answer accurately about their own prose, and the answer you get ("clear and friendly") is unusable by the Output Gates.

## Measuring a Sample in Five Minutes

1. Take 20 consecutive sentences from the middle of the piece — not the opening, which is always overworked.
2. Word-count each. Record min, max, and whether any three consecutive sentences land within ±3 words.
3. Underline the grammatical subject of each. Tally people / named things / abstractions / dummy subjects.
4. Count photographable nouns per 100 words.
5. List what is absent that you expected: no exclamation marks, no semicolons, no second person, no hedges.
6. Write those five results into the sample file's header as the `Metrics` line, and only the traits they support into `## Voice`.

Two samples of the same format that disagree on a dimension mean the dimension is context-dependent, not that one is wrong. Record the condition; do not average them.

## Reproducing It

- Draft normally first, then convert. Trying to write *in* a voice from the first word produces stiff prose that hits the tics and misses the rhythm.
- Convert in this order: subject slots → sentence-length spread → never-list purge → tics last. Reversing this produces text peppered with their favourite words and structured like yours, which is the most detectable failure.
- Read your draft and their sample aloud back to back. The mismatch is audible before it is analysable, and the place you hear it names the dimension.
- Keep their errors when the errors are the voice: a habitual sentence fragment, a comma splice for pace, a preferred non-standard spelling. Correcting these without asking is how "you made it sound like a corporate blog" happens.
- Never generate a claim, an opinion, a number, or a commitment the person has not made. Voice is *how* they say things; inventing *what* they say is forgery, and it is the one failure that cannot be fixed after publication.

## Which Voice Wins

Precedence, highest first, when sources conflict:

1. An instruction in this session ("make this one formal") — applies to this piece only, and is never written to `## Voice`.
2. The style sheet for the context (`style-sheets/<context>.md`) — a client's house style outranks the user's habits inside that client's work.
3. `voice_file` from `config.yaml` — a document the user wrote deliberately.
4. `## Voice` and `## Formats` in `memory.md` — observed traits.
5. The Format Specs defaults in `SKILL.md`.

A conflict between levels 2 and 4 is worth one line to the user ("Acme's sheet says no first person, your usual voice uses it — going with Acme's"), and a line recording the clash in that context's `style-sheets/<context>.md`.

## Voice Drift

Two kinds, with different fixes:

- **Their drift**: the person's writing genuinely changed — new job, new audience, deliberate reinvention. Signal: two recent samples agree with each other and disagree with `## Voice`. Fix: update `## Voice`, keep the old samples, note the date of the shift.
- **Your drift**: your drafts have been sliding toward a generic register and the user has stopped correcting them because it is tiring. Signal: `## Corrections` has repeat entries for the same trait across months. Fix: re-read the samples before the next draft, and promote the repeated trait to `## Voice` so an Output Gate catches it.

Schedule a re-check against the newest samples as a `## Due` row when the user writes regularly; quarterly is enough for someone publishing weekly.

## Ghostwriting and Brand Voices

- A byline selects a voice. Writing under a company name, a founder's name, or a persona means the user's stored voice is **not** the default and must not be applied (SKILL.md Traps).
- Brand voices need the same four dimensions plus one: the claim boundary — what the brand may state as fact, what needs legal review, what it never says about competitors. Store it in that context's style sheet.
- Multiple personas are separate style sheets, never sub-sections of one. The moment two personas share a file, they start converging.
- When ghostwriting for a real person, the samples must be *their* writing, not marketing copy written about them. A press release is not a voice sample.

**After any session where a voice trait was confirmed, corrected or contradicted**, write it in the same turn: the trait to `## Voice` phrased as checkable behaviour, the rejection to `## Never`, the edit to `## Corrections` with its trait, and any representative text they shared to `samples/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`). A trait that stays in the chat is a trait you will violate next week.
