# Software Strings — Catalogs, Plurals, Placeholders

Product text fails differently from prose: the defects are structural, they appear at runtime, and the person who caused them is usually the developer, not the translator. Everything here is about making the string *translatable* before anyone translates it.

**Contents:** [Before Anything: Read the Setup](#before-anything-read-the-setup) · [Keys and Context](#keys-and-context) · [Placeholders](#placeholders) · [Plurals](#plurals) · [Gender and Select](#gender-and-select) · [Catalog Formats](#catalog-formats) · [Framework Traps](#framework-traps) · [Expansion and Character Limits](#expansion-and-character-limits) · [Pseudolocalization](#pseudolocalization) · [Locale Resolution and Fallback](#locale-resolution-and-fallback) · [Store Listings and Microcopy](#store-listings-and-microcopy) · [Extraction Checklist](#extraction-checklist) · [What To Write Down](#what-to-write-down)

**Before touching a catalog you have touched before**, read `## Environment` and the pair's glossary in `~/Clawic/data/translate/memory.md` (or the file `## Boxes` points to), plus any `artifacts/char-limits-*.md` it indexes. Which file holds the strings, which plural categories the framework actually exposes, and which terms are settled were all derived once already.

## Before Anything: Read the Setup

Three facts decide everything downstream, and all three are observable in the repository:

1. **Which library renders the message** — it fixes the placeholder syntax and whether ICU is available at all.
2. **Which plural categories the catalog format can express** — a JSON file with `_one`/`_other` keys cannot hold Russian's four, and no translator can fix that from inside the file.
3. **Where the locale comes from at runtime** — a header, the OS, a user setting, or a URL segment. A string that "did not translate" is usually a locale that never resolved (`Locale Resolution and Fallback`).

## Keys and Context

- **Semantic keys, never the English text as the key.** `checkout.button.pay` survives a copy edit; `"Pay now"` as a key orphans every translation the moment marketing changes it to "Pay securely". It also collapses homographs: one `"Open"` key cannot serve a button and a status.
- **Every key carries a context note**, and the note answers three things: what part of the UI this is (button, title, toast, error), what the placeholder holds, and any length limit. Formats differ — `msgctxt` and `#.` comments in PO, `comment` in `.xcstrings`, a developer comment above the key in JSON, `<!-- -->` in `strings.xml` — but the content is the same.
- **A screenshot beats every note.** When the tooling supports attaching one (most TMS platforms do), it removes the most common class of error outright: correct words in the wrong grammatical role.
- Mark strings that must never be translated in the file itself (`translate="no"` in XLIFF, `translatable="false"` in `strings.xml`) rather than trusting a separate list nobody opens.
- **Never reuse one key in two places to save space.** The day one of the two needs a different word in German, the reuse is discovered by a user.

## Placeholders

| Syntax | Where | Notes |
|---|---|---|
| `{name}` | ICU MessageFormat, react-intl/FormatJS, Flutter ARB | Named, reorderable, and the only syntax that also carries plural and select |
| `{0}`, `{1}` | Java `MessageFormat`, .NET | Positional; .NET supports `{0:C}` format specifiers that must survive untouched |
| `%s`, `%d` | C, Python `%`, Go, PHP | **Not reorderable** — a target that needs another word order breaks |
| `%1$s`, `%2$d` | printf positional, Android | The fix for the above: always use the positional form when there is more than one argument |
| `%@`, `%1$@`, `%lld` | Apple `.strings` | `%@` is any object; `%lld` for 64-bit integers |
| `{{name}}` | i18next, Mustache, Handlebars | Double braces; single braces are literal text |
| `%{name}` | Rails, Ruby I18n | — |
| `%(name)s` | Python `%`-formatting with a dict | The `s` is part of the syntax |

Rules that hold across all of them:

- **Parity is a check, not a hope**: for every segment, the multiset of placeholders in the target equals the one in the source. A single missing `%s` is a crash in Java and Swift, and a silent `%!s(MISSING)` in Go.
- **Order may change; names may not.** Translators reorder placeholders freely when the syntax is named or positional — that is the point of positional forms.
- **A placeholder is not a word.** `You have {count} {itemType}` cannot be translated: the adjective, article and verb agreement depend on `itemType`, which is invisible. Write one full message per case, or use `select`.
- **Never wrap a placeholder in markup that the translator can break.** `<b>{name}</b>` inside a translatable string means every locale can lose the tag; prefer rich-text formatting where the library reinserts the tag by name (FormatJS `<b>{name}</b>` with a tag handler, Android `<xliff:g>`).

## Plurals

CLDR defines six possible categories — `zero`, `one`, `two`, `few`, `many`, `other` — and each language uses a subset. `other` is mandatory and is the fallback.

| Language | Categories | What an English-shaped catalog gets wrong |
|---|---|---|
| ja, zh, ko, vi, th, id, ms | `other` only | Nothing grammatically, but a translator forced into `one`/`other` writes the same string twice |
| en, de, es, it, nl, sv, da, no, fi, hu, tr, el, bg | `one`, `other` | — |
| fr, pt-BR | `one`, `other` (+`many` in recent CLDR for large magnitudes) | Note that French uses `one` for 0 and 1 |
| ru, uk, hr, sr, be | `one`, `few`, `many`, `other` | 1 and 21 differ from 2-4, which differ from 5-20; two forms produce wrong text for most numbers |
| pl, cs, sk, lt | `one`, `few`, `many`, `other` | Same shape, different boundaries — never copy Russian's rule into Polish |
| ro | `one`, `few`, `other` | `few` covers 0 and 2-19, which surprises everyone |
| sl | `one`, `two`, `few`, `other` | Dual form for exactly 2 |
| lv | `zero`, `one`, `other` | `zero` is grammatical here, unlike English |
| ar | `zero`, `one`, `two`, `few`, `many`, `other` | All six; a two-form catalog is unusable |
| cy, ga | five or six categories | Rare targets that expose the same catalog defect as Arabic |

Worked example — Russian's rule, which is the one people get wrong: `one` when n%10 = 1 and n%100 ≠ 11 (1, 21, 31, 101); `few` when n%10 is 2-4 and n%100 is not 12-14 (2, 3, 4, 22); `many` for everything else (0, 5-20, 25). So 21 takes the same form as 1, and 11 does not.

- **`zero` is a grammatical category, not "count is 0".** English `0 items` uses `other`. For a special empty-state message, use an exact match: `{n, plural, =0 {No items} one {# item} other {# items}}`.
- **Exact matches (`=1`, `=2`) beat categories only for special-cased copy**, never for grammar; a translator cannot add categories the file does not have, but they can and should ignore an exact match that makes no sense in their language.
- **Ordinals are a separate rule set**: `{n, selectordinal, one {#st} two {#nd} few {#rd} other {#th}}`. English's ordinal categories are not its cardinal ones.
- **Nested plurals are legal ICU and unreadable in practice.** Two counts in one sentence is a rewrite, not a nesting exercise.
- **Do not let the code pick the branch.** `count === 1 ? t('item') : t('items')` hardcodes English's two-form rule and no catalog can override it. This is the most common plural bug in JavaScript codebases.

## Gender and Select

`{gender, select, female {She uploaded a file} male {He uploaded a file} other {They uploaded a file}}` — and in many targets the *verb*, the *adjective* and the *article* also change, so the branch must contain the whole sentence, never a fragment.

- Provide `other` always; it is the fallback for unknown, non-binary, and for locales where the distinction is unavailable.
- Gender of a *thing* matters as much as gender of a person: `{count} new {itemType}` needs `select` on the item type, or one message per type.
- When the subject is a user-supplied name, no `select` value exists. Rewrite impersonally (`A file was uploaded by {name}`) rather than guessing.

## Catalog Formats

| Format | Plurals | Context field | Watch out |
|---|---|---|---|
| JSON (i18next, vue-i18n) | Key suffixes `_one`, `_other`, `_few` (i18next v21+) | Comment convention only | Suffix set must match the target's CLDR categories or the extra forms are dropped |
| ICU JSON / FormatJS | Inline ICU in the value | `description` field | The ICU string is machine-parsed: a broken brace kills the whole message |
| Gettext `.po`/`.pot` | `msgid_plural` + `msgstr[0..n]`, driven by the `Plural-Forms` header | `msgctxt`, `#.` comments | `fuzzy` flag means the string is *not used* at runtime; clearing it is part of finishing |
| XLIFF 1.2 / 2.0 | Depends on the extractor | `<note>` | `state` attribute (`new`, `translated`, `reviewed`, `final`) is the workflow; inline `<g>`/`<ph>` tags must survive |
| Android `strings.xml` | `<plurals>` with `<item quantity="one|few|many|other">` | XML comments | Escape `'` as `\'` and `&` as `&amp;`; a leading `@` or `?` is a resource reference |
| Apple `.strings` + `.stringsdict` | `.stringsdict` only, via `NSStringPluralRuleType` | `/* comment */` above the key | Every line ends in `;`; a missing one breaks the file silently at build |
| Apple `.xcstrings` (Xcode 15+) | Built in, per language, with variations | `comment` field | JSON, but merge conflicts are brutal — regenerate rather than hand-merge |
| Flutter `.arb` | ICU in the value | `@key` metadata object with `description` and `placeholders` | Placeholder types are declared in metadata and must match |
| .NET `.resx` | Not native — needs a plural library | `<comment>` | XML; `{0}` composite formatting with format specifiers |
| Java `.properties` | Via `ChoiceFormat`/ICU4J | `#` comment | UTF-8 since Java 9; older readers assume ISO-8859-1 and mangle accents |
| Rails YAML | `:one`, `:few`, `:other` keys | Comment only | Indentation-sensitive; a target with more categories needs more keys |
| Qt `.ts` | `<numerusform>` per category | `<comment>`, `<extracomment>` | — |

## Framework Traps

- **Java and ICU `MessageFormat` treat `'` as a quote character.** `L'utilisateur {0}` silently swallows the placeholder; the literal apostrophe must be doubled: `L''utilisateur {0}`. This bites French, Italian and Catalan on the first day and is invisible in review because the string looks correct.
- **Android**: an apostrophe or `&` unescaped fails the build or truncates at render; multiple `%s` without positions throws `IllegalFormatException` in some locales only, because the translator reordered them. `formatted="false"` disables the check rather than fixing it.
- **i18next**: the plural suffix set changed at v21 (`_plural` → `_other`, plus `_zero`/`_two`/`_few`/`_many`). A v20-shaped file loaded by v21 falls back to the singular for every count.
- **iOS `.stringsdict`**: the format key (`%#@items@`) and the variable name must match exactly, and `NSStringFormatValueTypeKey` must match the argument type (`d`, `lld`, `@`) or the plural silently resolves to `other`.
- **Vue i18n and Angular**: pipe-separated plural forms (`no items | one item | {count} items`) map to positions, not categories — usable only for two-form languages.
- **Server-side rendering**: the locale must be resolved before the first render or the page ships English and hydrates into the target, which users see as a flash and search engines see as the English page (`web.md`).

## Expansion and Character Limits

Expansion budget by source length is in `SKILL.md` Rule 5 — that table is canonical; do not restate different numbers here. What belongs in the catalog:

- **A length limit is a property of the string**, written in its comment as `[MAX 20]` and enforced at delivery, not discovered in QA. Without it, a translator has no way to know the button is fixed-width.
- **Count what the renderer counts.** For CJK, a full-width character occupies roughly two Latin character widths; a 20-character limit means about 10 full-width characters. Say which you mean in the comment.
- **Short strings are the dangerous ones.** `On`/`Off` become `Ein`/`Aus`, `Encendido`/`Apagado` — the last pair is over 200% longer, which is exactly what the table predicts and what a toggle switch cannot absorb.
- When the limit cannot be met, the fix is upstream: change the source string, change the component to wrap or scale, or use an icon with a tooltip. Truncating the target with an ellipsis is a last resort and must be reported, never done silently.

## Pseudolocalization

The cheapest localization test, runnable before a single word is translated. Transform every extracted string by: padding to +30-40% length, replacing Latin letters with accented look-alikes, and wrapping in visible delimiters — `[!!! Ĥéļļö Ŵöŕļď !!!]`.

What each part catches: the **padding** finds truncation and layout breaks; the **accents** find encoding loss and fonts missing glyphs; the **brackets** find truncation at the boundary and, when a string appears unwrapped, prove it was never extracted; running it as an **RTL pseudo-locale** (`ar-XB` on Android and Chrome, alongside `en-XA`) finds unmirrored layout without needing Arabic text.

Run it on every screen before the string freeze, and record the findings as `artifacts/pseudoloc-findings-<app>.md` with the screens that broke — the same screens break again next release.

## Locale Resolution and Fallback

- The chain is: explicit user setting → account preference → `Accept-Language` or OS locale → default. Log which one won when debugging; "the translation is missing" is usually "the locale was never `pt-BR`, it was `pt`".
- **Fallback must degrade by specificity, not alphabetically**: `pt-BR` → `pt` → default. A missing key in `pt-BR` should show Portuguese, not English, and never a raw key.
- Never show a raw key to a user. A missing translation renders the source string; a missing *source* string is a bug the build should have caught.
- Region-only differences (`en-GB` vs `en-US`) are usually a small override file over a shared base, not a full duplicate catalog. Duplicating guarantees the two drift.

## Store Listings and Microcopy

- App store metadata is localized separately from the app and has hard limits: title, subtitle, short description, keyword field. Keywords are researched per market, never translated (`web.md` covers per-locale keyword work).
- Screenshots contain text. A localized listing with English screenshots reads as abandoned; the screenshot text is a string set of its own and belongs in the same freeze.
- Error messages, empty states and permission prompts are the highest-read microcopy in a product and the most often left in English because they live in code, not in the catalog. Grep for user-facing literals in error paths specifically.
- Legal and consent strings (privacy notice, cookie banner, terms acceptance) are translation with liability attached — route them through `legal-medical.md`, not through the normal string flow.

## Extraction Checklist

Before sending anything to a translator:

| Check | Passing looks like |
|---|---|
| Hardcoded strings | Grep for user-facing literals; pseudolocalization proves it empirically |
| Concatenation | No string built by `+` or interpolation of translated fragments (`SKILL.md` Rule 3) |
| Placeholders | Positional or named everywhere there is more than one |
| Plurals | Every count-bearing message is a plural message, with the categories the target needs |
| Context | Every key has a comment or a screenshot; homographs are separate keys |
| Length limits | Marked in the comment where the UI is fixed-width |
| Non-translatables | Marked in the file, not in a side list |
| Dates, numbers, currency | Formatted by the locale library, never assembled from translated fragments (`numbers-and-names.md`) |
| Sort order | Lists sorted with a locale-aware collator, not by code point (`numbers-and-names.md`) |
| Images and icons | No text baked into images; no gestures, hands, or flags used to mean a language |

## What To Write Down

Three destinations (`memory-template.md`):

- **`## Environment` in `~/Clawic/data/translate/memory.md`**: which files hold the strings, the library and its version, which plural categories the format exposes, how the locale resolves. This is what stops the next session from re-deriving the setup, and it is what makes a plural bug diagnosable in one line.
- **The pair's glossary** for every UI term settled here — button verbs and object nouns are the terms that get re-decided most often.
- **`artifacts/char-limits-<surface>.md`** the first time length limits are collected, and **`artifacts/pseudoloc-findings-<app>.md`** after a pseudolocalization pass. Both get their `## Boxes` line, with a read condition naming the surface, in the same turn.
