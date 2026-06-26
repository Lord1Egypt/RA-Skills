
### 4.4 Keyword & Content Writing Rules

| Key | pt Override | Base Default |
|-----|-------------|--------------|
| `KEYWORD_COMPOUND_RULE` | `space-separated` | `space-separated` |
| `META_DESC_MAX_CHARS` | `155` | `160` |

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

*Last updated: 2026-04-04 (v0.6)*  
*Maintainer: Chris — SEOwlsClaw Portuguese locale overrides*