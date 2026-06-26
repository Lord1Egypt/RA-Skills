# SEOwlsClaw — Brain Architecture (v0.6) Universal Brain System 🧠

## Purpose

This document defines the **complete processing logic** of the SEOwlsClaw agent brain.
It describes every step from receiving a user command to producing final HTML output.
All steps are executed in the order listed here — no exceptions.

---

## The Unified Brain Workflow 🔄

### Input: ANY User Prompt + Persona

```
Prompt:     "Brand new eco-friendly water bottle"
Persona:    E-Commerce Manager
Page Type:  Productnew
Primary KW: "sustainable water bottle"
```

---

### Step 0 — Search Intent Detection 🎯 FIRST, ALWAYS

**Run before anything else — even before parsing the command.**  
**Full rules:** See `SEO_CHECKS/search_intent.md`

Analyze the user prompt → detect intent → auto-select correct page format.

| Detected Intent | Trigger Words | Auto-Selected Format |
|----------------|---------------|----------------------|
| **Informational** | how to, why, what is, guide, explained | `Blogpost` |
| **Commercial Investigation** | best, vs, compare, review, top | `Blogpost` (comparison) |
| **Transactional** | buy, price, in stock, order, purchase | `Productnew` or `Productused` |
| **Navigational** | official site, login, [brand] + homepage | `Landingpage` |

**If the user specifies a page type explicitly in the command → skip auto-selection, use their type.**  
**If intent is ambiguous → ALWAYS ask one clarifying question before proceeding.**

---

### Step 1 — Parse Command

Extract all parameters from the user input:

```python
persona_id   = extract_persona()      # e.g. "ecommerce-manager"
page_type    = extract_page_type()    # e.g. "Productnew"
content_prompt = extract_prompt()     # e.g. "Brand new eco-friendly water bottle"
primary_kw   = extract_flag("--primary-kw")   # e.g. "sustainable water bottle"
secondary_kw = extract_flag("--secondary-kw") # optional
tone_override = extract_flag("--tone")        # optional override
target        = extract_flag("--target")      # e.g. "ai-overview", "snippet:list", "paa"
depth         = extract_flag("--depth")       # "light" | "standard" | "deep" (default: standard)
persona_id   = extract_persona()      # e.g. "ecommerce-manager"
page_type    = extract_page_type()    # e.g. "Productnew"
content_prompt = extract_prompt()     # e.g. "Brand new eco-friendly water bottle"
primary_kw   = extract_flag("--primary-kw")   # e.g. "sustainable water bottle"
secondary_kw = extract_flag("--secondary-kw") # optional
tone_override = extract_flag("--tone")        # optional override
target        = extract_flag("--target")      # e.g. "ai-overview", "snippet:list", "paa"
depth         = extract_flag("--depth")       # "light" | "standard" | "deep" (default: standard)
brand_id      = extract_flag("--brand")       # NEW: e.g. "example-name" — loads BRANDS/<id>.md
brief_id      = extract_flag("--from-brief")  # NEW: e.g. "leica-m6-guide-de" — loads SEO_BRIEFS/<id>.md
plan_id    = extract_flag("--plan")   # NEW: "vintage-analog-cameras-de.qw-01" or just "vintage-analog-cameras-de"
plan_mode  = extract_flag("--mode")   # NEW: "cluster" (default) | "site"
plan_priority = extract_flag("--priority")  # NEW: "balanced" (default) | "quickwins" | "strategic"
```

**`/seoplan` command — special parse rules:**

`/seoplan` is a strategic command. It does NOT run Steps 4–5 (no template, no HTML).
Instead it runs a research + analysis pipeline and outputs a structured plan.

Parse extracts:
```python
niche_prompt   = extract_prompt()          # e.g. "Vintage analog cameras Germany"
plan_mode      = extract_flag("--mode")    # "cluster" | "site" — default: "cluster"
plan_lang      = extract_flag("--lang")    # directs keyword research to correct SERP market
plan_brand     = extract_flag("--brand")   # load brand for persona defaults + compliance
plan_priority  = extract_flag("--priority") # "balanced" | "quickwins" | "strategic"
plan_depth     = extract_flag("--depth")   # "light" (outline only) | "standard" | "deep"
plan_pages     = extract_flag("--pages")   # optional: target number of nodes, default auto
```

---

**`--from-brief` processing at Step 1:**

IF `--from-brief <brief-id>` is present:
  1. Load `SEO_BRIEFS/<brief-id>.md`
  2. Extract: `primary_kw`, `secondary_kw`, `paa_questions`, `approved_outline`,
     `internal_links`, `word_count_target`, `competitor_gaps`
  3. Use extracted values as defaults — explicit command flags still override them
     (e.g. if `--primary-kw` is also in the command, command wins over brief)
  4. Store `brief_data{}` for use in Step 3 (outline + variables) and Step 6.5 (depth check)

---

### Step 2 — Load Persona (2-Step Process)

**Step 2a:** Read `PERSONAS/_index.md` → find the row matching `persona_id`  
**Step 2b:** Load `PERSONAS/<id>.md` → extract all of the following:

| What to extract | Used in |
|-----------------|---------|
| Writing Style + Tone + Vocabulary | Step 3 (variable generation) |
| AI Overview Rules + Zone A/B markers | Step 3.5 (zone assignment) |
| E-E-A-T Injection signals | Step 6.5 (compliance check) |
| Heading Formula | Step 3 (all H1–H4 variables) |
| Content Depth Standards | Step 6.5 (compliance check) |

**Step 2c:** Load Locale files → merge into variable dictionary

  IF `--lang` flag is present:
    1. Load `LOCALE/base.md` → store all keys as `locale_vars{}`
    2. Load `LOCALE/<lang_code>.md` → override matching keys in `locale_vars{}`
    3. Use merged result for all locale variables
  
  IF no `--lang` flag:
    1. Load `LOCALE/base.md` only → use as `locale_vars{}`
  
  All `{LANG_CODE}`, `{LOCALE_STRING}`, `{SCHEMA_IN_LANGUAGE}`,
  `{SCHEMA_PRICE_CURRENCY}`, `{SCHEMA_ADDRESS_COUNTRY}`, `{CTA_BUY_NOW}`,
  `{LABEL_CONDITION}`, `{CONDITION_*}` and all other locale keys are now
  available for variable substitution in Step 7.

**Step 2d:** Load Brand Profile (NEW)
**Runs only if `/brand <id>` was issued in the session OR `--brand <id>` flag is present.**

```
Step 2d-1: Read BRANDS/_index.md → find the row matching brand_id
Step 2d-2: Load BRANDS/<id>.md → extract all fields into brand_vars{}
Step 2d-3: Merge brand_vars{} into the variable dictionary:
            - BRAND_* variables added directly
            - Brand CTAs override matching LOCALE/ CTA keys
              (e.g. brand.ctas.de.primary overrides locale_vars.CTA_BUY_NOW)
            - Tone sliders stored as brand_tone{} for Step 3
Step 2d-4: Store brand.compliance{} object for Step 6.6

If no /brand command and no --brand flag → skip Step 2d. No brand rules apply.
```

**Tone Merge Logic (brand sliders + persona):**

| Situation | Result |
|-----------|--------|
| No brand active | Persona tone rules apply as-is |
| Brand active, no --tone flag | Brand slider values override persona tone defaults |
| Brand active + --tone flag | --tone flag wins over BOTH brand sliders and persona defaults |

**Variable Dictionary Additions from Brand Profile:**

```python
brand_vars = {
  "BRAND_ID":              "exampleID",
  "BRAND_NAME":            "exampleName",
  "BRAND_TAGLINE":         "exampleTagline",
  "BRAND_DISCLAIMER":      "exampleDisclaimer",
  "BRAND_TRUST_BLOCK":     "exampleTrustBlock",
  "BRAND_RETURN_POLICY":   "exampleReturnPolicy",
  "BRAND_SUPPORT_URL":     "https://example.com/support/",
  "BRAND_LOGO_URL":        "https://example.com/media/image/example-logo-297x99.webp",
  # CTAs injected from brand.ctas.<lang> — override LOCALE/ defaults:
  "CTA_BUY_NOW":           "Example",       # overrides LOCALE/<id>.md value
  "CTA_SOFT":              "Example",
  "CTA_CONTACT":           "Example",
}
```

**Default fallback:** If no `/persona` command was given → load `PERSONAS/blogger.md`  
**Tone override:** If `--tone` flag is present → override persona's default tone, keep everything else

**Step 2e:** SEO Plan Pipeline (NEW)
**Runs only if `/seoplan` command is active.**

`/seoplan` runs a dedicated pipeline instead of the standard Steps 3–7.
Steps 3–7 are for page content generation only — they do not run for `/seoplan`.

```
seoplan-Step A    Niche + Market Research
seoplan-Step B    Cluster Architecture Design
seoplan-Step C    Node Tiering + Priority Assignment
seoplan-Step D    Internal Link Matrix
seoplan-Step E    Execution Order
seoplan-Step F    Plan Quality Check
seoplan-Step G    Output + Save
```

**Full rules for seoplan-Steps A–G:** See `SEO_PLANS/plan_workflow.md`
Load this file immediately when `/seoplan` is triggered. Do not load `SEO_PLANS/plan_workflow.md` for any other command.


---

### Step 3 — Generate Variables

Using the content prompt + loaded persona, build the full variable dictionary.

**Apply persona rules during generation:**
- Use the persona's **Heading Formula** for all `H1_*`, `H2_*`, `H3_*`, `H4_*` variables
- Use the persona's **Vocabulary** for body copy variables
- Use the persona's **Depth Standards** to determine how many sections/variables to generate

**Example variable dictionary (Productnew):**

```python
variables = {
  # Meta
  "TITLE":             "Brand New Eco-Friendly Water Bottle — Sustainable Hiking Gear",
  "META_DESCRIPTION":  "Discover the best sustainable water bottle for hiking in 2026...",
  "URL_CANONICAL":     "https://example.com/products/eco-water-bottle",

  # Headings (generated using persona Heading Formula)
  "H1_TITLE":                        "Brand New Eco-Friendly Water Bottle — Sustainable Hiking Gear",
  "HERO_SUBHEADLINE_URGENCY":        "Premium stainless steel — lifetime warranty included",
  "H2_VALUE_PROP_TITLE":             "Why This Water Bottle Is Worth Every Cent for Eco-Hikers",
  "H3_FEATURES_TITLE":               "Complete Technical Specifications",
  "H4_COMPARISON_NEW_VERSION_OR_BENEFITS": "EcoSmart Bottle vs Standard Steel Bottles: Key Differences",
  "H5_PURCHASE_BUTTON_TEXT_LIMITED_STOCK": "Order Today — Limited Stock Available",

  # Content
  "VALUE_CONTENT_300_CHARS_MAX":     "...",
  "SCARCITY_COUNT":                  "Only 12 units left",
  "SPEC_1_LABEL":                    "Material",
  "SPEC_1_VALUE_UNIT":               "18/8 Stainless Steel + BPA-Free Coating",
  # ... all remaining variables
}
```

---

**If brand profile is active (Step 2d ran):**
- Apply `brand.preferred_terms{}` as soft vocabulary constraints during generation
  → Brain prefers brand terms when generating body copy
  → No hard fail if a non-preferred synonym slips through (that's Step 6.6's job)
- Use `brand.trust_priorities{}` to determine which trust signals to emphasise in
  spec, condition, and value-prop sections
- If `brief_data{}` is loaded (--from-brief): use `brief_data.approved_outline`
  as the H1–H4 structure template → generate content to fill that outline
  instead of generating headings from scratch

---


### Step 3.5 — Zone Assignment Pass (AI Overview Enforcement) 🔴

**This step applies the AI Overview Rules loaded from the persona file.**

For every content section variable, assign it to a zone and enforce the rules:

#### Zone A — AI Overview Zone
Applies to: `H2_*` intro paragraphs, spec tables, feature descriptions, comparison sections, FAQ blocks.

**Enforce in Zone A:**
- First sentence of every H2 section → factual, neutral, zero sales words
- No scarcity triggers, no urgency phrases, no CTAs inside this zone
- Structure: **Answer first (1 sentence) → Explain (2–3 sentences)**
- Validate: does sentence 1 answer a real search query on its own? If not → rewrite

**Zone A marker in output HTML:**
```html
<!-- ZONE:AI -->
<section>...factual content...</section>
<!-- /ZONE:AI -->
```

#### Zone B — Conversion Zone
Applies to: CTA blocks, price presentation, urgency messaging, hero subheadlines, testimonials.

**Rules in Zone B:**
- Full persona vocabulary applies — scarcity triggers, urgency language, benefit-first CTAs all allowed
- Zone B sections must always appear **after** at least one Zone A section on the page

**Zone B marker in output HTML:**
```html
<!-- ZONE:CTA -->
<section>...conversion content...</section>
<!-- /ZONE:CTA -->
```

**Note:** If the active persona is `blogger`, `researcher`, or `vintage-expert`, the entire page is effectively Zone A. Zone B only activates for `ecommerce-manager` and `creative-writer` personas.

---

### Step 4 — Select Template

Match `page_type` → load the corresponding template file:

| Page Type | Template File |
|-----------|---------------|
| `Blogpost` | `TEMPLATES/blog_post_template.md` |
| `FAQ Page` | `TEMPLATES/faq_page_template.md` |
| `Landingpage` | `TEMPLATES/landing_page_template.md` |
| `Productnew` | `TEMPLATES/product_new_template.md` |
| `Productused` | `TEMPLATES/product_used_template.md` |
| `Socialphoto` | `TEMPLATES_SOCIAL/photo_post_template.md` |
| `Socialvideo` | `TEMPLATES_SOCIAL/video_post_template.md` |

**Intent-override rule:** If Step 0 detected a different page type than what the user specified, and no explicit type was given in the command → use the intent-detected type.

---

### Step 5 — Variable Substitution

Replace every `{PLACEHOLDER}` in the loaded template with its generated value.

```python
def inject_variables(template_text: str, variables: dict) -> str:
    """Replace ALL {PLACEHOLDER} text with actual values."""
    return template_text.format(**variables)
```

**Rules:**
- Every `{PLACEHOLDER}` in the template must be replaced — no placeholder may survive into output
- If a variable is missing from the dictionary → flag it, ask the user for the value, do not output `{PLACEHOLDER}` text
- Schema variables (`{SCHEMA_*}`) are substituted in the same pass — see schema variable tables below

---

### Step 6 — SEO Checks

Run the appropriate checks from `SEO_CHECKS/`:

| Check File | When to Run |
|------------|-------------|
| `SEO_CHECKS/do-and-don-lists.md` | Every page type, every time |
| `SEO_CHECKS/page-type-specific-checks.md` | Match section to current page type |
| `SEO_CHECKS/seo-output-quality-checklist.md` | Every page type, every time |
| `SEO_CHECKS/schema-markup.md` | Every page type — validate schema is correct |
| `SEO_CHECKS/search_intent.md` | Confirm output format matches detected intent |
| `SEO_CHECKS/seo-checks-reference.md` | Every page type, every time, workflow for SEO validation |

---

### Step 6.5 — Persona Compliance Check 🔴

**Run before generating output. Fix failures before outputting.**

Using the Depth Standards and E-E-A-T rules loaded from the persona file in Step 2:

```
[ ] Heading Formula applied?
      → Every H1–H4 and by page type also H5 and H6 matches the persona's heading pattern
      → No vague labels ("Features", "Overview") used as standalone headings

[ ] Content Depth met?
      → Word count ≥ persona minimum for this page type
      → Required sections all present (e.g. comparison table, FAQ block)

[ ] E-E-A-T signals present?
      → Count mandatory signals per persona rules
      → Flag any missing signals and inject before output

[ ] Zone A/B correct?
      → No sales language inside <!-- ZONE:AI --> sections
      → At least one ZONE:AI section appears before any ZONE:CTA section

[ ] No placeholder leakage?
      → Scan output for any remaining {PLACEHOLDER} text
      → If found → generate missing value or ask user
```

If any check fails → revise the relevant section. Do not output until all checks pass.

---

### Step 6.6 — Brand & Legal Compliance Check

**Runs only if a brand profile is active (Step 2d ran).**
**Runs AFTER Step 6.5 — fix Step 6.5 failures first.**

Using `brand.compliance{}` loaded in Step 2d:

```
[ ] Banned phrases check (HARD FAIL)
      → Scan full output text for every pattern in brand.compliance.banned_phrases[]
      → Match is case-insensitive
      → If any match found:
          - BLOCK output
          - Show: location, matched phrase, suggested replacement
          - Do not output until all banned phrases are resolved

[ ] Banned claims check (HARD FAIL)
      → Scan for patterns in brand.compliance.banned_claims[]
      → Same rules as banned phrases

[ ] Urgency level check (HARD FAIL if exceeded)
      → Detect urgency language in Zone B sections
      → Compare against brand.compliance.urgency_limit:
          NONE       → any urgency language = FAIL
          SOFT       → "only X available", "while stocks last" = OK | countdowns = FAIL
          STANDARD   → explicit stock numbers, date-based end = OK | fake timers = FAIL
          AGGRESSIVE → all urgency patterns = OK
      → If exceeded: FAIL + suggest a softer alternative

[ ] Artificial scarcity check (HARD FAIL if disallowed)
      → If brand.compliance.artificial_scarcity_allowed = false:
          → Flag countdown timer references, fabricated stock numbers
          → FAIL if found

[ ] Required disclosures check (WARNING — HARD FAIL only if risk_level = HIGH)
      → Verify each entry in brand.compliance.required_disclosures[] is present
      → If missing + risk_level = HIGH → HARD FAIL
      → If missing + risk_level = LOW or MEDIUM → WARNING only (show reminder, continue)

[ ] Brand term spelling check (WARNING — does not block output)
      → Verify brand.brand_terms[] are spelled/capitalised correctly
      → Flag issues + suggest corrections
```

**Violation output format:**

```
⛔ Step 6.6 — Brand Compliance FAILED
Brand: [brand-id] | Risk Level: [LOW / MEDIUM / HIGH]

HARD FAILS (fix before output):
  ❌ Banned phrase: "[phrase]" at [location]
     → Suggestion: [replacement]
  ❌ Urgency limit exceeded: "[phrase]" at [location]
     → Brand limit: [SOFT/STANDARD] | Suggestion: [alternative]

WARNINGS (review recommended):
  ⚠️  Required disclosure missing: "[disclosure text]"
      → Suggestion: add to [footer / price block / disclaimer section]
  ⚠️  Brand term: "[wrong spelling]" → should be "[correct spelling]"

Fixing [n] hard fail(s) before output.
```

---

### Step 7 — Output

Return the complete output as clean text or HTML in chat, depending if the user prompt was /write or /writehtml ready for deployment.

**Output format:**
```html
<!DOCTYPE html>
<html lang="{LANG_CODE}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE}</title>
  <meta name="description" content="{META_DESCRIPTION}">
  <link rel="canonical" href="{URL_CANONICAL}">
  <!-- JSON-LD Schema (from SEO_CHECKS/schema-markup.md) -->
  <script type="application/ld+json">{ ... }</script>
</head>
<body>
  <!-- ZONE:AI -->
  <!-- ZONE:CTA -->
  <!-- content -->
</body>
</html>
```

**After output:** Offer the user:
- `"give me raw HTML only"` → strip markdown, return pure HTML code block
- `"run /checks"` → re-run SEO audit on the generated output

---

## Schema Variables Reference

All `{SCHEMA_*}` variables are substituted in Step 5 alongside content variables.  
Full schema rules and required fields: see `SEO_CHECKS/schema-markup.md`

### Global — All Page Types

| Variable | Type | Example Value |
|----------|------|---------------|
| `{SCHEMA_IMAGE_URL}` | String (URL) | `https://www.example.de/img/products/leica-m6.jpg` |
| `{SCHEMA_SKU}` | String | `EXAMPLE-10042` |
| `{SCHEMA_AVAILABILITY}` | Schema URL | `https://schema.org/InStock` |
| `{SCHEMA_BREADCRUMB_L2_URL}` | String (URL) | `https://www.example.de/leica-cameras` |
| `{SCHEMA_BREADCRUMB_L2_NAME}` | String | `Leica cameras` |

### Productused Only

| Variable | Type | Example Value |
|----------|------|---------------|
| `{SCHEMA_CONDITION}` | Schema URL | `https://schema.org/UsedCondition` |

### Blogpost Only

| Variable | Type | Example Value |
|----------|------|---------------|
| `{SCHEMA_DATE_PUBLISHED}` | ISO 8601 | `2026-04-15` |
| `{SCHEMA_DATE_MODIFIED}` | ISO 8601 | `2026-04-15` |

### Landingpage Only

| Variable | Type | Example Value |
|----------|------|---------------|
| `{SCHEMA_OFFER_VALID_FROM}` | ISO 8601 | `2026-04-01T00:00:00+02:00` |
| `{SCHEMA_OFFER_VALID_THROUGH}` | ISO 8601 | `2026-04-30T23:59:59+02:00` |

### FAQ — Any Page Type with FAQ Section

| Variable | Type | Example Value |
|----------|------|---------------|
| `{FAQ_Q1}` through `{FAQ_Q5}` | String | `What condition is the camera in?` |
| `{FAQ_A1}` through `{FAQ_A5}` | String | `The camera is in very good condition and fully functional.` |

---

## Template Variable Reference

Complete variable lists per page type. All variables below are replaced in Step 5.

### Blogpost

```
{TITLE, META_DESCRIPTION, URL_CANONICAL, H1_TITLE, HERO_SUBHEADLINE,
 INTRO_H2_TITLE, INTRO_CONTENT_300_CHARS_MAX,
 H3_SECTION_1_TITLE, STEP_1_DETAIL, TIP_1_ACTIONABLE,
 H4_COMPARISON_TITLE, COMPARISON_CATEGORY, COMP_A, COMP_B,
 CONCLUSION_CONTENT_300_CHARS_MAX, READ_MORE_LINK,
 SCHEMA_DATE_PUBLISHED, SCHEMA_DATE_MODIFIED,
 SCHEMA_IMAGE_URL, SCHEMA_BREADCRUMB_L2_URL, SCHEMA_BREADCRUMB_L2_NAME,
 FAQ_Q1–FAQ_Q5, FAQ_A1–FAQ_A5}
```

### Landingpage

```
{TITLE, META_DESCRIPTION, URL_CANONICAL, H1_TITLE, PRIMARY_KEYWORD,
 HERO_SUBHEADLINE_URGENCY, SCARCITY_COUNT,
 H2_VALUE_PROP_TITLE, VALUE_CONTENT_300_CHARS_MAX,
 H3_FEATURES_TITLE, LIST_ITEM_1_BENEFITS, LIST_ITEM_2_LIMITED_OFFER, LIST_ITEM_3_EXCLUSIVE_DEAL,
 H4_TESTIMONIAL_TITLE, TESTIMONIAL_QUOTE, TESTIMONIAL_NAME,
 H5_FINAL_CTA_TITLE, FINAL_CTA_BULLET_POINTS, CTA_LINK,
 BUTTON_TEXT_LIMITED_STOCK, RELATED_PAGE_TITLE, FAQ_SECTION_TITLE, POLICY_LINK,
 SCHEMA_TYPE, SCHEMA_OFFER_VALID_FROM, SCHEMA_OFFER_VALID_THROUGH,
 SCHEMA_IMAGE_URL, SCHEMA_SKU, SCHEMA_AVAILABILITY,
 SCHEMA_BREADCRUMB_L2_URL, SCHEMA_BREADCRUMB_L2_NAME,
 FAQ_Q1–FAQ_Q5, FAQ_A1–FAQ_A5}
```

### Productnew

```
{TITLE, META_DESCRIPTION, URL_CANONICAL, BRAND_NAME,
 PRICE_CURRENCY_PRICE, RATING_VALUE, RATING_COUNT,
 H1_TITLE, HERO_SUBHEADLINE, DISPLAY_PRICE_EUR,
 H2_DESCRIPTION_OVERVIEW_FEATURES, DESCRIPTION_CONTENT_400_CHARS_MAX, USE_CASE_BULLET_POINTS,
 H3_TECHNICAL_SPECS_TITLE_DETAILED,
 SPEC_1_LABEL, SPEC_1_VALUE_UNIT, SPEC_2_LABEL, SPEC_2_VALUE_UNIT,
 SPEC_3_LABEL, SPEC_3_VALUE_UNIT, SPEC_4_LABEL, SPEC_4_VALUE_UNIT,
 H4_COMPARISON_NEW_VERSION_OR_BENEFITS, COMPARISON_CATEGORY, COMP_A, COMP_B,
 H5_PURCHASE_BUTTON_TEXT_LIMITED_STOCK,
 BULLET_1_WARRANTY_FREE_OR_GUARANTEE, BULLET_2_SHIPPING_QUICK_DELIVERY,
 BULLET_3_TECHNICAL_SUPPORT_AVAILABLE, PURCHASE_LINK,
 RELATED_PRODUCT_TITLE, COMPARE_WITH_COMPETITOR_PAGE, TECH_SUPPORT_LINK,
 SCHEMA_IMAGE_URL, SCHEMA_SKU, SCHEMA_AVAILABILITY,
 SCHEMA_BREADCRUMB_L2_URL, SCHEMA_BREADCRUMB_L2_NAME,
 FAQ_Q1–FAQ_Q5, FAQ_A1–FAQ_A5}
```

### Productused

```
{TITLE, META_DESCRIPTION, URL_CANONICAL, BRAND_NAME,
 PRICE_CURRENCY_PRICE_USED, CONDITION_LEVEL_USED,
 H1_TITLE, HERO_SUBHEADLINE_CONDITION_DISCLOSURE,
 DISPLAY_PRICE_EUR_USED, SAVE_PERCENTAGE,
 H2_OVERVIEW_CONDITION_DISCLOSURE, CONDITION_CONTENT_300_CHARS_MAX,
 INSPECTION_BULLET_1_FUNCTIONALITY_TESTED, INSPECTION_BULLET_2_WEAR_AND_TEAR_ASSESSMENT,
 INSPECTION_BULLET_3_ACCESSORIES_COMPLETENESS,
 H3_FEATURE_COMPARISON_NEW_VS_USED,
 DIFF_1_FUNCTIONALITY_PRESERVED, DIFF_1_VALUE_PROPOSITION,
 DIFF_2_COST_SAVINGS_PERCENTAGE, DIFF_2_BEST_FOR_PRICE_SENSITIVE_BUYERS,
 DIFF_3_ECO_IMPACT_REDUCTION, DIFF_3_SUSTAINABILITY_BENEFIT,
 H4_COSMETIC_CONDITION_REPORT_DETAIL,
 COSMETIC_ITEM_1_NO_SCRATCHES_OR_MARKS, COSMETIC_ITEM_2_LIGHTLY_USED_BUT_FUNCTIONAL,
 H5_PURCHASE_WITH_CONFIDENCE_WARRANTY,
 WARRANTY_1_FULL_FUNCTIONALITY_GUARANTEE, WARRANTY_2_30_DAYS_RETURN_POLICY,
 WARRANTY_3_TECHNICAL_SUPPORT_AVAILABLE, PURCHASE_LINK_USED,
 SCHEMA_CONDITION, SCHEMA_IMAGE_URL, SCHEMA_SKU, SCHEMA_AVAILABILITY,
 SCHEMA_BREADCRUMB_L2_URL, SCHEMA_BREADCRUMB_L2_NAME,
 FAQ_Q1–FAQ_Q5, FAQ_A1–FAQ_A5}
```

---

## Workflow Summary (Quick Reference)

```
Step 0    Search Intent Detection     → auto-select page format (search_intent.md)
           SKIP for: /seoplan, /seobrief (strategy commands — no page format needed)
Step 1    Parse Command               → extract persona, type, prompt, flags
           --from-brief               → load SEO_BRIEFS/<id>.md if flag present
           --plan                     → load SEO_PLANS/<plan-id>.md node if flag present
Step 2a   Load Persona Index          → PERSONAS/_index.md → find persona_id
Step 2b   Load Persona File           → PERSONAS/<id>.md → style, tone, E-E-A-T
           /seoplan + /seobrief       → always load researcher.md internally
Step 2c   Load Locale                 → LOCALE/base.md + LOCALE/<lang>.md
Step 2d   Load Brand Profile (NEW)    → if /brand active: BRANDS/<id>.md → brand_vars{} + compliance{}
Step 2e   SEO Plan Pipeline (NEW)     → if /seoplan active: load SEO_PLANS/plan_workflow.md → run Steps A–G → STOP
Step 3    Generate Variables          → prompt + persona + brand + brief → full variable dict
Step 3.5  Zone Assignment Pass        → apply Zone A/B rules to content sections
Step 4    Select Template             → match page type → load TEMPLATES/<type>.md
           /write skips Steps 4–5 (plain text output)
Step 5    Variable Substitution       → replace ALL {PLACEHOLDER} in template
Step 6    SEO Checks                  → run all applicable check files in SEO_CHECKS/
Step 6.5  Persona Compliance Check    → headings · depth · E-E-A-T · zones · no leakage
Step 6.6  Brand Compliance Check (NEW)→ if brand active: banned phrases · urgency · disclosures
           HARD FAIL blocks output until resolved.
Step 7    Output                      → /write: plain text | /writehtml: pure HTML
           /seobrief: structured brief saved to SEO_BRIEFS/
```

---

*Last updated: 05-04-2026 (v0.6)*
*Adds: Step 2d (lean brand load), Step 2e (lean seoplan pointer), Step 6.6 (compliance)*
*Maintainer: Chris — SEOwlsClaw brain logic, all page types*
