# SEOwlsClaw — Locale Spanish (es)

## Purpose

This file contains **only the keys that differ from `LOCALE/base.md`**.  
Load `base.md` first, then apply these overrides on top.  
Any key not listed here is inherited from base unchanged.

**Applies to:** All content generated with `--lang es`  
**Locale string:** `es-ES`  
**Primary market:** Spain (EU)  
**Currency:** EUR

> **Latin America note:** See the regional variant table at the bottom.  
> Mexico (`es-mx`), Argentina (`es-ar`), and others use different currencies,  
> vocabulary, and formality conventions.

---

## Section 1 — HTML & Meta

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `LANG_CODE` | `es` | `en` |
| `LOCALE_STRING` | `es-ES` | `en-US` |

---

## Section 2 — Formatting

### 2.1 Date Formatting

Spanish uses day-first format with slashes.

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `DATE_FORMAT` | `DD/MM/YYYY` | `Month DD, YYYY` |
| `DATE_EXAMPLE` | `04/04/2026` | `April 4, 2026` |
| `DATE_SHORT_FORMAT` | `DD/MM/YY` | `MM/DD/YYYY` |
| `DATE_SHORT_EXAMPLE` | `04/04/26` | `04/04/2026` |

### 2.2 Price Formatting

Spain uses the same decimal convention as Germany and Portugal — period for thousands,  
comma for decimal, € symbol after the number.

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `PRICE_SYMBOL_POSITION` | `after` | `before` |
| `PRICE_FORMAT` | `X.XXX,XX €` | `€X,XXX.XX` |
| `PRICE_EXAMPLE` | `1.090,00 €` | `€1,090.00` |

### 2.3 Number Formatting

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `NUMBER_THOUSANDS_SEP` | `.` | `,` |
| `NUMBER_DECIMAL_SEP` | `,` | `.` |

---

## Section 3 — Schema Fields

| Key | es Override | Schema Field | Notes |
|-----|-------------|--------------|-------|
| `SCHEMA_IN_LANGUAGE` | `es` | `inLanguage` | |
| `SCHEMA_ADDRESS_COUNTRY` | `ES` | `addressCountry` | ISO 3166-1 alpha-2 |
| `SCHEMA_STORE_LOCALE` | `es-ES` | `availableLanguage` | |
| `SCHEMA_TIMEZONE_OFFSET` | `+01:00` | datetime strings | Winter time (CET) |

**Agent note — Timezone offset for Spain (mainland):**  
Use `+01:00` (CET) from last Sunday of October → last Sunday of March.  
Use `+02:00` (CEST) from last Sunday of March → last Sunday of October.  
Same schedule as Germany and France. Default to `+01:00` if date is unclear.  
Note: Canary Islands use `+00:00` / `+01:00` (one hour behind mainland).

---

## Section 4 — SEO & Writing Rules

### 4.1 Formality

Spanish in Spain defaults to **informal "tú"** for e-commerce and most consumer content.  
Unlike German and French, the informal register is standard and friendly — not a sign of poor quality.  
Use formal "usted" only for high-end luxury brands, B2B content, or legal/insurance contexts.

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `FORMALITY_MODE` | `informal` | `informal` |
| `FORMALITY_SECOND_PERSON` | `tú / tu` | `you / your` |
| `FORMALITY_POSSESSIVE` | `tu / tus` | `your` |

**Informal example (default):** *"Encuentra la cámara que encaja con tu estilo."*  
**Formal override (--tone formal):** *"Encuentre la cámara que se adapta a su estilo."*

### 4.2 Punctuation & Typography

Spanish uses **guillemets** as the typographically correct quotation marks — «así».  
Unlike French, there are **no spaces** inside the guillemets in Spanish.  
Spanish also uses inverted opening punctuation — ¿ for questions, ¡ for exclamations.  
The agent must apply opening punctuation marks in all question and exclamation sentences.

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `QUOTE_OPEN` | `«` | `"` |
| `QUOTE_CLOSE` | `»` | `"` |
| `QUOTE_SINGLE_OPEN` | `'` | `'` |
| `QUOTE_SINGLE_CLOSE` | `'` | `'` |

**Inverted punctuation rule (mandatory in Spanish):**
```
Correct:  ¿Cuál es el estado de la cámara?
Correct:  ¡Solo quedan 2 unidades en stock!
Incorrect: Cuál es el estado de la cámara?
Incorrect: Solo quedan 2 unidades en stock!
```

**Agent rule:** Always insert ¿ / ¡ at the start of question and exclamation sentences  
in body copy, headings, FAQ questions, and CTA phrases. Do NOT include in slugs.

### 4.3 Slug & URL Rules

Spanish accented characters and special punctuation must be removed from slugs.

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `SLUG_UMLAUT_RULE` | `replace` | `keep` |
| `SLUG_UMLAUT_MAP` | `á→a, é→e, í→i, ó→o, ú→u, ñ→n, ü→u, ¿→(remove), ¡→(remove)` | `(none)` |

**Slug examples:**
```
"Cámara analógica usada"        → camara-analogica-usada
"Leica M6 buen estado"          → leica-m6-buen-estado
"Objetivos para película de 35mm" → objetivos-para-pelicula-de-35mm
"¿Qué cámara elegir?"           → que-camara-elegir
```

### 4.4 Keyword & Content Writing Rules

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `KEYWORD_COMPOUND_RULE` | `space-separated` | `space-separated` |
| `META_DESC_MAX_CHARS` | `155` | `160` |

**Agent note on Spain vs Latin America vocabulary:**  
When writing for Spain (`--lang es`), use Castilian Spanish vocabulary:
- `objetivo` (not `lente`) for camera lens
- `cámara` for camera (same in both, but accent required)
- `película` for film
- `fotografía analógica` for analog photography
- `en stock` is widely used as-is in Spanish e-commerce (no translation needed)
- Avoid Latin American terms: `lente`, `rollo` (for film roll), `celular`

---

## Section 5 — CTA & UI Phrases

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `CTA_BUY_NOW` | `Comprar ahora` | `Buy Now` |
| `CTA_ADD_TO_CART` | `Añadir al carrito` | `Add to Cart` |
| `CTA_VIEW_PRODUCT` | `Ver producto` | `View Product` |
| `CTA_READ_MORE` | `Leer más` | `Read More` |
| `CTA_LEARN_MORE` | `Saber más` | `Learn More` |
| `CTA_CONTACT_US` | `Contáctanos` | `Contact Us` |
| `CTA_BACK_TO_TOP` | `Volver arriba` | `Back to Top` |
| `LABEL_CONDITION` | `Estado` | `Condition` |
| `LABEL_PRICE` | `Precio` | `Price` |
| `LABEL_AVAILABILITY` | `Disponibilidad` | `Availability` |
| `LABEL_BRAND` | `Marca` | `Brand` |
| `LABEL_SKU` | `Ref.` | `Item No.` |
| `LABEL_IN_STOCK` | `En stock` | `In Stock` |
| `LABEL_OUT_OF_STOCK` | `Agotado` | `Out of Stock` |
| `LABEL_LIMITED_STOCK` | `Últimas unidades` | `Limited Availability` |
| `FAQ_SECTION_HEADING` | `Preguntas frecuentes` | `Frequently Asked Questions` |
| `BREADCRUMB_HOME_LABEL` | `Inicio` | `Home` |

---

## Section 6 — Condition Labels (Productused)

| Key | es Override | Base Default |
|-----|-------------|--------------|
| `CONDITION_NEW` | `Nuevo` | `New` |
| `CONDITION_MINT` | `Como nuevo / Mint` | `Mint` |
| `CONDITION_VERY_GOOD` | `Muy buen estado (A)` | `Very Good` |
| `CONDITION_GOOD` | `Buen estado (A/B)` | `Good` |
| `CONDITION_ACCEPTABLE` | `Estado aceptable (B/C)` | `Acceptable` |
| `CONDITION_VERY_USED` | `Muy usado (C/D)` | `Very Used` |
| `CONDITION_REFURBISHED` | `Revisado / CLA` | `Refurbished / Serviced` |
| `CONDITION_FOR_PARTS` | `Para piezas / Averiado` | `For Parts / Defective` |

---

## Regional Variants — Latin America

These are not separate locale files — just the keys to override **on top of es.md** if needed.

### Mexico (`--lang es-mx`)

| Key | es-MX Override | es (Spain) value |
|-----|----------------|-----------------|
| `LOCALE_STRING` | `es-MX` | `es-ES` |
| `SCHEMA_ADDRESS_COUNTRY` | `MX` | `ES` |
| `SCHEMA_PRICE_CURRENCY` | `MXN` | `EUR` |
| `SCHEMA_STORE_LOCALE` | `es-MX` | `es-ES` |
| `SCHEMA_TIMEZONE_OFFSET` | `-06:00` | `+01:00` |
| `PRICE_SYMBOL` | `MX$` | `€` |
| `PRICE_SYMBOL_POSITION` | `before` | `after` |
| `PRICE_FORMAT` | `MX$X,XXX.XX` | `X.XXX,XX €` |
| `NUMBER_THOUSANDS_SEP` | `,` | `.` |
| `NUMBER_DECIMAL_SEP` | `.` | `,` |
| `FORMALITY_MODE` | `formal` | `informal` |
| `FORMALITY_SECOND_PERSON` | `usted` | `tú / tu` |
| `CTA_ADD_TO_CART` | `Agregar al carrito` | `Añadir al carrito` |
| `CTA_CONTACT_US` | `Contáctenos` | `Contáctanos` |
| `LABEL_IN_STOCK` | `Disponible` | `En stock` |

### Argentina (`--lang es-ar`)

| Key | es-AR Override | es (Spain) value |
|-----|----------------|-----------------|
| `LOCALE_STRING` | `es-AR` | `es-ES` |
| `SCHEMA_ADDRESS_COUNTRY` | `AR` | `ES` |
| `SCHEMA_PRICE_CURRENCY` | `ARS` | `EUR` |
| `SCHEMA_TIMEZONE_OFFSET` | `-03:00` | `+01:00` |
| `PRICE_SYMBOL` | `AR$` | `€` |
| `PRICE_SYMBOL_POSITION` | `before` | `after` |
| `PRICE_FORMAT` | `AR$X.XXX,XX` | `X.XXX,XX €` |
| `FORMALITY_MODE` | `informal` | `informal` |
| `FORMALITY_SECOND_PERSON` | `vos / tu` | `tú / tu` |
| `CTA_ADD_TO_CART` | `Agregar al carrito` | `Añadir al carrito` |

**Agent note on Argentine Spanish:** Argentina uses **voseo** — "vos" instead of "tú"  
with different verb conjugations (`vos tenés` not `tú tienes`). Apply consistently  
throughout content when `--lang es-ar` is active.

---

*Last updated: 2026-04-04 (v0.6)*  
*Maintainer: Chris — SEOwlsClaw Spanish locale overrides*