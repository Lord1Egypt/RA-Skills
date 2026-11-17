# Locales — Codes, Variants, and Register

A language is not a locale. Picking `es` instead of `es-419` is the difference between text that fits a market and text that sounds imported, and picking `zh` instead of `zh-Hant` produces characters half the readers cannot use.

**Contents:** [BCP 47 in One Pass](#bcp-47-in-one-pass) · [Codes People Get Wrong](#codes-people-get-wrong) · [Fallback Chains](#fallback-chains) · [Variants Worth Splitting](#variants-worth-splitting) · [Register Defaults](#register-defaults) · [Per-Language Notes](#per-language-notes) · [Choosing Which Locales To Launch](#choosing-which-locales-to-launch) · [What To Write Down](#what-to-write-down)

**Before writing into a locale**, read `## Locale Register` in `~/Clawic/data/translate/memory.md` and open `styles/<locale>.md` if `## Boxes` names it. Register was decided once; re-deciding it mid-product is the defect Rule 7 exists to prevent.

## BCP 47 in One Pass

Shape: `language[-Script][-REGION][-variant]`, and each part has its own standard — language from ISO 639-1 (two letters) or 639-3 where no two-letter code exists, script from ISO 15924 (four letters, title case: `Hans`, `Hant`, `Latn`, `Cyrl`, `Arab`), region from ISO 3166-1 alpha-2 (two letters, uppercase) or UN M.49 (three digits, for supranational areas such as `419` = Latin America).

- Include the script **only when it disambiguates**: `zh-Hans` yes, `fr-Latn` no. Include the region when behavior differs: spelling, currency, date order, terminology.
- Case is convention, not requirement — matching is case-insensitive — but write `pt-BR`, not `pt-br`, because half the tooling in the chain compares strings naively.
- Private-use and pseudo-locales (`en-XA`, `ar-XB`) are legal subtags and are how pseudolocalization ships (`software-strings.md`).

## Codes People Get Wrong

| Wrong | Right | Why it matters |
|---|---|---|
| `en-UK` | `en-GB` | `UK` is not an ISO 3166-1 code; Google ignores the hreflang entirely (`web.md`) |
| `zh-CN` used to mean "Simplified" | `zh-Hans` (plus `-CN`/`-SG` when needed) | Script and region are different questions; Singapore uses Simplified, Hong Kong uses Traditional |
| `zh-TW` used to mean "Traditional" | `zh-Hant-TW` or `zh-Hant` | Taiwan and Hong Kong both use Traditional and differ in vocabulary |
| `iw`, `in`, `ji` | `he`, `id`, `yi` | Legacy ISO codes; the JDK still emits the old ones in places, so normalize on read |
| `no` for Norwegian text | `nb` (Bokmål) or `nn` (Nynorsk) | `no` is a macrolanguage; almost all product text is `nb` |
| `tl` for the Philippines | `fil` | `fil` is the standardized national language; `tl` is the underlying one |
| `sr` without a script | `sr-Latn` or `sr-Cyrl` | Serbian is written in both, and readers do not want the other |
| `es-LA` | `es-419` | `LA` is Laos |
| `pt` for Brazil | `pt-BR` | Different spelling, vocabulary, and register from `pt-PT` |
| `gb`, `us` as language codes | `en-GB`, `en-US` | The region is never the language |

## Fallback Chains

Degrade by specificity, one subtag at a time: `zh-Hant-HK` → `zh-Hant` → `zh` → default. Never fall back sideways (`pt-BR` → `pt-PT` is a business decision, not a default), and never fall back to English silently in a market where partial English is worse than a missing feature.

- Region-only variants are best built as a small **override file** over a shared base: `en-GB` holds the 40 strings that differ from `en-US`, not a full copy. Two full copies drift within one release.
- A user's preferred-language list (`Accept-Language: pt-BR,pt;q=0.9,en;q=0.8`) is ordered — honor the order, and match on the longest supported prefix rather than on exact equality.

## Variants Worth Splitting

`variant_policy: regional` splits these; `neutral` merges them and accepts the cost.

| Pair | Diverges in | Merge is defensible when |
|---|---|---|
| es-ES / es-419 | vocabulary (ordenador/computadora, móvil/celular), `vosotros` vs `ustedes`, register | Technical documentation, legal text, developer docs |
| es-419 / es-MX / es-AR | voseo in Argentina and much of Central America, local vocabulary | Almost always — `es-419` is a real, written standard |
| pt-BR / pt-PT | vocabulary, verb placement, gerund usage, second person | Rarely; these read as clearly foreign to each other |
| fr-FR / fr-CA | terminology enforced by Quebec's language body (courriel, clavardage), typography | Internal tools; never consumer or public-sector text in Quebec |
| de-DE / de-AT / de-CH | months (Jänner), vocabulary, and Swiss German never uses `ß` | Usually mergeable to `de-DE` plus a Swiss `ß`→`ss` transform |
| en-US / en-GB | spelling, date order, vocabulary, punctuation inside quotes | Internal tools; not marketing or anything with dates |
| zh-Hans / zh-Hant | script **and** vocabulary — not a character mapping | Never automatically (see below) |
| ar-SA / ar-EG / MSA | dialect for marketing; MSA is the written standard | Documentation and UI: MSA. Ads and social: dialect wins |

**Simplified to Traditional is not a conversion.** One simplified character can map to several traditional ones (发 → 發 "issue" or 髮 "hair"; 干 → 乾 / 幹 / 干), and the technical vocabulary differs independently of the script (软件 / 軟體 / 軟件 for "software" in CN / TW / HK). A script converter produces text that is readable and visibly machine-made; treat `zh-Hant` as its own target with its own reviewer.

## Register Defaults

What `formality: per-locale` applies when the user has stated nothing. Product UI assumed; marketing is often one step warmer.

| Locale | Default address form | Notes |
|---|---|---|
| de, at | `Sie` in product, `du` increasingly in consumer apps | Pick once per brand; switching is the most-noticed inconsistency in German |
| fr | `vous` | `tu` only for youth or gaming brands |
| es-ES | `tú` in product, `usted` in finance, health and public sector | — |
| es-419 | `tú`; `usted` in Colombia and much of Central America | Voseo (`vos`) only for a single-country Argentine target |
| pt-BR | `você` | `tu` reads regional |
| it | `tu` in product, `Lei` in formal or B2B | — |
| nl | `je` in product, `u` in finance and government | — |
| pl | third-person `Pan`/`Pani` in formal; direct `ty` in consumer apps | Polish formality is a grammatical construction, not a pronoun swap |
| ru, uk | `вы`/`ви`, lowercase in general address | Capitalized `Вы` is for addressing one named person in a letter |
| ja | `desu`/`masu`; no honorific escalation in UI | Keigo levels in `styles/<locale>.md` if the brand needs them |
| ko | `해요체` (polite) in UI, `합니다체` for formal notices | Particles depend on the preceding syllable (see below) |
| zh | neutral polite; 您 for finance and formal notices | — |
| ar | MSA, formal | Dialect for advertising only |
| sv, da, nb, fi | informal `du`/`sinä` universally | Formal forms read archaic or sarcastic |
| tr | `siz` | — |
| hi | `आप` (aap) | `तुम` is too familiar for product text |
| vi | pronoun depends on the reader's age and relationship | Default `bạn`; anything else needs a brand decision |
| th | polite particles (ครับ/ค่ะ) are gendered by the *speaker* | For a brand voice, pick one and record it in `styles/th.md` |

## Per-Language Notes

- **Japanese**: no spaces between words; line breaking follows kinsoku rules (a line never starts with 。、」or a closing bracket); no grammatical plural; particles carry the roles that word order carries in English, so a reordered placeholder changes the meaning rather than the style. Full-width punctuation, and ASCII digits are normal in product text.
- **Korean**: subject and object particles alternate by the previous syllable's final consonant (`이/가`, `을/를`, `은/는`). A template like `{name}이(가)` is the visible symptom of a system that cannot inflect — rewrite to avoid the particle, or place the name where a fixed particle works.
- **Chinese**: no spaces, full-width punctuation, and a space is conventionally inserted between Han characters and Latin words in high-quality typography. Measure words (个, 张, 本) depend on the noun, so counted messages need the noun to be part of the string.
- **Arabic and Hebrew**: right-to-left, with all the layout consequences in `rtl-and-scripts.md`. Arabic has dual number and six plural categories; Hebrew has grammatical gender on verbs, so a message addressed to the user changes with the user's gender — provide a neutral phrasing or a `select` (`software-strings.md`).
- **German**: nouns are capitalized; compounds are single words and are the main cause of overflow; Switzerland writes `ss` where Germany writes `ß`; quotation marks are „…" .
- **French**: a non-breaking space precedes `; : ! ?` and sits inside `« »` in France (Canadian French uses it only before the colon); the space must be non-breaking or the punctuation wraps to the next line alone.
- **Spanish**: opening `¿` and `¡` are not optional; capitalization in headings is sentence case, not title case — a title-cased Spanish heading is an instant tell.
- **Russian, Polish, Czech**: case endings mean a noun cannot be inserted into a slot without agreement; this is the deepest reason Rule 3 bans concatenation.
- **Turkish**: agglutination makes any string with a suffixed placeholder unsafe, and the dotless `ı`/dotted `i` pair breaks locale-sensitive case conversion — `"I".toLowerCase()` under the `tr` locale yields `ı`, which turns identifier comparison into a bug. Case-fold identifiers with the invariant locale, always.
- **Thai and Lao**: no spaces between words; line breaking needs a dictionary, so a naive renderer wraps mid-word. Do not insert spaces to "help".
- **Finnish and Hungarian**: heavy case systems and long compounds; expect the top of the expansion range.
- **Ukrainian**: not Russian with different spelling. Terminology diverges deliberately, and using Russian-derived terms is read as a political statement.
- **Catalan, Basque, Galician, Welsh, Irish**: co-official languages with legal presence requirements in their regions. Treat them as full targets, never as fallbacks to the state language.

## Choosing Which Locales To Launch

Decide by evidence in this order, and stop at the first one that gives a clear answer: existing traffic and signup share by country (already in the analytics); competitor coverage in the market; support ticket language; then market size. Rank by expected revenue per locale, not by speaker count — a language with 300 million speakers and no payment method is not a market.

Cost per locale is not the translation: it is translation plus review plus every future release plus support in that language. A locale added is a permanent commitment; three locales done well beat eight half-maintained, and a half-maintained locale is visible to users as mixed-language screens.

## What To Write Down

- Every register, variant and script decision goes in **`## Locale Register`** in `~/Clawic/data/translate/memory.md`, one row per locale, with the date it was decided.
- Anything longer than a line — punctuation rules, voice, worked examples, keigo policy — becomes **`styles/<locale>.md`**, born as its own file, with its `## Boxes` line and a read condition naming the locale, in the same turn.
- A launch decision (which locales, in what order, why) is an **`artifacts/`** file if it has reasoning worth keeping, and a line in the shared project file if the user tracks the launch as a project (`memory-template.md`).
