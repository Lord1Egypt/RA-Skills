---
name: seo-article-pipeline
description: End-to-end SEO article pipeline for any blog. Research keywords → analyze competition → write article → generate images → fact-check → humanize → assemble → translate. Use when asked to write a blog article, create SEO content, or generate articles. Input is a target keyword or list of keywords.
metadata:
  openclaw:
    requires:
      env: ["DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD"]
---

# SEO Article Pipeline

## Setup

Before first use, configure your project in a `seo-config.md` file in your workspace:

```markdown
# SEO Pipeline Config

## Product
- **Name**: Your Product Name
- **URL**: https://yourproduct.com
- **Positioning**: One-line description of what you sell
- **Differentiators**: What makes you different from competitors

## Blog
- **Articles path**: ./content/blog/{locale}/slug.mdx
- **Images path**: ./public/blog/
- **Repo**: ./
- **Branch**: main
- **Locales**: en, fr (add/remove as needed)

## Brand Voice
- **Tone**: Professional but direct (customize this)
- **Person**: First person / Third person
- **Avoid**: List words or patterns to avoid

## Image Style
- **Background**: #1a1a2e (customize)
- **Accent color**: #e94560 (customize)
- **Style**: Semi-flat illustration (customize)
- **Always add**: "No text, no words, no letters"

## CTA
- **Component**: <YourCTAComponent /> (or markdown CTA block)
- **Placement**: Top (after intro) + Bottom (before FAQ)
```

If no config file exists, ask the user for these details before starting.

## Pipeline Steps

### Step 1: Research
Run `scripts/research-keyword.sh "keyword" [lang] [location]` to get:
- Search volume, CPC, competition
- Related keywords (secondary targets for H2/H3)
- Google Suggest queries

Default locations: `2840` (US), `2250` (France). Requires `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` env vars.

### Step 2: Analyze Competition
Search the target keyword on Google (web_search tool). Fetch the top 3-5 results (web_fetch). Note:
- What they all cover (must include in our article)
- What none cover (our differentiator)
- Format and length
- Their H2 structure

### Step 2b: Topic Research
Before writing, research the actual subject in depth. Do NOT rely on model knowledge alone.

**If the article is about your own product:**
1. Read your own documentation. Scrape the relevant pages with `web_fetch` if they're online.
2. Check the actual config options, features, limitations, and examples.
3. If the article covers a specific feature, verify against source code or changelog if docs are incomplete.

**If the article is about an external topic:**
1. Search for **primary sources** first: official documentation, original research papers, company blogs, data reports. Avoid secondary blog posts that just rehash other articles.
2. Run 5-10 targeted `web_search` queries from different angles (how-to, comparison, stats, problems, trends).
3. Fetch and read the top 3-5 most authoritative sources (`web_fetch`).
4. Look for real data: surveys, case studies, benchmarks, pricing pages, changelogs.
5. Check community discussions (Reddit, Stack Overflow, GitHub issues) for real user pain points and questions.

**Output: Research Brief**
Before moving to Step 3, compile a short research brief (in your working notes, not in the article):
- Key facts and numbers collected (with sources)
- Common user questions/pain points found
- Gaps in existing content you can fill
- Any claims you planned to make that turned out to be wrong or unverifiable

This brief feeds directly into writing. If your brief is thin, do more research — don't start writing.

### Step 3: Write Article
Follow `references/article-checklist.md` if it exists, otherwise use these defaults:

#### 3a: Keyword Map (before writing)
Map keywords to placement before you start:
- **Primary keyword** → title, H1, intro (first 150 words), conclusion
- **Secondary keywords** → H2 headings, body paragraphs
- **LSI/Related terms** → sprinkle throughout naturally
- **Question keywords** → FAQ section headings

#### 3b: Title & Meta
- **Title**: Generate 3 title options. For each, note character count and keyword position. Pick the best (keyword near start, under 60 chars, compelling).
- **Meta description**: 150-160 chars, include primary keyword + a CTA or value prop.

#### 3c: Write with CORE-EEAT Checklist
Apply these while writing (check each one off):

**Content Quality:**
- [ ] **Intent Alignment** — title promise matches content delivery exactly
- [ ] **Direct Answer** — core answer/value in the first 150 words
- [ ] **Query Coverage** — cover ≥3 query variants/synonyms of the target keyword
- [ ] **Audience Targeting** — state who this article is for (e.g. "If you're a developer looking to...")
- [ ] **Semantic Closure** — conclusion answers the opening question + gives concrete next steps

**Structure & Readability:**
- [ ] **Heading Hierarchy** — H1→H2→H3, never skip levels
- [ ] **Summary Box** — include a TL;DR or "Key Takeaways" section near the top
- [ ] **Data Tables** — put comparisons in tables, not paragraphs
- [ ] **Section Chunking** — one topic per section, paragraphs 3-5 sentences max
- [ ] **Information Density** — no filler, consistent terminology throughout

**Credibility & Evidence:**
- [ ] **Data Precision (HARD REQUIREMENT)** — include ≥5 precise numbers with units (not "many users" but "12,000+ users"). If you can't hit 5, research harder. Use web_search to find real stats. This is non-negotiable.
- [ ] **Citation Density** — ≥1 external citation per 500 words
- [ ] **Evidence-Claim Mapping** — every claim is backed by evidence or a source
- [ ] **Entity Precision** — full names for people/orgs/products (never "a company" or "a tool")

**Differentiation:**
- [ ] **Gap Filling** — cover questions/angles that top competitors don't
- [ ] **Practical Tools** — include at least one checklist, template, calculator, or decision framework

#### 3d: Links & Snippet Optimization
- **Internal links**: 2-5 to other blog articles, with descriptive anchor text (not "click here")
- **External links (HARD REQUIREMENT)**: Minimum 3 external links to authoritative sources. Each must back a specific claim in the article. If you can't find 3 credible sources to link, your article lacks enough verifiable claims. Fix the content, not the link count.
- **Featured snippets**: Format FAQ answers at 40-60 words. Use definition/list/table/how-to formats where applicable.

Article format (markdown with frontmatter):
```markdown
---
title: "Meta Title Here (60 chars max)"
slug: keyword-slug
description: "Meta description (155 chars max)"
keywords: [primary, secondary1, secondary2]
lang: en
date: YYYY-MM-DD
readingTime: X min
---

# H1 Title

Intro (2-3 sentences, hook + value promise)

[CTA: adapt text to article topic]

## H2 sections...

## FAQ
**Q: question?**
A: answer

[CTA: bottom]
```

Rules:
- Use image placeholders: `![alt text](IMAGE_SLOT:description-of-needed-image)`
- Include your CTA at top (after intro) and bottom
- Adapt the CTA text to the article topic (never generic)
- Naturally position your product where relevant, never force it
- Cite stats with sources when possible
- Internal links to other blog articles where relevant
- Length: 1500-2500 words (pillar), 800-1200 (tier 2/3)

### Step 4: Generate Images
For each `IMAGE_SLOT` in the article, generate an image using nano-banana-pro skill (or any available image generation tool).

Use the image style defined in your `seo-config.md`. If no config exists, use a clean, professional SaaS style.

**Always add to prompts**: "No text, no words, no letters"

Image types:
- **Hero**: Main visual for the article
- **Infographic**: Data visualization, comparisons
- **Workflow diagram**: "How it works" in 3-4 steps
- **Screenshots**: Capture from relevant websites using agent-browser

Save all generated images to `output/[slug]/images/` (staging area).

### Step 4b: SEO Self-Score
After writing (before fact-check), score the article on these 10 factors. Each is 0 or 1. Target: ≥8/10.

| # | Factor | Check |
|---|--------|-------|
| 1 | **Title** | Primary keyword present, under 60 chars, compelling |
| 2 | **Meta description** | 150-160 chars, keyword + CTA |
| 3 | **H1** | Contains target keyword, matches search intent |
| 4 | **Keyword placement** | Primary keyword in intro, ≥1 H2, conclusion |
| 5 | **H2 structure** | Secondary keywords in H2s, logical hierarchy |
| 6 | **Internal links** | 2-5 with descriptive anchor text |
| 7 | **External links** | ≥3 to authoritative sources (BLOCKER if < 3) |
| 8 | **FAQ section** | ≥3 questions, answers 40-60 words, snippet-ready |
| 9 | **Readability** | Short paragraphs, tables for data, no filler |
| 10 | **Word count** | 1500-2500 (pillar) or 800-1200 (supporting) |

If score < 8, fix the weak areas before proceeding.

### Step 4c: Fact-Check
Before assembling, verify all factual claims in the article.

**Process:**
0. **Research first**: Before writing OR fact-checking, actively look up information you're unsure about. Use `web_search` and `web_fetch` to:
   - Read official documentation for any product/tool you mention
   - Check pricing pages for current prices
   - Verify stats and numbers from primary sources
   - Read existing top-ranking articles on the keyword for accuracy
   - Fetch GitHub repos, changelogs, or release notes when citing features
   Don't rely on memory alone. If you're not 100% sure of a fact, look it up before including it.
1. **Identify claims**: Extract every specific factual assertion (stats, features, pricing, technical details, company info, tool capabilities)
2. **Classify by source**:
   - **Product claims**: verify against official docs/websites
   - **Stats/numbers**: verify against a live source or remove
   - **Technical claims**: verify against official documentation
   - **Pricing**: verify against the product's current pricing page
   - **Community anecdotes**: mark as anecdotal or remove if presented as fact
3. **Verify or fix**:
   - ✅ Confirmed: keep as-is
   - ❌ False: correct with verified info
   - ⚠️ Unverifiable: either (a) soften the language ("reportedly", "according to community reports"), (b) remove the claim, or (c) add a source
4. **Cross-article consistency**: If the article references facts from other blog articles, ensure numbers match. Never invent specific numbers.

**Common pitfalls:**
- GitHub star counts (change daily, never hardcode)
- Plugin/integration counts on marketplaces
- Specific performance claims
- Config syntax (must match official docs)
- Competitor pricing (check their website, not memory)

**Rule: When in doubt, leave it out.** A wrong fact hurts credibility more than a missing one.

### Step 4d: AI-Tone Check & Humanize
After fact-checking, review the entire article for AI writing patterns. This step is mandatory. Do NOT skip it.

**Process:**
1. **Read the full article** and flag every sentence/section that sounds AI-generated
2. **Search for each flagged pattern** using `web_search` if needed (e.g. verify cited sources, check if phrasing is a known AI tell)
3. **Rewrite flagged sections** to sound human, direct, and natural
4. **Re-read after fixes** to make sure the article flows as a whole

**AI writing patterns to catch and kill:**

| Pattern | Example | Fix |
|---------|---------|-----|
| Filler openers | "This isn't a hypothetical." / "Let's dive in." / "Here's the thing." | Delete or rewrite with substance |
| Buzzword conclusions | "liberating", "fundamental shift", "game-changer", "paradigm shift" | Use concrete language |
| Symmetric lists | "More important / Less important" with matching bullet counts | Break symmetry, use prose when possible |
| Hedging stacks | "It's worth noting that..." / "It's important to understand that..." | Just say the thing |
| Em dashes (—) | "AI tools — like Claude — can..." | Use periods, commas, or rewrite |
| Overly smooth transitions | "That said," / "With that in mind," / "Here's where it gets interesting:" | Cut or rephrase naturally |
| Gratuitous signposting | "Let's break this down." / "Here's what that looks like in practice:" | Delete, the reader can figure it out |
| Perfect parallel structure | Every section follows the exact same pattern/length | Vary rhythm and section lengths |
| Corporate passive voice | "It should be noted that improvements were observed" | Active voice, first person when appropriate |
| Fake enthusiasm | "incredibly powerful", "truly remarkable", "absolutely essential" | Tone down, be specific instead |
| Template FAQ | Generic Q&A that restates the article | Make answers add new info or perspective |

**Tone targets:**
- Write like a practitioner sharing experience, not a content marketer optimizing for engagement
- First person is fine and often better than third person
- Short sentences mixed with longer ones (vary rhythm)
- Concrete > abstract. Numbers > adjectives. Examples > claims.
- If a section reads like it could be in any article on any topic, it's too generic. Make it specific.

**Product mentions specifically:**
- Must feel earned, not forced. If an example feels like a detour just to mention your product, reframe or cut it.
- The best product mentions solve the same problem the article discusses. If the connection isn't obvious, don't force it.

**Final check:** Read the intro and conclusion out loud. If they sound like a LinkedIn post or a press release, rewrite them.

### Step 5: Assemble
Convert the draft article into final format for your blog:

1. **Convert images to webp**: Use `cwebp` (preferred) or `ffmpeg` to convert all images from `output/[slug]/images/` to webp format. Copy to your blog's image directory.

2. **Create the article file** with your blog's frontmatter format:
   ```yaml
   ---
   title: "..."
   description: "..."
   category: "guide"
   tags: ["tag1", "tag2"]
   publishedAt: "YYYY-MM-DD"
   author: "Your Name"
   image: "/blog/hero-image.webp"
   imageAlt: "..."
   draft: true
   ---
   ```
   - Remove the H1 title if your blog template displays it automatically
   - Replace image paths: `IMAGE_SLOT:xxx` → `/blog/xxx.webp`
   - Add your CTA component at the top if applicable
   - Inline images: `![alt](/blog/image-name.webp)`

3. **Git commit & push**:
   ```bash
   cd your-project
   git add content/blog/en/slug.mdx public/blog/*.webp
   git commit -m "feat(blog): add EN article — slug"
   git push origin main
   ```

### Step 6: Translate
Create translated versions of the article:

1. Translate naturally (not literally) to target language
2. **Slug must be in the target language.** Not the English slug in a different folder.
   - Rules: lowercase, no accents in slugs, short and descriptive
3. Save to the appropriate locale folder with translated frontmatter (title, description, imageAlt, slug)
4. Keep the same image paths (images are shared between locales)
5. Add `pairSlug` in both articles' frontmatter pointing to each other (if your blog supports language switching)
6. Git commit & push

## Scripts
- `scripts/research-keyword.sh` — Keyword research via DataForSEO API (requires DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD env vars)

## Requirements
- **DataForSEO account** for keyword research (free tier available)
- **Image generation tool** (nano-banana-pro skill recommended, or any image gen)
- **cwebp** for image conversion (`brew install webp` or `apt install webp`)
- **Git** for version control
