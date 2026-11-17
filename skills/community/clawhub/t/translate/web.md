# Web — Markup, URLs, CMS, and Multilingual SEO

Web localization has a second audience: the crawler. A page can be perfectly translated and still invisible, or perfectly indexed and served to the wrong country. Both are configuration, not language.

**Contents:** [Markup: What Is Translatable](#markup-what-is-translatable) · [Inline Tags](#inline-tags) · [Markdown](#markdown) · [URL Structure](#url-structure) · [hreflang](#hreflang) · [Language Switching and Redirects](#language-switching-and-redirects) · [Multilingual SEO](#multilingual-seo) · [CMS and Help Centers](#cms-and-help-centers) · [Email](#email) · [User-Generated and Dynamic Content](#user-generated-and-dynamic-content) · [Launch Checklist](#launch-checklist) · [What To Write Down](#what-to-write-down)

**Before working on a site you have touched before**, read `## Environment` in `~/Clawic/data/translate/memory.md` and open the URL and hreflang policy if `## Boxes` names it. The URL scheme is a decision that is expensive to reverse, so it gets made once and then followed.

## Markup: What Is Translatable

| Translate | Leave alone |
|---|---|
| Element text content | `class`, `id`, `data-*`, `name`, `for` |
| `alt`, `title` | `href` and `src` (except deliberately localized URLs) |
| `placeholder`, `aria-label`, `aria-description`, `aria-placeholder` | `type`, `role`, `rel` |
| `value` on submit and button inputs | `value` on option and hidden inputs (it is data) |
| `<meta name="description">`, `og:title`, `og:description`, `twitter:*` text | `og:type`, `og:url`, `charset` |
| `<title>` | Inline script and style content |
| Structured data (JSON-LD) *text* fields: `name`, `description`, `addressLocality` | JSON-LD types, `@context`, identifiers, ISO codes |
| `content` of `og:locale` — but as a locale code, not prose | — |

- Set `lang` on `<html>` for every page, and on any inline run in another language. It drives hyphenation, font selection for Han characters (`rtl-and-scripts.md`), quotation marks in generated content, and screen-reader pronunciation.
- Set `dir="rtl"` on the root for RTL locales and `dir="auto"` on fields holding user text.
- `&nbsp;` and other entities are content: French punctuation spacing depends on them (`locales.md`), and a CMS that strips them changes the typography.

## Inline Tags

- A sentence broken across tags cannot be translated: `<p>Click <a>here</a> to continue</p>` forces the link into the middle of a target sentence where it may not belong. Write the whole clause inside the link, or use a message with a tag placeholder that the framework reinserts (`software-strings.md`).
- Translators reorder around inline tags; the tag count and nesting must survive, the position must not be assumed.
- Bold and italic move with the word they emphasize, which is not the same position in the target. Italics for emphasis do not exist as a CJK convention (`rtl-and-scripts.md`).
- Self-closing and empty elements (`<br>`, `<img>`) sit at layout points, not language points — expect them to move or disappear when a sentence restructures, and confirm rather than forbid.

## Markdown

- Segment by block, not by line: a hard-wrapped paragraph is one unit, and re-wrapping the target at the source's line breaks produces ragged output.
- Reference-style links (`[text][ref]`) keep the reference key untranslated; the definition list at the bottom is not content.
- Code fences and inline code are untranslatable, including comments inside them unless the user asks otherwise — a translated code comment in a docs site is fine, a translated identifier is a broken example.
- Tables need re-aligning after translation, and heading anchors change when headings do, which breaks in-page links and any external link to them.
- Front matter has translatable values (`title`, `description`) and untranslatable keys, slugs and dates.

## URL Structure

| Scheme | Example | Use when |
|---|---|---|
| Subdirectory | `example.com/es/` | Default: one domain's authority serves every locale, cheapest to run |
| Subdomain | `es.example.com` | Separate infrastructure or teams per market |
| ccTLD | `example.es` | Real local presence, local legal entity, budget to build authority per domain |
| Parameter | `example.com?lang=es` | Never — crawlers treat it poorly and users cannot share a language-specific link reliably |

- **Translate slugs.** `/es/precios/` beats `/es/pricing/` for both readers and search. Keep them lowercase, without accents where the market's convention avoids them, and stable.
- A published URL is a promise: changing a slug later requires a 301 and still costs ranking. Decide the slug policy before the first launch.
- Do not mix schemes across a site — one locale on a ccTLD and the rest in subdirectories confuses users, crawlers and the analytics.

## hreflang

Annotations telling search engines which page serves which locale. Five rules, and breaking any one of them makes the whole cluster ignored:

1. **Reciprocal.** If A points at B, B must point at A. One-way annotations are dropped.
2. **Self-referencing.** Every page in the cluster lists itself.
3. **Valid codes.** ISO 639-1 language, optional ISO 3166-1 alpha-2 region. `en-UK` is invalid (`en-GB`), `es-LA` is invalid (`es-419`), and a region alone is never a valid value.
4. **Canonical URLs only.** Each page's canonical points to itself, and hreflang points at canonical URLs — never at a page that canonicalizes elsewhere.
5. **One implementation.** In the `<head>`, in the XML sitemap, or as HTTP headers for non-HTML files. Pick one; contradictory duplicates are the most common cause of a cluster being ignored.

Add `x-default` for the page shown when no locale matches — a language selector or the global default. Note that hreflang is a *targeting* signal, not a ranking one: it decides which version is shown to whom, and does not make the page rank.

## Language Switching and Redirects

- **Do not auto-redirect by IP address.** It traps travelers and VPN users in the wrong language, hides content from crawlers that crawl from one country, and makes a shared link resolve differently for each recipient. Offer a dismissible banner suggesting the local version, and remember the choice.
- The switcher lists each language **in its own language and script** (Deutsch, 日本語, العربية), never as flags — a flag is a country, and it excludes every speaker outside it.
- Switching language should keep the user on the equivalent page, not dump them on the home page. Where no translation exists, say so rather than silently serving the source.
- Persist the choice in a cookie or the account, and keep the URL authoritative so a shared link still works.

## Multilingual SEO

- **Keywords are researched per market, never translated.** Search behavior differs even between variants of one language: the term with volume in Mexico is not the literal translation of the English term, and may not be the Spanish term used in Spain. Get volume data for the target market before writing titles.
- Title and description length limits are measured in **pixels, not characters**, so CJK titles fit fewer characters and German fits fewer words. Write to the target's practical limit, do not translate to the source's length.
- Local search engines matter where they have share — Baidu (China), Yandex (Russia), Naver (Korea), Seznam (Czechia) — and their guidelines differ from Google's, including hosting and verification requirements.
- Localize structured data text and keep its codes: currency in ISO 4217, availability and country in their controlled vocabularies (`numbers-and-names.md`).
- Local trust signals are part of the page: a local address and phone number, local payment methods, local currency, prices with the market's tax convention. A perfectly translated checkout that only accepts one country's cards converts like an untranslated one.
- Backlinks and authority do not transfer between locales; a new market starts near zero regardless of the source site's strength. Say that before anyone predicts traffic.

## CMS and Help Centers

- Know which model the CMS uses: **entity translation** (a separate content item per locale, linked) or **field translation** (one item, translated fields). It decides whether an editor can publish locales independently and how a missing translation renders.
- Publish state is per locale: a page that goes live before its translation exists shows the source language to that market. Check the fallback behavior before the first launch, not after.
- Help centers (Zendesk, Intercom, Document360) have their own gaps: article bodies are translated, but categories, section names, labels, macros, canned responses, email templates and the search placeholder often are not — and those are what a support user sees first.
- Editor round-trips destroy markup: a rich-text editor that strips `<xliff:g>`, entities, or non-breaking spaces is an environment fact worth writing down, because it will do it again.
- Whatever the CMS, the source of truth for the glossary is this skill's boxes, not the CMS's built-in term list, which usually cannot express parts of speech or forbidden renderings (`terminology.md`).

## Email

- Subject lines have practical limits (roughly 40-50 characters visible on mobile) and expand like every other short string; preheader text is a separate string that is frequently forgotten.
- RTL email needs `dir="rtl"` in the body markup: many clients ignore CSS, and a table-based template needs its columns mirrored (`rtl-and-scripts.md`).
- Always ship a plain-text alternative in the same language as the HTML part.
- Legal footers — unsubscribe wording, company registration details, imprint requirements — are jurisdiction-specific and are not a translation of the source footer. Get the target market's required text (`legal-medical.md`).
- Transactional emails carry names, dates, currencies and addresses assembled at send time: they are strings with placeholders, not documents (`software-strings.md`).

## User-Generated and Dynamic Content

- Machine-translated user content must be **labeled as machine-translated** with an option to see the original. Presenting it as native content misleads the reader and, for reviews and listings, can be a legal problem.
- Do not index machine-translated pages as if they were original content; thin auto-translated pages at scale are the classic quality-guideline violation.
- User content mixes directions and scripts inside one page: `dir="auto"` per item, and never assume the item's language matches the page's.
- Search over multilingual content needs per-language analyzers; one analyzer over all locales returns confident nonsense.

## Launch Checklist

| Check | Passing looks like |
|---|---|
| Every page in the cluster has reciprocal, self-referencing hreflang with valid codes | Crawl report shows zero one-way or invalid annotations |
| Canonical points to self on every locale | No locale canonicalizes to the source language |
| `lang` and `dir` correct on every template | Including error pages, emails and PDFs |
| No mixed-language pages | Crawl and eyeball the top 20 pages per locale |
| Slugs translated and stable, redirects in place for any change | 301s, not 302s |
| Titles and descriptions written to the market's keywords, not translated | Volume data exists for each |
| Local currency, payment, address and phone formats | `numbers-and-names.md` |
| Sitemap per locale, submitted, and robots not blocking the new paths | — |
| Language switcher present, in-language, non-flag, and preserving the page | — |
| Legal pages present for the market (privacy, imprint, consent wording) | `legal-medical.md` |

## What To Write Down

- The **URL scheme, slug policy and hreflang implementation** go in `artifacts/url-and-hreflang-policy.md`, born as its own file with its `## Boxes` line, because they are decisions that every future page follows and that nobody remembers a year later.
- CMS behavior that costs time — an editor that strips markup, a fallback that serves the source language silently, a publish workflow with a locale trap — goes in **`## Environment`** in `~/Clawic/data/translate/memory.md`.
- Per-market keyword research, once done, is an **`artifacts/keywords-<market>.md`** with its date; search volume ages, so the date is what makes it usable later.
- If the user agrees to a periodic in-market review of the top pages, it becomes a row in **`## Due`**.
