# Numbers, Dates, Money, Addresses, Names

The rule that governs this whole file: **adapt the format, never the value.** A translated number that changed magnitude is worse than an untranslated one, and it is the class of defect that reaches courts and support queues.

**Contents:** [Numbers](#numbers) · [Dates](#dates) · [Times](#times) · [Currency](#currency) · [Units and Measures](#units-and-measures) · [Addresses](#addresses) · [Personal Names](#personal-names) · [Phone Numbers](#phone-numbers) · [Sorting and Search](#sorting-and-search) · [Forms and Validation](#forms-and-validation) · [What To Write Down](#what-to-write-down)

**Before formatting anything for a market**, read `## Locale Register` in `~/Clawic/data/translate/memory.md` and open `styles/<locale>.md` or any `artifacts/*-conversions.md` that `## Boxes` names. Which currency prices are quoted in, whether units get converted, and which calendar a market's documents use were settled once, per market.

In software, none of this is translated at all: the locale library formats it at render time from a raw value. Everything below is for **prose** — documents, marketing, subtitles, contracts — and for reviewing what a library produced.

## Numbers

| Element | Variation | Examples |
|---|---|---|
| Decimal separator | Period or comma | `1.5` (en, zh, ja) · `1,5` (de, fr, es, pt, ru, most of Europe and Latin America) |
| Grouping separator | Comma, period, space, apostrophe, or none | `1,234,567` (en) · `1.234.567` (de, es, it) · `1 234 567` (fr, ru, sv — SI-recommended, non-breaking) · `1'234'567` (de-CH) |
| Grouping size | Three, or 2-2-3, or none | `1,234,567` · Indian `12,34,567` (one lakh = `1,00,000`) · CJK counts in myriads: 10,000 is 一万, 100 million is 一亿 |
| Negative | Sign or parentheses | `-42` · `(42)` in accounting contexts |
| Percent | Spacing differs | `50%` (en, de) · `50 %` with a non-breaking space (fr, sv) |

- A comma and a period both mean "1500" to somebody, so **an ambiguous number in prose must be disambiguated by grouping**: write `1.500,00` or `1,500.00`, never `1,500` alone in a document that crosses locales.
- Large-magnitude words do not map: a US **billion** is 10⁹, but the long-scale *billón* in Spanish and *Billion* in German is 10¹². Translate the digits or the scale word explicitly; never carry the word across.
- Ranges and dashes: use an en dash without spaces in English (`10–20`), and follow the target's convention elsewhere; a hyphen in a range next to a minus sign is a proofreading trap.
- CJK financial and legal text sometimes spells amounts in formal numerals (壹, 貳, 叁) precisely because digits can be altered. Preserve them when they appear.

## Dates

- **Order**: DMY in most of the world, MDY in the United States, YMD in China, Japan, Korea and ISO 8601. `03/04/2026` is two different days, so in prose spell the month whenever the audience is mixed.
- **ISO 8601 (`2026-07-26`) for anything machine-read or logged**, always, in every locale.
- Month and weekday names are **lowercase** in Spanish, French, Italian, Portuguese and Russian, and capitalized in English and German. A capitalized `Enero` is an instant tell.
- Month names inflect in Slavic and Finnic languages: the genitive form used in a date differs from the nominative form in a dropdown. Never build a date by concatenating a translated month name into a numeric template (`software-strings.md`).
- Week start: Monday almost everywhere; Sunday in the US, Canada, Japan and Israel. Calendar widgets and "week 27" reports differ accordingly.
- Non-Gregorian systems appear in real documents: the Japanese imperial era (令和 8 = 2026), the Hijri calendar in Saudi Arabia, the Buddhist era in Thailand (2569 = 2026), the Republic of China era in Taiwan (民國115 = 2026). In a document, keep the original and add the Gregorian equivalent in brackets on first use.
- Relative dates ("next Friday", "in a fortnight") are ambiguous in the source before they are hard in the target. Resolve to a date, then format.

## Times

- 24-hour clock is the default in most of Europe, Latin America and Asia; 12-hour with AM/PM dominates the US, UK conversation, Australia and the Philippines. Separator is `:` almost everywhere, `.` in some British and Nordic usage.
- AM/PM is not universally translatable: many languages write it as English, others use their own markers (午前/午後 in Japanese). Let the locale library decide; in prose, follow the target's newspaper convention.
- **Time zones are part of the value.** A time without a zone in a document that crosses borders is a defect; write `14:00 CET (13:00 UTC)`, and prefer IANA zone names (`Europe/Madrid`) over abbreviations, which are ambiguous (`CST` is three different zones).
- Japanese business and broadcast schedules legitimately use hours past 24 (`25:30` = 01:30 the following day). Do not "fix" it.
- Durations are not times: `1:30` meaning ninety minutes needs a unit in the target, because the colon form is read as a clock time in many locales.

## Currency

- **Never convert an amount unless the user asked.** A price, a contract sum, a salary and a legal penalty are the value, not a quantity to be re-expressed. When a conversion is genuinely wanted, state the rate and its date in the text — an unstated rate makes the number unverifiable a month later.
- Symbol position and spacing follow the locale: `$1,234.56` · `1.234,56 €` (de) · `1 234,56 €` (fr) · `€1.234,56` (nl) · `CHF 1'234.56`. Never move a symbol without checking the target.
- **Use the ISO 4217 code when the symbol is ambiguous**: `$` is used by more than twenty currencies, so a document for a mixed audience writes `USD 1,200` or `CAD 1,200`.
- Decimal digits are a property of the currency, not the locale: JPY and KRW have none, most have two, and KWD, BHD and OMR have three. Adding `.00` to a yen amount is wrong.
- Indian financial prose uses lakh (10⁵) and crore (10⁷) with the 2-2-3 grouping; converting to millions in a document written for India removes information the reader expects.

## Units and Measures

- **Convert only when asked, and never in a specification, a legal text or a technical drawing** where the number is a requirement. In consumer prose, converting is usually right.
- When safety depends on the number (dosage, load, temperature, torque), give both: `120 kg (265 lb)`. Round the converted value to the precision of the original — `100 miles` is not `160.934 km`, it is about `160 km`.
- Paper size (A4 vs Letter) breaks layouts in translated documents (`documents.md`); clothing and shoe sizes have no linear mapping and need a size table, not a formula.
- Non-breaking space between value and unit (`5 kg`, `20 °C`) so the pair never wraps. Degrees: `20 °C` with a space, `20°` for angles without.

## Addresses

- **A mailing address is delivered by the destination country's postal service, so it is not translated.** Keep it in the destination's language and script; translate only the country name, and only into the language of the country the letter is sent *from*.
- Field order, presence and names differ: Japan writes largest unit first (prefecture → city → block → building) and the "street" often does not exist as a concept; Ireland has no universal postal code in the old sense (Eircode is per-address); many countries have no state or province at all.
- A form that requires "State" and a five-digit ZIP is an American form with translated labels. Localize the *fields*, not just the words; when that is impossible, accept a free-text address block.
- Postal codes are strings, not numbers — leading zeros are meaningful, and several countries include letters and spaces (`SW1A 1AA`, `K1A 0B1`).

## Personal Names

- **There is no universal first name and last name.** Family name comes first in Japanese, Chinese, Korean, Hungarian and Vietnamese; Spanish and Portuguese speakers carry two family names; Icelandic uses patronymics rather than family names; mononyms exist. A single "full name" field plus an optional "how to address you" field survives all of it.
- Display order is separate from storage: a Japanese name is 山田 太郎 in Japanese and often Taro Yamada in English text. Follow the target's convention and be consistent inside a document.
- Do not translate names. Transliterate only when the target script requires it, use the person's own preferred transliteration when it exists, and keep the original in brackets on first mention in academic and legal text.
- Honorifics are part of address, not of the name: Japanese `-san` never accompanies the person's own self-reference; German `Herr`/`Frau` with the family name; Spanish `Don`/`Doña` with the given name. Getting the pairing wrong is more visible than a mistranslated sentence.
- Case-changing a name is unsafe: uppercasing is impossible in CJK and Arabic, and lowercasing breaks names with internal capitals.

## Phone Numbers

Store and transmit in **E.164** (`+34612345678`), format for display per locale, and never translate or reformat a number printed in a legal or emergency context. Emergency numbers are country-specific (112 in the EU, 911 in North America, 119 in Japan) — a translated document that keeps the source country's emergency number is a safety defect.

## Sorting and Search

- Sort with a **locale-aware collator**, never by code point. Code-point order puts `Zebra` before `apple` and scatters every accented word to the end of the list.
- Locale rules genuinely conflict: German dictionary order treats `ä` as `a`, while phonebook order treats it as `ae`; Swedish and Finnish place `å ä ö` **after** `z`; Spanish sorts `ñ` after `n`, and `ch`/`ll` stopped being separate letters in 1994; Czech sorts `ch` after `h`.
- **Japanese cannot be sorted from its written form**: the reading is not derivable from kanji, so a system that sorts Japanese names must store a kana reading field alongside the name. Chinese sorts by pinyin or by stroke count, and the choice must be stated.
- Search needs the mirror of this: normalize (NFC), fold case with the locale in mind, and usually fold accents on input so `cafe` finds `café` — but never fold accents in the stored value.

## Forms and Validation

| Field | The assumption that breaks | Do instead |
|---|---|---|
| Name | Two fields, Latin letters, no apostrophes | One field, full Unicode, no regex beyond a length bound |
| Postal code | Five digits | Per-country pattern, or free text |
| State / province | Always required | Required only where the country has them |
| Phone | Fixed length, national format | E.164 with country selector |
| Date input | MM/DD/YYYY placeholder | A date picker, or an ISO placeholder with the locale's order |
| Address | US field order | Country first, then a country-appropriate field set |
| Title / salutation | Mr / Mrs | Optional and free text, or omitted |
| Character limit on a text field | Counted in bytes | Counted in grapheme clusters (`rtl-and-scripts.md`) |

## What To Write Down

- A per-market convention the user settled — which currency prices are quoted in, whether units get converted, which calendar appears in documents for a market — is a line in **`## Locale Register`** or, if it needs a paragraph, in **`styles/<locale>.md`** (`memory-template.md`).
- A conversion table the user's domain needs (sizes, grades, regulatory units) is an **`artifacts/<domain>-conversions.md`** file, born as its own file, with its `## Boxes` line and read condition, in the same turn. Deriving one costs an afternoon; nobody should pay it twice.
