---
name: tech-marketing-framework
description: Turn Claude Code or Codex into a senior product marketer with repeatable skills for developer tools content, messaging, and campaign generation
triggers:
  - "help me create marketing content for my developer tool"
  - "generate a messaging framework for my technical product"
  - "build a product marketing strategy"
  - "create social posts for my SaaS launch"
  - "write a sales deck for my API product"
  - "set up marketing automation for my dev tool"
  - "run a messaging workshop"
  - "generate product hunt launch assets"
---

# Tech Marketing Framework

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

A comprehensive marketing framework that turns Claude Code and Codex into a senior product marketer for technical audiences. Provides identity guidelines, content standards, template docs, and autonomous skills for content generation, messaging workshops, and campaign optimization.

## What It Does

This project provides:

- **Identity and voice guidelines** that prioritize technical accuracy over marketing fluff
- **Content guidelines** with strict standards for writing, formatting, and AI discoverability
- **Template docs** for product briefs, personas, competitive intel, and messaging
- **Skills for content generation** (email sequences, social posts, messaging workshops)
- **Autoresearch** for autonomous skill optimization via binary evals

## Installation

**Prerequisites:** [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) or [OpenAI Codex CLI](https://help.openai.com/en/articles/11096431-openai-codex-ci-getting-started)

```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Or install OpenAI Codex CLI
npm install -g @openai/codex

# Clone the framework into your project
git clone https://github.com/j1ngg/tech-marketing-framework.git
cd tech-marketing-framework

# Run Claude Code
claude

# Or run Codex
codex
```

Claude Code automatically loads `claude.md` and `.claude/` directory.
Codex automatically loads `AGENTS.md` and `.agents/skills/` directory.

## Project Structure

```
├── AGENTS.md                        # Codex repo instructions
├── claude.md                        # Claude Code instructions
├── .agents/skills/                  # Codex skill wrappers
├── .claude/
│   ├── rules/
│   │   └── content-guidelines.md    # Writing standards
│   ├── skills/                      # Marketing skill workflows
│   │   ├── messaging-positioning/
│   │   ├── social-posts/
│   │   ├── email/
│   │   ├── ads/
│   │   ├── sales-deck/
│   │   ├── blog/
│   │   ├── editorial-calendar/
│   │   ├── image/
│   │   ├── launch-roundup/
│   │   ├── producthunt-launch/
│   │   └── autoresearch/
│   └── agents/
│       ├── asset-reviewer.md
│       ├── ads-auditor.md
│       └── how-they-market.md
├── docs/
│   ├── inputs/                      # Product-specific templates
│   │   ├── product_brief.md
│   │   ├── target_personas.md
│   │   ├── messaging_positioning.md
│   │   ├── competitor_intel.md
│   │   ├── testimonials.md
│   │   └── brand_guidelines.md
│   └── reference/
│       └── channel_directory.md
└── output/                          # Generated assets
    ├── social/
    ├── blog/
    ├── email/
    ├── ads/
    ├── decks/
    ├── images/
    └── research/
```

## Getting Started

### 1. Fill in Product Templates

Navigate to `docs/inputs/` and complete these foundational documents:

```bash
# Edit product brief with your product details
vi docs/inputs/product_brief.md

# Define your target personas
vi docs/inputs/target_personas.md

# Add competitor intelligence
vi docs/inputs/competitor_intel.md

# Include approved customer testimonials
vi docs/inputs/testimonials.md
```

**Required fields in product_brief.md:**
- Product name and tagline
- Core problem solved
- Key features and capabilities
- Target audience
- Unique value proposition

**Required fields in target_personas.md:**
- Persona name and role
- Pain points
- Goals and success metrics
- Preferred channels
- Technical sophistication level

### 2. Run Your First Skill

In Claude Code, use slash commands:

```
/messaging-positioning
```

In Codex, use dollar sign or plain English:

```
$messaging-positioning
```

or simply ask:

```
Help me build a messaging framework for my product
```

## Core Skills

### Messaging & Positioning Workshop

Interactive workshop that builds your messaging foundation:

```
/messaging-positioning
```

Walks through four discovery sections:
1. **Vision** - Long-term company direction
2. **Product** - Capabilities and differentiation
3. **Competitive** - Market alternatives
4. **Targeting** - ICP and personas

**Output:** `docs/inputs/messaging_positioning.md`

### Social Media Posts

Generate platform-optimized social content:

```
/social-posts
```

**Supported platforms:**
- LinkedIn (brand and personal accounts)
- Twitter/X (threads and standalone posts)

**Process:**
1. Select platform and account type
2. Provide source material (blog post, feature announcement, etc.)
3. Skill generates 3-5 variants optimized for each platform's audience

**Output:** `output/social/[platform]-[timestamp].md`

### Email Sequences

Generate programmatic email sequences:

```
/email
```

**Current support:** Event follow-up sequences (post-conference, post-meeting, post-dinner)

**4-email sequence structure:**

| Email | Timing | Purpose |
|-------|--------|---------|
| 1 | Day 0 | Event recall + pain points (no link) |
| 2 | +2 days | Peer social proof + product demo |
| 3 | +6 days | Customer results + resource link |
| 4 | +11 days | Soft close + problem list (no link) |

**Key rules:**
- Real links only (no placeholders)
- Approved customers only (reads from `testimonials.md`)
- Programmatic personalization (shared context, not fabricated 1:1 details)

**Output:** `output/email/[sequence-type]-[timestamp].md`

### Paid Ads Generator

Generate ad copy for Google, Meta, and LinkedIn:

```
/ads
```

Uses creative matrix: Topics × Personas × Angles

**Supported platforms:**
- Google Ads (Search, Display)
- Meta (Facebook, Instagram)
- LinkedIn Ads

**Each variant includes:**
- Headlines (platform character limits enforced)
- Descriptions
- Image/creative briefs
- Target audience mapping

**Output:** `output/ads/[platform]-[timestamp].md`

### Sales Deck Builder

Create B2B sales narrative decks using April Dunford's methodology:

```
/sales-deck
```

**8-step structure:**

**Phase 1: The Setup (Slides 1-10)** - No product mentioned
1. Title/Thesis - Bold provocative insight
2. TLDR - Executive summary
3-4. Status Quo - Why current approach was rational
5-6. Disruption - What changed
7-8. Alternatives - Why other options fall short
9-10. Perfect World - New purchase criteria

**Phase 2: Follow-Through (Slides 11-17)**
11. Introduction - Product positioning
12-14. Differentiated Value - Capabilities mapped to criteria
15. Proof - Customer results
16. Objections (optional)
17. The Ask - CTA

**Output:**
- Markdown outline: `output/decks/[product-name]-sales-deck.md`
- PPTX file: `output/decks/[product-name]-sales-deck.pptx`

### Blog Post Generator

Generate SEO and AEO optimized blog posts:

```
/blog
```

**Supported blog types:**

| Type | Best For | Length |
|------|----------|--------|
| Feature announcement | Release notes, new capability | 800-1,200 words |
| Product launch | New product, major release | 1,200-1,800 words |
| Thought leadership | Opinion piece, contrarian take | 1,500-2,500 words |
| Cookbook/tutorial | How-to guide, integration walkthrough | 1,500-3,000 words |
| Report conversion | Whitepaper/case study → blog | 1,000-1,500 words |

**Every blog includes:**
- TLDR section (LLM-extractable)
- Metadescription (<160 chars)
- FAQ section (3-5 questions, AEO optimized)
- Schema markup suggestions
- Internal linking recommendations
- Visual callout flags

**Tri-publish variants:**
- Website/blog (long-tail keywords, schema)
- LinkedIn Pulse (DR 98 domain, LLM citations)
- X article (For You feed optimization)

**Output:** `output/blog/[title-slug]-[timestamp].md`

### Editorial Calendar

Build a monthly rolling content plan using MKT1 methodology:

```
/editorial-calendar
```

**Workshop sections:**
1. Business Context - Goals, revenue levers, GTM motion
2. Perceptions - What audience should say about you
3. Content Pillars & Audience - Topics, channels, formats
4. Capacity - Team size, cadence, backlog
5. Product & Market Context - Launches, events, competitive moves

**Output artifacts:**
- 3-Month Theme Roadmap
- 4-Week Editorial Calendar
- Monthly Refresh Checklist

**Output:** `output/editorial/[month]-editorial-calendar.md`

### Product Hunt Launch

Generate complete Product Hunt launch package:

```
/producthunt-launch
```

**Generated assets:**
- Product name and tagline
- Description (260 chars)
- Gallery images brief (3 required)
- First comment (detailed walkthrough)
- Hunter outreach template
- 8-week launch timeline with milestones

**Output:** `output/launch/producthunt-[product-name].md`

## Agents

### Asset Reviewer

Reviews generated assets against content guidelines:

```
/asset-reviewer
```

Point it at any generated asset in `output/` to get compliance scoring.

### Ads Auditor

Audits ad performance with health scoring:

```
/ads-auditor
```

Requires ad performance data (CSV export from ad platform).

### Competitive Intelligence

Analyzes how others market similar products:

```
/how-they-market
```

**Input:** Competitor URL or product name

**Output:** `output/research/competitor-[name]-analysis.md`

## Configuration

### Environment Variables

If using image generation skill (requires MCP):

```bash
# .env
ANTHROPIC_API_KEY=your_api_key_here
```

### Brand Guidelines

Customize voice and style in `docs/inputs/brand_guidelines.md`:

```markdown
## Voice Principles

- Technical accuracy over marketing fluff
- Show, don't tell (code examples, not promises)
- Developers are sophisticated buyers

## Writing Rules

- Use active voice
- Lead with the insight
- No empty superlatives
```

## Content Guidelines

The framework enforces strict content standards defined in `.claude/rules/content-guidelines.md`:

**Core principles:**
- Technical accuracy is non-negotiable
- No marketing fluff or empty superlatives
- Code examples must be real and runnable
- Claims require proof (links, customer quotes, data)

**Formatting standards:**
- Markdown-first
- Archetypal phrasing for LLM extraction
- Answer-first structure
- Schema markup where applicable

## Common Workflows

### Launch a New Feature

```
# 1. Update product brief with new feature
vi docs/inputs/product_brief.md

# 2. Generate feature announcement blog
/blog

# 3. Create social promotion
/social-posts

# 4. Build email sequence
/email

# 5. Update sales deck
/sales-deck
```

### Quarterly Marketing Refresh

```
# 1. Run messaging workshop
/messaging-positioning

# 2. Build editorial calendar
/editorial-calendar

# 3. Generate ad variants
/ads

# 4. Review all assets
/asset-reviewer
```

### Competitive Response

```
# 1. Analyze competitor marketing
/how-they-market

# 2. Update competitive intel
vi docs/inputs/competitor_intel.md

# 3. Refresh messaging
/messaging-positioning

# 4. Generate new ad variants
/ads
```

## Advanced Features

### Autoresearch (Skill Optimization)

The framework includes a meta-skill that autonomously optimizes other skills:

```
/autoresearch
```

**How it works:**
1. Runs target skill multiple times with variations
2. Applies binary evals to outputs
3. Updates skill definition based on what works
4. Commits improvements

**Output:** `output/research/autoresearch-[skill-name]-[timestamp].md`

### Skill Builder

Create new custom skills:

```
/skill-builder
```

Walks through skill creation workflow and generates new skill definition in `.claude/skills/`.

## Troubleshooting

### Skills Not Loading

**Claude Code:**
```bash
# Verify claude.md exists
ls -la claude.md

# Verify .claude directory structure
ls -la .claude/skills/
```

**Codex:**
```bash
# Verify AGENTS.md exists
ls -la AGENTS.md

# Verify .agents directory structure
ls -la .agents/skills/
```

### Missing Product Context

Skills pull from `docs/inputs/`. If getting generic output:

```bash
# Check which templates are filled in
ls -la docs/inputs/

# Minimum required: product_brief.md and target_personas.md
```

### Generated Content Too Generic

Ensure you've completed:
1. `messaging_positioning.md` - Provides voice and positioning
2. `testimonials.md` - Provides proof points
3. `competitor_intel.md` - Provides differentiation context

### Image Generation Fails

Image skill requires MCP (Model Context Protocol) setup:

```bash
# Verify MCP is configured
claude mcp status

# Check API key is set
echo $ANTHROPIC_API_KEY
```

## Best Practices

1. **Start with messaging workshop** - Run `/messaging-positioning` before generating assets
2. **Keep inputs updated** - Treat `docs/inputs/` as source of truth
3. **Review generated assets** - Always run `/asset-reviewer` before publishing
4. **Maintain testimonials** - Add new customer quotes to `testimonials.md` regularly
5. **Refresh competitive intel** - Run `/how-they-market` quarterly
6. **Version control outputs** - Commit generated assets for team review
7. **Use tri-publish strategy** - Maximize content ROI with blog → LinkedIn Pulse → X

## File Locations

All generated assets go to `output/` directory:

```
output/
├── social/           # Social media posts
├── blog/            # Blog posts and articles
├── email/           # Email sequences
├── ads/             # Ad copy and creative briefs
├── decks/           # Sales and pitch decks
├── images/          # Generated marketing images
└── research/        # Competitive analysis and autoresearch
```

Template inputs live in `docs/inputs/`:

```
docs/inputs/
├── product_brief.md
├── target_personas.md
├── messaging_positioning.md
├── competitor_intel.md
├── testimonials.md
└── brand_guidelines.md
```
