# SEOwlsClaw — Locale Base (Default: English)

## Purpose

This file defines **all locale keys** used by SEOwlsClaw with their English/generic defaults.  
It is **always loaded first**, for every language, including English.

**How the agent uses this file:**
1. Load `LOCALE/base.md` at Step 2c (after persona, before variable generation)
2. If `--lang <code>` flag is present → load `LOCALE/<code>.md` and override matching keys
3. Use the merged result to populate all `{LOCALE_*}` and `{SCHEMA_*}` locale variables

**Rule:** If a key is not overridden by a language file, the base value is used.  
**Rule:** Never hardcode locale values in templates or schema blocks — always source from this file.

---

## Section 1 — HTML & Meta

These values go directly into the HTML `<head>` and `<html>` tag.

| Key | Default Value | Used In |
|-----|--------------|---------|
| `LANG_CODE` | `en` | `<html lang="{LANG_CODE}">` |
| `LOCALE_STRING` | `en-US` | Open Graph `og:locale`, schema `inLanguage` |
| `HTML_DIR` | `ltr` | `<html dir="{HTML_DIR}">` |
| `CHARSET` | `UTF-8` | `<meta charset="{CHARSET}">` |

---

## Section 2 — Formatting

Rules for how dates, prices, and numbers are formatted in the **visible content** (not schema).  
Schema dates always use ISO 8601 regardless of locale — see Section 3.

### 2.1 Date Formatting

| Key | Default Value | Example Output |
|-----|--------------|----------------|
| `DATE_FORMAT` | `Month DD, YYYY` | `April 4, 2026` |
| `DATE_EXAMPLE` | `April 4, 2026` | Reference only |
| `DATE_SHORT_FORMAT` | `MM/DD/YYYY` | `04/04/2026` |
| `DATE_SHORT_EXAMPLE` | `04/04/2026` | Reference only |

### 2.2 Price Formatting

| Key | Default Value | Example Output |
|-----|--------------|----------------|
| `PRICE_SYMBOL` | `€` | Symbol used in content |
| `PRICE_SYMBOL_POSITION` | `before` | `€1,090` (before) vs `1.090 €` (after) |
| `PRICE_FORMAT` | `€X,XXX.XX` | `€1,090.00` |
| `PRICE_EXAMPLE` | `€1,090.00` | Reference only |

### 2.3 Number Formatting

| Key | Default Value | Notes |
|-----|--------------|-------|
| `NUMBER_THOUSANDS_SEP` | `,` | `1,000` |
| `NUMBER_DECIMAL_SEP` | `.` | `1,090.50` |

---

## Section 3 — Schema Fields

These values are injected into JSON-LD schema blocks.  
**Agent note:** `SCHEMA_IN_LANGUAGE`, `SCHEMA_PRICE_CURRENCY`, and `SCHEMA_ADDRESS_COUNTRY`  
are sourced from the locale merged result — never hardcode them in templates.

| Key | Default Value | Schema Field | Notes |
|-----|--------------|--------------|-------|
| `SCHEMA_IN_LANGUAGE` | `en` | `inLanguage` | Language of the page content |
| `SCHEMA_PRICE_CURRENCY` | `EUR` | `priceCurrency` | ISO 4217 currency code |
| `SCHEMA_ADDRESS_COUNTRY` | `US` | `addressCountry` | ISO 3166-1 alpha-2 country code |
| `SCHEMA_STORE_LOCALE` | `en-US` | `availableLanguage` | Language available at the store |
| `SCHEMA_TIMEZONE_OFFSET` | `+00:00` | Used in datetime strings | e.g. `2026-04-15T00:00:00+00:00` |

---

## Section 4 — SEO & Writing Rules

Rules that affect how the agent writes content and generates slugs.

### 4.1 Formality

| Key | Default Value | Options | Effect |
|-----|--------------|---------|--------|
| `FORMALITY_MODE` | `informal` | `informal` / `formal` | Controls second-person address in body copy |
| `FORMALITY_SECOND_PERSON` | `you / your` | Language-specific | Word the agent uses to address the reader |
| `FORMALITY_POSSESSIVE` | `your` | Language-specific | Possessive pronoun used in CTAs |

**Informal example (default):** *"Find the camera that fits your style."*  
**Formal example (de.md override):** *"Finden Sie die Kamera, die zu Ihrem Stil passt."*

### 4.2 Punctuation & Typography

| Key | Default Value | Notes |
|-----|--------------|-------|
| `QUOTE_OPEN` | `"` | Opening quotation mark |
| `QUOTE_CLOSE` | `"` | Closing quotation mark |
| `QUOTE_SINGLE_OPEN` | `'` | Opening single quote |
| `QUOTE_SINGLE_CLOSE` | `'` | Closing single quote |

### 4.3 Slug & URL Rules

| Key | Default Value | Options | Notes |
|-----|--------------|---------|-------|
| `SLUG_UMLAUT_RULE` | `keep` | `keep` / `replace` | Whether to transliterate special characters in slugs |
| `SLUG_UMLAUT_MAP` | `(none)` | Key-value pairs | e.g. `ä→ae, ö→oe, ü→ue, ß→ss` — defined per language |
| `SLUG_SPACE_CHAR` | `-` | `-` / `_` | Character used for spaces in slugs |
| `SLUG_LOWERCASE` | `true` | `true` / `false` | Force lowercase in generated slugs |

### 4.4 Keyword & Content Writing Rules

| Key | Default Value | Notes |
|-----|--------------|-------|
| `KEYWORD_COMPOUND_RULE` | `space-separated` | How multi-word keywords are written in content |
| `META_DESC_MAX_CHARS` | `160` | Max meta description character count |
| `TITLE_TAG_MAX_CHARS` | `60` | Max title tag character count |
| `CONTENT_READING_DIRECTION` | `left-to-right` | Used for editorial layout hints |

---

## Section 5 — CTA & UI Phrase Defaults

Generic English defaults for common UI phrases.  
Language files override these with natural-sounding translations.  
The agent uses these in template placeholder variables like `{CTA_BUY_NOW}`.

| Key | Default Value | Used In |
|-----|--------------|---------|
| `CTA_BUY_NOW` | `Buy Now` | Purchase buttons |
| `CTA_ADD_TO_CART` | `Add to Cart` | E-commerce CTAs |
| `CTA_VIEW_PRODUCT` | `View Product` | Category/listing pages |
| `CTA_READ_MORE` | `Read More` | Blog teasers, related content |
| `CTA_LEARN_MORE` | `Learn More` | Informational CTAs |
| `CTA_CONTACT_US` | `Contact Us` | Support/inquiry links |
| `CTA_BACK_TO_TOP` | `Back to Top` | Page navigation |
| `LABEL_CONDITION` | `Condition` | Used/refurbished product pages |
| `LABEL_PRICE` | `Price` | Product pages |
| `LABEL_AVAILABILITY` | `Availability` | Stock status label |
| `LABEL_BRAND` | `Brand` | Product spec tables |
| `LABEL_SKU` | `Item No.` | Product identifier label |
| `LABEL_IN_STOCK` | `In Stock` | Availability text |
| `LABEL_OUT_OF_STOCK` | `Out of Stock` | Availability text |
| `LABEL_LIMITED_STOCK` | `Limited Availability` | Scarcity signal |
| `FAQ_SECTION_HEADING` | `Frequently Asked Questions` | FAQ section H2 |
| `BREADCRUMB_HOME_LABEL` | `Home` | First breadcrumb item |

---

## Section 6 — Condition Labels (Productused)

Maps internal condition codes to display labels in the current language.  
These appear in visible content — NOT in schema (schema always uses `schema.org` URLs).

| Key | Default Value (English) |
|-----|------------------------|
| `CONDITION_NEW` | `New` |
| `CONDITION_MINT` | `Mint` |
| `CONDITION_VERY_GOOD` | `Very Good` |
| `CONDITION_GOOD` | `Good` |
| `CONDITION_ACCEPTABLE` | `Acceptable` |
| `CONDITION_VERY_USED` | `Very Used` |
| `CONDITION_REFURBISHED` | `Refurbished / Serviced` |
| `CONDITION_FOR_PARTS` | `For Parts / Defective` |

---

## Agent Load Instructions

```
Step 2c — Load Locale (after persona load, before variable generation)

IF --lang flag is present:
  1. Load LOCALE/base.md → store all keys as locale_vars{}
  2. Load LOCALE/<lang_code>.md → override matching keys in locale_vars{}
  3. Merge result = base keys + language overrides

IF --lang flag is NOT present:
  1. Load LOCALE/base.md only → use as locale_vars{}

Add all locale_vars{} to the variable dictionary before Step 3 (Generate Variables).
This makes all {LANG_CODE}, {CTA_BUY_NOW}, {SCHEMA_IN_LANGUAGE} etc.
available for variable substitution in Step 7.
```

---

*Last updated: 2026-04-04 (v0.6)*  
*Maintainer: Chris — SEOwlsClaw locale base, all supported languages*
