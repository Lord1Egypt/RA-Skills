# SEOwlsClaw — Locale French (fr)

## Purpose

This file contains **only the keys that differ from `LOCALE/base.md`**.  
Load `base.md` first, then apply these overrides on top.  
Any key not listed here is inherited from base unchanged.

**Applies to:** All content generated with `--lang fr`  
**Locale string:** `fr-FR`  
**Primary market:** France (EU)  
**Currency:** EUR

> **Belgium / Switzerland note:** See the regional variant table at the bottom.  
> Belgium (`fr-BE`) uses EUR but different CTA conventions.  
> Switzerland (`fr-CH`) uses CHF and different price formatting.

---

## Section 1 — HTML & Meta

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `LANG_CODE` | `fr` | `en` |
| `LOCALE_STRING` | `fr-FR` | `en-US` |

---

## Section 2 — Formatting

### 2.1 Date Formatting

French uses day-first format with slashes.

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `DATE_FORMAT` | `DD/MM/YYYY` | `Month DD, YYYY` |
| `DATE_EXAMPLE` | `04/04/2026` | `April 4, 2026` |
| `DATE_SHORT_FORMAT` | `DD/MM/YY` | `MM/DD/YYYY` |
| `DATE_SHORT_EXAMPLE` | `04/04/26` | `04/04/2026` |

### 2.2 Price Formatting

French uses a **thin non-breaking space** as the thousands separator and a comma as the decimal separator. The € symbol follows the number with a space.

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `PRICE_SYMBOL_POSITION` | `after` | `before` |
| `PRICE_FORMAT` | `X XXX,XX €` | `€X,XXX.XX` |
| `PRICE_EXAMPLE` | `1 090,00 €` | `€1,090.00` |

### 2.3 Number Formatting

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `NUMBER_THOUSANDS_SEP` | ` ` (thin non-breaking space U+202F) | `,` |
| `NUMBER_DECIMAL_SEP` | `,` | `.` |

**Agent note:** Use a thin non-breaking space (`\u202f`) for thousands separation  
in price and number output — not a regular space. This is the correct French  
typographic standard and prevents line breaks inside numbers.

---

## Section 3 — Schema Fields

| Key | fr Override | Schema Field | Notes |
|-----|-------------|--------------|-------|
| `SCHEMA_IN_LANGUAGE` | `fr` | `inLanguage` | |
| `SCHEMA_ADDRESS_COUNTRY` | `FR` | `addressCountry` | ISO 3166-1 alpha-2 |
| `SCHEMA_STORE_LOCALE` | `fr-FR` | `availableLanguage` | |
| `SCHEMA_TIMEZONE_OFFSET` | `+01:00` | datetime strings | Winter time (CET) |

**Agent note — Timezone offset for France:**  
Use `+01:00` (CET) from last Sunday of October → last Sunday of March.  
Use `+02:00` (CEST) from last Sunday of March → last Sunday of October.  
Same schedule as Germany. Default to `+01:00` if date is unclear.

---

## Section 4 — SEO & Writing Rules

### 4.1 Formality

French e-commerce defaults to **formal "vous"** — respectful and standard for all customer-facing content.  
Use informal "tu" only when `--tone casual` is set or the brand explicitly targets youth culture.

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `FORMALITY_MODE` | `formal` | `informal` |
| `FORMALITY_SECOND_PERSON` | `vous` | `you / your` |
| `FORMALITY_POSSESSIVE` | `votre / vos` | `your` |

**Formal example:** *"Trouvez l\'appareil photo qui correspond à votre style."*  
**Casual override (--tone casual):** *"Trouve l\'appareil photo qui correspond à ton style."*

### 4.2 Punctuation & Typography

French uses **guillemets with non-breaking spaces inside** — « comme ça » — not "English quotes".  
French also requires a non-breaking space **before** `:`, `!`, `?`, and `;`.  
The agent must apply this rule throughout all generated French content.

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `QUOTE_OPEN` | `«\u00a0` | `"` |
| `QUOTE_CLOSE` | `\u00a0»` | `"` |
| `QUOTE_SINGLE_OPEN` | `‹\u00a0` | `'` |
| `QUOTE_SINGLE_CLOSE` | `\u00a0›` | `'` |

**Punctuation spacing rule (French typographic standard):**
```
Correct:  Prix\u00a0: 1 090,00 €   (non-breaking space before colon)
Correct:  En stock\u00a0!           (non-breaking space before exclamation)
Correct:  Disponible\u00a0?         (non-breaking space before question mark)
Incorrect: Prix: 1 090,00 €
Incorrect: En stock!
```

### 4.3 Slug & URL Rules

French accented characters must be transliterated in slugs.

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `SLUG_UMLAUT_RULE` | `replace` | `keep` |
| `SLUG_UMLAUT_MAP` | `é→e, è→e, ê→e, ë→e, à→a, â→a, ä→a, î→i, ï→i, ô→o, ö→o, ù→u, û→u, ü→u, ç→c, œ→oe, æ→ae` | `(none)` |

**Slug examples:**
```
"Appareil photo argentique"      → appareil-photo-argentique
"Objectif 50mm pour débutants"   → objectif-50mm-pour-debutants
"Leica M6 état très bon"         → leica-m6-etat-tres-bon
"Vente été — caméras analogiques" → vente-ete-cameras-analogiques
```

### 4.4 Keyword & Content Writing Rules

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `KEYWORD_COMPOUND_RULE` | `space-separated` | `space-separated` |
| `META_DESC_MAX_CHARS` | `155` | `160` |

**Agent note on French SEO writing:**
> - Accented characters are fine and preferred in **visible content and headings**
> - French words are on average longer than English — keep title tags tight
> - "vous" form must be consistent throughout — never mix with "tu" in one piece
> - Avoid anglicisms when a natural French equivalent exists:
>  - Use `appareil photo` not `caméra` for still cameras (caméra = video camera in French)
>  - Use `objectif` not `lens`
>  - Use `argentique` for analog/film photography

---

## Section 5 — CTA & UI Phrases

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `CTA_BUY_NOW` | `Acheter maintenant` | `Buy Now` |
| `CTA_ADD_TO_CART` | `Ajouter au panier` | `Add to Cart` |
| `CTA_VIEW_PRODUCT` | `Voir le produit` | `View Product` |
| `CTA_READ_MORE` | `Lire la suite` | `Read More` |
| `CTA_LEARN_MORE` | `En savoir plus` | `Learn More` |
| `CTA_CONTACT_US` | `Nous contacter` | `Contact Us` |
| `CTA_BACK_TO_TOP` | `Retour en haut` | `Back to Top` |
| `LABEL_CONDITION` | `État` | `Condition` |
| `LABEL_PRICE` | `Prix` | `Price` |
| `LABEL_AVAILABILITY` | `Disponibilité` | `Availability` |
| `LABEL_BRAND` | `Marque` | `Brand` |
| `LABEL_SKU` | `Réf.` | `Item No.` |
| `LABEL_IN_STOCK` | `En stock` | `In Stock` |
| `LABEL_OUT_OF_STOCK` | `Épuisé` | `Out of Stock` |
| `LABEL_LIMITED_STOCK` | `Stock limité` | `Limited Availability` |
| `FAQ_SECTION_HEADING` | `Questions fréquentes` | `Frequently Asked Questions` |
| `BREADCRUMB_HOME_LABEL` | `Accueil` | `Home` |

---

## Section 6 — Condition Labels (Productused)

| Key | fr Override | Base Default |
|-----|-------------|--------------|
| `CONDITION_NEW` | `Neuf` | `New` |
| `CONDITION_MINT` | `Comme neuf / Mint` | `Mint` |
| `CONDITION_VERY_GOOD` | `Très bon état (A)` | `Very Good` |
| `CONDITION_GOOD` | `Bon état (A/B)` | `Good` |
| `CONDITION_ACCEPTABLE` | `État acceptable (B/C)` | `Acceptable` |
| `CONDITION_VERY_USED` | `Très usé (C/D)` | `Very Used` |
| `CONDITION_REFURBISHED` | `Révisé / CLA` | `Refurbished / Serviced` |
| `CONDITION_FOR_PARTS` | `Pour pièces / Défectueux` | `For Parts / Defective` |

---

## Regional Variants — Belgium & Switzerland

These are not separate locale files — just the keys to override **on top of fr.md** if needed.

### Belgium (`--lang fr-be`)

| Key | fr-BE Override | fr (France) value |
|-----|----------------|-------------------|
| `LOCALE_STRING` | `fr-BE` | `fr-FR` |
| `SCHEMA_ADDRESS_COUNTRY` | `BE` | `FR` |
| `SCHEMA_STORE_LOCALE` | `fr-BE` | `fr-FR` |
| `CTA_CONTACT_US` | `Contactez-nous` | `Nous contacter` |

Currency stays EUR. Timezone stays `+01:00`. Everything else identical to France.

### Switzerland (`--lang fr-ch`)

| Key | fr-CH Override | fr (France) value |
|-----|----------------|-------------------|
| `LOCALE_STRING` | `fr-CH` | `fr-FR` |
| `SCHEMA_ADDRESS_COUNTRY` | `CH` | `FR` |
| `SCHEMA_PRICE_CURRENCY` | `CHF` | `EUR` |
| `SCHEMA_STORE_LOCALE` | `fr-CH` | `fr-FR` |
| `SCHEMA_TIMEZONE_OFFSET` | `+01:00` | `+01:00` *(same)* |
| `PRICE_SYMBOL` | `CHF` | `€` |
| `PRICE_FORMAT` | `CHF X\'XXX.00` | `X XXX,XX €` |
| `PRICE_EXAMPLE` | `CHF 1\'090.00` | `1 090,00 €` |
| `NUMBER_THOUSANDS_SEP` | `\'` (apostrophe) | ` ` (thin space) |
| `NUMBER_DECIMAL_SEP` | `.` | `,` |

Note: Swiss French uses apostrophe as thousands separator and period as decimal — the opposite of mainland France. This is a common source of errors in multi-locale shops.

---

*Last updated: 2026-04-04 (v0.6)*  
*Maintainer: Chris — SEOwlsClaw French locale overrides*