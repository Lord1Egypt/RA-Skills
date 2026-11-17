# SEOwlsClaw 🦉⚡
### *Pronounced "See-Owls-Claw"*

> Drop it into your AI agent. Get a full-stack SEO content system.

SEOwlsClaw is a modular SEO skill for AI agents. One install turns your agent
into a structured SEO writer, content strategist, and brand-aware publishing
engine — with zero generic AI filler.

---

## What It Does

You give it a niche. It builds you a ranked content plan.
You give it a topic. It writes a full brief before touching a word.
You give it a prompt. It returns deploy-ready HTML or clean CMS text.

Every output matches search intent, passes a built-in SEO audit,
respects your brand rules, and is ready to publish.

---

## ✨ What's Inside

**🧠 Intelligent Search Intent Detection**
Automatically picks the right page format before writing a single word.
Informational → Blogpost. Transactional → Productnew. No mismatches.

**🗺️ SEO Cluster Planning** `seoplan`
Build a complete content cluster for any niche. Nodes are tiered into
PILLAR / QUICKWIN / FOUNDATION / STRATEGIC — with keyword data,
difficulty scores, persona assignments, an internal link matrix,
and a numbered execution order. One command, full roadmap.

**📋 Brief-First Workflow** `seobrief`
Generate a structured content brief before writing — keyword cluster,
H1–H4 outline, PAA questions, competitor gaps, internal link targets.
Pass it to `write` with `--from-brief` and the content matches it exactly.

**🏢 Multi-Client Brand Profiles** `brand`
Load a client brand profile per session. Activates brand-specific CTAs,
tone sliders, vocabulary rules, banned phrases, and a compliance check
that hard-blocks output if violations are found.

**✍️ Persona-Driven Writing**
Six built-in personas: E-Commerce Manager, Researcher, Creative Writer,
Blogger, Vintage Expert, Travel Photographer. Each has its own heading
formula, vocabulary set, E-E-A-T signals, and Zone A/B content rules.

**🌐 Locale-Aware Output**
Multilingual support via locale files. Language, currency, schema fields,
date formats, and CTAs all adapt automatically with `--lang`.

**✅ Built-In SEO Audit Pipeline**
Every output runs through: title length, meta description, H1–H6
structure, Schema.org markup (Article, Product, FAQ, BreadcrumbList),
Zone A AI-overview compliance, persona compliance, and brand compliance.

---

## 🛠️ Quick Start

```text
# Plan a full content cluster
seoplan "Best hiking gear Germany" --lang de --priority quickwins

# Brief a single page from the plan
seobrief Blogpost "Hiking boots guide" --plan hiking-gear-de.qw-01 --lang en

# Write deploy-ready HTML from the brief
brand my-client
persona blogger
writehtml Blogpost "Hiking boots guide" --from-brief hiking-boots-guide-de --lang en
```

Or skip straight to content:

```text
persona ecommerce-manager
write Productnew "TrailMaster X5 Hiking Boot, waterproof, sizes 38–47" \
  --primary-kw "waterproof hiking boots buy" --lang en
```

---

## 📦 What's Included

- Core skill + full brain architecture (13-step processing pipeline)
- 6 writing personas with heading formulas and E-E-A-T rules
- HTML templates: Blogpost, Productnew, Productused, Landingpage, FAQ, Social
- SEO audit checklists per page type + schema markup rules
- Brand profile system (`BRANDS/`) with compliance enforcement
- SEO writing rules (`SEO_RULES/`) — universal + per-page-type, consulted before generation
- SEO brief system (`SEO_BRIEFS/`) with `--from-brief` integration
- SEO cluster planning system (`SEO_PLANS/`) with lazy-loaded workflow logic
- Locale files for multilingual output

---

*SEOwlsClaw — because good SEO content should be structured, not scattered.*

───

✅ Built-in SEO Pipeline
Every output runs through:

🔍 Search intent detection — wrong format = wrong ranking signal, caught before writing

📋 E-E-A-T checks — expertise, experience, authority, and trust signals verified

🏷️ Schema.org validation — Product, Article, FAQPage, BreadcrumbList, Event/Offer

📏 On-page SEO — title length, meta description, H1 uniqueness, heading structure

🚫 Trap detection — keyword stuffing, thin content, missing schema, broken links

🌐 Locale compliance — correct date format, price format, formality register, slugs

───

🗂️ Page Types
| Type        | Best For                  | Words      |
| ----------- | ------------------------- | ---------- |
| Blogpost    | Guides, articles, how-tos | 1,500w+    |
| Landingpage | Sales, campaigns, promos  | 900–1,200w |
| Productnew  | New product listings      | 400–600w   |
| Productused | Used / refurbished items  | 500–700w   |
| FAQ Page    | FAQ pages, PAA targeting  | 800–1,200w |
| Socialphoto | Image captions, alt text  | 100–200w   |
| Socialvideo | YouTube / TikTok metadata | 150–300w   |

___

🎭 Personas
| ID                  | Vibe                                             |
| ------------------- | ------------------------------------------------ |
| blogger             | Friendly, educational, story-driven (default)    |
| ecommerce-manager   | Persuasive, urgent, conversion-focused           |
| creative-writer     | Narrative, emotional, brand-driven               |
| researcher          | Neutral, fact-based, structured                  |
| vintage-expert      | Authoritative, precise, collector-focused        |
| travel-photographer | Scenario-driven, gear-focused, location-specific |

___

🌍 Multilingual — 4 Languages Ready
Uses a Base + Delta architecture. base.md holds all English defaults. Language files only define what's different — keeping files short and easy to maintain.
> LOCALE/
> 
> ├── base.md   ← English defaults for everything
>
> ├── de.md     ← German (Sie-form, DD.MM.YYYY, 1.090,00 €, umlaut slugs)
>
> ├── fr.md     ← French (vous-form, « guillemets », thin-space thousands)
>
> ├── es.md     ← Spanish (tú-form, ¿¡ punctuation, MX + AR variants)
>
> └── pt.md     ← Portuguese (você-form, PT + BR variant)

___

## ⚡ Commands

### Strategy
| Command | What it does |
|---------|-------------|
| `seoplan "niche"` | Build a full content cluster — tiered nodes, keyword data, link matrix, execution order |
| `seobrief <type> "topic"` | Generate a structured brief before writing — KWs, outline, PAA, competitor gaps |

### Brand
| Command | What it does |
|---------|-------------|
| `brand <id>` | Load a client brand profile — activates CTAs, tone, vocab rules, and compliance checks |
| `brands` | List all brand profiles |
| `brands --show <id>` | Show full details of one brand profile |

### Content
| Command | What it does |
|---------|-------------|
| `persona <id>` | Set writing persona (stays active for the session) |
| `personas` | List all personas with one-line descriptions |
| `personas --show <id>` | Show full persona details |
| `write <type> "prompt"` | Plain text output — editor/CMS-ready |
| `writehtml <type> "prompt"` | Pure HTML output — deploy-ready |

### Research & Audit
| Command | What it does |
|---------|-------------|
| `research "topic"` | Keyword cluster + SERP analysis |
| `checks <url>` | SEO audit on a live URL |
| `checks <type>` | SEO audit on a page type (preview mode) |

---

### 🚩 Flags

| Flag | Works with | Purpose |
|------|-----------|---------|
| `--primary-kw "kw"` | `write` `writehtml` | Main target keyword |
| `--secondary-kw "kw"` | `write` `writehtml` | Secondary keyword cluster |
| `--lang de\|fr\|es\|pt` | all commands | Output language + locale (omit for English default) |
| `--tone casual\|formal\|…` | `write` `writehtml` | Override persona tone |
| `--depth light\|standard\|deep` | `write` `writehtml` `seobrief` | Content depth level |
| `--from-brief <id>` | `write` `writehtml` | Load a saved brief — aligns output to its outline and KWs |
| `--plan <plan-id>.<node-id>` | `write` `writehtml` `seobrief` | Load a plan node — pulls KWs, page type, and link targets |
| `--brand <id>` | all commands | Load brand profile inline (alternative to `brand`) |
| `--mode cluster\|site` | `seoplan` | Single cluster or full site architecture |
| `--priority balanced\|quickwins\|strategic` | `seoplan` | What tiers to focus on |
| `--pages <n>` | `seoplan` | Override node count |

___

📁 Structure

> seo-owls-claw/
> 
> │
> 
> ├── SKILL.md                    ← This file — core instructions + command reference
>
> ├── BRAIN_ARCHITECTURE.md       ← Complete processing logic (all 9 brain steps)
>
> ├── COMMANDS.md                 ← Full command reference with all flags
>
> ├── PAGE_STRUCTURES.md          ← Master index + links to all page templates
>
> ├── SEO_PATH.md                 ← Full SEO workflow: research → analysis → writing → checks
>
> │
>
> ├── PERSONAS/                   ← One file per persona
>
> │   ├── _index.md               ← Load first — lists all persona IDs and file paths
>
> │   ├── ecommerce-manager.md
>
> │   ├── creative-writer.md
>
> │   ├── blogger.md              ← Default persona when none specified
>
> │   ├── researcher.md
>
> │   ├── vintage-expert.md
>
> │   └── travel-photographer.md
>
> │
>
> ├── BRANDS/                     ← One file per client brand profile
>
> │   ├── _index.md               ← Load first — lists all brand IDs and file paths
>
> │   └──  brand-template.md       ← Copy this to create a new brand profile
>
> │
>
> ├── LOCALE/                     ← Language override files (Base + Delta architecture)
>
> │   ├── base.md                 ← English defaults for all locale keys — always loaded
>
> │   ├── de.md                   ← German overrides (--lang de)
>
> │   ├── fr.md                   ← French overrides (--lang fr)
>
> │   ├── es.md                   ← Spanish overrides (--lang es)
>
> │   └── pt.md                   ← Portuguese overrides (--lang pt)
>
> │
>
> ├── SEO_BRIEFS/                 ← Generated content briefs (one per topic/page)
>
> │   └── _index.md               ← Registry: brief-id | topic | type | date | status
>
> │
>
> ├── SEO_PLANS/                  ← One plan file per niche/site campaign
>
> │   ├── _index.md               ← Registry: plan-id | niche | mode | lang | date
>
> │   ├── plan-template.md        ← Format reference + example plan
>
> │   └── plan_workflow.md        ← Full seoplan pipeline logic (Steps A–G) — loaded only on seoplan
>
> │
> 
> ├── SEO_RULES/                  ← SEO writing rules, consulted before generation
>
> │   ├── _index.md               ← Registry of all rule files
>
> │   ├── universal.md            ← Rules for every page type
>
> │   └── (one file per page type: landingpage.md, blogpost.md, etc.)
>
> │
>
> ├── SEO_CHECKS/                 ← SEO audit mechanics — scores against SEO_RULES/
>
> │   ├── search_intent.md        ← Step 0 rules — intent detection + format selection
>
> │   ├── schema-markup.md        ← Schema.org rules + {SCHEMA_*} variable definitions
>
> │   ├── seo-checks-reference.md ← Universal audit workflow, scores against SEO_RULES/universal.md
>
> │   ├── page-type-specific-checks.md ← Per-type audit scoring, scores against SEO_RULES/<type>.md
>
> │   └── seo-output-quality-checklist.md ← Pre-output quality gates
>
> │
>
> ├── TEMPLATES/                  ← HTML output templates (used by writehtml only)
>
> │   ├── blog_post_template.md
>
> │   ├── landing_page_template.md
>
> │   ├── product_new_template.md
>
> │   ├── product_used_template.md
>
> │   └── faq_page_template.md
>
> │
>
> ├── TEMPLATES_SOCIAL/           ← Social media output templates
>
> │   ├── photo_post_template.md
>
> │   └── video_post_template.md
>
> │
>
> ├── OUTPUT_EXAMPLES/            ← Reference output examples for agent guidance
>
> │   ├── blog_post_example.html    ← Reference output examples for agent guidance (under development)
>
> │   ├── landing_page_example.html ← Reference output examples for agent guidance (under development)
>
> │   ├── product_new_example.html  ← Reference output examples for agent guidance (under development)
>
> │   └── product_used_example.html ← Reference output examples for agent guidance (under development)
> 

___

  
🎯 Perfect for

* SEO projects & organic content creation
* E-Commerce product pages (new & refurbished)
* Sales campaigns & newsletter launches
* Personal branding & storytelling content

───

Version: v0.9.2 · Status: Active development · Maintainer: Chris
SEOwlsClaw — Because good SEO content shouldn't need 10 different tools. 🦉

───
SEOwlsClaw v0.9.2 — Changelog

Added `SEO_RULES/` as the single source of truth for SEO writing rules — `universal.md` (E-E-A-T,
on-page SEO, common traps, FAQ requirements, quality principles, natural language rules incl. an
AI-writing-pattern check) plus one file per page type (Landingpage, Blogpost, Productnew,
Productused, FAQ, Socialphoto, Socialvideo), each with Do's/Don'ts, required elements, and
keyword placement rules. Loaded at a new brain Step 2f, before content generation, so output is
written correctly the first time instead of only caught by the Step 6 audit afterward.

Removed `SEO_CHECKS/do-and-don-lists.md` — its content moved into `SEO_RULES/`.
`page-type-specific-checks.md` and `seo-checks-reference.md` were trimmed to audit scoring
mechanics only (HARD FAIL/WARNING thresholds, pass-rate math), now pointing at `SEO_RULES/`
instead of duplicating its values.

Reconciled two values that had drifted to different numbers across files: meta description
length (was 140–155 / 150–160 / "max 160" depending on the file, now 140–155 everywhere,
including `LOCALE/` and the HTML templates that previously baked "160" into a placeholder name)
and Landingpage minimum word count (was 500w in one file, 800–1,200w in another, now 900–1,200w
everywhere).

Updated `BRAIN_ARCHITECTURE.md`, `SKILL.md`, `SEO_PATH.md`, `COMMANDS.md`, and this README to
reference the new structure throughout.

───
SEOwlsClaw v0.8 — Changelog

feat(SEO_CHECKS): add page-type-specific-checks.md with hard fails, warnings, schema rules, and pass thresholds for all 7 page types; update seo-checks-reference.md and SKILL.md references

Updated SEOwlsClaw command syntax: Removed leading slash (/) style from internal commands and standardized on bare commands like persona, write, writehtml, seobrief, seoplan.

Fixed misleading bash references: Replaced bash-style labels and code fences with neutral text code blocks to avoid treating SEOwlsClaw commands as shell commands.

Clarified command execution rules: Documented that all SEOwlsClaw commands are internal skill/chat commands and must not be executed via system/OS tools (no shell, no cron) except for explicit scheduling requests.

Aligned SKILL.md and COMMANDS.md: Ensured both core docs use the same command syntax and examples, reducing ambiguity for the agent when parsing SEO workflows.

SKILL.md
Updated from v0.6 → v0.8. Extended description to reflect full-stack agency capabilities. Added 12 new trigger phrases for brand, seobrief, and seoplan. Added 4 new rows to the Core Commands table. Replaced the Workflow Steps block with the complete 13-step version covering Steps 2d, 2e, 6.6 and skip rules for strategy commands. Added 2 new workflow examples (brief-first flow and full 3-phase agency flow). Extended the file tree with BRANDS/, SEO_BRIEFS/, and SEO_PLANS/ folder entries.

BRAIN_ARCHITECTURE.md
Apply patches to v0.8

Added brand_id, brief_id, and --from-brief / --plan flag parsing to Step 1.
v0.8 FINAL patch — Added Step 2d (brand profile load: reads BRANDS/<id>.md, merges brand variables and CTAs into the variable dict, stores compliance object for Step 6.6, skipped when no brand is active). Added Step 2e (SEO plan pointer: if seoplan is active, load SEO_PLANS/plan_workflow.md and run Steps A–G, then stop — Steps 3–7 do not run). Added Step 6.6 (brand and legal compliance check: banned phrase scan, urgency limit enforcement, required disclosure validation — HARD FAIL blocks output). Updated the Workflow Summary Quick Reference to reflect all 13 steps.

COMMANDS.md
Apply patches v0.8

Full brand, brands, and seobrief command documentation including all flags, examples, and the --from-brief integration with write.
v0.8 patch — Full seoplan command documentation including --mode, --priority, --depth, --pages flags, node tier reference table with difficulty thresholds and timeline estimates, all three priority modes explained, and the complete 3-phase workflow example. Added --plan <plan-id>.<node-id> flag documentation for seobrief and write.

BRANDS/ (new folder)
_index.md — Registry of all client brand profiles. One row per brand. Referenced by brand and brands commands at runtime.
brand-template.md — Blank template for any new client. Fields include: tone sliders, CTAs per language, vocabulary rules (allowed/banned phrases, brand terms), trust blocks, compliance settings (urgency limit, artificial scarcity flag, required disclosures), and condition grade vocabulary.

SEO_BRIEFS/ (new folder)
_index.md — Registry of all generated content briefs. Auto-populated when /seobrief runs. Tracks brief-id, topic, page type, language, brand, date, and status (draft / approved / in-production / published).

SEO_PLANS/ (new folder)
_index.md — Registry of all generated SEO cluster and site plans. Auto-populated when seoplan runs.

plan-template.md — Defines the exact machine-parseable format for all plan files. Includes a fully filled-in example (11-node cluster, vintage analog cameras, DE market) covering all four tiers with keyword data, persona assignments, internal link matrix, and execution order.

plan_workflow.md — Full seoplan processing pipeline (Steps A–G). Lazy-loaded only when /seoplan fires — never loaded during content generation commands. Contains: niche research logic, quick win threshold calculation, cluster architecture design rules for --mode cluster and --mode site, node tiering criteria for all four tiers (PILLAR / QUICKWIN / FOUNDATION / STRATEGIC), persona assignment per tier, internal link matrix rules (no orphan nodes), execution order logic for all three --priority modes, plan quality check gate, and output + save instructions.
