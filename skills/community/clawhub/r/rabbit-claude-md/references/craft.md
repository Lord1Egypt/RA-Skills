# Craft

The positive discipline. Everything in `patterns.md` says what to remove. This says what to do instead, and it is the layer that makes prose good rather than merely clean.

Use it for drafting from scratch, for converting a document into someone's voice, and for any rewrite that has to be more than un-flagged.

---

## Orwell's six rules

From *Politics and the English Language* (1946), and still the shortest complete style guide anyone has written.

1. Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.
2. Never use a long word where a short one will do.
3. If it is possible to cut a word out, always cut it out.
4. Never use the passive where you can use the active.
5. Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.
6. **Break any of these rules sooner than say anything outright barbarous.**

Rule six governs this entire skill. It is the reason a pattern catalog cannot be run as a linter. When a rule would make the sentence clumsy, false, or less precise, the rule loses.

Rule one is also the deepest AI-specific rule in the set, written 80 years early. Every aphorism formula, dead metaphor, and stock phrase in `patterns.md` is a figure of speech you are used to seeing in print. That is exactly what a next-token predictor produces.

---

## The audience frame

Hold this on every piece, always:

> **Write for a smart non-expert who has not seen the thing you are describing.**

Three independent clinical studies found that a plain audience-and-grade-level frame dropped reading difficulty by two to five levels with no loss of accuracy. It outperforms every readability formula as a steering instruction, and it costs one sentence.

**Do not optimize toward a readability score.** Flesch, Flesch-Kincaid, Gunning Fog, and SMOG are poor proxies for comprehension, disagree with each other, reward gaming at the expense of cohesion, and cannot tell whether a reader knows a word. `scripts/scan.py` reports Flesch-Kincaid as a diagnostic. Never treat it as a target.

---

## Structure

Convergent across the US Federal Plain Language Guidelines, the National Archives principles, ISO 24495-1, and the Microsoft and Google style guides.

- **Main point first.** Inverted pyramid. Context can come second. If the piece opens with broad scene-setting before the news, move the news up.
- **One idea per paragraph,** with the first sentence carrying the weight. Readers scan first lines.
- **Descriptive, front-loaded headings.** A heading should tell the reader what is under it, not label a slot ("Overview", "Key Points").
- **Conditions before instructions.** "If you are on Windows, run X" beats "Run X if you are on Windows."
- **Numbered lists for sequences. Bullets for non-sequences.** Prose for anything that is not actually a list.
- **Progressive disclosure.** Reveal complexity in layers rather than front-loading everything.
- **Organize around what the reader needs,** not around how the material is structured internally.

Nielsen Norman's usability work measured the effect: concise writing raised usability 58%, scannable formatting 47%, plain objective style 27%, and all three together 124%.

---

## Sentences

- Average 15-20 words. Avoid exceeding 25-30.
- One complete thought per sentence.
- Keep subject and verb close together.
- Active voice by default. Passive is a deliberate tool, correct when the actor is irrelevant or the object needs emphasis.
- Make verbs do the work. "Made a decision" → "decided." "Has the ability to" → "can."
- **Vary the length anyway.** The 15-20 average is a center of gravity, not a target for every sentence. A page where every sentence hits 18 words is the uniformity problem in `patterns.md` §52.

**No hard word-count caps on the piece.** Models overshoot numeric targets, and a cap set in advance is usually wrong about what the piece needs.

---

## Words

- Prefer the common word over the technical synonym.
- Define a technical term on first use when it cannot be replaced.
- Avoid stacked modifiers.
- Address the reader as "you."
- Be concrete. Abstraction is where writing goes to die. "The integration improved efficiency" → "The integration cut deploy time from 40 minutes to 4."
- Names, numbers, dates, mechanisms, and examples beat abstractions every time.
- **Open it up, do not dumb it down.** Keep the substance, nuance, and precision. Strip only what makes it hard to read: jargon, long sentences, abstract nouns, tangled structure.
- **Protect the specific fact.** Do not smooth a useful detail into generic importance.

---

## Technical and instructional prose

The ASD-STE100 Simplified Technical English baseline. Use it by default for documentation, procedures, product copy, and business prose.

1. Short sentences. One main action or statement each.
2. A clear subject and an active verb. Name the actor when the actor matters.
3. **The same term for the same thing.** Do not change a term only to avoid repetition. This is the direct inverse of synonym cycling.
4. Familiar words with one precise meaning. Avoid idioms, slang, figurative language, and vague verbs.
5. Use a specific technical term when accuracy requires it. Define it or link its definition.
6. Keep noun groups short. Use prepositions to show relationships between terms.
7. Write procedures as direct instructions: state the condition, the action, and the expected result.
8. Use positive instructions. State what the reader must do.
9. Consistent spelling per the user's style guide.
10. **Preserve code, commands, identifiers, product names, legal text, and required quotations.** Never simplify these silently.

When strict STE is not possible, keep the text clear and mark the terms or passages that need a domain exception. Do not claim STE conformance without checking the current issue and dictionary.

---

## Creative writing

For fiction, poetry, memoir, scripts, and lyrical prose, treat all of the above as a clarity aid and never as a constraint that overrides the form.

Keep intentional ambiguity, cadence, dialogue style, imagery, and character voice when they create a real effect. Invented detail is the job in fiction. The never-invent-facts rule governs everything else.

Remove only language that is inherited, inflated, evasive, or lazy. Apply strict simplification only when the user asks for it, and say when that request conflicts with an effect they seem to want.

---

## Why layering matters

Compliance drops as the number of simultaneous instructions rises. Firing an 800-line rule set at a draft in one pass produces worse results than three narrower passes, which is why this skill splits into a router, references loaded per mode, a script for the mechanical layer, and a self-check at the end.

When you draft or convert a document to a voice, apply this file. When you deslop, apply `patterns.md`. Do not try to hold both at full resolution at once.

A conversion needs both halves and takes them in order: this file decides the shape the document should end up in, `patterns.md` cleans what is left at the sentence and word level. A deslop only ever needs the second.
