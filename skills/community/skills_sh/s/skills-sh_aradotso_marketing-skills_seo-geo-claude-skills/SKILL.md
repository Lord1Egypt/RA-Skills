---
name: seo-geo-claude-skills
description: Master 20 SEO & GEO skills for Claude Code agents - keyword research, content optimization, technical audits, rank tracking with CORE-EEAT and CITE frameworks
triggers:
  - help me optimize content for search engines
  - audit this page for SEO best practices
  - research keywords for my content strategy
  - analyze competitor SEO performance
  - optimize content for AI citations and GEO
  - check technical SEO issues on my site
  - generate schema markup for better rankings
  - track keyword rankings and performance
---

# seo-geo-claude-skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

`seo-geo-claude-skills` is a comprehensive library of 20 specialized skills that enable AI coding agents to perform Search Engine Optimization (SEO) and Generative Engine Optimization (GEO) tasks. Each skill follows a standard contract and includes built-in quality benchmarks: CORE-EEAT (80-item content quality framework) and CITE (40-item domain authority framework).

The library is organized into five phases: Research, Build, Optimize, Monitor, and Cross-cutting protocol skills. All skills work with user-provided data (Tier 1) and optionally integrate with external tools via MCP connectors.

## Installation

### Claude Code
```bash
/plugin marketplace add aaron-he-zhu/seo-geo-claude-skills
```

### ClawHub.ai / OpenClaw
```bash
clawhub install aaron-he-zhu/seo-geo-claude-skills
# Or install individual skills:
clawhub install aaron-he-zhu/keyword-research
```

### Generic Agent Skills Hosts (skills.sh)
```bash
npx skills add aaron-he-zhu/seo-geo-claude-skills

# Install single skill:
npx skills add aaron-he-zhu/seo-geo-claude-skills -s keyword-research
```

### Gemini CLI
```bash
gemini extensions install https://github.com/aaron-he-zhu/seo-geo-claude-skills
```

### Qwen Code
```bash
qwen extensions install https://github.com/aaron-he-zhu/seo-geo-claude-skills
```

### Amp
```bash
amp skill add aaron-he-zhu/seo-geo-claude-skills
```

### Kimi Code CLI
```bash
kimi plugin install https://github.com/aaron-he-zhu/seo-geo-claude-skills.git
```

## Core Commands

The library provides user-facing slash commands for common workflows:

- `/aaron:auto` - Automatically routes to the best skill based on your goal (recommended starting point)
- `/aaron:max` - Maximum-depth exhaustive analysis mode
- `/aaron:discover` - Keyword research workflow
- `/aaron:compete` - Competitor analysis
- `/aaron:map` - SERP and content gap analysis
- `/aaron:brief` - Generate content briefs
- `/aaron:write` - SEO-optimized content creation
- `/aaron:series` - Multi-article content series planning
- `/aaron:refresh` - Update existing content
- `/aaron:publish` - Content quality gate (CORE-EEAT)
- `/aaron:audit` - On-page SEO audit
- `/aaron:visibility` - Schema markup and meta optimization
- `/aaron:tech` - Technical SEO checks
- `/aaron:authority` - Domain authority audit (CITE)
- `/aaron:watch` - Rank tracking
- `/aaron:report` - Performance reporting
- `/aaron:remember` - Memory management (HOT/WARM/COLD)

### Maintenance Commands
- `/aaron:skillify` - Review proposed skills or routes
- `/aaron:evolve` - Controlled library changes from evidence
- `/aaron:guard` - Maintainer validation

## Skill Structure

Each skill follows this contract:

1. **Quick Start** - Immediate activation instructions
2. **Skill Contract** - Expected inputs/outputs
3. **Handoff Summary** - What to pass to next skill
4. **Data Sources** - Where data comes from (user, tools, memory)
5. **Instructions** - Step-by-step execution
6. **Reference Materials** - Supporting frameworks
7. **Next Best Skill** - Recommended workflow progression

## The 20 Skills

### Research Phase

**keyword-research** - Discover and prioritize keywords
```bash
# Natural language trigger:
"Research keywords for my SaaS product targeting small teams"

# Or direct command:
/aaron:discover "project management software"
```

**competitor-analysis** - Analyze competitor SEO strategies
```bash
/aaron:compete https://competitor.com
```

**serp-analysis** - Analyze search engine results pages
```bash
/aaron:map "best project management tools 2024"
```

**content-gap-analysis** - Find missing content opportunities
```bash
"Find content gaps between my site and competitors for 'team collaboration'"
```

### Build Phase

**seo-content-writer** - Create SEO-optimized content
```bash
/aaron:write "How to improve team productivity with async communication"
```

**geo-content-optimizer** - Optimize for AI citation (Perplexity, ChatGPT)
```bash
"Optimize this article for AI search engines and citations"
```

**meta-tags-optimizer** - Generate optimized meta tags
```bash
/aaron:visibility --meta https://example.com/blog/post
```

**schema-markup-generator** - Create structured data markup
```bash
/aaron:visibility --schema https://example.com/product/widget
```

### Optimize Phase

**on-page-seo-auditor** - Audit individual pages
```bash
/aaron:audit https://example.com/blog/my-article
```

**technical-seo-checker** - Check technical SEO issues
```bash
/aaron:tech https://example.com
```

**internal-linking-optimizer** - Improve internal link structure
```bash
"Suggest internal linking improvements for my blog posts about productivity"
```

**content-refresher** - Update and improve existing content
```bash
/aaron:refresh https://example.com/old-blog-post
```

### Monitor Phase

**rank-tracker** - Track keyword rankings
```bash
/aaron:watch --keywords "project management,team collaboration,async tools"
```

**backlink-analyzer** - Analyze backlink profile
```bash
"Analyze backlinks for example.com"
```

**performance-reporter** - Generate performance reports
```bash
/aaron:report --weekly
```

**alert-manager** - Configure and manage alerts
```bash
"Set up alerts for ranking drops > 3 positions"
```

### Cross-cutting Protocol Skills

**content-quality-auditor** - 80-item CORE-EEAT quality gate
```bash
/aaron:publish https://example.com/draft-article
```

**domain-authority-auditor** - 40-item CITE trust assessment
```bash
/aaron:authority https://example.com
```

**entity-optimizer** - Build canonical entity profiles
```bash
"Create entity profile for [Company Name] with knowledge graph optimization"
```

**memory-management** - HOT/WARM/COLD project memory + wiki layer
```bash
/aaron:remember compile wiki "content strategy"
/aaron:remember query "what keywords did we target last month?"
```

## Working with Memory (v9.9.9+)

The library maintains three memory tiers:

- **HOT** - Active session state (current outputs, open loops)
- **WARM** - Recent project context (skills, routes, evidence)
- **COLD** - Long-term archive (retired files, wiki history)

### Wiki Layer Workflow

**Phase 1 (Automatic)**: Index auto-refreshes at `memory/wiki/index.md`

**Phase 2 (Manual Compilation)**:
```bash
# When you have ≥3 WARM files on a topic:
"Compile a wiki page on our content strategy for Q1"
"Synthesize what we know about keyword targeting"

# Handle contradictions when prompted:
# (a) Accept version A
# (b) Accept version B  
# (s) Skip/postpone
# (i) Ignore permanently
```

**Phase 3 (Retirement)**:
```bash
# Preview retirement candidates:
/aaron:guard --wiki --retire-preview

# After confirmation, WARM files move to memory/archive/

# Recover if needed:
/aaron:remember recover wiki
# Or directly:
bash scripts/recover-retired-warm.sh
```

**Clean restart**:
```bash
rm -rf memory/wiki/  # Reverts cleanly, preserves COLD history
```

## Quality Frameworks

### CORE-EEAT (80 items)
Content quality benchmark covering:
- **C**redibility
- **O**riginality  
- **R**elevance
- **E**xpertise
- **E**xperience
- **A**uthoritativeness
- **T**rustworthiness

Used by: `content-quality-auditor`, `seo-content-writer`, `geo-content-optimizer`

### CITE (40 items)
Domain authority benchmark covering:
- **C**redibility signals
- **I**nfluence metrics
- **T**rust indicators
- **E**xpertise markers

Used by: `domain-authority-auditor`, `backlink-analyzer`

## Common Workflows

### Full SEO Campaign
```bash
# 1. Research
/aaron:discover "target keyword topic"
/aaron:compete https://competitor.com
/aaron:map "target keyword"

# 2. Build
/aaron:brief "article topic based on research"
/aaron:write "article title from brief"
/aaron:visibility --meta --schema

# 3. Quality gate
/aaron:publish https://example.com/new-article

# 4. Optimize
/aaron:audit https://example.com/new-article
/aaron:tech https://example.com

# 5. Monitor
/aaron:watch --keywords "keyword1,keyword2,keyword3"
/aaron:report --weekly
```

### GEO Optimization
```bash
# Optimize content for AI citations (Perplexity, ChatGPT, etc.)
"Optimize this article for generative engine optimization"
/aaron:visibility --geo https://example.com/article

# Entity-first approach:
"Create entity profile for [Brand/Topic]"
"Optimize content hub around [Entity] for AI discoverability"
```

### Content Refresh
```bash
/aaron:refresh https://example.com/old-article
# Analyzes current performance
# Suggests content updates
# Identifies new keyword opportunities
# Recommends internal linking improvements
```

## Configuration

### Environment Variables
```bash
# Optional external tool connectors (see CONNECTORS.md):
export SERP_API_KEY=${SERP_API_KEY}
export AHREFS_API_KEY=${AHREFS_API_KEY}
export SEMRUSH_API_KEY=${SEMRUSH_API_KEY}
export GSC_CREDENTIALS_PATH=${GSC_CREDENTIALS_PATH}

# Memory persistence (default: ./memory):
export AARON_MEMORY_PATH=${AARON_MEMORY_PATH}
```

All skills work at **Tier 1** (user-provided data) without any external API keys.

### Connector Tiers

- **Tier 1**: User provides data (copy-paste, screenshots, files)
- **Tier 2**: Fetch-only tools (cURL, Puppeteer, read-only APIs)
- **Tier 3**: Premium APIs with write access (publish, modify, delete)

See `CONNECTORS.md` for full MCP integration details.

## Troubleshooting

### Command Not Found
```bash
# If /aaron:* commands don't work:
/aaron:auto "your original request"
# The auto command will route to the correct skill
```

### Old /seo:* Commands
```bash
# Breaking rename in v9.9.9
# Convert old commands:
/aaron:auto /seo:audit-page https://example.com/blog/post
# Returns: /aaron:audit https://example.com/blog/post
```

### Memory Conflicts
```bash
# If wiki contradictions pile up:
/aaron:remember query "contradictions"
# Resolve via (a)/(b)/(s)/(i) prompts

# Nuclear option - clean restart:
rm -rf memory/wiki/
# Next session rebuilds from WARM
```

### Skill Routing Issues
```bash
# Review available skills and routes:
/aaron:skillify

# Check current memory state:
/aaron:remember query "last 5 skills used"

# Validate library health:
/aaron:guard --validate
```

## Advanced Usage

### Custom Skill Chaining
```bash
# Explicit skill sequence:
"Use keyword-research, then competitor-analysis, then seo-content-writer for 'project management automation'"
```

### Batch Operations
```bash
# Audit multiple pages:
/aaron:audit https://example.com/page1
/aaron:audit https://example.com/page2
/aaron:audit https://example.com/page3

# Or natural language:
"Audit all pages in sitemap.xml for on-page SEO"
```

### Report Customization
```bash
/aaron:report --weekly --format=json --output=reports/
/aaron:report --monthly --include-competitors --email
```

## Best Practices

1. **Start with /aaron:auto** - Let the library route your request automatically
2. **Use memory-management** - Compile wiki pages once you have recurring topics
3. **Quality gate everything** - Run `/aaron:publish` before publishing content
4. **Monitor continuously** - Set up `/aaron:watch` alerts for key metrics
5. **Document decisions** - Memory layer captures why you chose specific strategies
6. **Combine auditors** - Use both `content-quality-auditor` (80 items) + `domain-authority-auditor` (40 items) for complete assessment

## Files and Directory Structure

```
seo-geo-claude-skills/
├── commands/              # Slash command definitions
├── research/             # Research phase skills
│   ├── keyword-research/
│   ├── competitor-analysis/
│   ├── serp-analysis/
│   └── content-gap-analysis/
├── build/                # Build phase skills
│   ├── seo-content-writer/
│   ├── geo-content-optimizer/
│   ├── meta-tags-optimizer/
│   └── schema-markup-generator/
├── optimize/             # Optimize phase skills
│   ├── on-page-seo-auditor/
│   ├── technical-seo-checker/
│   ├── internal-linking-optimizer/
│   └── content-refresher/
├── monitor/              # Monitor phase skills
│   ├── rank-tracker/
│   ├── backlink-analyzer/
│   ├── performance-reporter/
│   └── alert-manager/
├── cross-cutting/        # Protocol skills
│   ├── content-quality-auditor/
│   ├── domain-authority-auditor/
│   ├── entity-optimizer/
│   └── memory-management/
├── references/           # Frameworks and benchmarks
│   ├── core-eeat-benchmark.md
│   ├── cite-domain-rating.md
│   ├── auditor-runbook.md
│   └── skill-contract.md
├── scripts/              # Helper scripts
│   └── recover-retired-warm.sh
└── memory/               # Memory persistence
    ├── wiki/
    ├── archive/
    └── index.md
```

## Further Reading

- [Full skill list](https://github.com/aaron-he-zhu/seo-geo-claude-skills#skills)
- [CORE-EEAT benchmark](https://github.com/aaron-he-zhu/core-eeat-content-benchmark)
- [CITE domain rating](https://github.com/aaron-he-zhu/cite-domain-rating)
- [Connector tiers](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md)
- [Marketplace compatibility](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/marketplaces/README.md)
- [Contributing guide](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONTRIBUTING.md)

## License

Apache License 2.0
