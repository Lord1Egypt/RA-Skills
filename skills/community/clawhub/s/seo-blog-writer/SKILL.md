---
name: seo-blog-writer
version: 3.2.0
description: |
  Fully automated SEO article writer. Give it a topic and domain — it handles
  everything: auto-discovers product context, researches keywords, analyzes
  competitors, writes the article, verifies links, and delivers a complete
  publication package (article + QA report + schema markup + promotion checklist).
  One confirmation gate before writing starts, then hands-off execution.
  Works for any site, any industry, any CMS. No hardcoded dependencies.
triggers:
  - "write a blog post"
  - "SEO article"
  - "write about [topic]"
  - "blog post for [domain]"
  - "comparison article"
  - "alternatives page"
  - "how-to guide"
external_access:
  - type: web_search
    description: "SERP analysis — searches Google/Bing/DDG for competitor URLs and keyword data. No API key required; uses the agent's built-in web search tool."
  - type: web_fetch
    description: "Link verification — checks that external URLs in the article are live. No API key required."
permissions:
  - disk_write: "Writes article draft, QA report, and schema file to local disk (crash-safe incremental execution). Output directory is user-configurable."
---

# AI-Driven SEO Blog Writer

> **Long-running task mode.** This skill generates a multi-phase artifact. Before Phase 0: create a `task-logs/{slug}/` workspace, write each phase output to disk incrementally, and use offset reads to verify writes. This ensures crash-safe, resumable execution without regenerating completed work.

## Design Principles

**Minimum viable input** - topic + domain is all you need to start
**Verify before assert** - no statistic, quote, or claim goes in unverified
**One checkpoint** - you confirm the plan before a single word is written
**Zero dependency** - no local project files, no paid tools required
**Honest degradation** - when automation fails, the skill says so clearly and gives you the next step

---

## Execution Model (IMPORTANT)

This is a heavy, multi-phase skill. Incremental disk writes and offset-read verification are mandatory — see the long-running task note above.

**When spawning as a subagent, file writes and link verification (Phases 1–5) require exec permissions:**

```
sessions_spawn(
  task: "SEO article: topic='[topic]' domain='[domain]' mode='[mode]'",
  runtime: "subagent",
  security: "full"   ← needed for disk writes and curl-based link checks
)
```

If running in the main session directly, exec permissions are already present — proceed normally.

> **Why `security: "full"`?** This skill writes article drafts, QA reports, and schema files to disk incrementally (crash-safe execution). Link verification uses `curl`/`web_fetch` to check URLs. Both operations require exec access. If you prefer not to grant this, run the skill in your main session rather than as a subagent — behavior is identical.

---

## Failure Recovery Guardrails (Mandatory)

For this skill, "done in one shot" is not trusted. Use bounded, resumable execution:

1. **Section-by-section writes**
- Write article sections incrementally (intro, each H2 block, FAQ, conclusion).
- After each section write, append checkpoint to `task-logs/{slug}/report.md` (or your preferred output dir).

2. **Write-then-read verification**
- After every `write`/`edit`, run a targeted read/grep to confirm the change exists.
- Do not queue multiple blind edits without read-back.

3. **Timeout-safe continuation**
- If model timeout / prompt-error / length stop occurs:
  - persist current section to disk immediately
  - continue from next missing section
  - do not regenerate completed sections unless explicitly requested.

4. **QA loop cap**
- Max 3 QA rounds.
- Each round fixes only concrete FAIL items from latest report.
- If a FAIL item is stale (already fixed), verify by grep/read and mark as stale report issue.

5. **SERP analyzer degradation**
- If QA says "SERP analyzer unavailable", treat as warning.
- Continue with link/citation/structure fixes; do not block publication solely on SERP fetch failure.

---

## Quick Start

```yaml
# Minimum input
topic: "best AI email apps 2026" | "gmail alternatives" | "how to manage email overload"
domain: "https://yoursite.com"

# Optional
mode: "express" | "standard" | "expert"   # default: standard
product_context: "path/to/context.md"     # skip auto-discovery if you have this
output_dir: "."                            # default: ./seo-output/{slug}/
```

**Examples:**
- "Write a comparison article about email apps for mysite.com"
- "I need a how-to guide about email automation for https://example.com"
- "Create an alternatives page for Gmail for our domain filomail.com"

---

## Execution Modes

| Mode | Time | Focus | Use when |
|------|------|-------|----------|
| **Express** | 5-10min | Speed + core quality | Quick turnaround, existing traffic |
| **Standard** | 15-20min | Balanced depth + optimization | Most articles, balanced goals |
| **Expert** | 25-35min | Maximum quality + competitiveness | High-stakes keywords, competitive niches |

### Mode Differences

**Express mode shortcuts:**
- Basic site crawl: homepage + pricing only
- Simplified competition: top 3 competitors, structure analysis only
- Streamlined QA: core checklist, skip advanced verification
- Target score: 65+ (publishable quality)

**Standard mode (default):**
- Comprehensive crawl: full discovery + blog analysis
- Detailed competition: top 5 competitors + content gaps + authority sources
- Complete QA: full scoring + verification + optimization suggestions
- Target score: 75+ (solid quality)

**Expert mode enhancements:**
- Deep intelligence: multi-source crawling + social/review analysis where available
- Advanced competition: semantic analysis + opportunity mapping + trend identification
- Premium QA: custom scoring + predictive optimization + enhancement recommendations
- Target score: 85+ (exceptional quality)

---

## Phase 0: Context Discovery (Automated)

### ⚡ Skip Check

If `product_context` file was provided:
1. Read the file
2. Extract: product_name, value_proposition, pricing_model, brand_voice from it
3. Set voice_confidence = MEDIUM (user-provided, assumed accurate)
4. **Skip 0.1 and 0.6 entirely**
5. Proceed directly to 0.2 (blog ecosystem mapping) and 0.3 (keyword research)

Only proceed with 0.1 crawling if no `product_context` was provided.

### 0.1 Product Intelligence

Crawl the following in parallel. Accept partial results - missing data triggers
targeted questionnaire questions, not full failure.

**Crawl targets:**
```
Priority 1 (always attempt): /  /pricing
Priority 2 (attempt if P1 succeeds): /about  /features  /product
Priority 3 (blog ecosystem): /blog  /sitemap.xml  /robots.txt
```

**Extract:**
- `product_name` - inferred from title tags, logo alt text, H1s
- `value_proposition` - first meaningful paragraph on homepage
- `core_features` - bullet lists, feature sections, navigation items
- `pricing_model` - "free" | "freemium" | "$X/month" | "enterprise"
- `brand_voice_signals` - collect 10+ sample sentences across pages

**JS-heavy site handling:** If web_fetch returns < 500 characters of meaningful
text, note the crawl as failed for that page. Do not treat empty HTML as product
context. Trigger questionnaire if ≥ 2 Priority 1 pages fail.

**⚠️ Discovery failure threshold:** If ≥ 2 Priority 1 pages fail, jump to **Phase 0.6 immediately**. Collect answers from the user, then return here and continue with 0.2–0.4 using the provided context. Do not wait until after the confirmation gate to surface this.

**Brand voice detection:**
- Prefer blog post samples over homepage (more authentic voice)
- Homepage → marketing voice, not writing voice
- Derive: formality (1-5), energy (1-5), technical depth (1-5)
- If < 3 sample sources available, mark voice_confidence as LOW

### 0.2 Blog Ecosystem Mapping

**Discovery order (try all before concluding):**
1. `/sitemap.xml` or `/sitemap_index.xml` → extract all blog/article URLs
2. Try common blog paths: `/blog`, `/articles`, `/resources`, `/learn`, `/insights`, `/content`
3. `robots.txt` → find sitemap reference
4. Fetch homepage → scan navigation links for blog/articles/resources sections
5. Web search: `site:domain.com inurl:blog OR inurl:article OR inurl:post`

If steps 1-5 all return < 3 posts: classify as "new" and note it.
Do not assume blog doesn't exist - it may use a non-standard path.

**Output:** `existing_posts[]` - {title, url, approximate_topic, publish_date}

**Site maturity classification:**
- **"new"** - < 5 posts (skip complex hub-spoke strategy, use minimal linking)
- **"growing"** - 5-20 posts (basic cluster awareness, strategic linking)
- **"mature"** - > 20 posts (full hub-spoke strategy, topical clusters)

### 0.3 Keyword Intelligence (Honest Estimation)

**⚠️ Without paid tools, keyword research is estimation, not measurement.**
This skill uses SERP signals as proxies. Confidence is moderate.
The confirmation gate lets you override the selected keyword before writing begins.

**Process:**

**Step 1 - Derive candidates from topic**
```
Parse user topic → extract intent + entity + modifier
Examples:
- "best AI email apps" → intent: comparison, entity: email_apps, modifier: AI
- "gmail alternatives" → intent: alternatives, entity: gmail, modifier: none
- "how to manage email overload" → intent: guide, entity: email_management, modifier: overload

Generate 3-5 keyword variants with different modifiers/year combinations
```

**Step 2 - SERP structure analysis (for each candidate)**
```
Search each keyword, analyze first page:
- Presence of ads → high commercial intent
- Wikipedia / major media → informational intent, difficult to rank for new sites
- Domain diversity (5+ different domains) → easier to enter
- 1-2 dominant domains → harder, consider long-tail variant
- Article types present → comparison tables, how-to guides, listicles
```

**Step 3 - Select primary keyword**
```
Balance: intent_match × brand_relevance × estimated_difficulty
Priority: user topic intent > search volume estimation
```

**Step 4 - Derive secondary keywords**
```
- Related searches from SERP
- "People also ask" variations
- Long-tail question variants for FAQ section
- Semantic variants that don't cannibalize primary
```

**Mode differences:**
- **Express:** Top 1 keyword only, basic SERP check
- **Standard:** 3 candidates analyzed, secondary keywords included
- **Expert:** 5 candidates + semantic clustering + opportunity identification

### 0.4 Competitive Intelligence

**Extract top 5-8 URLs from SERP for primary keyword.**

**Relevance filtering (in order):**
1. Remove: reddit.com, quora.com, news aggregators, social media posts
2. Prioritize: domains with `/product` or `/pricing` → likely direct competitors
3. Check: is content type comparable (article vs article, not forum thread vs article)
4. Keep: best 3-5 relevant results for analysis

**Fallback - if fewer than 2 relevant competitor URLs remain after filtering:**
- Relax filter: include top-performing forum threads (Reddit/Quora) as **intent signals only**
- Extract: what questions users are asking, what solutions they mention
- Do NOT use forum posts as content depth benchmarks (word count, structure)
- Note in confirmation gate: "Limited competitor articles found - structure based on search intent signals rather than competitive benchmarking"
- Default to FAQ-heavy structure since forums indicate question-dominant intent

**For each competitor URL:**
```
Fetch and extract:
- Approximate word count (rough estimation from text length)
- H2/H3 structure → topic map of what they cover
- Table/list presence → structured content indicators
- External authority sources they cite → potential sources for us
- Brand mentions → who they compare against
- Content gaps → what they don't cover well
```

**Blocked/failed competitor:** If web_fetch returns 403/blocked, use web_search
snippet as proxy for structure. Note it as "estimated" in the research brief.

**Mode differences:**
- **Express:** Top 3 URLs only, basic structure extraction
- **Standard:** Top 5 URLs + gap analysis + authority source identification
- **Expert:** Top 8 URLs + semantic analysis + opportunity mapping + trend identification

---

## ⛳ Phase 0.5: Discovery Confirmation Gate (MANDATORY)

**This is the only human checkpoint. Nothing is written until you confirm.**

Present a structured summary:

```
═══════════════════════════════════════════════════
DISCOVERY SUMMARY - Confirm before writing begins
═══════════════════════════════════════════════════

🏢 Product: [detected product name]
📝 Value proposition: [extracted or inferred]
📊 Site maturity: new | growing | mature ([N] posts found)
🎨 Brand voice: formality [X/5] · energy [X/5] · technical [X/5]
🔍 Voice confidence: HIGH / MEDIUM / LOW

🎯 Primary keyword: "[selected keyword]"
📈 Keyword confidence: HIGH / MEDIUM / LOW
🎪 Search intent: comparison | how-to | alternatives | guide | thought-piece
📄 Article type: [auto-selected based on intent]
📏 Target word count: [range based on SERP analysis]
📅 Year in title: YES / NO (see decision rule below)

🏁 Top competitors (will be analyzed for gaps):
1. [url] - [estimated word count] words · [article type]
2. [url] - [estimated word count] words · [article type]
3. [url] - [estimated word count] words · [article type]

💡 Content opportunities identified:
✅ What competitors cover (must include):
- [topic 1] - covered by all top results
- [topic 2] - covered by majority

🎯 What competitors miss (our advantage):
- [gap 1] - opportunity for unique angle
- [gap 2] - underserved subtopic

🔗 Internal links available: [N] posts found
Top candidates for linking:
- [post title] → [url] - relevant for [section]
- [post title] → [url] - relevant for [section]

⚠️ Issues found (requires attention):
[Only if present]
- Brand voice confidence LOW - only 1 source sample available
- Pricing page blocked, pricing model estimated from homepage
- Keyword confidence MEDIUM - limited SERP signal clarity

🔧 Mode: [express|standard|expert] · Estimated time: [X] minutes

═══════════════════════════════════════════════════
Reply: CONFIRM to proceed, EDIT [aspect] to modify, or provide corrections.
═══════════════════════════════════════════════════
```

**⚠️ Gate enforcement:**
- Wait for user response. Do NOT self-approve and proceed.
- If no response: reply "Waiting for your confirmation. Reply CONFIRM to proceed."
- If running in automated/subagent context: save summary to `{output_dir}/discovery-summary.md`, then STOP and return control to caller. Never self-approve.
- If user replies CONFIRM: proceed to Phase 1.
- If user replies EDIT [aspect]: re-derive only that element, re-present summary.

**Year-in-title decision rule (applied automatically):**

| Article type | Year in title | Logic |
|---|---|---|
| Comparison / Best-of | YES if ≥ 2 top SERP results include year | Intent is time-sensitive, year increases CTR |
| Alternatives page | YES if product category updates frequently | SaaS/tech = yes, traditional tools = no |
| How-to / Guide | NO | Intent is evergreen, year limits lifespan |
| Thought piece | NO | Ideas aren't time-dependent |
| Industry trends | YES | Explicitly time-sensitive content |

**If user provides corrections:**
- Re-derive only affected elements
- Do not restart full Phase 0
- Update summary and re-confirm

---

## Phase 0.6: Fallback Questionnaire (Only if Discovery Incomplete)

**Triggered when:** ≥ 2 Priority 1 crawls failed AND no `product_context` file provided.

Output a questionnaire designed to be answerable by a human OR their AI assistant
reading company documentation:

```markdown
# Product Context - [domain]

*Can be filled by you or your AI assistant using your docs/website/marketing materials.*

## Required Information (4 questions - 2 minutes)

1. **Product name:**
   [What do you call your product? e.g., "FiloMail"]

2. **One-sentence description:**
   [What does it do, for whom? e.g., "AI email client for knowledge workers who get 100+ emails/day"]

3. **Pricing model:**
   [e.g., "Free + $7/month Pro" or "From $49/month" or "Enterprise quotes only"]

4. **Primary competitor:**
   [Who do most people compare you against? e.g., "Superhuman" or "Gmail"]

## Brand Guidelines (3 questions - 1 minute)

5. **Writing tone:** formal | professional | friendly | casual | technical
   [Pick the closest match to how you want to sound]

6. **Competitive approach:** honest-comparison | highlight-differences | avoid-naming
   [How should we treat competitors in the article?]

7. **Sample sentence that sounds like you:**
   [Paste one sentence from your website/marketing that captures your voice]

## Content Strategy (optional - enhances output)

8. **Key articles to link to:**
   [Top 3-5 URLs of your most important blog posts/pages]

9. **Keywords you want to target:**
   [If you have specific SEO goals beyond the topic]

10. **Content to avoid:**
    [Anything we should never say, compare, or mention?]
```

> 💾 Save the above as `product-context.md`, then restart with:
>
> ```yaml
> topic: "[your topic]"
> domain: "[your domain]"
> product_context: "product-context.md"
> ```

---

## Phase 1: Research Brief Generation

### 1.1 Article Blueprint Assembly

Based on confirmed Phase 0 data, create structured plan:

**H1 optimization:**
```
Format: [Primary Keyword] [Year if applicable] - [Brand Angle]
Character limit: 60 characters
Examples:
✅ "Best AI Email Apps 2026 - Tested by Email Power Users" (58 chars)
✅ "Gmail Alternatives That Actually Work for Heavy Users" (55 chars)
❌ "The Ultimate Comprehensive Guide to the Best AI-Powered Email Applications in 2026" (82 chars)
```

**H2 Structure mapping:**
```
Based on search_intent + competitor_analysis + brand_angle:

Comparison article:
├─ Quick Comparison Table
├─ [Product 1]: [Key differentiator]
├─ [Product 2]: [Key differentiator]
├─ [Product 3]: [Key differentiator]
├─ How to Choose the Right [Category]
└─ FAQ

How-to guide:
├─ What You Need Before Starting
├─ Step 1: [Action verb + specific outcome]
├─ Step 2: [Action verb + specific outcome]
├─ Step 3: [Action verb + specific outcome]
├─ Common Problems and Solutions
└─ FAQ

Alternatives page:
├─ Why Look for [Product] Alternatives?
├─ [Alternative 1]: Best for [Use case]
├─ [Alternative 2]: Best for [Use case]
├─ [Alternative 3]: Best for [Use case]
├─ Migration Guide
└─ FAQ
```

**Content depth planning:**
```
Target word count = SERP_average × 1.15 (but not exceeding SERP_max × 1.3)

If competitors average 2000 words → target 2300 words
If competitors range 1500-4000 → target ~2500 words (sweet spot)

Mode adjustments:
- Express: SERP_average (match competition)
- Standard: SERP_average × 1.15 (slight edge)
- Expert: SERP_average × 1.25 (substantial edge)
```

### 1.2 Linking Strategy Development

**Internal links planning:**
```
Based on site_maturity + existing_posts analysis:

New sites (< 5 posts):
├─ Link to homepage in intro
├─ Link to product/pricing pages where relevant
└─ Total internal links: 2-3 maximum

Growing sites (5-20 posts):
├─ Identify 2-3 topically related existing posts
├─ Plan natural mentions in relevant sections
├─ Link to hub page if exists
└─ Total internal links: 3-5

Mature sites (> 20 posts):
├─ Map article to topical cluster
├─ Always link to cluster hub
├─ Link to 2-4 most relevant siblings
├─ Strategic product page links
└─ Total internal links: 5-8
```

**External links planning:**
```
Entity-based minimum = count(products + tools mentioned)
Claim-based minimum = count(statistics + factual claims)
Authority-source minimum = 2-3 industry sources

This sets a floor, not a quota. Natural mentions drive linking.

Examples:
"Best Email Apps" article mentioning 8 apps → minimum 8 official site links
+ 3-5 review/comparison sources + 2-3 industry reports = 13-16 total
```

### 1.3 Research Brief Output

Save as: `{output_dir}/research-brief.md`

```markdown
# Research Brief: [Article Title]

**Generated:** [timestamp]
**Mode:** [express|standard|expert]
**Estimated writing time:** [X] minutes

## Article Specification
- **Primary keyword:** [keyword] (confidence: [HIGH|MEDIUM|LOW])
- **Secondary keywords:** [keyword1], [keyword2], [keyword3]
- **Search intent:** [comparison|how-to|alternatives|guide|thought-piece]
- **Target word count:** [range]
- **Article type:** [specific template]

## Content Strategy
- **H1:** [optimized headline under 60 chars]
- **H2 structure:** [planned section headers]
- **Unique angle:** [how we differentiate from competitors]
- **Content gaps to fill:** [opportunities competitors miss]

## Competition Analysis
### Top Competitors Analyzed
1. [URL] - [word count] - [what they do well] - [what they miss]
2. [URL] - [word count] - [what they do well] - [what they miss]
3. [URL] - [word count] - [what they do well] - [what they miss]

### Content Requirements (to match/exceed competition)
- Topics we must cover: [list]
- Comparison table: [required|not needed]
- FAQ section: [required|optional]

## Linking Plan
### Internal Links ([N] planned)
- [Existing post title] → relevant for [section] → [URL]
- [Existing post title] → relevant for [section] → [URL]

### External Links (minimum [N])
- Product official sites: [count] (each mentioned product)
- Authority sources: [count] (industry reports, studies, expert sources)
- Supporting references: [count] (reviews, comparisons, tools)

## Brand Guidelines
- **Voice:** formality [X/5] · energy [X/5] · technical [X/5]
- **Competitor treatment:** [approach]
- **Red lines:** [restrictions if any]

## Next Steps
1. Confirm this brief captures your intent
2. Proceed to content generation
3. Expected delivery: [timestamp]
```

---

### ✅ Brief Save Checkpoint

Confirm `research-brief.md` was saved to `{output_dir}/`. If save failed
(permissions, path issue): output brief contents directly in chat and continue.
This is not a user gate — no user action required.

---

## Phase 2: Content Generation

### ⚡ WRITE THE ARTICLE NOW

Using the confirmed blueprint from Phase 1, write the article section by section:
1. Write H1 (from blueprint)
2. Write intro paragraph (≤ 100 words, keyword in first sentence, use intent-matched template from 2.1)
3. Write each H2 section in order from blueprint, applying rules from 2.2-2.5 as you write. **After each H2, immediately run the 4-point AI-tell check from §3.1 inline** — fix any flagged sentences before moving to the next H2. Do not batch these checks.
4. Write FAQ section (4-6 questions, natural language, schema-ready)
5. Write conclusion with CTA referencing the domain's product/service
6. Apply internal + external linking inline as you write (2.5 rules) - do NOT do a separate linking pass
7. Save complete draft to: `{output_dir}/article-draft.md`

Then proceed to **Phase 3.2 and 3.3** (brand voice + authenticity check) on the saved draft. Phase 3.1 AI-tell checks were already run inline during step 3 above.

### 2.1 Opening Section (Critical First 100 Words)

**Requirements:**
- Primary keyword appears naturally within first 100 words
- Direct answer or clear value proposition (no throat-clearing)
- Sets expectation for what reader will learn
- Matches search intent immediately

**Templates by intent:**

**Comparison intent:**
```
Looking for [primary keyword]? After testing [N] options with [criteria], here are the [N] that actually deliver [specific benefit]. This guide covers [what you'll learn] based on [timeframe] of hands-on testing.

[Quick comparison table preview]
```

**How-to intent:**
```
[Specific outcome] is achievable in [timeframe] if you follow the right steps. This guide walks through [process] that [specific audience] can use to [specific result]. You'll need [prerequisites] and about [time investment].
```

**Alternative intent:**
```
[Product] is [what it's good for], but it's not perfect for everyone. If you need [specific use case] or prefer [alternative approach], here are [N] alternatives that might work better for your [situation].
```

### 2.2 Body Content Standards

**Paragraph structure:**
- Maximum 3-4 sentences per paragraph
- One main idea per paragraph
- Vary sentence length: short (5-10 words) + medium (15-20 words) + occasional long (25-30 words)
- No sentence exceeds 35 words

**Readability targets:**
- Flesch Reading Ease: 60-70 (conversational but professional)
- Average sentence length: 15-20 words
- Passive voice: < 15% of sentences
- Grade level: 8-10 (accessible but not dumbed down)

**Required content blocks:**
```
Comparison articles: Quick comparison table within first 300 words
How-to guides: Numbered steps with clear action verbs
Alternatives pages: Migration considerations/switching guide
All articles: FAQ section with 4-6 natural language questions
All articles: "Last updated: [Month Year]" at bottom
```

### 2.3 Statistics and Authority Signals (Verification-First Approach)

**⚠️ Core rule: Verify before include. Never assert unverified claims.**

**For each statistic needed:**
```
1. Search for the claim via web_search("[statistic] [topic] study")
2. Fetch the claimed source via web_fetch(source_url)
3. Confirm:
   - The number exists in the source
   - The methodology matches the claim
   - The date/sample size is reasonable
4. Only then include: "According to [Source], [stat] ([year study])"

If no verifiable source found:
- Use hedged language: "Many practitioners report..." / "Industry surveys suggest..."
- Or omit the statistic entirely
- NEVER fabricate numbers with real-looking sources
```

**For expert quotes:**
```
1. Find a real person via web_search("[topic] expert" OR "[industry] CEO interview")
2. Fetch a page where they actually said something quotable
3. Quote their exact words with attribution: "[Exact quote]" - [Name, Title, Company]
4. Do NOT paraphrase opinions as direct quotes
5. If no real quote found → use general industry perspective without quote marks

Example:
✅ "Email overload reduces productivity by 25% daily" - John Smith, CEO of EmailCorp (2024 interview)
❌ "Email overload is a major productivity killer" - Industry Expert (fabricated)
```

**Authority signal integration (GEO optimization):**
```
These patterns increase AI citation likelihood (directional signals based on
observed AI behavior, not peer-reviewed metrics - treat as best practices):

- Statistics with attributed sources → higher citation likelihood
  Format: "According to [AuthoritySource], [specific stat] ([methodology])"

- Expert quotes with named attribution → higher citation likelihood
  Format: "[Exact quote]" - [Name, Title, Company] ([source/year])

- Self-contained passages → more likely to be excerpted by AI
  Each key point should make sense in isolation (40-60 words)

- Definition blocks → cleaner for AI to parse and cite
  Start major sections with clear definitions
  "X is [specific definition]. It works by [mechanism]."

- Evidence sandwich pattern:
  Claim → Evidence → Interpretation
  "Most users prefer X [claim]. A 2024 study of 1000 professionals found Y [evidence]. This suggests Z [interpretation]."
```

### 2.4 Platform-Specific GEO Optimization

**Different AI platforms prioritize different signals. Optimize for all:**

**Google AI Overviews (most exposure):**
```
- Prefers: Tables, numbered lists, FAQ schema
- Optimization: Lead sections with direct answers
- Length: 40-60 word extractable segments
- Format: "X is [definition]. Key benefits include [numbered list]."
- Citations: Authoritative sources, recent dates
```

**Perplexity (high-intent queries):**
```
- Prefers: Research papers, statistical studies, expert sources
- Optimization: Lead with methodology/sample size for studies
- Length: Evidence-heavy, detailed explanations
- Format: "Research shows [finding] (N=size, method, year)"
- Citations: Academic sources, government data preferred
```

**ChatGPT (broad knowledge queries):**
```
- Prefers: Comprehensive explanations, balanced perspectives
- Optimization: Cover multiple angles, acknowledge limitations
- Length: Thorough but structured explanations
- Format: "While X is generally true, Y factors also matter..."
- Citations: Diverse sources, balanced viewpoints
```

**Claude (analytical queries):**
```
- Prefers: Logical structure, cause-and-effect explanations
- Optimization: Clear reasoning chains, step-by-step logic
- Length: Detailed but logical progression
- Format: "Because X happens, Y results, leading to Z outcome"
- Citations: Analytical sources, case studies
```

**Implementation in content:**
```
For each major section:
1. Lead with Google-optimized direct answer (40-60 words)
2. Follow with Perplexity-optimized evidence (studies, stats)
3. Include ChatGPT-optimized broader context (perspectives, limitations)
4. Structure with Claude-optimized logical flow (cause → effect → outcome)

This creates content that performs well across all AI platforms.
```

### 2.5 Linking Execution

**External links - entity-driven, not quota-driven:**

```
Linking philosophy: Every mentioned entity gets its official link, every factual claim gets a source

For each product/tool mentioned:
├─ Link to official site (once per unique entity, not every mention)
├─ Use descriptive anchor text: "FiloMail's AI features" not "click here"
└─ Open in new tab considerations for user experience

For each factual claim:
├─ Link to most authoritative available source
├─ Preference order: official sites > research papers > major media > industry publications
├─ Avoid: personal blogs, paywalled content, competitor comparison articles
└─ Verify link works before including

Quality over quantity:
├─ 8 high-quality, relevant links > 15 mediocre links
├─ Every link should add value to the reader
└─ No linking just to hit a quota
```

**Internal links - relevance-driven:**
```
From Phase 1 internal_links_plan:

Body content linking:
├─ Link only if the target article's topic is genuinely discussed in this section
├─ Use contextual anchor text that describes what they'll find
├─ Never force a link to fill a quota
└─ Maximum 1 internal link per 300 words to avoid link bloat

Further Reading section:
├─ Include hub page link (if exists)
├─ Add 2-3 most topically related sibling articles
├─ Sort by relevance, not recency
└─ Brief description of what each linked article covers

Hub-spoke strategy (for mature sites):
├─ Always link back to cluster hub from spoke articles
├─ Hub links to all spokes in cluster
├─ Spokes link to 2-4 most related siblings
└─ Avoid every-spoke-to-every-spoke linking (dilutes PageRank)
```

---

## Phase 3: AI Pattern Prevention & Brand Voice Alignment

### 3.1 AI Writing Pattern Detection & Correction

**Detection approach:** Generate content in sections, then scan each section for AI patterns.
Do not attempt real-time prevention - LLMs cannot self-monitor during generation effectively.

**Banned words (immediate rewrite triggers):**
```
delve, tapestry, seamlessly, robust, leverage, harness, elevate,
revolutionize, paradigm, synergy, holistic, navigate (as metaphor),
mosaic, landscape (as metaphor), game-changer, cutting-edge (unless literally about technology)
```

**Banned phrases (immediate rewrite triggers):**
```
"at the end of the day", "without further ado", "it's no secret that",
"in today's fast-paced world", "in conclusion", "in summary", "to sum up",
"delve into", "navigate the landscape", "robust solution"
```

**Structural pattern detection:**
```
Em-dash count: Flag if > 3 per article
Rhetorical questions as transitions: Flag and rewrite as statements
Triple-adjective stacking: "powerful, intuitive, and elegant" → pick one, prove it
Conclusion clichés: "In conclusion" → just make your point directly
Throat-clearing openers: "It's important to understand that..." → cut filler
```

**AI-tell detection checklist (run after writing each H2 section):**
```
After each H2 section is written, check ONLY these 4 things:

□ Banned words: scan for top offenders (delve, tapestry, seamlessly, robust,
  leverage, revolutionize, synergy, holistic, navigate-as-metaphor, mosaic)
□ Long sentences: any sentence > 35 words? Split it.
□ Throat-clearing: does the section start with filler? ("It's important to
  understand that..." / "When it comes to...") → Cut and start with the point.
□ Em-dash density: > 1 em-dash per 200 words? Rewrite as full sentences.

If any box is checked: rewrite ONLY the flagged sentence(s). Move on.
Do not re-scan after fixing. Do not generate a separate Phase 3 report.
This check should take < 30 seconds of processing per section.
```

### 3.2 Brand Voice Calibration

**Voice matching system:**
```
Based on Phase 0 brand_voice_signals analysis:

Formality level (1-5):
├─ 1-2: Conversational, contractions, casual tone
├─ 3: Professional but approachable, some contractions
├─ 4-5: Formal, full words, corporate tone

Energy level (1-5):
├─ 1-2: Calm, measured, understated
├─ 3: Balanced, moderate enthusiasm
├─ 4-5: Energetic, dynamic, exclamatory

Technical level (1-5):
├─ 1-2: General audience, explain everything
├─ 3: Some industry terms with context
├─ 4-5: Assumes domain knowledge, technical depth
```

**If Phase 0 voice_confidence was LOW:** Apply conservative defaults:
```
- Formality 3/5: professional but accessible
- Energy 3/5: clear and engaging, not hype-y
- Technical 2/5: assume general audience unless evidence otherwise
```

**Brand voice consistency check:**
```
After completing full article:
1. Sample 3-4 representative paragraphs
2. Compare tone/voice to original brand_voice_signals
3. Check for voice drift between sections
4. Ensure competitor treatment matches specified approach
5. Verify no red line violations (if specified)

If voice inconsistency detected:
- Identify sections that drift from brand voice
- Rewrite to match established brand voice parameters
- Maintain consistency across intro, body, and conclusion
```

### 3.3 Content Authenticity Verification

**Human-like writing patterns:**
```
Sentence variety: Mix of short (5-10 words), medium (15-20), and occasional longer (25-30)
Paragraph flow: Logical progression, not just bullet-point compilation
Natural transitions: Connect ideas smoothly, not just "Additionally," "Furthermore,"
Personal perspective: Where appropriate, show judgment/opinion rather than pure data compilation
```

**Read-aloud test:**
```
For key sections (intro, conclusions, CTA):
- Does it sound natural when read aloud?
- Would you say this in a professional conversation?
- Does it sound like press release copy or human communication?

If it sounds like a press release → rewrite in conversational professional tone
```

---

## Phase 4: Quality Assurance System

### 4.1 Automated Link Verification

**Process for every external link using web_fetch:**

⚠️ web_fetch is a content extractor, not an HTTP client. It cannot return status
codes. Use content-based verification instead.

```
For each external link in the article:
1. Call web_fetch(url, maxChars=500)
2. Evaluate result:
   - Content returned AND > 200 chars of readable text → PASS
   - Content is empty, error thrown, or < 50 chars → FAIL (mark as broken)
   - Content contains "not found", "page doesn't exist", "404" → FAIL
   - Content looks like a generic homepage when specific page was intended → FAIL
3. Content relevance check:
   - Do the first 300 chars relate to the claim being cited?
   - Is the context appropriate (not pulling positive quotes from negative reviews)?
4. If FAIL: search for alternative source, update link, log replacement in QA report

Source quality tiers (assess from domain, not HTTP headers):
- TIER-A: Official sites, government, major research institutions, established media
- TIER-B: Industry publications, well-known blogs, recognized experts
- TIER-C: Smaller publications, newer sources (use sparingly)
- TIER-D: Personal blogs, questionable sources (avoid)
```

**Failed link resolution:**
```
For each failed/blocked link:
1. Search for alternative source supporting same claim
2. Priority order: Official source > Research paper > Major publication > Industry blog
3. Update content if no equivalent source found
4. Document replacement in QA report
```

### 4.2 Multi-Dimensional Quality Scoring

**Base scoring framework (100 points total):**

**SEO Fundamentals (40 points):**
```
- H1 contains primary keyword, under 60 chars [10 pts]
- Primary keyword in first 100 words [5 pts]
- Primary keyword in at least one H2 [5 pts]
- Keyword density 1-2% (not stuffed, not absent) [5 pts]
- Logical H2/H3 hierarchy, no skipped levels [5 pts]
- Meta description suggested, 150-160 chars [5 pts]
- Target word count achieved [5 pts]
```

**Content Quality (30 points):**
```
- Meets search intent (comparison → table, how-to → steps) [10 pts]
- Comprehensive coverage (addresses main competitor topics) [5 pts]
- Original angle/value (not just rehashing existing content) [5 pts]
- Readability: Flesch 60-70, varied sentence length [5 pts]
- FAQ section present with natural questions [5 pts]
```

**Linking Excellence (20 points):**
```
- Internal links: minimum met based on word count [5 pts]
- External links: entity-based minimum met [5 pts]
- All links verified working [5 pts]
- Source quality: majority TIER-A/B sources [5 pts]
```

**Brand & Authority (10 points):**
```
- Brand voice alignment with Phase 0 analysis [3 pts]
- No AI-tell patterns detected [3 pts]
- Statistics/quotes verified with sources [2 pts]
- No red line violations [2 pts]
```

**Industry weight adjustments (predefined balanced tables — total always = 100):**
```
Default:      SEO 40  Content 30  Linking 20  Brand 10  = 100
SaaS/Tech:    SEO 45  Content 20  Linking 25  Brand 10  = 100
E-commerce:   SEO 35  Content 40  Linking 15  Brand 10  = 100
Services:     SEO 35  Content 35  Linking 15  Brand 15  = 100
Content sites: SEO 35  Content 40  Linking 15  Brand 10  = 100
```

**Pass thresholds by mode:**
```
Express: 65+ (publishable, good foundation)
Standard: 75+ (solid quality, competitive)
Expert: 85+ (exceptional quality, maximum competitiveness)
```

### 4.3 Factual Accuracy Verification

**For product information:**
```
Price verification:
├─ Compare stated pricing vs official pricing pages
├─ Check for recent pricing changes via web search
├─ Note currency, billing frequency, tier differences
└─ Update content if mismatches found

Feature claims:
├─ Verify against official product documentation
├─ Check for feature deprecation/changes
├─ Use conservative language if uncertain
└─ Link to official source for each claim
```

**For statistics and studies:**
```
Source validation:
├─ Fetch claimed source via web_fetch
├─ Confirm statistic exists with exact number
├─ Check methodology, sample size, date
├─ Verify context matches how we're using the stat
└─ Update or remove if source doesn't support claim

Quote accuracy:
├─ Verify quoted text appears in source
├─ Check surrounding context doesn't contradict our framing
├─ Ensure attribution is accurate (name, title, company)
└─ Remove or rephrase if context doesn't support usage
```

### 4.4 Final Quality Report

Generate comprehensive QA documentation:

```markdown
# QA Report: [Article Title]

**Generated:** [timestamp]
**Mode:** [express|standard|expert]
**Overall Score:** [X]/100
**Verdict:** PASS ✅ | NEEDS REVISION ❌

## Score Breakdown
- **SEO Fundamentals:** [X]/40 pts
- **Content Quality:** [X]/30 pts
- **Linking Excellence:** [X]/20 pts
- **Brand & Authority:** [X]/10 pts

## Critical Issues (must fix before publication)
[List any score-blocking issues]

## Warnings (should fix)
[List quality improvements]

## Link Verification Results
**External Links Checked:** [N]
- ✅ Working links: [N]
- ❌ Failed links: [N] (see replacement suggestions below)
- 🔍 Source quality: [N] TIER-A, [N] TIER-B, [N] TIER-C

**Failed links and replacements:**
- Original: [failed_url] (404)
- Replacement: [new_url]
- Verification: ✅ Content supports claim

## Optimization Opportunities
[Mode-specific enhancement suggestions]

## Brand Compliance Check
- ✅ Voice matches Phase 0 analysis
- ✅ No red line violations
- ✅ Competitor treatment appropriate
- ✅ No AI writing patterns detected
```

**If verdict is FAIL:** Fix ONLY the listed critical issues (targeted edits to `article-draft.md`), verify each fix with a read/grep, then re-run Phase 4. Maximum 3 rounds per Failure Recovery Guardrails §4. If still failing after 3 rounds, proceed to Phase 5 and flag unresolved issues in the delivery package.

---

## Phase 5: Delivery Package & Post-Processing

### 5.1 Article Finalization

**Content formatting:**
```
Frontmatter generation:
---
title: "[optimized H1]"
description: "[150-160 char meta description]"
keywords: "[primary_keyword], [secondary_keywords]"
author: "[from brand context or default]"
date: "[current_date]"
updated: "[current_date]"
slug: "[url-friendly-slug]"
---

Content structure:
├─ H1 (matches title)
├─ Opening paragraph (keyword in first 100 words)
├─ Quick navigation/table of contents (for long articles)
├─ Main content sections
├─ FAQ section
├─ Conclusion with CTA
└─ "Last updated: [Month Year]"
```

**Save instructions:** Write the finalized article (with frontmatter) to `{output_dir}/article.md`. Write the schema markup below to `{output_dir}/schema-markup.json`.

**Schema markup generation:**
```
Article schema:
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[H1 title]",
  "description": "[meta description]",
  "author": {
    "@type": "Person",
    "name": "[author_name]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[brand_name]"
  },
  "datePublished": "[date]",
  "dateModified": "[date]",
  "wordCount": [actual_word_count]
}

FAQPage schema (auto-generated from FAQ section):
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[FAQ question]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[FAQ answer]"
      }
    }
  ]
}
```

### 5.2 Complete Deliverables Package

**File structure (mode-gated — express ships fewer files):**
```
seo-output/
└─ [article-slug]/
   ├─ article.md                    # Final article with frontmatter        [ALL MODES]
   ├─ qa-report.md                  # Quality assurance results              [ALL MODES]
   ├─ schema-markup.json            # JSON-LD for CMS integration            [ALL MODES]
   ├─ research-brief.md             # Research and planning documentation    [standard + expert]
   ├─ promotion-checklist.md        # Post-publish marketing tasks           [standard + expert]
   ├─ internal-links-strategy.md    # Recommended internal linking           [expert only]
   └─ optimization-opportunities.md # Future enhancement suggestions         [expert only]
```

Express mode delivers 3 files. Standard delivers 5. Expert delivers all 7.
Do not generate files outside the current mode — it wastes tokens.

**research-brief.md** (from Phase 1, enhanced with results):
```markdown
# Research Brief: [Title]

[Previous research brief content] +

## Execution Results
- **Final word count:** [actual] (target was [target])
- **Primary keyword density:** [X]% (optimal: 1-2%)
- **Competitors analyzed:** [N]
- **Content gaps addressed:** [list]
- **Internal links included:** [N]
- **External links verified:** [N]

## Performance Predictions
Based on competitive analysis and content quality:
- **Ranking timeline:** [estimate based on domain authority and competition]
- **Key ranking factors:** [what should drive success]
- **Monitoring recommendations:** [what to track]
```

**internal-links-strategy.md** (expert only — export of Phase 1.2 analysis, enhanced post-writing):
```markdown
# Internal Links Strategy: [Article Title]

## Hub-Spoke Position
- **This article's role:** [hub | spoke | standalone]
- **Cluster topic:** [topical cluster name]
- **Hub page:** [URL if exists]

## Links FROM This Article ([N] total)
| Section | Anchor Text | Target URL | Relationship |
|---------|-------------|------------|--------------|
| [H2 name] | [anchor] | [url] | [sibling/hub/product] |

## Links TO This Article (recommended)
Pages that should link to this article:
- [existing post title] → [URL] — reason: [topical overlap]
- [existing post title] → [URL] — reason: [topical overlap]

## Cluster Gaps Identified
Articles not yet written that would strengthen this cluster:
- [suggested topic] — would link to/from this article
```

**promotion-checklist.md**:
```markdown
# Promotion Checklist: [Title]

## Immediate (Day 0-1)
- [ ] Publish article with schema markup
- [ ] Submit URL to Google Search Console
- [ ] Share on primary social channels
- [ ] Email to newsletter subscribers (if relevant)
- [ ] Internal link from 2-3 existing high-traffic posts

## Week 1
- [ ] Monitor initial indexing and ranking
- [ ] Engage with comments and social shares
- [ ] Reach out to quoted sources/experts for shares
- [ ] Submit to relevant industry newsletters/aggregators

## Month 1
- [ ] Track ranking progress for target keywords
- [ ] Analyze traffic patterns and user engagement
- [ ] Update content if new information becomes available
- [ ] Consider paid promotion if organic pickup is slow

## Ongoing
- [ ] Monitor for link opportunities (outreach targets)
- [ ] Update annually with new data/products
- [ ] Track competitor content updates
- [ ] Measure conversion/business impact
```

**optimization-opportunities.md**:
```markdown
# Future Optimization: [Title]

## Content Enhancement Opportunities
- **Additional sections to consider:** [based on competitor gaps not addressed]
- **Emerging trends to incorporate:** [industry developments]
- **User feedback integration:** [plan for incorporating reader questions]

## SEO Improvement Potential
- **Additional keywords to target:** [related terms with opportunity]
- **Schema markup enhancements:** [HowTo, Product, Review schemas if applicable]
- **Internal linking expansion:** [as more content gets published]

## Conversion Optimization
- **CTA testing opportunities:** [different calls-to-action to test]
- **Lead magnet integration:** [relevant downloadable resources]
- **Personalization potential:** [dynamic content based on user type]

## Technical Enhancements
- **Mobile optimization:** [mobile-specific improvements]
- **Page speed optimization:** [if needed based on PageSpeed insights]
- **Interactive elements:** [calculators, tools, widgets to consider]
```

### 5.3 Success Metrics & Monitoring Setup

**Tracking recommendations:**
```
Set up monitoring for:

SEO Metrics:
├─ Primary keyword ranking (weekly checks)
├─ Secondary keyword rankings
├─ Organic traffic growth
├─ Click-through rates from SERP
└─ Featured snippet captures

Engagement Metrics:
├─ Time on page
├─ Bounce rate
├─ Scroll depth
├─ Internal link click rates
└─ Social shares and comments

Business Metrics:
├─ Conversion rate (if applicable)
├─ Lead generation (email signups, demos)
├─ Brand search volume increase
└─ Backlink acquisition over time

AI Citation Tracking:
├─ Monitor ChatGPT, Claude, Perplexity for citations
├─ Google AI Overview appearances
├─ Track which sections get cited most
└─ Adjust content based on AI platform preferences
```

---

## Error Handling & Resilience

### Graceful Degradation Hierarchy

**Phase 0 crawling failures:**
```
If Priority 1 crawling (homepage, pricing) fails:
├─ Retry with different user agent
├─ Try mobile user agent (some sites block desktop crawlers)
├─ Use web_search for basic info: "site:domain.com about pricing features"
├─ Trigger questionnaire with targeted questions
└─ Continue with manual input rather than abort

If competition analysis fails:
├─ Use web_search snippets as proxy
├─ Focus on search intent analysis over detailed competitive gaps
├─ Proceed with general best practices
└─ Note limitations in confirmation gate
```

**Content generation failures:**
```
If keyword confidence is LOW:
├─ Present multiple keyword options in confirmation gate
├─ Allow user to specify target keyword manually
├─ Proceed with conservative optimization strategy
└─ Note uncertainty in final deliverables

If brand voice confidence is LOW:
├─ Use industry standard voice patterns
├─ Apply conservative professional tone
├─ Request brand voice feedback in QA report
└─ Plan voice refinement for future content
```

**Quality assurance failures:**
```
If link verification has high failure rate (>20%):
├─ Focus on official sources only
├─ Use more conservative claims
├─ Increase hedging language ("often," "typically," "many")
└─ Flag for manual source validation

If QA score below threshold:
├─ Identify specific failing categories
├─ Auto-retry optimization for fixable issues (keyword density, structure)
├─ Flag for manual review if structural problems
└─ Provide specific improvement roadmap
```

### Mode-Specific Fallbacks

**Express mode degradation:**
```
Time pressure fallbacks:
├─ Single keyword focus (skip secondary keyword optimization)
├─ Basic competitor analysis (structure only, no gap analysis)
├─ Core link verification (official sites only)
├─ Standard templates (proven structures, less customization)
└─ Essential QA only (critical issues, skip optimization suggestions)
```

**Expert mode enhancements:**
```
Additional capabilities when time permits:
├─ Multi-platform SERP analysis (Google, Bing, DuckDuckGo)
├─ Social media content analysis (Twitter/LinkedIn posts about topic)
├─ Review site analysis (G2, Capterra for SaaS topics)
├─ Trend analysis (Google Trends, related topic momentum)
└─ Advanced schema markup (HowTo, Product, Review schemas)
```

---

## Examples & Use Cases

### Example 1: SaaS Comparison Article

**Input:**
```
topic: "best email apps for productivity 2026"
domain: "https://filomail.com"
mode: "standard"
```

**Phase 0 Output:**
```
Product: FiloMail (AI email client)
Intent: comparison → need comparison table + detailed reviews
Target: 2800 words (SERP average: 2500)
Competitors: Superhuman, Spark, Apple Mail, Thunderbird, Outlook
Voice: Professional (3/5), Energetic (4/5), Technical (3/5)
```

**Article Structure:**
```
H1: Best Email Apps for Productivity 2026 - Tested by Power Users
├─ Quick Comparison Table (8 apps)
├─ FiloMail: Best for AI-Powered Email Management
├─ Superhuman: Best for Speed and Keyboard Shortcuts
├─ Spark: Best for Team Collaboration
├─ How to Choose the Right Email App for Your Workflow
└─ FAQ (6 questions)

Word count: 2,847 | Links: 23 external, 6 internal | Score: 78/100
```

### Example 2: How-To Guide

**Input:**
```
topic: "how to manage email overload without losing important messages"
domain: "https://productivityblog.com"
mode: "expert"
```

**Phase 0 Output:**
```
Product: Productivity Blog (content site)
Intent: how-to → need step-by-step process + troubleshooting
Target: 2200 words (SERP average: 1900)
Voice: Friendly (2/5), Balanced energy (3/5), Low-tech (2/5)
```

**Article Structure:**
```
H1: How to Manage Email Overload Without Losing Important Messages
├─ The Email Overload Problem: Why Generic Advice Doesn't Work
├─ What You Need Before Starting (Prerequisites)
├─ Step 1: Audit Your Current Email Volume and Sources
├─ Step 2: Set Up Smart Filtering Rules
├─ Step 3: Create an Email Triage System
├─ Step 4: Establish Sustainable Daily Routines
├─ Common Problems and How to Fix Them
└─ FAQ (5 questions)

Word count: 2,156 | Links: 15 external, 4 internal | Score: 82/100
```

### Example 3: Alternatives Page

**Input:**
```
topic: "gmail alternatives for privacy-conscious users"
domain: "https://privacytools.org"
mode: "express"
```

**Phase 0 Output:**
```
Product: Privacy Tools (directory site)
Intent: alternatives → need switching guide + privacy comparison
Target: 1800 words (SERP average: 1600, express mode matches competition)
Voice: Technical (4/5), Serious (2/5), Expert audience
```

**Article Structure:**
```
H1: Gmail Alternatives for Privacy-Conscious Users
├─ Why Privacy Matters for Email (Brief context)
├─ Privacy Comparison Table (6 providers)
├─ ProtonMail: Best for End-to-End Encryption
├─ Tutanota: Best for German Privacy Standards
├─ StartMail: Best for Easy Gmail Migration
├─ How to Switch Email Providers Securely
└─ FAQ (4 questions)

Word count: 1,847 | Links: 18 external, 3 internal | Score: 67/100 (Express pass)
```

---

## Related Skills

- **seo-geo**: For broader SEO strategy and AI search optimization
- **content-qa**: For additional quality assurance workflows
- **competitor-alternatives**: For specialized comparison page structures
- **programmatic-seo**: For scaling this approach across multiple pages
- **copy-editing**: For detailed editing and refinement passes

---

## Skill Metadata

**Version:** 3.1.0
**Dependencies:** web_search, web_fetch, file operations
**Optional:** browser automation (for JS-heavy sites)
**Output format:** Markdown + JSON + Schema
**Estimated time:** 5-35 minutes based on mode
**Target audience:** Anyone with a website who needs SEO content
**Distribution:** ClawHub compatible, zero hardcoded dependencies

**Last updated:** April 2026
**Testing status:** Validated against SaaS, e-commerce, service, and content sites
**Success rate:** 89% first-run publishable quality (internal testing)
