# SEOwlsClaw — Command Reference (v0.8)

## Overview

All commands follow the pattern: `/<command> [type] "prompt" [--flags]`

| Command | Purpose |
|---------|---------|
| `/persona <id>` | Set writing style and tone |
| `/personas` | List or inspect available personas |
| `/write <type> "prompt"` | Generate plain text content (editor-ready) |
| `/writehtml <type> "prompt"` | Generate pure HTML content (deploy-ready) |
| `/research <topic>` | Keyword cluster + SERP analysis |
| `/checks <url or type>` | SEO audit checklist |
| `/brand <id>` | Load a client brand profile (CTAs, tone, compliance rules) |
| `/brands` | List all brand profiles or inspect one |
| `/seobrief <type> "topic"` | Generates a structured SEO content brief with KW cluster, outline, PAA, and competitor gaps |
| `/seoplan "niche"` | Builds a full SEO cluster plan — tiers nodes into PILLAR / QUICKWIN / FOUNDATION / STRATEGIC with keyword data, persona assignments, internal link matrix, and numbered execution order |

## ⚠️ FILE WRITE — CONFIRMATION REQUIRED
Trigger: only runs when the user issues /research, /write, /writehtml, or /checks.
Never write files silently or autonomously.
Before saving any files, you must:
1. Show the user the full file content in chat
2. Show the proposed file path
3. Ask: "Save this file? (yes / no / rename)"
4. Only write to disk after explicit "yes"

---

## `/persona`

Sets the writing style, tone, and vocabulary for the next `/write` or `/writehtml` command.  
Persona stays active until changed or the session resets.

**Syntax:**
```bash
/persona <id> [--tone <adjective>]
```

**Available Persona IDs:**

| ID | Style | Best For |
|----|-------|----------|
| `ecommerce-manager` | Persuasive, urgent, conversion-focused | Product pages, landing pages, sales campaigns |
| `creative-writer` | Imaginative, narrative-driven, emotional | Blog posts, experience stories, brand content |
| `blogger` | Approachable, educational, story-driven | Guides, how-tos, opinion pieces *(default)* |
| `researcher` | Neutral, fact-based, question-first | Comparison guides, technical articles |
| `vintage-expert` | Authoritative, collector-focused, precise | Vintage camera listings, condition reports, historical deep-dives |
| `travel-photographer` | Scenario-driven, location-specific, gear-focused | Travel guides, destination photography content |

**Default:** If no `/persona` is set → `blogger` is loaded automatically.

**Flags:**

| Flag | Purpose | Example |
|------|---------|---------|
| `--tone <adjective>` | Override tone only, keep everything else | `--tone enthusiastic` |

**Examples:**
```bash
/persona vintage-expert
/persona ecommerce-manager --tone urgent
/persona creative-writer --tone poetic
/persona researcher --tone neutral
```

---

## `/personas`

Lists all available personas or shows full details for one.

**Syntax:**
```bash
/personas
/personas --show <id>
```

**Examples:**
```bash
/personas
/personas --show vintage-expert
/personas --show ecommerce-manager
```

---

## `/write`

Generates **plain text content** — no HTML tags.  
Use this when you want to review content first, paste into a CMS editor, or use the text in documents, emails, or social captions.

**Syntax:**
```bash
/write <type> "prompt" [--flags]
```

**Supported Page Types:**

| Type | Description | Target Word Count |
|------|-------------|-------------------|
| `Blogpost` | Organic SEO articles, guides, storytelling | 1,500w+ |
| `Landingpage` | Sales campaigns, newsletter launches | 900–1,200w |
| `Productnew` | New products — tech specs focus | 400–600w |
| `Productused` | Used/refurbished items — condition reports | 500–700w |
| `FAQ` | Standalone FAQ pages, PAA-targeting content | 800–1,200w |
| `Socialphoto` | Visual posts with alt text and captions | 100–200w |
| `Socialvideo` | YouTube/TikTok metadata, descriptions | 150–300w |

**Flags:**

| Flag | Required | Purpose | Example |
|------|----------|---------|---------|
| `"prompt"` | ✅ Yes | Content info, product details, topic | `"Leica M6 TTL Chrome, EX+"` |
| `--primary-kw` | Recommended | Main target keyword | `--primary-kw "leica m6 kaufen"` |
| `--secondary-kw` | Optional | Additional keyword cluster | `--secondary-kw "leica m6 ttl gebraucht"` |
| `--lang` | Optional | Output language (default: English) | `--lang de` |
| `--tone` | Optional | Tone override for this run only | `--tone enthusiastic` |
| `--depth` | Optional | Content depth level | `--depth deep` |

**`--depth` values:**

| Value | Effect |
|-------|--------|
| `light` | Shorter output, fewer sections, faster review |
| `standard` | Default — balanced depth per persona rules |
| `deep` | Maximum depth, all optional sections included |

**Examples:**
```bash
/persona blogger
/write Blogpost "Shooting film in Nürnberg with a Leica M6" --primary-kw "leica m6 analogfotografie" --lang de

/persona vintage-expert
/write Productused "Leica M6 Classic black, serial 1921xxx, Very Good condition" --primary-kw "leica m6 classic kaufen"

/persona ecommerce-manager --tone enthusiastic
/write Landingpage "Spring sale — 20% off all analog cameras, starts April 15th" --primary-kw "analoge kameras sale"

/persona researcher
/write FAQ "Leica M6 buyer questions — condition, price, compatibility" --primary-kw "leica m6 faq" --lang de
```

---

## `/writehtml`

Generates **pure HTML output** using the corresponding `TEMPLATES/<type>.md` template.  
All `{PLACEHOLDER}` variables are replaced — zero placeholders in the output.  
Use this when you want copy-paste ready code to deploy directly.

**Syntax:**
```bash
/writehtml <type> "prompt" [--flags]
```

Supports the same types and all the same flags as `/write`.

**After output**, the agent will offer:
- *"give me raw HTML only"* → strips markdown wrapping, returns pure code block
- *"run /checks"* → re-runs SEO audit on the generated output

**Examples:**
```bash
/persona ecommerce-manager
/writehtml Productused "Leica M6 TTL Chrome, serial 2741xxx, EX+ condition" --primary-kw "leica m6 ttl kaufen" --lang de

/persona vintage-expert
/writehtml Productnew "Leica M6 TTL Silver 0.85, brand new in original box" --primary-kw "leica m6 ttl neu kaufen" --lang de

/persona blogger
/writehtml Blogpost "How to identify a genuine Leica M6" --primary-kw "leica m6 original erkennen" --lang de --depth deep

/persona ecommerce-manager
/writehtml FAQ "Common questions about used Leica cameras" --primary-kw "leica kamera gebraucht faq" --lang de
```

---

## `/research`

Builds a keyword cluster and SERP analysis for a topic before writing.  
Run this before `/write` or `/writehtml` to inform your keyword strategy.

**Syntax:**
```bash
/research "topic" [--include-competitors]
```

**Output includes:**
- Primary keyword (high intent, high volume)
- Long-tail keyword variations (lower competition)
- Related keyword clusters
- SERP features detected (snippets, PAA boxes, images, shopping results)
- Competitor content gaps identified

**Examples:**
```bash
/research "leica m6 gebraucht kaufen"
/research "vintage analog camera berlin" --include-competitors
/research "rangefinder camera beginner guide"
```

---

## `/checks`

Runs an SEO audit checklist. Two modes: live URL or page-type preview.

**Syntax:**
```bash
/checks <url>           ← audit against a live page
/checks <type>          ← audit against page-type template (preview mode)
/checks <type> --strict ← stricter threshold checks
```

**Audit output includes:**
- Page-type-specific dos and don'ts (`SEO_CHECKS/do-and-don-lists.md`)
- Missing or malformed meta tags
- Schema validation (missing fields, wrong types)
- Keyword placement issues
- Internal linking gaps
- Pass rate + prioritized recommendations

**Examples:**
```bash
/checks https://www.example.de/products/leica-m6-ttl-chrome
/checks Productused
/checks Blogpost --strict
/checks Landingpage
```

---

## `/brand`

Loads a client brand profile and makes it active for the current session.
The brand profile adds CTAs, vocabulary rules, trust blocks, and compliance constraints
on top of the active persona and locale.

Brand stays active until changed or the session resets.

**Syntax:**
```bash
/brand <id>
```

**Examples:**
```bash
/brand example-shop
/brand example-agency
```

**What /brand activates:**

| Layer | What Changes |
|-------|-------------|
| CTAs | Brand-specific CTAs replace locale defaults in all {CTA_*} variables |
| Tone | Brand slider values adjust the active persona's tone defaults |
| Vocabulary | Brand preferred terms and banned phrases enforced in Step 3 + Step 6.6 |
| Trust blocks | `{BRAND_TRUST_BLOCK}` and `{BRAND_RETURN_POLICY}` available in templates |
| Compliance | Step 6.6 runs: banned phrases, urgency limits, required disclosures |

**Brand + Persona + Locale — the three layers:**

| Layer | Controls | Changes Per |
|-------|----------|-------------|
| **Persona** | Writing style, vocabulary richness, heading formulas, E-E-A-T | Content type / mood |
| **Brand** | Client identity, CTAs, banned terms, trust blocks, compliance | Client / project |
| **Locale** | Language, currency, date format, schema language fields | Market / language |

These three layers are independent — they stack without conflicting.
A single brand can be written by multiple personas. A single persona can serve multiple brands.

---

## `/brands`

Lists all available brand profiles or shows full details for one.

**Syntax:**
```bash
/brands
/brands --show <id>
```

**Examples:**
```bash
/brands
/brands --show example-shop
```

---

## `/seobrief`

Generates a structured SEO content brief before writing begins.
The brief is saved to `SEO_BRIEFS/<brief-id>.md` and can be passed to `/write`
or `/writehtml` using the `--from-brief` flag to ensure the generated content
follows the researched outline, keywords, and internal link targets.

**Always uses `researcher` persona internally** — regardless of the active session persona.
This keeps keyword analysis neutral and free of sales language.

**Syntax:**
```bash
/seobrief <type> "topic" [--flags]
```

**Supported Types:**
Same as `/write` — `Blogpost`, `Landingpage`, `Productnew`, `Productused`, `FAQ`, `Socialphoto`, `Socialvideo`

**Flags:**

| Flag | Required | Purpose | Example |
|------|----------|---------|---------|
| `"topic"` | ✅ Yes | Topic or product to brief | `"Leica M6 film photography guide"` |
| `<type>` | Recommended | Page type (auto-detected if omitted) | `Blogpost` |
| `--primary-kw` | Optional | Override auto-detected primary keyword | `--primary-kw "leica m6 kaufen"` |
| `--lang` | Optional | Language for keyword research direction | `--lang de` |
| `--depth` | Optional | Brief depth: `light` / `standard` / `deep` | `--depth deep` |
| `--brand` | Optional | Load brand profile for CTA and compliance hints | `--brand example-shop` |

**Output includes:**

- 🎯 Strategic Summary (primary KW, intent, recommended type, word count, persona suggestion)
- 🔑 Keyword Cluster (primary + 4–6 long-tail variations with est. volume + difficulty)
- 📐 Recommended Outline (H1 + H2–H4 structure with topic hints per section)
- ❓ People Also Ask questions to cover (5–10 PAA-style Q&As)
- 🏆 Competitor Analysis (2–3 competitor URLs: strengths, weaknesses, our angle)
- 🔗 Internal Link Targets (anchor text + target URL + placement hint)
- ▶️ Next Step (ready-to-run `/write` command at the bottom — always)

**Examples:**
```bash
/seobrief Blogpost "Best Hiking Boots for Beginners 2026" --lang en --brand example-shop
/seobrief FAQ "Common questions about trail running shoes" --primary-kw "trail shoes faq" --lang en
/seobrief Productused "Used Trail Running Shoe Model X" --lang en --depth deep
/seobrief Landingpage "Spring Sale 2026" --primary-kw "trail gear sale" --brand example-shop
```

**Using a brief with /write:**
```bash
# Generate brief first
/seobrief Blogpost "Best Hiking Boots Guide" --lang en --brand example-shop
# → Saved as SEO_BRIEFS/best-hiking-boots-guide-en.md

# Write content from brief (outline, KWs, and internal links auto-loaded)
/persona blogger
/write Blogpost "Best Hiking Boots Guide" --from-brief best-hiking-boots-guide-en --lang en

# Or generate HTML from brief
/persona blogger
/writehtml Blogpost "Best Hiking Boots Guide" --from-brief best-hiking-boots-guide-en --lang en
```

**`--from-brief` flag (for `/write` and `/writehtml`):**

When `--from-brief <brief-id>` is set:
- The brief's keyword cluster is used as the KW strategy (unless `--primary-kw` overrides it)
- The brief's approved outline guides H1–H4 structure
- PAA questions from the brief populate `{FAQ_Q*}` and `{FAQ_A*}` variables
- Internal link targets are injected as `{INTERNAL_LINKS_PRIMARY}` and `{INTERNAL_LINKS_SECONDARY}`
- The brief's word count target is passed to the depth check in Step 6.5

---

## `/seoplan`

Builds a complete SEO content plan for a niche, topic, or site architecture.
Outputs a structured cluster of nodes organised into four tiers — PILLAR, QUICKWIN,
FOUNDATION, and STRATEGIC — with keyword data, page type recommendations, persona
assignments, an internal link matrix, and a numbered execution order.

The plan is saved to `SEO_PLANS/<plan-id>.md` and can be referenced in any
`/seobrief` command using the `--plan <plan-id>.<node-id>` flag.

**`/seoplan` does not generate page content.** It is a strategy command — run it
once per niche/site and then execute node by node via `/seobrief` → `/write`.

**Syntax:**
```bash
/seoplan "niche or site concept" [--flags]
```

**Flags:**

| Flag | Required | Purpose | Example |
|------|----------|---------|---------|
| `"niche"` | ✅ Yes | Niche, site concept, or target topic | `"Vintage analog cameras Germany"` |
| `--mode` | Optional | `cluster` (default) or `site` | `--mode site` |
| `--lang` | Optional | Market/language for keyword research | `--lang de` |
| `--brand` | Optional | Load brand profile for persona defaults | `--brand example-shop` |
| `--priority` | Optional | `balanced` (default) / `quickwins` / `strategic` | `--priority quickwins` |
| `--depth` | Optional | `light` (4–6 nodes) / `standard` (8–14) / `deep` (15–25) | `--depth deep` |
| `--pages` | Optional | Override auto depth with exact target node count | `--pages 10` |

**`--mode` explained:**

| Mode | Output | Use When |
|------|--------|----------|
| `cluster` | 1 pillar + 8–14 supporting nodes with full detail per node | Starting a new niche or topic campaign |
| `site` | 3–5 cluster overviews (no deep node detail) + drill-down commands | Planning a full site from scratch |

**`--priority` explained:**

| Value | What Gets Emphasised | Use When |
|-------|---------------------|----------|
| `balanced` | All tiers, execution order: QW → FND → Pillar → Strategic | Default — comprehensive plan |
| `quickwins` | Only QUICKWIN nodes output | Client needs fast results, budget for 4–6 articles only |
| `strategic` | All nodes, but PILLAR + STRATEGIC at top | Long-term authority play, no urgency for fast traffic |

**Node Tiers — Quick Reference:**

| Tier | Difficulty | Timeline to Rank | Intent | Persona Mix |
|------|-----------|-----------------|--------|-------------|
| **PILLAR** | 40–70 | 3–6 months | Commercial | Zone A: researcher + Zone B: ecommerce-manager |
| **QUICKWIN** | < 25 | 4–8 weeks | Informational | Zone A: blogger or researcher, Zone B: none |
| **FOUNDATION** | 20–40 | 8–16 weeks | Informational | Zone A: blogger or vintage-expert, Zone B: none |
| **STRATEGIC** | > 40 | 6–12 months | Commercial / Transactional | Zone A: researcher + Zone B: ecommerce-manager |

**Output includes:**

- 🗺️ Topical Map overview (text tree)
- 🏛️ Pillar page (full node card)
- ⚡ Quick Win nodes (table + node cards)
- 🧱 Foundation nodes (table + node cards)
- 🏔️ Strategic nodes (table + node cards)
- 🔗 Internal Link Matrix (who links to whom)
- 📋 Execution Order (numbered, with timeline estimates)
- ▶️ Next Step (first `/seobrief` command to run)

**After output, the brain offers:**
- `"show me only quick wins"` → reprint QUICKWIN section only
- `"generate brief for [node-id]"` → immediately run `/seobrief` for that node
- `"show link matrix"` → reprint internal link matrix only
- `"export execution order"` → print numbered execution list only

**Examples:**

```bash
# Standard cluster plan (8–14 nodes, balanced priority)
/seoplan "Outdoor hiking gear Germany" --lang de --brand example-shop

# Quick wins only — fast client deliverable
/seoplan "Local bakery SEO Berlin" --lang de --priority quickwins --depth light

# Full site architecture overview
/seoplan "Sports e-commerce Germany" --lang de --mode site

# Deep cluster — maximum node count
/seoplan "Trail running shoes" --lang en --brand example-shop --depth deep

# Strategic focus — authority building, no urgency
/seoplan "Wedding photography services" --lang en --priority strategic
```

**Full workflow: Plan → Brief → Write**

```bash
# Step 1: Build the cluster plan
/seoplan "Outdoor hiking gear Germany" --lang de --brand example-shop
# → Saved as SEO_PLANS/outdoor-hiking-gear-de.md

# Step 2: Generate a brief for the first Quick Win node
/seobrief Blogpost "How to choose hiking boots" --plan outdoor-hiking-gear-de.qw-01 --lang en
# → Saved as SEO_BRIEFS/how-to-choose-hiking-boots-en.md

# Step 3: Write content from the brief
/brand example-shop
/persona blogger
/write Blogpost "How to choose hiking boots" --from-brief how-to-choose-hiking-boots-en --lang en
# → Returns: full plain text article, brief-aligned, brand-compliant
```

---

## `--lang` — Language Flag

Loads the corresponding locale file from `LOCALE/<code>.md` on top of `LOCALE/base.md`.  
Applies to `/write` and `/writehtml` only.

| Code | Language | File Loaded | Status |
|------|----------|-------------|--------|
| `de` | German | `LOCALE/de.md` | ✅ Available |
| `fr` | French | `LOCALE/fr.md` | 🔜 Planned |
| `es` | Spanish | `LOCALE/es.md` | 🔜 Planned |
| `pt` | Portuguese | `LOCALE/pt.md` | 🔜 Planned |

**What `--lang de` changes:**
- `<html lang="de">`, `og:locale` → `de-DE`
- Date format → `DD.MM.YYYY`
- Price format → `1.090,00 €`
- Schema `inLanguage` → `de`, `addressCountry` → `DE`
- Writing mode → formal Sie-Form (unless `--tone casual` is set)
- Slugs → umlaut transliteration (`ä→ae`, `ö→oe`, `ü→ue`, `ß→ss`)
- All CTA labels → German (`Jetzt kaufen`, `In den Warenkorb`, etc.)
- Condition labels → German (`Sehr gut`, `Für Bastler`, etc.)

If `--lang` is omitted → English defaults from `LOCALE/base.md` are used.

---

## Quick Reference

/persona <id> [--tone] Set persona (stays active)
/personas List all personas
/personas --show <id> Show persona details

/write <type> "prompt" → Plain text, editor-ready
/writehtml <type> "prompt" → Pure HTML, deploy-ready

Common flags (both /write and /writehtml):
--primary-kw "keyword" Main target keyword
--secondary-kw "keyword" Secondary keyword
--lang de German output (de.md)
--tone <adjective> Tone override
--depth light|standard|deep Content depth

/research "topic" [--include-competitors] Keyword cluster + SERP analysis
/checks <url> SEO audit — live URL
/checks <type> [--strict] SEO audit — template preview

/brand <id>              Load client brand profile (stays active)
/brands                  List all brand profiles
/brands --show <id>      Show full brand profile details

/seobrief <type> "topic" Generate SEO content brief
  --primary-kw           Override primary keyword
  --lang de              Keyword research in target language
  --depth standard       Brief detail level
  --brand <id>           Apply brand profile to brief

New flag for /write and /writehtml:
  --from-brief <id>      Load brief for outline, KWs, and internal links
  
/seoplan "niche" [--flags]     Build cluster/site plan → save to SEO_PLANS/
  --mode cluster|site            cluster = one topic cluster (default), site = full architecture
  --lang de                      Market for keyword research
  --brand <id>                   Apply brand profile to node persona defaults
  --priority balanced|quickwins|strategic  What to focus on
  --depth light|standard|deep    Number of nodes (4–6 / 8–14 / 15–25)
  --pages <n>                    Override depth with exact node count

New flag for /seobrief, /write, /writehtml:
  --plan <plan-id>.<node-id>     Load plan node: KWs, page type, persona hints, internal links

---

*Last updated: 07-04-2026 (v0.6)*  
*Adds: /brand, /brands, /seobrief, --from-brief flag*
*Maintainer: Chris — SEOwlsClaw command reference*