# Machine Translation and Post-Editing

MT is a productivity tool with a specific, repeatable failure profile. Knowing the profile is what separates post-editing from proofreading something you do not understand.

**Contents:** [Where MT Belongs](#where-mt-belongs) · [The Five Failures](#the-five-failures) · [Other Characteristic Errors](#other-characteristic-errors) · [Post-Editing Levels](#post-editing-levels) · [The Retranslate Threshold](#the-retranslate-threshold) · [Preparing the Source](#preparing-the-source) · [Placeholders and Tags](#placeholders-and-tags) · [Prompted LLM Translation](#prompted-llm-translation) · [Choosing and Testing an Engine](#choosing-and-testing-an-engine) · [Automatic Metrics](#automatic-metrics) · [Confidentiality](#confidentiality) · [Labeling](#labeling) · [What To Write Down](#what-to-write-down)

**Before proposing MT on a content type**, read `## Environment` in `~/Clawic/data/translate/memory.md`: which engine was used for this client, how it behaved, and what `mt_policy` and the client's contract allow.

## Where MT Belongs

| Content | Verdict |
|---|---|
| Internal comprehension — "what does this email say" | Yes, raw, labeled as machine output |
| Support tickets and chat, both directions | Yes, with post-editing on the outbound side |
| High-volume, low-value catalog and listing text | Yes, full post-editing, sampled QA |
| Documentation and help articles | Usually, full post-editing against the glossary |
| UI strings | Sometimes: short strings with no context are where MT is weakest, and where a mistake is most visible |
| Marketing and brand copy | No — transcreation is not a translation task (`transcreation.md`) |
| Legal, medical, safety, regulated claims | Never, whatever `mt_policy` says (`legal-medical.md`) |
| Anything under an NDA that forbids third-party processing | Never, regardless of quality |
| Low-resource language pairs | Treat output as a hint, not a draft; error rates are qualitatively different |

## The Five Failures

`SKILL.md` Rule 8's checklist, run before reading for style. Each is a smooth, fluent sentence that is wrong — which is why reading for style first hides them.

1. **Negation.** Dropped, doubled, or moved to the wrong clause. Search the source for every negative and confirm it in the target; this is the failure with the worst consequences and the lowest visibility.
2. **Gender and agreement.** Defaults to masculine for unspecified subjects and for role nouns; loses agreement in long sentences. In targets where the reader's gender inflects the verb (`locales.md`), MT invents one.
3. **Terminology.** Ignores your glossary unless the engine was given it, and drifts between renderings across segments because each segment is translated independently.
4. **Register and politeness.** Picks a default T-V form and a default politeness level per engine, not per your style guide, and switches between them inside one document.
5. **Numbers and units.** Usually copied correctly, occasionally reformatted, and never converted — but the *separator* may change (`1,000` → `1.000`), which silently changes the value in a locale that reads it the other way (`numbers-and-names.md`).

## Other Characteristic Errors

- **Omission on long or noisy input.** Whole clauses disappear without a trace. A length-ratio sanity check catches most: compare the target-to-source character ratio against the expansion expected for the pair (`SKILL.md` Rule 5); a ratio far below expectation means text is missing.
- **Hallucination on short or degenerate input** — an empty segment, a fragment, a list of numbers, a repeated character. Output appears that has no source at all.
- **Ambiguity resolved confidently and wrongly.** A one-word UI string has no context, so the engine picks the frequent sense: `Open` as an adjective, `Left` as a direction when it meant remaining.
- **Names and entities mangled**: translated when they should be kept, transliterated inconsistently, or inflected into something unrecognizable.
- **Idioms taken literally**, or replaced with an unrelated target idiom that changes the register.
- **Consistency drift**: the same source sentence in two places gets two targets, because there is no memory between calls.

## Post-Editing Levels

Agree the level in writing before starting; the two are different jobs at different prices.

| Level | Target | Acceptable in the output |
|---|---|---|
| Light | Accurate and understandable | Awkward phrasing, uneven style, machine flavor — as long as nothing is wrong |
| Full | Indistinguishable from a human translation | Nothing a reviewer of human work would flag; terminology, register and style all correct |

The professional standard for full post-editing (ISO 18587) is exactly that indistinguishability requirement. Two rules follow: **light post-editing is not a discount on full**, and a client asking for "quick MT cleanup" on customer-facing text is asking for full post-editing at a light price — say so before accepting.

What both levels require: correct meaning, no omissions or additions, glossary compliance, no offensive or nonsensical output, and formatting and placeholders intact.

## The Retranslate Threshold

Edit distance is the ratio of edits to source words. **Above roughly 30%, delete the segment and translate it fresh.** Two independent reasons: past that point retyping is faster than repairing, and heavy post-editing leaves the machine's sentence structure embedded in the target, which is exactly the residue readers perceive as translated text.

Setting the threshold in the tool matters more than watching it manually: an editor anchored on a bad segment will keep repairing it well past the point where starting over was cheaper.

## Preparing the Source

MT quality is bounded by input quality, and the cheapest gains are here:

- One sentence per segment, no soft line breaks inside sentences (they split the sentence and the engine translates fragments).
- Fix source typos, missing punctuation and inconsistent terminology first — each of them multiplies through every target language.
- Expand abbreviations and remove ambiguous pronouns where the source allows.
- Give the engine whole sentences, not concatenated fragments (`SKILL.md` Rule 3 again, from the other direction).
- Where the source is written for translation (controlled language, `documents.md`), MT output improves measurably across every pair at once.

## Placeholders and Tags

- MT engines reorder, translate, or drop placeholders and inline tags. Protect them: use the engine's tag-handling mode, mask them before sending and restore after, or use a CAT tool that does both.
- Verify parity after MT, per segment, as a mechanical check (`software-strings.md`). A `%s` translated into `%s` in Cyrillic script is a runtime crash.
- Never send a whole JSON or XML catalog to a generic engine as text. The structure is not content, and repairing a mangled file costs more than the translation.

## Prompted LLM Translation

A general model prompted to translate behaves differently from a dedicated MT engine: better at using context, following a glossary and holding a register; worse at staying inside the task.

Rules that make it usable:

- **Supply the glossary, the register, the audience and the target locale in the instruction.** This is the one real advantage over classical MT — an engine cannot be told to use `usted` and this glossary; a model can.
- **Translate in context blocks**, not segment by segment, so pronouns and terminology cohere — then verify the block came back with the same number of segments.
- **Forbid commentary and forbid "improvement".** Models silently fix perceived errors in the source, drop repetition they judge redundant, and add explanatory clauses. Every one of those is a defect in a translation.
- **Check length ratio and segment count on every response**: omission is the failure mode that fluent output hides best.
- Expect inconsistency across calls: the same sentence in two batches can come back two ways. A glossary and a memory are what stabilize it (`translation-memory.md`).
- Refusals and safety filtering can silently truncate content in legitimate texts (medical, legal, fiction with violence). A missing paragraph is not always the model's opinion — check the output length before assuming the source was short.

## Choosing and Testing an Engine

Test on **your own content**, never on a vendor demo: take 50 representative segments per pair, run every candidate engine, strip the engine names, and have a native reviewer rank them. Engines differ by pair and by domain, so the winner for one language is not the winner for the next.

Use the engine's own terminology and formality features where they exist (glossary upload, formality parameter, adaptive or domain-tuned models) — they address failures 3 and 4 directly and are usually free with a paid tier.

Re-run the test when the engine ships a new model. That is what the `on change` cadence in `## Due` is for.

## Automatic Metrics

- **BLEU is a corpus-level metric.** Using it on single segments, or comparing BLEU scores computed with different tokenizations, produces numbers that mean nothing. chrF is more robust for morphologically rich targets; neural metrics such as COMET correlate better with human judgment.
- No automatic metric replaces a human review for a deliverable. Use them to compare engines or track a trend, never to sign off a file.
- A "quality estimation" score per segment is a triage signal — which segments to look at first — not a pass mark.

## Confidentiality

- Sending text to a hosted engine is disclosure to a third party. Consumer tiers of several services retain input and may use it for training; paid or enterprise tiers usually offer no-logging and no-training terms in writing.
- Before proposing MT, say which content leaves the machine and under which terms. If the material is under NDA, personal, medical, or legal, propose a workflow that does not send it — a local model, the client's own contracted engine, or no MT at all.
- Never paste credentials, personal data or client documents into a free web interface to "just check something". That is the single most common confidentiality breach in this industry.

## Labeling

Machine output shown to end users is labeled as machine-translated with access to the original (`web.md`). Machine output delivered to a client is disclosed as such, with the post-editing level applied. Undisclosed MT sold as human translation is a professional integrity failure, and it is detectable.

## What To Write Down

- **Engine, tier, terms (logging and training), and observed behavior per content type** go in `## Environment` in `~/Clawic/data/translate/memory.md`. The engine's weaknesses on this client's text are the most valuable thing here, because they tell the next session what to check first.
- The **blind engine comparison** and its result is an `artifacts/mt-engine-test-<pair>.md`, with the date and the sample size, plus its `## Boxes` line in the same turn — it is re-run, not remembered.
- Any post-editing level agreed with a client goes in the client's brief artifact, and the delivery row records which level was applied (`deliveries/<year>.md`).
- "Re-check MT output after an engine or model change" is a standing **`## Due`** row with the `on change` cadence (`memory-template.md`).
