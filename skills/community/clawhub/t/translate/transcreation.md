# Transcreation — Marketing, Humor, and Literary Voice

Where a reader is meant to *feel* something, fidelity to the words is the wrong target. Transcreation reproduces the effect and treats the source as a brief. It is a different job with a different deliverable, a different rate, and a different failure mode: the sentence that is correct and does nothing.

**Contents:** [When To Switch Modes](#when-to-switch-modes) · [The Brief](#the-brief) · [The Deliverable](#the-deliverable) · [Wordplay](#wordplay) · [Humor](#humor) · [Slogans and Names](#slogans-and-names) · [Cultural Landmines](#cultural-landmines) · [Claims That Are Regulated](#claims-that-are-regulated) · [Literary Prose](#literary-prose) · [Poetry and Song](#poetry-and-song) · [Testing It](#testing-it) · [What To Write Down](#what-to-write-down)

**Before writing marketing copy in a locale**, read `styles/<locale>.md` and the pair's glossary if `## Boxes` names them, plus any `artifacts/naming-*.md`. Brand voice decisions are expensive to make and cheap to contradict.

## When To Switch Modes

| Mode | Content | Test of success |
|---|---|---|
| Translation | Documentation, UI, legal, technical, news | A bilingual reader finds every claim in the source |
| Adaptation | Web copy, help articles, product descriptions | Reads as written in the target; claims intact; structure may change |
| Transcreation | Slogans, campaigns, headlines, names, humor, fiction, poetry | A target reader has the reaction the source reader had; wording is negotiable |

Switching mode without saying so is the mistake in both directions: transcreating a specification invents claims, and translating a slogan produces a sentence nobody would ever say. State which mode you are in when the content is ambiguous, and quote accordingly (`jobs.md`).

## The Brief

Transcreation cannot be done from the source text alone. A usable brief carries seven things:

1. **Objective** — what the reader should do or believe afterwards.
2. **Audience** — who they are in the target market, not the source market.
3. **The insight** — why the source line works, in one sentence. This is what gets carried across; without it, everything is guesswork.
4. **Tone and brand voice** — with two examples of copy the brand approved and one it rejected.
5. **Mandatories** — brand name treatment, legal wording, the product's actual function, the call to action's meaning.
6. **Constraints** — character or syllable count, where it appears (billboard, button, thirty-second spot), whether it must rhyme or alliterate.
7. **What must not change** — usually a claim, a number, a trademark, or a compliance line.

When the client supplies only the source text, writing the missing brief and confirming it is the first deliverable.

## The Deliverable

Not one line. **Two or three options**, each with:

- the target line;
- a **back-translation** into the source language, literal enough that a client who does not speak the target can see what it says;
- one sentence of rationale — what it does and why it works in this market;
- a risk note where one exists (a double meaning, a regional limitation, a term a competitor owns).

Back-translation here is a communication device, not a quality check (`quality.md` covers the verification kind). Say so, or a client will treat the awkward literal English as the quality of the work.

Transcreation is priced by hour or by project, never per word: three words can take a day, and per-word pricing on a headline is how the craft gets treated as a lookup.

## Wordplay

Four strategies, in the order to try them:

1. **Substitution** — a different pun in the target with the same function. The strongest result and the usual answer.
2. **Compensation** — the joke cannot land here, so an equivalent effect is placed nearby where the target language allows one. Standard practice in fiction and dubbing.
3. **Literal plus signal** — keep the meaning and mark the play (italics, a rhyme elsewhere in the line). Weak, but survivable in prose.
4. **Omission** — drop it and pay the effect back elsewhere. Legitimate; silently losing it and saying nothing is not.

A footnote is available in literature and impossible in a subtitle, a button, or a billboard. Match the strategy to the medium before choosing.

## Humor

- **The reference, not the joke, is what usually fails.** A celebrity, a snack, a TV show or an institution the target audience does not know produces silence. Substitute a reference of the same *kind* and the same *status*, not the same field.
- Register humor (a formal word in a casual sentence) is often portable; puns rarely are; humor built on grammatical accident (homophones, gendered nouns) almost never is.
- Irony and self-deprecation travel unevenly across markets, and humor aimed at authority, religion or ethnicity is a market-specific risk, not a taste question.
- Comedy timing survives translation only if length survives: a punchline that arrives two beats late is not funny. In subtitles and dubbing the reading and lip budgets govern (`subtitles.md`).

## Slogans and Names

- A slogan is judged on rhythm and length as much as sense. Count syllables in the target, say it aloud, and check it against the visual it will sit on.
- Imperatives are not equally available: some languages have no natural short imperative for the verb you need, and some markets read imperative advertising as rude.
- Brand names integrated into a slogan constrain grammar in inflected languages — the name may need a case ending it cannot take. Rewrite around it rather than declining a trademark.
- **Naming a product for a new market is not translation.** It needs: native speakers checking for unintended readings across the market's languages *and* its major dialects, a trademark search in that jurisdiction, a domain and handle check, and a decision on transliteration versus a new name (`locales.md` for the CJK case). The decision and what was rejected go in `artifacts/naming-<market>.md` with the reason.

## Cultural Landmines

Check these before delivery, not after a market complains:

- **Colors and numbers** carry local meaning — white for mourning in parts of East Asia, the number 4 avoided in Chinese, Japanese and Korean contexts, 13 in much of Europe and the Americas.
- **Gestures and hands** in images and emoji mean different things by market; a thumbs-up, an OK sign and a beckoning palm all have offensive readings somewhere.
- **Animals, food and drink** carry religious and dietary constraints; alcohol and pork imagery is unusable in several markets.
- **Maps, flags and borders** are political statements in disputed regions, and using a flag to mean a language is a separate error (`web.md`).
- **Names and dates** with historical weight: a campaign date, a color combination, or a number can coincide with a national tragedy or a political anniversary.
- **Gender and family depiction** norms differ enough that the same image reads as progressive, invisible, or provocative depending on the market.

The reliable procedure is one in-market native reader with a mandate to say "this is fine but nobody would say it" — a role worth a contacts row of its own (`memory-template.md`).

## Claims That Are Regulated

Advertising language is law in several markets, and the constraint sits exactly where transcreation is most tempted to be bold:

- **Superlatives and comparative claims** must be substantiated in many jurisdictions, and comparative advertising naming a competitor is restricted or banned in some.
- **Health, nutrition and cosmetic claims** are governed by approved wording lists in the EU and elsewhere: "supports immunity" and "boosts immunity" are not interchangeable, and neither is a free choice.
- **Financial promotions** carry mandatory risk wording whose target-language text is prescribed, not composed.
- **Prices, discounts and "free"** have market-specific rules about what must be disclosed alongside them.

The rule: a claim that changes strength in translation is a defect even when it reads better. Anything in these categories goes past the client's legal review with the back-translation attached (`legal-medical.md`).

## Literary Prose

- **Voice first.** Establish the narrator's register, sentence rhythm and vocabulary range in the first pages, write it down, and hold it for the whole book. Inconsistent voice is what readers notice and reviewers name.
- **Dialect is not mapped to a dialect.** Rendering a rural Southern US voice as a rural Andalusian one imports a whole other set of associations. Build the effect from register, syntax, idiolect and lexical choice instead — the character sounds *marked*, not relocated.
- **Realia** — the culturally specific object, dish, institution — sits on a spectrum from keeping the foreign word (foreignizing, which keeps the setting) to replacing it with a local equivalent (domesticating, which keeps the ease). Choose a policy for the whole text, not per instance, and state it.
- **Meaningful names** in fiction: translate them all, or none, and say which. Half-translated casts are the most common amateur signal in genre fiction.
- Repetition that looks clumsy is often deliberate. Check whether the word recurs elsewhere before smoothing it — a leitmotif destroyed by synonym variation cannot be recovered by the reader.
- A translator's note or afterword is the legitimate home for what genuinely cannot cross. Use it rarely; a note per page is a failed strategy, not a scholarly one.

## Poetry and Song

The permanent trade-off: **form, sense, or singability — you get two at most.** Decide which is the point of this text before starting, and tell the client which you sacrificed.

- Meter and rhyme schemes are not portable: languages differ in stress, syllable weight and the availability of rhymes. A target-language form with the same *function* (its own tradition's equivalent) usually beats an imported one.
- For song, **singability governs**: syllable count per musical phrase, stressed syllables on strong beats, and open vowels on long notes. A line that is beautiful and unsingable is unusable.
- Deliver poetry and lyrics with a literal prose gloss alongside, so the client can see what was traded.
- In subtitling, the default is the literal reading unless the song is being dubbed (`subtitles.md`).

## Testing It

- Read it aloud. Marketing copy that cannot be said comfortably will not be remembered.
- Show it to one in-market native who was not involved, with no context, and ask what it makes them think of. The first association is the test.
- Search the exact phrase in the target market: an unintended existing meaning, a competitor's tagline, or a slang usage shows up immediately.
- For anything going on a package, a billboard or a product name, the native check is not optional and its result is recorded.

## What To Write Down

- A **naming or tagline decision** — what was chosen, what was rejected, and why — is an `artifacts/naming-<market>.md`, born as its own file with its `## Boxes` line, in the same turn. It is re-litigated every campaign otherwise.
- A rendering the client or the in-market reviewer rejected goes to **`### Forbidden Renderings`** in the glossary with the accepted form, so it is never proposed again.
- Brand voice per locale — register, humor appetite, how far copy may stray — lives in **`styles/<locale>.md`**, and the one-line summary in `## Locale Register`.
- The in-market reviewer is a row in the shared **contacts** box, with their market and what they are trusted to judge (`memory-template.md`).
