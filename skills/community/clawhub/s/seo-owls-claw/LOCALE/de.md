# SEOwlsClaw — Locale German (de)

## Purpose

This file contains **only the keys that differ from `LOCALE/base.md`**.  
Load `base.md` first, then apply these overrides on top.  
Any key not listed here is inherited from base unchanged.

**Applies to:** All content generated with `--lang de`  
**Locale string:** `de-DE`  
**Market:** Germany (primary), Austria (de-AT), Switzerland (de-CH) — all use this file as base

---

## Section 1 — HTML & Meta

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `LANG_CODE` | `de` | `en` |
| `LOCALE_STRING` | `de-DE` | `en-US` |

---

## Section 2 — Formatting

### 2.1 Date Formatting

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `DATE_FORMAT` | `DD.MM.YYYY` | `Month DD, YYYY` |
| `DATE_EXAMPLE` | `04.04.2026` | `April 4, 2026` |
| `DATE_SHORT_FORMAT` | `DD.MM.YY` | `MM/DD/YYYY` |
| `DATE_SHORT_EXAMPLE` | `04.04.26` | `04/04/2026` |

### 2.2 Price Formatting

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `PRICE_SYMBOL_POSITION` | `after` | `before` |
| `PRICE_FORMAT` | `X.XXX,XX €` | `€X,XXX.XX` |
| `PRICE_EXAMPLE` | `1.090,00 €` | `€1,090.00` |

### 2.3 Number Formatting

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `NUMBER_THOUSANDS_SEP` | `.` | `,` |
| `NUMBER_DECIMAL_SEP` | `,` | `.` |

---

## Section 3 — Schema Fields

| Key | de Override | Schema Field | Notes |
|-----|-------------|--------------|-------|
| `SCHEMA_IN_LANGUAGE` | `de` | `inLanguage` | |
| `SCHEMA_ADDRESS_COUNTRY` | `DE` | `addressCountry` | ISO 3166-1 alpha-2 |
| `SCHEMA_STORE_LOCALE` | `de-DE` | `availableLanguage` | |
| `SCHEMA_TIMEZONE_OFFSET` | `+01:00` | datetime strings | Winter time (CET) |

**Agent note — Timezone offset for Germany:**  
Use `+01:00` (CET) from last Sunday of October → last Sunday of March.  
Use `+02:00` (CEST) from last Sunday of March → last Sunday of October.  
When generating datetime strings for `{SCHEMA_OFFER_VALID_FROM}` and  
`{SCHEMA_OFFER_VALID_THROUGH}`, determine the correct offset from the  
date in the prompt. Default to `+01:00` if date is unclear.

---

## Section 4 — SEO & Writing Rules

### 4.1 Formality

German defaults to **formal address (Sie-Form)**.  
Use `Du-Form` only when the persona explicitly sets `--tone casual` or the  
brand identity is youth-oriented (e.g. streetwear, gaming, lifestyle).

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `FORMALITY_MODE` | `formal` | `informal` |
| `FORMALITY_SECOND_PERSON` | `Sie / Ihr` | `you / your` |
| `FORMALITY_POSSESSIVE` | `Ihr` | `your` |

**Formal example:** *"Finden Sie die Kamera, die zu Ihrem Stil passt."*  
**Casual override (--tone casual):** *"Finde die Kamera, die zu deinem Stil passt."*

### 4.2 Punctuation & Typography

German uses „lowered-open" quotation marks — **„Anführungszeichen"** — not "English quotes".

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `QUOTE_OPEN` | `„` | `"` |
| `QUOTE_CLOSE` | `"` | `"` |
| `QUOTE_SINGLE_OPEN` | `‚` | `'` |
| `QUOTE_SINGLE_CLOSE` | `'` | `'` |

### 4.3 Slug & URL Rules

German umlauts and ß must be transliterated in slugs — search engines and  
browsers handle them inconsistently, and lowercase ASCII slugs rank more reliably.

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `SLUG_UMLAUT_RULE` | `replace` | `keep` |
| `SLUG_UMLAUT_MAP` | `ä→ae, ö→oe, ü→ue, Ä→ae, Ö→oe, Ü→ue, ß→ss` | `(none)` |

**Slug examples:**
```
"Leica M6 TTL Schwarz"     → leica-m6-ttl-schwarz
"Für Bastler / Defekt"     → fuer-bastler-defekt
"Analogkamera Übersicht"   → analogkamera-uebersicht
"Contax RTS III"           → contax-rts-iii
```

### 4.4 Keyword & Content Writing Rules

German SEO uses compound nouns extensively. The agent must recognize and  
generate compound keyword forms correctly — Google.de indexes them as single tokens.

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `KEYWORD_COMPOUND_RULE` | `compound` | `space-separated` |

**Compound keyword examples:**
```
Leica + Kamera        → Leica-Kamera (hyphenated compound, common in headlines)
Vintage + Kamera      → Vintage-Kamera
Analog + Fotografie   → Analogfotografie (merged compound, use in body copy)
gebraucht + Kamera    → gebrauchte Kamera (adjective form — no merge)
```

**Agent rule:** In H1 and meta title → use hyphenated compound (`Leica-Kamera`).  
In body copy → use natural merged form (`Analogfotografie`) where it reads naturally.

---

## Section 5 — CTA & UI Phrases

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `CTA_BUY_NOW` | `Jetzt kaufen` | `Buy Now` |
| `CTA_ADD_TO_CART` | `In den Warenkorb` | `Add to Cart` |
| `CTA_VIEW_PRODUCT` | `Zum Produkt` | `View Product` |
| `CTA_READ_MORE` | `Weiterlesen` | `Read More` |
| `CTA_LEARN_MORE` | `Mehr erfahren` | `Learn More` |
| `CTA_CONTACT_US` | `Kontakt aufnehmen` | `Contact Us` |
| `CTA_BACK_TO_TOP` | `Nach oben` | `Back to Top` |
| `LABEL_CONDITION` | `Zustand` | `Condition` |
| `LABEL_PRICE` | `Preis` | `Price` |
| `LABEL_AVAILABILITY` | `Verfügbarkeit` | `Availability` |
| `LABEL_BRAND` | `Marke` | `Brand` |
| `LABEL_SKU` | `Art.-Nr.` | `Item No.` |
| `LABEL_IN_STOCK` | `Auf Lager` | `In Stock` |
| `LABEL_OUT_OF_STOCK` | `Nicht verfügbar` | `Out of Stock` |
| `LABEL_LIMITED_STOCK` | `Nur noch wenige verfügbar` | `Limited Availability` |
| `FAQ_SECTION_HEADING` | `Häufig gestellte Fragen` | `Frequently Asked Questions` |
| `BREADCRUMB_HOME_LABEL` | `Startseite` | `Home` |

---

## Section 6 — Condition Labels (Productused)

German vintage camera market uses a mix of English condition terms (internationally  
understood) and German translations. Both are provided — agent uses the label  
that matches the shop\'s own condition system as set in the prompt.

| Key | de Override | Base Default |
|-----|-------------|--------------|
| `CONDITION_NEW` | `Neu` | `New` |
| `CONDITION_MINT` | `Wie neu / Mint` | `Mint` |
| `CONDITION_VERY_GOOD` | `Sehr gut (A)` | `Very Good` |
| `CONDITION_GOOD` | `Gut (A/B)` | `Good` |
| `CONDITION_ACCEPTABLE` | `Akzeptabel (B/C)` | `Acceptable` |
| `CONDITION_VERY_USED` | `Stark gebraucht (C/D)` | `Very Used` |
| `CONDITION_REFURBISHED` | `Überholt / CLA` | `Refurbished / Serviced` |
| `CONDITION_FOR_PARTS` | `Für Bastler / Defekt` | `For Parts / Defective` |

---

*Last updated: 2026-04-04 (v0.6)*  
*Maintainer: Chris — SEOwlsClaw German locale overrides*