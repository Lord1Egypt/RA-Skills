# SEOwlsClaw — Core Skill (v0.6)

## Name & Description

**Name**: `seowlowsclaw`  
**Description**: Full-stack SEO and content marketing system.
Generates SEO-optimised content (landing pages, blog posts, product pages, FAQ, social) using persona-driven writing, multi-client brand profiles, and locale-aware templates.
Supports brief-first agency workflows via /seobrief + --from-brief, strategic cluster planning via /seoplan, and a three-layer architecture (Locale → Brand → Persona) for clean multi-client work.
Outputs plain text or deploy-ready HTML with full schema markup. 
Named "SEOwlsClaw" (pronounced "See Owls Claw") — the single 'O' makes it sound like "See".

---

## When to Use

Use only when Chris needs SEO-ready content generated with specific personas, keyword strategies, and clean output that can be directly deployed.

**Trigger phrases**:
- "Generate SEO blog post about X"
- "Write product description using E-Commerce Manager persona"
- "Create landing page for Y sale campaign"
- "Audit my SEO strategy"
- "Give me the HTML for a product page about X"
- "Create a content brief for X"
- "Brief me on [topic] before writing"
- "I need a brief for a Blogpost about X"
- "Load brand profile for [client]"
- "Activate brand [id]"
- "Set up brand [client name]"
- "Build an SEO plan for [niche]"
- "Plan a content cluster for [topic]"
- "Give me a site architecture for [niche]"
- "What pages should I build for [topic]?"
- "Show me quick wins for [niche]"
- "I need a content strategy for [client]"

---

## Capability Declaration

| Capability | Status | Notes |
|-----------|--------|-------|
| Network / web search | ✅ Read-only | SERP lookup via search tool — no credentials stored in this skill |
| File system writes | ⚠️ Confirmation required | Agent must ask user before saving any file — never writes autonomously |
| Purchases / payments | ❌ None | Generates transactional *content text* only — does not initiate, process, or interact with any payment system |
| OAuth / API credentials | ❌ None | No API keys, tokens, or authentication stored or required by this skill |
| Crypto / blockchain | ❌ None | Schema.org JSON-LD is used for SEO structured data only — no crypto or blockchain operations allowed |
| Autonomous execution | ⚠️ Gated | File saves and SERP lookups require explicit user trigger — no background runs |

---

## Core Commands

| Command | Output | Example |
|---------|--------|---------|
| `/persona <name>` | Sets writing style/tone for next `/write` or `/writehtml` | `/persona vintage-expert` |
| `/write <type> "prompt"` | **Plain text content** — readable in chat, ready to paste into any editor | `/write Blogpost "Why is iPhone 16 Pro Max better than 15"` |
| `/writehtml <type> "prompt"` | **Pure HTML code** — uses `TEMPLATES/<type>.md` structure, copy-paste ready for deployment | `/writehtml Productnew "Leica M6 TTL Chrome, serial 2741xxx, mint condition"` |
| `/research <topic>` | Keyword cluster + SERP analysis | `/research best sony bravia 55 inch tv` |
| `/checks <url>` | SEO audit checklist against a live URL | `/checks https://example.com/blog-post-example` |
| `/checks <type>` | SEO audit against page type template (preview mode) | `/checks Productnew` |
| `/personas` | List all available personas with one-line descriptions | `/personas` |
| `/personas --show <id>` | Show full details of one persona | `/personas --show vintage-expert` |
| `/brand <id>` | Loads client brand profile (CTAs, tone sliders, compliance rules) | `/brand example-id` |
| `/brands` | Lists all brand profiles or shows details for one | `/brands --show example-id` |
| `/seobrief <type> "topic"` | Generates a structured SEO content brief with KW cluster, outline, PAA, and competitor gaps | `/seobrief Blogpost "DIY computer build" --lang de` |
| `/seoplan "niche"` | Builds a full SEO cluster plan — tiers nodes into PILLAR / QUICKWIN / FOUNDATION / STRATEGIC with keyword data, persona assignments, internal link matrix, and numbered execution order | `/seoplan "best vlogging camera for beginners" --lang en` |

## Skill File Map — Quick Navigation

This is the master reference for every file in the skill. The agent uses this to know what to load and when.
Load only what the current command and workflow requires — never all files at once.

### Root Files (Always Available)

| File | Purpose | When to Load |
|------|---------|--------------|
| `SKILL.md` | Entry point — this file | Always loaded first |
| `BRAIN_ARCHITECTURE.md` | Full 10-step processing logic, variable engine | Load at workflow start |
| `COMMANDS.md` | Complete command + flag reference | Load when user asks about commands or flags |
| `PAGE_STRUCTURES.md` | Master index linking all page templates | Load when selecting a template |
| `SEO_PATH.md` | Full SEO workflow: research → write → check | Load for /research and strategic planning |

### PERSONAS/

| File | Purpose | When to Load |
|------|---------|--------------|
| `_index.md` | Registry of all persona IDs + file paths | Load first on every /persona command |
| `blogger.md` | Default persona — load if no /persona set | Step 2b fallback |
| `ecommerce-manager.md` | Conversion-focused writing | On /persona ecommerce-manager |
| `creative-writer.md` | Narrative, emotional writing | On /persona creative-writer |
| `researcher.md` | Neutral, fact-based — also used internally by /seobrief | Always on /seobrief |
| `vintage-expert.md` | Collector-focused, authoritative | On /persona vintage-expert |
| `travel-photographer.md` | Location + gear-focused | On /persona travel-photographer |

### LOCALE/

| File | Purpose | When to Load |
|------|---------|--------------|
| `base.md` | English defaults for all locale keys | Load on every /write or /writehtml |
| `de.md` | German overrides (Sie-form, DD.MM.YYYY, 1.090,00 €) | Load when --lang de |
| `fr.md` | French overrides (vous-form, guillemets, thin-space thousands) | Load when --lang fr |
| `es.md` | Spanish overrides (tú-form, ¿¡ punctuation) | Load when --lang es |
| `pt.md` | Portuguese overrides (você-form, pt-BR variant) | Load when --lang pt |

### BRANDS/

| File | Purpose | When to Load |
|------|---------|--------------|
| `_index.md` | Registry of all brand IDs + file paths | Load first on every /brand command |
| `<id>.md` | Brand CTAs, tone sliders, compliance rules | Load when /brand active or --brand flag |

### SEO_CHECKS/

| File | Purpose | When to Load |
|------|---------|--------------|
| `search_intent.md` | SERP lookup + intent scoring + disambiguation | Step 0 — before everything else |
| `do-and-don-lists.md` | Page-type specific dos and don'ts | Step 6 SEO checks |
| `schema-markup.md` | Schema.org rules + all {SCHEMA_*} variable definitions | Step 5–6 for /writehtml |
| `seo-checks-reference.md` | Full SEO audit reference | Step 6 + /checks command |
| `seo-output-quality-checklist.md` | Pre-output quality gates | Step 6.5 before final output |

### TEMPLATES/ and TEMPLATES_SOCIAL/

| File | Purpose | When to Load |
|------|---------|--------------|
| `blog_post_template.md` | HTML template for Blogpost | /writehtml Blogpost |
| `landing_page_template.md` | HTML template for Landingpage | /writehtml Landingpage |
| `product_new_template.md` | HTML template for Productnew | /writehtml Productnew |
| `product_used_template.md` | HTML template for Productused | /writehtml Productused |
| `faq_page_template.md` | HTML template for FAQ | /writehtml FAQ |
| `photo_post_template.md` | Social photo post template | /writehtml Socialphoto |
| `video_post_template.md` | Social video metadata template | /writehtml Socialvideo |

### SEO_BRIEFS/ and SEO_PLANS/

| File | Purpose | When to Load |
|------|---------|--------------|
| `SEO_BRIEFS/_index.md` | Registry of all generated briefs | Load on /seobrief or --from-brief |
| `SEO_PLANS/_index.md` | Registry of all generated plans | Load on /seoplan or --plan |
| `SEO_PLANS/plan_workflow.md` | /seoplan pipeline logic (Steps A–G) | Load only on /seoplan |

---

## Output Format

### `/write` — Plain Text Output
Returns clean, structured text content — no HTML tags.  
Use this when you want to **review content first**, paste into a CMS editor, or use the text elsewhere (social caption, email, document).

```
/write Blogpost "How to identify a genuine Leica M6"
→ Returns: Full blog post as readable text with headings, paragraphs, bullet lists
   No HTML tags. Ready to paste into WordPress, JTL Shop editor, Notion, etc.
```

### `/writehtml` — Pure HTML Output
Returns a complete HTML document using the corresponding `TEMPLATES/<type>.md` template.  
All `{PLACEHOLDER}` variables are replaced with real content. Zero placeholders in the output.  
Use this when you want **copy-paste ready code** to deploy directly.

```
/writehtml Productused "Leica M6 TTL, serial 2741xxx, condition EX+"
→ Returns: Full HTML file with all placeholders replaced, schema included,
   Zone:AI and Zone:CTA sections marked, ready to deploy
```

**After any output** the agent will offer:
- `"give me raw HTML only"` → strip markdown wrapping, return pure code block
- `"run /checks"` → re-run SEO audit on the generated output

---

## `/write` vs `/writehtml` — When to Use Which

| Situation | Use |
|-----------|-----|
| Reviewing content before publishing | `/write` |
| Pasting into a visual CMS editor | `/write` |
| Deploying directly to a page | `/writehtml` |
| Checking HTML structure and schema | `/writehtml` |
| Social media captions | `/write` |
| Testing a new template | `/writehtml` |

---

## Page Types Supported

| Type | Description | Recommended Word Count |
|------|-------------|----------------------|
| `Blogpost` | Organic SEO articles, guides, storytelling content | 1,500w+ |
| `Landingpage` | Sales campaigns, newsletter launches, promotions | 900–1,200w |
| `Productnew` | New physical/digital products — tech specs focus | 400–600w |
| `Productused` | Refurbished/second-hand items — condition reports | 500–700w |
| `FAQ` | Standalone FAQ pages, PAA-targeting content with FAQPage schema | 800–1,200w |
| `Socialphoto` | Visual posts with alt text and captions | 100–200w |
| `Socialvideo` | YouTube/TikTok metadata, descriptions, transcripts | 150–300w |

---

## Search Intent Detection 🎯 CRITICAL — Runs Before Everything Else

**When it runs**: Step 0 — BEFORE parsing the command, BEFORE loading any persona.  
**Purpose**: Analyze the user prompt → determine search intent → auto-select the correct page format.  
Wrong format = wrong ranking signal. A product description written for an informational query will not rank.

**Full rules**: See `SEO_CHECKS/search_intent.md`

### Quick Reference

| Detected Intent | Trigger Words | Auto-Selected Format |
|----------------|---------------|----------------------|
| **Informational** | how to, why, what is, guide, explained | `Blogpost` |
| **Commercial Investigation** | best, vs, compare, review, top | `Blogpost` (comparison) |
| **Transactional** | buy, price, in stock, order, purchase | `Productnew` or `Productused` |
| **Navigational** | official site, login, [brand] + homepage | `Landingpage` |

- If the user specifies a page type explicitly → skip auto-selection, use their type
- If intent is ambiguous → ask **one** clarifying question before proceeding

---

## Workflow Steps (Internal Brain) 🧠

> Full processing logic with all step details: see `BRAIN_ARCHITECTURE.md`
> All commands, types, and flags in full detail: see `COMMANDS.md`
> Page template index and structure overview: see `PAGE_STRUCTURES.md`
> Full SEO research and writing workflow: see `SEO_PATH.md`

```
Step 0    Search Intent Detection     Analyze prompt → auto-select page format (SEO_CHECKS/search_intent.md)
           SKIP for: /seoplan, /seobrief — strategy commands, no page format needed
Step 1    Parse Command               Extract persona, type, prompt, all flags
           --from-brief               If flag present → load SEO_BRIEFS/<id>.md at parse time
           --plan                     If flag present → load SEO_PLANS/<plan-id>.md node at parse time
Step 2a   Load Persona Index          PERSONAS/_index.md → find persona_id
Step 2b   Load Persona File           PERSONAS/<id>.md → style, tone, E-E-A-T rules
           /seoplan + /seobrief       Always load researcher.md internally (overrides session persona)
           Default fallback           If no /persona command → load PERSONAS/blogger.md
           Tone override              If --tone flag present → override persona tone, keep everything else
Step 2c   Load Locale                 LOCALE/base.md + LOCALE/<lang>.md (if --lang flag present)
Step 2d   Load Brand Profile          If /brand active or --brand flag: BRANDS/<id>.md → brand_vars{} + compliance{}
           Skip if                    No /brand command and no --brand flag → no brand rules apply
Step 2e   SEO Plan Pipeline           If /seoplan active: load SEO_PLANS/plan_workflow.md → run Steps A–G → STOP (Steps 3–7 do not run)
Step 3    Generate Variables          Prompt + persona + brand + brief + plan node → full variable dictionary
Step 3.5  Zone Assignment Pass        Apply Zone A (neutral/factual) vs Zone B (CTA/sales) to each content section
Step 4    Select Template             Match page type → load TEMPLATES/<type>.md
           /write skips Steps 4–5     Plain text output — no template loading
Step 5    Variable Substitution       Replace ALL {PLACEHOLDER} in template with real values
Step 6    SEO Checks                  Run all applicable files in SEO_CHECKS/
           /seoplan                   Runs plan quality check (Step F in SEO_PLANS/plan_workflow.md) instead
Step 6.5  Persona Compliance Check    Headings formula · depth · E-E-A-T signals · Zone A/B · zero placeholder leakage
           /seoplan                   Skipped (no page content generated)
Step 6.6  Brand Compliance Check      If brand active: banned phrases · urgency limits · required disclosures
           HARD FAIL                  Blocks output until all violations resolved
           /seoplan                   Brand persona defaults applied to node assignments only
Step 7    Output                      /write → plain text | /writehtml → pure HTML
           /seoplan                   Structured plan saved to SEO_PLANS/
           /seobrief                  Structured brief saved to SEO_BRIEFS/
```

### Workflow Example — `/write` (Plain Text)

```bash
/persona creative-writer
/write Blogpost "Shooting film in Nürnberg with a Leica M6" --primary-kw "leica m6 film photography"

# Step 0: Informational intent detected → Blogpost confirmed
# Step 2: Loads PERSONAS/creative-writer.md
# Step 3: Generates variables using Story-Driven style + Heading Formula
# Step 3.5: Assigns Zone A to intro + body sections
# Step 4–5: Skipped (plain text output)
# Step 6–6.5: SEO checks + compliance pass
# Step 7: Returns readable blog post text — no HTML tags
```

### Workflow Example — `/writehtml` (HTML Output)

```bash
/persona ecommerce-manager
/writehtml Productused "Leica M6 TTL Chrome, serial 2741xxx, EX+ condition" --primary-kw "leica m6 ttl kaufen"

# Step 0: Transactional intent → Productused confirmed
# Step 2: Loads PERSONAS/ecommerce-manager.md
# Step 3: Generates full variable dict (all {SPEC_*}, {SCHEMA_*}, {FAQ_*} etc.)
# Step 3.5: Zone A for spec/condition sections, Zone B for CTA/pricing blocks
# Step 4: Loads TEMPLATES/product_used_template.md
# Step 5: Replaces ALL {PLACEHOLDER} — zero placeholders in output
# Step 6–6.5: SEO checks + compliance pass
# Step 7: Returns complete HTML — ready to deploy
```

### Workflow Example — `/seobrief` → `/write` (Brief-First Flow)

```bash
# Step 1: Generate the brief
/seobrief Blogpost "Leica M6 Analogfotografie Guide" --lang de --brand jbv-foto

# → Researcher persona loads internally (always)
# → Keyword cluster researched: primary KW auto-detected
# → 2-3 competitor URLs analysed for gaps
# → Brief saved: SEO_BRIEFS/<YEAR>/<MONTH>/leica-m6-analogfotografie-guide-de.md
# → Output: full structured brief with KW cluster, H1–H4 outline, PAA questions, internal link targets, and ready-to-run /write command

# Step 2: Write content from the brief
/brand jbv-foto
/persona blogger
/write Blogpost "Leica M6 Guide" --from-brief leica-m6-analogfotografie-guide-de --lang de

# → Step 1: Loads brief → KWs, outline, PAA, internal links merged into parse
# → Step 2a-c: blogger persona + de locale
# → Step 2d: jbv-foto brand profile (CTAs, compliance) merged
# → Step 3: Variables generated using brief outline as H-tag structure
# → Steps 6, 6.5, 6.6: SEO + persona + brand compliance all pass
# → Step 7: Returns plain text article following the brief's approved structure
```

### Workflow Example — /seoplan → /seobrief → /write (Full Agency Flow)

```bash
/seoplan "Vintage analog cameras Germany" --lang de --brand jbv-foto
```
→ Step 2e: SEO_PLANS/plan_workflow.md loaded, researcher runs Steps A–G
→ Step A: Keyword families mapped, quick win threshold = difficulty < 22
→ Steps B–C: 11 nodes built and tiered (1 PILLAR + 4 QW + 3 FND + 3 STR)
→ Step D: Internal link matrix generated — no orphan nodes
→ Step E: Execution order: qw-01 → qw-04 first, pillar-01 after, str-01–03 last
→ Step G: Saved as SEO_PLANS/<YEAR>/<MONTH>/vintage-analog-cameras-de.md

```bash
/seobrief Blogpost "Film einlegen Anleitung" --plan vintage-analog-cameras-de.qw-01 --lang de
```
→ Step 1: Node qw-01 loaded from plan → primary_kw, page_type, links_to extracted
→ Research runs on top of plan data, brief saved: SEO_BRIEFS/<YEAR>/<MONTH>/film-einlegen-anleitung-de.md

```bash
/brand jbv-foto
/persona blogger
/write Blogpost "Film einlegen" --from-brief film-einlegen-anleitung-de --lang de
```
→ Brief + plan node + brand all merged at Step 1
→ Steps 6 / 6.5 / 6.6 pass → Step 7: plain text article ready to publish

---

## Variable Substitution Engine 🧠

When you provide a content prompt, the brain:
1. **Extracts variables** from your prompt automatically
2. **Replaces all `{PLACEHOLDER}` text** in the template with real content
3. **Returns zero placeholders** — all `{VAR}` text is gone before output

**Full variable reference per page type**: see `BRAIN_ARCHITECTURE.md`

### Example — Variable Dictionary (Productused, Leica M6)

```python
{
  "TITLE":                              "Leica M6 TTL Chrome — Used, EX+ Condition | WebsiteName",
  "META_DESCRIPTION":                   "Buy a used Leica M6 TTL Chrome in EX+ condition. Serial 2741xxx, 2000–2001 production. Fully functional, CLA'd. 30-day return policy.",
  "URL_CANONICAL":                      "https://www.example.de/products/leica-m6-ttl-chrome-gebraucht",
  "H1_TITLE":                           "Leica M6 TTL Chrome (Type 10434) — EX+ Condition, Serial 2741xxx",
  "HERO_SUBHEADLINE_CONDITION_DISCLOSURE": "2000–2001 production · TTL flash metering · All functions verified",
  "CONDITION_LEVEL_USED":               "EX+",
  "DISPLAY_PRICE_EUR_USED":             "€1,090",
  "SCHEMA_CONDITION":                   "https://schema.org/UsedCondition",
  "SCHEMA_SKU":                         "EXMAMPLE-2741",
  "FAQ_Q1":                             "What condition is this Leica M6 TTL in?",
  "FAQ_A1":                             "EX+ — light use only. No brassing, viewfinder clear, shutter fires accurately at all speeds.",
  # ... all remaining variables
}
```

---

## File Locations & Dependencies

```
seowlowsclaw/
│
├── SKILL.md                    ← This file — core instructions + command reference
├── BRAIN_ARCHITECTURE.md       ← Complete processing logic (all 9 brain steps)
├── COMMANDS.md                 ← Full command reference with all flags
├── PAGE_STRUCTURES.md          ← Master index + links to all page templates
├── SEO_PATH.md                 ← Full SEO workflow: research → analysis → writing → checks
│
├── PERSONAS/                   ← One file per persona
│   ├── _index.md               ← Load first — lists all persona IDs and file paths
│   ├── ecommerce-manager.md
│   ├── creative-writer.md
│   ├── blogger.md              ← Default persona when none specified
│   ├── researcher.md
│   ├── vintage-expert.md
│   └── travel-photographer.md
│
├── BRANDS/                     ← One file per client brand profile
│   ├── _index.md               ← Load first — lists all brand IDs and file paths
│   └── brand-template.md       ← Copy this to create a new brand profile
│
├── LOCALE/                     ← Language override files (Base + Delta architecture)
│   ├── base.md                 ← English defaults for all locale keys — always loaded
│   ├── de.md                   ← German overrides (--lang de)
│   ├── fr.md                   ← French overrides (--lang fr)
│   ├── es.md                   ← Spanish overrides (--lang es)
│   └── pt.md                   ← Portuguese overrides (--lang pt)
│
├── SEO_BRIEFS/                 ← Generated content briefs (one per topic/page)
│   └── _index.md               ← Registry: brief-id | topic | type | date | status
│
├── SEO_PLANS/                  ← One plan file per niche/site campaign
│   ├── _index.md               ← Registry: plan-id | niche | mode | lang | date
│   ├── plan-template.md        ← Format reference + example plan
│   └── plan_workflow.md        ← Full /seoplan pipeline logic (Steps A–G) — loaded only on /seoplan
│
├── SEO_CHECKS/                 ← SEO rules, intent detection, schema, quality checks
│   ├── search_intent.md        ← Step 0 rules — intent detection + format selection
│   ├── do-and-don-lists.md     ← Page-type specific dos and don'ts
│   ├── schema-markup.md        ← Schema.org rules + {SCHEMA_*} variable definitions
│   ├── seo-checks-reference.md ← Full SEO check reference
│   └── seo-output-quality-checklist.md ← Pre-output quality gates
│
├── TEMPLATES/                  ← HTML output templates (used by /writehtml only)
│   ├── blog_post_template.md
│   ├── landing_page_template.md
│   ├── product_new_template.md
│   ├── product_used_template.md
│   └── faq_page_template.md
│
├── TEMPLATES_SOCIAL/           ← Social media output templates
│   ├── photo_post_template.md
│   └── video_post_template.md
│
├── OUTPUT_EXAMPLES/            ← Reference output examples for agent guidance
│   ├── blog_post_example.md
│   ├── landing_page_example.md
│   ├── product_new_example.md
│   └── product_used_example.md
│
#└── DOC/                        ← Internal project docs (not loaded by agent)
#    ├── BUGS.md                 ← Internal project docs (not loaded by agent)
#    ├── CHANGELOG.md            ← Internal project docs (not loaded by agent)
#    └── PLANNING.md             ← Internal project docs (not loaded by agent)
```

---

*Last updated: 05-04-2026 (v0.6)*  
*Adds: /brand, /brands, /seobrief, --from-brief flag, BRANDS/ and SEO_BRIEFS/ folders*
*Maintainer: Chris — SEOwlsClaw core skill file*
