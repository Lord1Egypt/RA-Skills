# SEOwlsClaw — Locale Portuguese (pt)

## Purpose

This file contains **only the keys that differ from `LOCALE/base.md`**.  
Load `base.md` first, then apply these overrides on top.  
Any key not listed here is inherited from base unchanged.

**Applies to:** All content generated with `--lang pt`  
**Locale string:** `pt-PT`  
**Primary market:** Portugal (EU)  
**Currency:** EUR

> **Brazil note:** See the Brazil Override section at the bottom.  
> Brazil (`pt-BR`) uses BRL and different vocabulary/formality conventions.

---

## Section 1 — HTML & Meta

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `LANG_CODE` | `pt` | `en` |
| `LOCALE_STRING` | `pt-PT` | `en-US` |

---

## Section 2 — Formatting

### 2.1 Date Formatting

Portuguese uses day-first format with slashes.

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `DATE_FORMAT` | `DD/MM/YYYY` | `Month DD, YYYY` |
| `DATE_EXAMPLE` | `04/04/2026` | `April 4, 2026` |
| `DATE_SHORT_FORMAT` | `DD/MM/YY` | `MM/DD/YYYY` |
| `DATE_SHORT_EXAMPLE` | `04/04/26` | `04/04/2026` |

### 2.2 Price Formatting

Portugal uses the same decimal convention as Spain and Germany — period for thousands,  
comma for decimal, € symbol after the number.

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `PRICE_SYMBOL_POSITION` | `after` | `before` |
| `PRICE_FORMAT` | `X.XXX,XX €` | `€X,XXX.XX` |
| `PRICE_EXAMPLE` | `1.090,00 €` | `€1,090.00` |

### 2.3 Number Formatting

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `NUMBER_THOUSANDS_SEP` | `.` | `,` |
| `NUMBER_DECIMAL_SEP` | `,` | `.` |

---

## Section 3 — Schema Fields

| Key | pt Override | Schema Field | Notes |
|-----|-------------|--------------|-------|
| `SCHEMA_IN_LANGUAGE` | `pt` | `inLanguage` | |
| `SCHEMA_ADDRESS_COUNTRY` | `PT` | `addressCountry` | ISO 3166-1 alpha-2 |
| `SCHEMA_STORE_LOCALE` | `pt-PT` | `availableLanguage` | |
| `SCHEMA_TIMEZONE_OFFSET` | `+00:00` | datetime strings | Winter time (WET) |

**Agent note — Timezone offset for Portugal (mainland + Madeira):**  
Use `+00:00` (WET) from last Sunday of October → last Sunday of March.  
Use `+01:00` (WEST) from last Sunday of March → last Sunday of October.  
Same DST switch dates as the rest of the EU, but **one hour behind** Spain/France/Germany  
year-round — mainland Portugal is on UK/Ireland time (WET/WEST), not CET/CEST.  
Note: the **Azores** are a further hour behind mainland Portugal (`-01:00` winter / `+00:00` summer).  
Default to `+00:00` if date is unclear.

---

## Section 4 — SEO & Writing Rules

### 4.1 Formality

European Portuguese e-commerce defaults to **"você"** — a neutral, professional register  
standard for customer-facing content in Portugal (distinct from Brazilian Portuguese, where  
"você" is the everyday informal default). Use "tu" only when `--tone casual` is set or the  
brand explicitly targets youth culture.

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `FORMALITY_MODE` | `formal` | `informal` |
| `FORMALITY_SECOND_PERSON` | `você` | `you / your` |
| `FORMALITY_POSSESSIVE` | `seu / sua` | `your` |

**Default example:** *"Encontre a câmara que se adapta ao seu estilo."*  
**Casual override (--tone casual):** *"Encontra a câmara que se adapta ao teu estilo."*

### 4.2 Punctuation & Typography

European Portuguese uses **guillemets** — «assim» — not "English quotes", with no  
inner spaces (unlike French). Standard sentence punctuation otherwise follows English  
conventions (no inverted ¿¡ marks, unlike Spanish).

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `QUOTE_OPEN` | `«` | `"` |
| `QUOTE_CLOSE` | `»` | `"` |
| `QUOTE_SINGLE_OPEN` | `'` | `'` |
| `QUOTE_SINGLE_CLOSE` | `'` | `'` |

### 4.3 Slug & URL Rules

Portuguese accented characters must be transliterated in slugs.

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `SLUG_UMLAUT_RULE` | `replace` | `keep` |
| `SLUG_UMLAUT_MAP` | `á→a, à→a, â→a, ã→a, é→e, ê→e, í→i, ó→o, ô→o, õ→o, ú→u, ç→c` | `(none)` |

**Slug examples:**
```
"Câmara analógica em bom estado" → camara-analogica-em-bom-estado
"Leica M6 muito bom estado"      → leica-m6-muito-bom-estado
"Objectivas para película de 35mm" → objectivas-para-pelicula-de-35mm
"Promoção de verão — câmaras"    → promocao-de-verao-cameras
```

### 4.4 Keyword & Content Writing Rules

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `KEYWORD_COMPOUND_RULE` | `space-separated` | `space-separated` |
| `META_DESC_MAX_CHARS` | `155` | `155` |

**Agent note on European Portuguese vs Brazilian Portuguese spelling:**  
Post-2009 orthographic agreement reduced differences, but some vocabulary and  
spelling variations remain. When writing for Portugal:
- Use `objectiva` not `objetiva` (lens)
- Use `câmara` not `câmera` (camera)
- Use `fotografia` (same in both)
- Avoid Brazilian colloquialisms (`bacana`, `legal`, etc.)

---

## Section 5 — CTA & UI Phrases

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `CTA_BUY_NOW` | `Comprar agora` | `Buy Now` |
| `CTA_ADD_TO_CART` | `Adicionar ao carrinho` | `Add to Cart` |
| `CTA_VIEW_PRODUCT` | `Ver produto` | `View Product` |
| `CTA_READ_MORE` | `Ler mais` | `Read More` |
| `CTA_LEARN_MORE` | `Saber mais` | `Learn More` |
| `CTA_CONTACT_US` | `Contacte-nos` | `Contact Us` |
| `CTA_BACK_TO_TOP` | `Voltar ao topo` | `Back to Top` |
| `LABEL_CONDITION` | `Estado` | `Condition` |
| `LABEL_PRICE` | `Preço` | `Price` |
| `LABEL_AVAILABILITY` | `Disponibilidade` | `Availability` |
| `LABEL_BRAND` | `Marca` | `Brand` |
| `LABEL_SKU` | `Ref.` | `Item No.` |
| `LABEL_IN_STOCK` | `Em stock` | `In Stock` |
| `LABEL_OUT_OF_STOCK` | `Esgotado` | `Out of Stock` |
| `LABEL_LIMITED_STOCK` | `Últimas unidades` | `Limited Availability` |
| `FAQ_SECTION_HEADING` | `Perguntas Frequentes` | `Frequently Asked Questions` |
| `BREADCRUMB_HOME_LABEL` | `Início` | `Home` |

---

## Section 6 — Condition Labels (Productused)

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `CONDITION_NEW` | `Novo` | `New` |
| `CONDITION_MINT` | `Como novo / Mint` | `Mint` |
| `CONDITION_VERY_GOOD` | `Muito bom (A)` | `Very Good` |
| `CONDITION_GOOD` | `Bom (A/B)` | `Good` |
| `CONDITION_ACCEPTABLE` | `Aceitável (B/C)` | `Acceptable` |
| `CONDITION_VERY_USED` | `Muito usado (C/D)` | `Very Used` |
| `CONDITION_REFURBISHED` | `Revisado / CLA` | `Refurbished / Serviced` |
| `CONDITION_FOR_PARTS` | `Para peças / Avariado` | `For Parts / Defective` |

---

## Brazil Override — `--lang pt-br`

When the target market is Brazil, the following keys change **on top of** the Portugal overrides above.  
The agent loads: `base.md` → `pt.md` → `pt-br.md` (three-layer merge).

> Create `LOCALE/pt-br.md` with only these Brazil-specific overrides:

| Key | pt-BR Override | pt (Portugal) value |
|-----|----------------|---------------------|
| `LOCALE_STRING` | `pt-BR` | `pt-PT` |
| `SCHEMA_ADDRESS_COUNTRY` | `BR` | `PT` |
| `SCHEMA_PRICE_CURRENCY` | `BRL` | `EUR` |
| `SCHEMA_STORE_LOCALE` | `pt-BR` | `pt-PT` |
| `SCHEMA_TIMEZONE_OFFSET` | `-03:00` | `+00:00` |
| `PRICE_SYMBOL` | `R$` | `€` |
| `PRICE_SYMBOL_POSITION` | `before` | `after` |
| `PRICE_FORMAT` | `R$ X.XXX,XX` | `X.XXX,XX €` |
| `PRICE_EXAMPLE` | `R$ 1.090,00` | `1.090,00 €` |
| `QUOTE_OPEN` | `"` | `«` |
| `QUOTE_CLOSE` | `"` | `»` |
| `FORMALITY_SECOND_PERSON` | `você` | `você` *(same)* |
| `CTA_CONTACT_US` | `Fale conosco` | `Contacte-nos` |
| `LABEL_IN_STOCK` | `Em estoque` | `Em stock` |
| `CONDITION_REFURBISHED` | `Revisado / Recondicionado` | `Revisado / CLA` |

---

*Last updated: 24-08-2026 (v0.9.2)*
*Adds: reconstructed the title, Purpose block, Section 1 (HTML & Meta), Section 2 (date/price/
number formatting), Section 3 (schema fields), and Section 4.1-4.3 (formality, punctuation, slugs)
that the v0.9.1 commit's message described adding but whose diff never actually included; also
fixed the stale Base Default column for META_DESC_MAX_CHARS (160 → 155)*
*Maintainer: Chris — SEOwlsClaw Portuguese locale overrides*