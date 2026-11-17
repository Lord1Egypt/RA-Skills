# Writing in a Second Language — Register, Not Grammar

Scope: prose written by someone in a language that is not their first. The mistakes that matter here are rarely grammatical — grammar is what spellcheckers and `grammar` already catch. What marks a text as non-native, and what actually costs the writer, is register, idiom and directness.

**Before editing an L2 draft**, read `languages` in `config.yaml` and `## Voice` in `~/Clawic/data/writing/memory.md`. A writer's L2 voice is a separate voice from their L1 voice and is recorded as its own entry under `## Formats` with the language as its condition — merging them produces drafts that read like a translation of the wrong person.

## The Rule

**Correct what changes meaning or register. Leave what only marks the writer as non-native and costs nothing.**

Over-correction is the real failure mode here. Editing every trace of the writer's first language out of the text removes their voice and replaces it with generic native-speaker prose, which reads as blander than what they wrote. A slightly unusual but clear construction is not an error.

Correct: wrong preposition that changes the relation, false friend, register mismatch, an idiom used wrong, a directness level that will be misread.
Leave: article usage that is unusual but unambiguous, a slightly formal register that is simply their voice, sentence rhythms borrowed from their L1 that read fine.

## Register: The Expensive Mistake

Formality maps differently across languages, and the mismatch is invisible to the writer while being loud to the reader.

| Pattern | Where it comes from | Effect in English | Fix |
|---|---|---|---|
| "Dear Sir/Madam", "I remain at your disposal" | Standard business register in several European languages | Reads as decades out of date, or sarcastic | "Hi <name>", "Happy to help" |
| "Please do the needful", "Kindly revert" | Established regional business English | Perfectly normal in some regions, opaque in others | Keep with a regional audience; make explicit with a global one |
| Bare imperatives — "Send me the file" | Neutral politeness in languages where the verb form carries deference | Reads as brusque or as an order | "Could you send me the file?" |
| Stacked politeness — "I would be extremely grateful if you might possibly..." | Compensating for uncertainty about the level | Reads as anxious and buries the ask | One politeness marker, then the ask (`emails.md`) |
| Titles everywhere — "Dear Engineer García" | Title-using professional cultures | Reads as formal to the point of distance in most English-speaking workplaces | First name unless the context is legal or academic |
| Diminutives and warmth markers | Languages where warmth is grammatical | Can read as unprofessional in a cold register | Warmth through specifics, not through form |

Directness is the deepest split: in some cultures a direct request is rude and hedging is respect; in most English-language business contexts, hedging past one marker reads as evasion. The user's audience decides, and the decision goes in that context's `style-sheets/<context>.md`.

## Interference Patterns Worth Knowing

Grouped by what they do to the reader, not by language of origin — the same pattern arrives from many L1s.

- **False friends**: `actually` (≠ *actualmente*, *actuellement* = currently) · `eventually` (≠ *eventualmente*, *éventuellement* = possibly) · `sensible` (≠ *sensible* = sensitive) · `assist` (≠ *assistere*, *asistir* = attend) · `pretend` (≠ *prétendre*, *pretender* = claim/intend) · `library` (≠ *librairie*, *librería* = bookshop) · `actual` (≠ *aktuell* = current) · `sympathetic` (≠ *sympathique* = nice). These produce sentences that are grammatical and wrong, so nothing flags them.
- **Preposition transfer**: `depends of`, `discuss about`, `explain me`, `arrive to`, `married with`, `on the end`. Harmless to comprehension, but dense enough to be distracting; fix them.
- **Tense and aspect**: present simple used for a running action ("I work on it now"); present perfect where the past is required, or the reverse. Fix — these change the timeline the reader builds.
- **Article usage**: missing or extra `the`/`a`. Fix where the meaning shifts (generic vs specific); leave where it is merely unusual.
- **Long-sentence transfer**: languages with heavier subordination produce 45-word English sentences that are correct and hard. Split them (`clarity.md`).
- **Punctuation transfer**: comma before every subordinate clause, spaced punctuation, quotation guillemets, decimal commas in numbers. Fix; these look like typos in English.
- **Capitalisation transfer**: capitalised nouns from German, lowercase month and day names from Romance languages, lowercase `i`. Fix.

## Words That Betray a Machine Translation

Machine-translated text has a distinct profile, different from an L2 writer's own prose, and the fix is different too: it needs rewriting, not correcting.

- Every sentence the same length and the same shape, with connectives that do not carry logical weight.
- Formal register applied uniformly, including where the context is casual.
- Idioms translated literally, producing phrases that are grammatical and meaningless.
- Terminology inconsistent for the same concept across a document, because each sentence was translated independently.
- Pronouns that lose their referent, because the source language dropped or gendered them differently.

Fix by rewriting the paragraph from its meaning, not by editing its sentences. Editing a machine translation sentence by sentence preserves the structural tell.

## Hedging Calibration

The single most useful thing to get right, because it maps directly onto how competent the writer sounds.

- One hedge per claim, maximum. `may potentially possibly` is three (`clarity.md`).
- Hedge the claim, not the self: "the data suggests X" reads as careful; "I'm not an expert but maybe X" reads as unqualified, and the writer usually meant the first.
- In English-language business writing, an unhedged statement of your own opinion is normal and expected. Writers from cultures where that is presumptuous systematically under-claim and are read as uncertain rather than as polite.
- Never hedge a fact you have measured. Hedging your own data invites the reader to discount it.

## Working With the Writer

- Explain the fix once, briefly, when the same interference pattern appears a third time. Explaining every instance is exhausting and unwanted.
- Offer the correction, not the grammar lesson, unless they asked. Most L2 writers want the sentence, not the rule.
- Never mention "non-native" in the output. Fix the text.
- When they use a construction that is unusual but effective, say so. They will otherwise assume it was a mistake you missed and remove it themselves.
- If the writer's L1 is one they may write in too, note both registers separately — the same person is often formal in one language and blunt in the other, and that is not an inconsistency to fix.

**When a recurring interference pattern is identified**, write it to `## Corrections` in `memory.md` with the trait, and after the third occurrence promote it to `## Voice` under the condition for that language. **When a register decision is settled for an audience** — how direct, how formal, which greeting set — it goes to that context's `style-sheets/<context>.md` in the same turn (`memory-template.md`).
