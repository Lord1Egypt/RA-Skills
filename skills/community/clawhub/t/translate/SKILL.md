---
name: Translate
slug: translate
version: 1.0.2
description: 'Translates and localizes text, software strings, documents, subtitles, and marketing copy between any language pair. Use when translating anything, when fixing a translation that reads machine-made, or when localizing a product: ICU plurals and gender, placeholders that must survive, string catalogs (JSON, XLIFF, .po, .strings, .xcstrings, ARB, RESX, YAML), locale codes and fallback chains, RTL and bidi breakage, CJK typography, mojibake, text expansion that overflows the UI, subtitle timing and reading speed, hreflang and multilingual SEO, glossaries, translation memory and fuzzy matches, and post-editing machine output. Use when choosing register (tu/vous, tú/usted, du/Sie, keigo), between es-ES and es-419 or zh-Hans and zh-Hant, or when a certified, legal, or medical translation carries liability. Not for writing original copy natively in one language (spanish, french, german, japanese, chinese) or generating captions from audio (video-captions).'
homepage: https://clawic.com/skills/translate
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    displayName: Translate
    emoji: 🌐
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/Clawic/data/translate/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/finances/
    - ~/Clawic/profile.yaml
    - ~/translate/
    - ~/clawic/translate/
  category: text
  difficulty: intermediate
  os: all
  tags:
  - translation
  - localization
  - languages
  - formatting
  openclaw:
    requires:
      config:
      - ~/Clawic/data/translate/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/finances/
      - ~/Clawic/profile.yaml
      - ~/translate/
      - ~/clawic/translate/
---

**Data.** At the start of every session, read `~/Clawic/data/translate/config.yaml` (what the user declared) and `~/Clawic/data/translate/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Before translating into a locale, open the glossary and the style box that `## Boxes` names for it: a term rendered differently from last month is a defect, even when both renderings are correct. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a term decided, a term rejected, a do-not-translate item, a register or variant decision for a locale, a language pair used for the first time, a delivered job and its word count, a reviewer's correction, an environment fact that cost effort to find (which file the strings live in, the plural rules the framework actually applies, a font that lacks a script), or something the user will re-read — a locale style guide, an LQA report, a translation brief, an approved reference text. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People and jobs go to the shared boxes, not here.** A translator, reviewer, or agency is a row in `~/Clawic/data/contacts/contacts.md`; a localization effort the user tracks as work in progress is `~/Clawic/data/projects/<project>.md`; what they pay for a CAT tool, an MT API plan, or an agency retainer is a row in `~/Clawic/data/finances/subscriptions.md`. Read the box before adding to it and update the existing entry in place — formats and identity keys are in `memory-template.md`, which carries them so the skill works whether or not the user has the owning skills installed.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. MT and CAT platforms are the temptation: store the pointer and strip the value — `env:DEEPL_AUTH_KEY`, `keychain:phrase-token`, `1password:Work/Lokalise/api`. If data sits at an old location (`~/translate/` or `~/clawic/translate/`), move it to `~/Clawic/data/translate/`, and say in one line that you moved it and from where.

A translation is wrong when a reader who never sees the source would still notice something is off, or when a reader who does see the source finds a claim that was not made. Everything below serves those two tests. Name the target locale, not just the language, before writing the first word — `es` is not a locale and `zh` is not a script. Work from defaults immediately: never open with questions about tooling, register, or how proactive to be. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, currency) → the Configuration table default.

## When To Use

- Translating anything: a sentence, a document, a repository of UI strings, a subtitle file, a slide deck, a contract
- Reviewing or repairing an existing translation — machine-made register, inconsistent terminology, a reviewer's complaint, a bug report in a language nobody on the team reads
- Localizing a product: extracting strings, plurals and gender, placeholder safety, pseudolocalization, expansion budgets, locale codes and fallbacks, RTL layout
- Deciding the locale question itself: es-ES versus es-419, zh-Hans versus zh-Hant, formal versus informal address, which locales to launch and in what order
- Running the work: scoping and quoting a job, briefing a translator, building a glossary, wiring translation memory, setting up post-editing, scoring quality
- Regulated output where a mistranslation has consequences: contracts, patents, clinical documents, device instructions, financial statements, anything requiring certification
- Not for writing original copy natively in one language (`spanish`, `french`, `german`, `japanese`, `chinese` — those teach how to sound native when nothing is being translated) or transcribing and time-coding captions from audio (`video-captions`, `speech-to-text-transcription`); this covers the source-to-target crossing itself, including translating a caption file those skills produced

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| Plain text or a document to translate, nothing exotic | Identify locale, register and audience; translate at sentence level; run the Output Gates | — |
| UI strings, a catalog file, a `%s` that must survive | Placeholders are payload; plurals come from CLDR for the target (Rule 4) | `software-strings.md` |
| Text overflows the button, the label, the column | Expansion budget by source length — the table below, before design freeze | `software-strings.md` |
| `?????`, `Ã©`, `æ¼¢`, or tofu boxes in the output | Encoding, not translation: decode chain, then font coverage | `rtl-and-scripts.md` |
| Arabic or Hebrew: punctuation at the wrong end, numbers reversed | Bidi isolation, not string reversal | `rtl-and-scripts.md` |
| Long document, DOCX/PDF/slides, footnotes and tables | Extract structure first, translate segments, reassemble, then check layout | `documents.md` |
| Website, CMS, Markdown, help center, or hreflang | Translatable attributes, URL policy, reciprocal hreflang, per-locale keywords | `web.md` |
| SRT, VTT, dubbing script, or subtitles out of sync | Reading speed and line budget first, frame rate second | `subtitles.md` |
| Slogan, campaign, joke, pun, poem, or a brand voice to carry | Transcreation: brief on effect, deliver options with back-translations | `transcreation.md` |
| Contract, patent, clinical, financial, or "it must be certified" | Route by regime; back-translation for the risk-bearing segments | `legal-medical.md` |
| Game text: dialogue variables, character limits, ratings | Variable-safe grammar, on-build LQA, culturalization pass | `games.md` |
| "Is this translation any good?" | Error typology and a score with a stated formula, not an opinion | `quality.md` |
| Same term keeps coming out differently | Glossary and do-not-translate list, enforced at delivery | `terminology.md` |
| TM, TMX, XLIFF, fuzzy matches, or a discount grid | Leverage math and the segmentation that decides it | `translation-memory.md` |
| MT output to post-edit, or "can we just machine-translate this?" | Five-failure checklist, post-editing level, when MT is banned | `machine-translation.md` |
| Which locale code, which variant, which fallback | BCP 47 shape, variant policy, register defaults per language | `locales.md` |
| Numbers, dates, currency, addresses, names, sorting | Format from the locale, never translate the digits | `numbers-and-names.md` |
| Scoping, quoting, briefing a translator, deadlines | Word counts, throughput figures, brief contents, handoff | `jobs.md` |
| Anything else | Translate it, then state the two assumptions you made (audience and register) so the user can correct one | — |

Coverage map: `software-strings.md` i18n catalogs and placeholders · `locales.md` codes, variants, register · `rtl-and-scripts.md` bidi, CJK, encoding · `numbers-and-names.md` locale data formats · `documents.md` long-form and structured files · `web.md` sites, CMS, multilingual SEO · `subtitles.md` subtitling and dubbing · `transcreation.md` marketing, literary, humor · `games.md` game localization · `legal-medical.md` regulated and certified work · `terminology.md` glossaries and DNT · `translation-memory.md` TM, XLIFF, fuzzy grids · `machine-translation.md` MT and post-editing · `quality.md` review, MQM, acceptance · `jobs.md` scoping, briefs, vendors.

## Core Rules

1. **Translate the sentence, never the word — and never past the sentence without saying so.** Word-level fidelity produces text that is accurate and unreadable; paragraph-level freedom produces text that is readable and unfaithful. The unit is the sentence, with the paragraph as context. When a sentence must be split, merged, or reordered to work in the target, that is a normal decision; when a claim, a number, or a hedge changes, that is a defect. Signal test: a bilingual reader can point at the source clause that carries every claim in your target.
2. **No string is translated without its context, and a missing context is stated, not guessed.** `Open` is a verb on a button and an adjective on a status badge, and the two are different words in most languages. Demand the screenshot, the `msgctxt`, or the developer comment; when none exists, translate for the most likely use and record the assumption in the delivery note. A catalog whose keys are the English text (`"Open": "Open"`) makes this impossible and is a defect to report (`software-strings.md`).
3. **Never build a sentence by concatenation.** `"Deleted " + n + " items"` has one word order in English and several in Turkish, Japanese, and Arabic, and it hides the agreement that Slavic and Semitic languages require. One message equals one string with named placeholders and ICU plural or select forms. This is the single most expensive i18n defect to retrofit, because fixing it changes code, not text.
4. **Plural forms come from CLDR for the target, never mirrored from the source.** English has two categories (`one`, `other`); Russian, Polish and Czech have four; Arabic and Welsh have six; Japanese, Chinese, Korean, Vietnamese and Thai have one. A catalog that only exposes `one`/`other` renders Russian wrong for 2, 21, and 101 — and the code, not the translator, is at fault. Check the target's categories before filling the file (table in `software-strings.md`).
5. **Budget expansion from source length, before layout freezes.** Short strings expand most. From English, plan for: 1-10 chars → up to +200%; 11-20 → +100%; 21-30 → +80%; 31-50 → +60%; 51-70 → +40%; 70+ → +30% (IBM's globalization table, the industry default). German, Finnish and Russian sit at the top of the range; CJK contracts by roughly a third but needs larger line height. A UI tested only in English has not been tested.
6. **One term, one rendering, written down the first time it is decided.** Consistency beats elegance: a reader who meets two words for one concept assumes they are two concepts. The first time a term is chosen, it becomes a glossary row with its part of speech and the reason; the first time one is rejected, it becomes a forbidden rendering. Boxes and formats: `memory-template.md`, mechanics in `terminology.md`.
7. **Register is a per-locale decision made once and reused.** T-V distinction (tu/vous, tú/usted, du/Sie), Japanese politeness level, Korean speech level, and Arabic MSA versus dialect are not sentence-level choices — switching mid-product is the most visible amateur signal there is. Default from `formality`; a stated preference becomes the locale's row in memory in the same turn (`locales.md`).
8. **Machine output is a draft with a known failure list.** Before reading MT for style, check five things in order: dropped or inverted negation, gender and number agreement, terminology against the glossary, politeness level, and numbers or units copied unchanged. Governed by `mt_policy`; MT is never the deliverable for legal, medical, or safety text (`machine-translation.md`).
9. **Nothing risky ships on one pair of eyes.** ISO 17100 defines a translation service as translation plus revision by a second person; where a second person is impossible, the substitute is a delayed self-review (minimum a few hours later, target-language only, source hidden) plus a back-translation of the risk-bearing segments — numbers, dosages, negations, obligations, deadlines, names. Define which segments are risk-bearing before starting, not after (`quality.md`).

## What Breaks, and What It Means

Decode rule: the layer that shows the damage names the cause. Garbled characters are bytes; wrong grammar around a number is a plural rule; a string that never changes was never extracted.

| Symptom | Most likely cause | First move |
|---|---|---|
| `Ã©`, `â€™`, `Ã±` | UTF-8 bytes decoded as Latin-1 somewhere in the chain | Find the one hop that assumes a legacy encoding; never "fix" by re-typing characters (`rtl-and-scripts.md`) |
| `?????` or `_____` where text should be | Lossy conversion to a single-byte charset, usually at a database or export boundary | Column charset and connection charset, then re-export from the source |
| Empty boxes (tofu) or a fallback face | Font lacks the script — a rendering problem, not an encoding one | Check font coverage for the script, not the file |
| String stays English no matter the locale | Never extracted, or the framework never got the locale | Grep for the literal in source; then confirm the resolved locale at runtime (`software-strings.md`) |
| Crash or `%!s(MISSING)` after translation | Placeholder count or order changed in the target | Placeholder parity check per segment (Output Gates); use positional forms (`%1$s`) |
| Wrong grammar at 2, 21, or 101 items | Target's CLDR categories missing from the catalog | Add the missing categories at the file level (Rule 4) |
| Korean text shows `이(가)` or `을(를)` | Particle chosen by the previous syllable's final consonant, impossible with concatenation | Rewrite the sentence to avoid the particle, or use a framework that inflects (`locales.md`) |
| Arabic sentence ends with the period on the left | The bidi algorithm working correctly on text lacking isolation | Wrap embedded LTR runs in isolates; never reverse the string (`rtl-and-scripts.md`) |
| Text truncated or the button grew a scrollbar | Expansion (Rule 5) | Re-measure at the target length; shorten the source before shortening the translation |
| Subtitles drift progressively out of sync | Frame-rate conversion, usually 23.976 versus 25 | Ratio-scale every timestamp, do not offset (`subtitles.md`) |
| Translated pages not indexed or the wrong one ranks | Non-reciprocal hreflang, or an invalid region code such as `en-UK` | Reciprocity and self-reference audit (`web.md`) |
| Same term in three renderings within one release | No glossary, or a TM containing all three | Consolidate, then enforce at delivery (`terminology.md`) |
| Reviewer says "correct but not how we say it" | Register or variant mismatch, not an error | Rule 7 — decide the locale's register and record it in `## Locale Register` |
| Anything else | Reproduce with the smallest possible segment, in isolation, in the target locale only | — |

## Do Not Translate

The default list, before any project-specific additions (`terminology.md` holds the user's own):

Code, identifiers, and CSS classes · placeholders in every syntax (`{name}`, `{{var}}`, `%s`, `%1$s`, `$1`, `%(name)s`, `#{}`) · HTML and XML tags and their attribute names · URLs, paths, and file extensions · email addresses and phone numbers · API endpoints, parameter names, header names, error codes · brand and product names unless the brand has a registered local form · units symbols (`kg`, `MB`) · license identifiers · keyboard shortcuts and key names when the target platform keeps them in English · legal entity names and their suffixes (`GmbH`, `S.L.`, `Ltd`) · citations, DOIs, ISBNs · quoted UI strings that refer to an interface the reader will see in the source language.

Two edge cases decide themselves: a **quoted error message** is translated only if the software the reader runs is localized, otherwise it must match what they will see on screen; a **brand name in CJK** is a marketing decision, not a translation one (`transcreation.md`).

## Output Gates

Before delivering any translated text:

- Is the target a locale, not a language — with its variant and script settled (`es-419`, `zh-Hant-TW`), and register applied consistently (Rules 4, 7)?
- Placeholder parity: same set, same count, same names in source and target for every segment; positional markers where the order changed?
- Every term in the glossary rendered as the glossary says, and no term on the do-not-translate list translated?
- Numbers, dates, currencies and units: values unchanged unless conversion was requested, formats adapted to the locale, and nothing silently rounded (`numbers-and-names.md`)?
- Negations, quantities, dosages, obligations ("must" versus "should") and names re-read against the source once, in isolation?
- Nothing invented and nothing dropped: every source clause has a home in the target, and no target clause lacks a source?
- Did the delivery state its two assumptions — intended audience and register — plus any segment where context was missing (Rule 2)?
- Did anything durable come out of this — a term, a rejected rendering, a register decision, a delivered job, a reviewer correction, a style guide, an LQA report? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/translate/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| source_lang | text (BCP 47) | en | Assumed source when a job does not name one; anchors the expansion table in Rule 5 |
| target_locales | list (BCP 47) | none | The locales every job covers by default; each gets its own glossary and style box |
| formality | formal \| informal \| per-locale | per-locale | The T-V, keigo and speech-level default of Rule 7; `per-locale` uses the table in `locales.md` |
| variant_policy | regional \| neutral | regional | Whether to write `es-ES`/`es-419` and `pt-BR`/`pt-PT` separately, or one neutral variant with the cost that implies (`locales.md`) |
| mt_policy | never \| draft-only \| mtpe \| free-rein | draft-only | Whether machine output may be used at all, and at what post-editing level (`machine-translation.md`); `never` for regulated content regardless of this value |
| review_stage | none \| self-review \| second-person \| back-translation | self-review | The gate Rule 9 enforces before delivery, and what `quality.md` scores |
| placeholder_style | icu \| printf \| mustache \| i18next | icu | Syntax of every generated message and plural example (`software-strings.md`) |
| catalog_format | json \| xliff \| po \| strings \| xcstrings \| arb \| resx \| yaml \| properties | json | File shape of every generated string catalog, plural block, and comment convention |
| subtitle_cps | number (chars/sec, 8-25) | 17 | Reading-speed ceiling for subtitle work and the point at which a line must be condensed (`subtitles.md`) |
| deliverable_shape | target-only \| bilingual-table \| inline-comments | target-only | Whether output is the translation alone, a source/target table, or annotated with the decisions taken |
| cat_tool | none \| trados \| memoq \| phrase \| crowdin \| lokalise \| weblate \| poedit | none | Which platform's export/import shape and fuzzy grid `translation-memory.md` writes for |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — CAT platform, MT engine choice, QA checker, terminology tool, whether files are edited in place or round-tripped through XLIFF — affects every file-shaped answer
- **Conventions** — key naming scheme, comment and `msgctxt` style, how translator notes are written, branch and PR habits for locale files, filename patterns per locale — affects generated catalogs and `web.md` URL advice
- **Platform** — where the strings live (repo, CMS, spreadsheet, TMS), target platforms (iOS, Android, web, print), font and script support available — affects extraction and `rtl-and-scripts.md`
- **Voice** — brand register per locale, inclusive-language policy, humor appetite, how far transcreation may stray from the source — affects `transcreation.md` and every marketing string
- **Risk posture** — what requires a second reviewer or certification, whether MT may touch a content type, how strictly the glossary is enforced — affects Rule 9 and `legal-medical.md`
- **Cadence** — glossary consolidation, TM cleanup, native review of high-traffic pages, re-check after an MT engine or model change — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Output register** — how much of the reasoning to show, whether alternatives are offered by default, whether back-translations accompany creative options — affects the shape of every answer

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Translating a string catalog from top to bottom | Alphabetical or file order is not narrative order; the same word gets four renderings by segment 300 | Group by screen or feature, translate the group, then sweep for terms (`terminology.md`) |
| Using the English source text as the key | Every copy edit orphans the translation, and identical English with different meanings collapses into one entry | Semantic keys plus a `msgctxt`/comment carrying the meaning (`software-strings.md`) |
| Reversing an Arabic string so it "looks right" | Storage order is logical, display order is the renderer's job — reversing produces text no Arabic reader can process | Fix the isolation, then look at it in a real RTL renderer (`rtl-and-scripts.md`) |
| Translating numbers and dates as text | `1,000` becomes `1.000` in one locale and stays a thousand in another — a wrong number is worse than untranslated | Format from locale data at render time; in prose, adapt the format and keep the value (`numbers-and-names.md`) |
| Adding `zero` because the language "has a zero form" | CLDR `zero` is a plural category, not "when count is 0" — English `0 items` uses `other` | `=0` exact match for a special zero message; CLDR categories for grammar (`software-strings.md`) |
| Accepting MT because it reads fluently | Fluency and accuracy fail independently: MT's characteristic error is a smooth sentence with the negation dropped | Run the five-point checklist before reading for style (Rule 8) |
| Post-editing a bad segment instead of retranslating | Anchoring: the edit distance grows past the point where retyping was cheaper, and the source's shape survives in the target | Above roughly 30% edit distance, delete the segment and translate it fresh (`machine-translation.md`) |
| "Neutral Spanish" as a cost saving | It exists for legal and technical text; in marketing it reads foreign in every market at once | Decide with `variant_policy`, and pick the primary market when only one variant is affordable (`locales.md`) |
| One 100% TM match reused blind | The match is textual; the surrounding context, product, or UI may have changed under it | In-context (101%) matches reuse silently; plain 100% matches get a read (`translation-memory.md`) |
| Sending the file without the brief | The translator invents the audience, the register, and the terminology, then bills for the rework | Brief with audience, register, glossary, DNT, reference, deadline (`jobs.md`) |
| Squeezing subtitles to fit the audio | Every syllable subtitled exceeds reading speed and the viewer stops watching the picture | Condense to the reading budget; the ear hears the rest (`subtitles.md`) |
| Certified means "a good translator did it" | Certification is a jurisdiction-specific procedure — sworn translator, notarization, apostille — and a good translation without it gets rejected at the counter | Identify the receiving authority's requirement first (`legal-medical.md`) |
| A decision that lives only in the chat | Re-litigated every release by whoever is translating that week | Glossary row, style box, or `artifacts/`, in the same turn (`memory-template.md`) |

## Where Experts Disagree

- **Faithful versus functional.** Skopos theory says the target's purpose governs and the source is raw material; the philological tradition says the source's form is part of its meaning. The frontier is consequence: where a reader acts on the text (instructions, contracts, dosages) fidelity to the claim wins outright; where a reader is meant to feel something (advertising, fiction, humor) the effect wins and the words are negotiable (`transcreation.md`).
- **Regional variants versus one neutral form.** Neutral Spanish, neutral Arabic and neutral Portuguese are real registers with real style guides, and they halve the cost. They also sound like nobody's home market. Practitioners split on whether neutrality is professional discipline or a budget excuse; the decidable version is content type, not preference (`variant_policy`).
- **MT-first workflows.** Some shops post-edit everything and treat from-scratch translation as an exception; others hold that post-editing caps quality below what a human would have produced unprompted, because the MT's structure survives the edit. Both agree it is content-dependent and that regulated content is out (`machine-translation.md`).
- **Gender-inclusive forms in gendered languages.** Spanish `-e`/`-x`, German `Gendersternchen`, French `écriture inclusive` — the language academies mostly object, parts of the audience expect it, and some governments restrict it in official documents. This is a brand and legal decision recorded per locale, never a default the translator picks mid-file.
- **Translating brand and product names into CJK.** Phonetic transliteration, semantic naming, or leaving the Latin name are all defensible and irreversible once the market knows you. Not a translation call: it needs the brand owner, trademark clearance in the market, and a native check for unintended readings.

## Security & Privacy

**Credentials:** this skill never asks for, stores, or transmits MT or CAT platform keys. When a workflow needs one, the pointer is recorded (`env:DEEPL_AUTH_KEY`) and the value stays in the user's environment or password manager.

**Content confidentiality:** source text is often under NDA, and machine translation means sending it to a third party. Before proposing an MT step, say which content is leaving the machine; if the material is legal, medical, personal, or marked confidential, propose a workflow that does not send it (`machine-translation.md`).

**Local storage:** preferences, glossaries, style decisions, delivery records and generated artifacts stay in `~/Clawic/data/translate/` on this machine, plus contact, project and subscription rows in the shared boxes. Terms, locale codes and word counts only — no secrets, and no full source documents unless the user asks for a reference text to be kept.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/translate (install if the user confirms):
- `spanish`, `french`, `german`, `japanese`, `chinese` — writing natively in one language, once the target text stops being a translation
- `video-captions` — generating and time-coding captions from audio before anything is translated
- `seo` — the ranking side of the multilingual pages this skill localizes
- `copywriting` — writing the source copy that transcreation will later have to carry

## Feedback

- If useful, star it: https://clawic.com/skills/translate
- Latest version: https://clawic.com/skills/translate

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/translate.
