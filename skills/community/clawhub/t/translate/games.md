# Game Localization

Games combine every hard problem in this skill — variables inside sentences, fixed-width UI, voice acting, humor, huge volume, no context — plus two of their own: platform certification and content ratings.

**Contents:** [The Text Types](#the-text-types) · [Variables Inside Sentences](#variables-inside-sentences) · [Character Limits and Fonts](#character-limits-and-fonts) · [Dialogue and Voice](#dialogue-and-voice) · [Culturalization and Ratings](#culturalization-and-ratings) · [Platform and Legal Text](#platform-and-legal-text) · [Series and Community Consistency](#series-and-community-consistency) · [LQA on the Build](#lqa-on-the-build) · [Live Games](#live-games) · [What To Write Down](#what-to-write-down)

**Before starting a title you have worked on**, read the pair's glossary and any `artifacts/char-limits-*.md` or `styles/<locale>.md` that `## Boxes` names. In a series, the glossary is the deliverable that outlives the project.

## The Text Types

Each has its own constraints and its own reviewer; a quote that treats them as one word count is wrong.

| Type | Constraint | Notes |
|---|---|---|
| UI and menus | Hard character limits | Shortest strings, worst expansion (`SKILL.md` Rule 5) |
| Dialogue | Voice, character, sometimes lip sync | The bulk of the volume in narrative games |
| Item and skill names | Very short, must be distinctive, often reused in generated sentences | The main source of variable-grammar bugs |
| Item and skill descriptions | Templated numbers and effects | Stat placeholders must survive exactly |
| Tutorial and hints | Instructional register, references to controls | Button names differ per platform and per market |
| System and network messages | Platform-mandated wording in places | Certification checks these |
| Achievements and trophies | Platform-imposed length limits | Locked and unlocked descriptions are separate strings |
| Store page and marketing | Transcreation, not translation | `transcreation.md` |
| EULA, privacy, age gate | Legal, market-specific | `legal-medical.md` |
| Patch notes | Fast, high-volume, community-facing | Terminology must match the shipped game |

## Variables Inside Sentences

The signature defect of game text: `{item} obtained!`, `{player} defeated {enemy}`, `{n} {resource} remaining`. In an inflected or gendered target, the sentence changes with the value, which is invisible to the writer.

- **Gender and number metadata on the noun** is the real fix where the engine supports it: the item table carries a gender and a plurality flag, and the message template selects the article and adjective from them.
- Where it does not, in order: write **one full sentence per case** via `select` (`software-strings.md`); rephrase to avoid agreement (`Obtained: {item}` as a label, not a sentence); or place the variable where the target's grammar is invariant.
- **Numbers in combat text need the target's plural categories**, not English's two (`software-strings.md`). Damage numbers, stack counts and timers all pass through this.
- Never let the engine build a phrase from fragments (`"+", "5", "damage"`). Word order and agreement die there, and it is the hardest defect to fix after launch because it lives in code.
- Item names get reused in menu headers, tooltips, combat logs and quest text. A name that works as a menu entry may need an article in a sentence — check every context the name appears in before settling it.

## Character Limits and Fonts

- Limits come from the UI, and they are per string. Collect them once as `artifacts/char-limits-<title>.md` and hand them to every translator; a translator without limits will overflow, and QA will find it on a console three weeks later.
- CJK counts in full-width characters — roughly half the Latin budget in width (`rtl-and-scripts.md`).
- **Fonts in games are often pre-generated atlases**, so a glyph that is not in the atlas renders as blank or as a placeholder box. Adding a language means regenerating the atlas with its full character set, and Chinese needs thousands of glyphs — this is a build task with real memory cost, and it must be raised before the language is promised.
- Text that is baked into textures (signs, posters, UI art) is an art task, not a translation task. List it separately in the quote.
- RTL support in a game engine is rarely free: mirrored HUDs, bidi text in dynamic strings and shaped Arabic all need engine support that either exists or does not (`rtl-and-scripts.md`). Confirm before committing to Arabic.

## Dialogue and Voice

- Ask for the **character bible** — who each speaker is, their register, their verbal tics — and build the target's equivalent before the first line. A cast whose voices are indistinguishable in the target is the most common narrative complaint.
- Dialogue exported as a spreadsheet arrives out of order and without the branch structure. Ask for the scene grouping and the speaker column; translating a branching conversation line by line produces replies that do not answer their question.
- Where lines are voiced, the three sync levels and their consequences are in `subtitles.md`; cinematics usually need rhythmic sync, in-game barks only duration.
- Deliver a **pronunciation guide** for names and invented terms with the recording script, and record the chosen pronunciation in `artifacts/pronunciation-<title>.md` — the sequel will need it.
- Subtitles in games follow the same reading budget as film, and default subtitle settings are an accessibility feature: size, background, speaker labels (`subtitles.md`).

## Culturalization and Ratings

Content that is legal in one market is a refusal in another, and text is part of what triggers it.

- **Ratings boards differ** — PEGI in Europe, ESRB in North America, CERO in Japan, USK in Germany, GRAC in Korea, and China's own approval process. Descriptors are triggered by content including dialogue, so a coarser target register can move a rating.
- Markets have specific historical sensitivities: symbols and imagery restricted by law in Germany, depictions of blood and skeletons restricted in China, religious imagery and gambling mechanics elsewhere. These are usually art and design changes, but the text must not contradict the changed build.
- Real-world flags, maps, borders and national anthems are political in disputed regions (`transcreation.md`).
- Gambling-adjacent mechanics carry disclosure requirements in several jurisdictions, and the disclosure wording is prescribed.
- Culturalization decisions belong to the publisher, not the translator. The translator's job is to raise them early, in writing, with the market and the specific risk named.

## Platform and Legal Text

- Console manufacturers publish terminology requirements — how their hardware, buttons, accounts and services must be named in each language. Using the wrong word for a button is a certification failure, not a style note. Get the current terminology list per platform and treat it as a locked glossary.
- Achievement and trophy names and descriptions have hard length limits per platform and are frequently the last strings written and the first to overflow.
- Age gates, EULAs and privacy text are market-specific legal content (`legal-medical.md`), and the age itself differs by market.

## Series and Community Consistency

- A sequel must match the previous entry's terminology, even where the previous entry was wrong: players know the old names, and changing one is a community event. Where a fix is genuinely needed, it is a publisher decision with a note in the patch notes.
- Fan translations and wikis establish terms before the official release in popular series. Knowing what the community already calls something is research, not capitulation — and diverging from it needs a reason.
- Import the previous game's glossary and translation memory before starting (`translation-memory.md`). This is where TM leverage is highest in the entire industry.

## LQA on the Build

Text review in a spreadsheet cannot find the defects that matter. Linguistic QA runs on the playable build:

| Pass | Looks for |
|---|---|
| UI sweep | Overflow, clipping, wrapping, misaligned RTL, missing glyphs |
| Context pass | Correct word in the wrong grammatical role; menu labels that read as verbs |
| Variable pass | Every templated sentence with a real value, plural boundaries at 0, 1, 2, 5, 21 |
| Voice pass | Line matches the subtitle, sync level acceptable, pronunciation correct |
| Certification pass | Platform terminology, mandated messages, achievement lengths |
| Flow pass | Play the sequence, not the strings — branching dialogue that does not cohere shows up only here |

Bug reports carry the string ID, the screenshot, the platform and the language. A report without a string ID cannot be fixed at scale.

## Live Games

- There is no string freeze: content ships weekly, often written the same week. Glossary and TM discipline is what keeps quality from decaying, because there is no time for a review cycle.
- Event and seasonal content is culturally loaded by definition — a holiday event needs a per-market check, not a translation.
- Player-facing communication (patch notes, outage notices, refund messages) is written under time pressure and read by everyone; keep pre-approved templates per locale rather than improvising them during an incident (`artifacts/`).
- User-generated content, chat and player names need per-locale moderation lists; a word filter built for English lets through everything else and blocks innocent words in other languages.

## What To Write Down

- **In-game terminology goes to the pair's glossary**, every session, with the context it appears in. In a series this file is worth more than any single delivery.
- **`artifacts/char-limits-<title>.md`** the first time limits are collected, and **`artifacts/pronunciation-<title>.md`** when a voice recording settles names — both born as their own files, with their `## Boxes` lines and read conditions, in the same turn.
- A culturalization or rating risk raised with the publisher, and their answer, goes in **`artifacts/`** with the date. It is the record that matters if the question returns after launch.
- Each delivered batch is a row in **`deliveries/<year>.md`** with the platform noted, and the title is a shared project file if the user tracks it as work in progress (`memory-template.md`).
