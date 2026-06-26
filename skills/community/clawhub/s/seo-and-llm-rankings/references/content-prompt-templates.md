# Content Creation Prompt Templates

Ready-to-use prompt templates for AI coding/writing agents. Select the template matching the page type you need, fill in the `[PLACEHOLDERS]` with audit findings and keyword research, and give the prompt to your AI agent (Cursor, Claude Code, Codex, etc.).

These prompts generate **content optimized for both Google rankings and LLM citations** (GEO). They do not produce generic articles -- they produce structured, citation-ready pages that AI search engines can extract from and traditional search engines can rank.

---

## How to Use

1. Run the SEO & GEO audit to identify content gaps or missing pages
2. Determine the page type needed (article, landing, glossary, comparison, FAQ, location/persona)
3. Copy the matching template below
4. Replace `[PLACEHOLDERS]` with specifics from your audit, keyword research, and product context
5. If `.agents/product-marketing-context.md` exists, pull company name, audience, and positioning from it
6. Paste the filled prompt into your AI agent

**For programmatic SEO:** When creating pages at scale (e.g., `/integrations/[tool]/` or `/glossary/[term]/`), use Template 3 (Glossary) or Template 6 (Location/Persona) with a batch variable pattern. Replace the single-topic placeholder with a list, and instruct the agent to loop through each item.

---

## Shared Rules (Apply to All Templates)

Every content prompt inherits these rules. They are repeated inside each template so prompts are self-contained when pasted into an agent.

### GEO Optimization (baked into every prompt)

- **Answer capsules**: After every question-style H2, write a 40-60 word self-contained answer that makes sense without surrounding context
- **Citation density**: Include 2-3 sourced statistics per major section, format: "Claim (Source, Year)"
- **Quotation slots**: Include at least 1 expert quote with full attribution per 500 words
- **Extractability**: Every key claim must stand alone -- an AI should be able to quote any single paragraph without needing the paragraph before or after it
- **Tables and lists**: Use tables for comparisons, numbered lists for processes, bullet lists for features. AI systems extract structured data more reliably than prose

### Anti-AI-Writing Rules (baked into every prompt)

- Do not use em dashes (--). Use commas, colons, or parentheses instead
- Avoid these verbs: delve, leverage, utilize, facilitate, foster, bolster, underscore, unveil, navigate, streamline, endeavour
- Avoid these adjectives: robust, comprehensive, pivotal, crucial, vital, transformative, cutting-edge, groundbreaking, innovative, seamless, intricate, nuanced, multifaceted, holistic
- Do not open with "In today's...", "In an era of...", "In the ever-evolving landscape of..."
- Do not use "That being said", "It's worth noting", "At its core", "Let's delve into"
- Do not close with "In conclusion...", "To sum up...", "All things considered..."
- Vary sentence length. No more than 2 consecutive sentences of similar word count
- Read every sentence aloud mentally -- if it sounds like a corporate press release, rewrite it

### Structure Rules (baked into every prompt)

- Single H1 with primary keyword
- H2 headings phrased as questions people actually search for
- H3 headings for subtopics under each H2
- No heading level skips (H1 > H2 > H3, never H1 > H3)
- Paragraphs: 2-3 sentences maximum
- First 150 words must contain a direct answer to the page's primary query

### E-E-A-T Signals (baked into every prompt)

- Include an author attribution section (name, title, credentials)
- Add `datePublished` and `dateModified` metadata
- Reference primary sources (research papers, official documentation, government data) over secondary blogs
- Include at least one first-hand experience or original insight, not just aggregated information

---

## Template 1: Article / Blog Post

Use when: creating informational content targeting a specific search query. Best for how-to guides, explainers, industry analysis, tutorials.

```markdown
---
description: "Create SEO + GEO optimized article: [ARTICLE_TITLE]"
agent: "agent"
tools: ["editFiles", "codebase", "search", "fetch"]
---

# Create Article: [ARTICLE_TITLE]

You are a senior content strategist who specializes in search engine
optimization and generative engine optimization. You write content that
ranks on Google AND gets cited by ChatGPT, Perplexity, Claude, and
Google AI Overviews.

Your job is not to write a generic blog post. Your job is to produce
a structured, citation-ready article that AI systems can extract from
and search engines can rank.

## Content Brief

- **Target query**: [PRIMARY_QUERY] (the exact question or search term this page answers)
- **Search intent**: [informational / commercial investigation / navigational]
- **Target audience**: [WHO_IS_READING -- be specific about role, experience level, goal]
- **Primary keyword**: [PRIMARY_KEYWORD]
- **Secondary keywords**: [KEYWORD_2, KEYWORD_3, KEYWORD_4]
- **Word count**: [1,200-2,500 words -- adjust based on SERP analysis]
- **Competing pages to outperform**: [URL_1, URL_2, URL_3]

## Pre-Writing Analysis (do this before writing)

Before drafting any content:

1. **Intent mapping**: What specific problem does the searcher have? What
   decision are they trying to make? Write one sentence answering this.
2. **SERP shape**: Based on the competing pages, what format dominates?
   (listicle, tutorial, comparison, definition). Match or improve on it.
3. **Gap analysis**: What do the competing pages miss? What questions do
   they leave unanswered? Your article must fill those gaps.
4. **Citation plan**: List 5-8 authoritative sources you will reference
   (research papers, official docs, industry reports with named authors).

## Article Structure

### H1: [ARTICLE_TITLE]
Must contain the primary keyword. Write it as a clear, specific title.

### Opening paragraph (first 150 words)
Directly answer the target query in 2-3 sentences. No preamble, no
background, no "In today's..." opener. State the answer, then expand.

### H2 sections (5-8 total)
Each H2 should be a question that a real person would search for.
Immediately after each H2, write a 40-60 word answer capsule -- a
self-contained paragraph that answers the question completely without
needing any surrounding text. Then expand with detail, examples, data.

### Data requirements per section
- 2-3 statistics with named sources and year: "Claim (Source, Year)"
- At least 1 expert quote with attribution per 500 words
- Tables for any comparison data (do not describe comparisons in prose)
- Numbered lists for any process or sequence

### FAQ section (bottom of article)
Add 5-8 frequently asked questions with answers. Each answer:
- Starts with a direct statement (never "Well, it depends...")
- Is 2-4 sentences long
- Contains at least one specific data point
- Stands alone without context

## Writing Rules

- Paragraphs: 2-3 sentences max
- No em dashes. Use commas, colons, or parentheses
- No filler words: basically, essentially, actually, certainly, obviously
- No AI-tell verbs: delve, leverage, utilize, foster, bolster, streamline
- No AI-tell adjectives: robust, comprehensive, pivotal, seamless, holistic
- No "In today's..." or "In the ever-evolving landscape of..." openings
- Vary sentence length naturally
- Use confident, specific language. Replace "many experts believe" with
  a named expert and a specific claim

## Schema Markup

Include this JSON-LD in the page output:

### Article Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[ARTICLE_TITLE]",
  "author": {
    "@type": "Person",
    "name": "[AUTHOR_NAME]",
    "jobTitle": "[AUTHOR_TITLE]",
    "url": "[AUTHOR_URL]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[COMPANY_NAME]",
    "url": "[SITE_URL]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "description": "[META_DESCRIPTION]",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".answer-capsule", ".faq-answer"]
  }
}
```

### FAQPage Schema (for the FAQ section)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[FAQ_QUESTION]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[FAQ_ANSWER]"
      }
    }
  ]
}
```

## Meta Tags

- **Title**: [50-60 chars, primary keyword near the beginning]
- **Description**: [150-160 chars, includes keyword, has a value prop and CTA]
- **OG image**: 1200x630px with the article title overlaid

## Validation Checklist

After writing, verify:
- [ ] H1 contains primary keyword
- [ ] First 150 words directly answer the target query
- [ ] Every H2 has a 40-60 word answer capsule immediately after it
- [ ] 2-3 sourced statistics per major section
- [ ] At least 1 expert quote per 500 words
- [ ] No em dashes anywhere in the text
- [ ] No AI-tell words (delve, robust, comprehensive, leverage, etc.)
- [ ] All paragraphs are 2-3 sentences max
- [ ] Tables used for all comparison data
- [ ] FAQ section has 5-8 questions with self-contained answers
- [ ] Article schema JSON-LD included
- [ ] FAQPage schema JSON-LD included
- [ ] Meta title is 50-60 chars
- [ ] Meta description is 150-160 chars
- [ ] datePublished and dateModified set
```

---

## Template 2: Landing / Product Page

Use when: creating a conversion-focused page for a product, feature, or service. Optimized for commercial-intent queries and AI recommendation engines.

```markdown
---
description: "Create SEO + GEO optimized landing page: [PAGE_TITLE]"
agent: "agent"
tools: ["editFiles", "codebase", "search"]
---

# Create Landing Page: [PAGE_TITLE]

You are a conversion copywriter with deep SEO and GEO expertise.
You write landing pages that rank on Google for commercial-intent
queries AND get recommended by AI assistants when users ask for
product suggestions.

This is not a generic marketing page. Every section must be
extractable by AI systems and rankable by search engines.

## Content Brief

- **Target query**: [PRIMARY_QUERY] (e.g., "best project management tool for startups")
- **Search intent**: commercial investigation
- **Target audience**: [SPECIFIC_BUYER_PERSONA -- role, company size, pain point]
- **Primary keyword**: [PRIMARY_KEYWORD]
- **Secondary keywords**: [KEYWORD_2, KEYWORD_3, KEYWORD_4]
- **Product/service**: [PRODUCT_NAME]
- **Core value proposition**: [ONE_SENTENCE_VALUE_PROP]
- **Key differentiators**: [DIFF_1, DIFF_2, DIFF_3]
- **Competing products**: [COMPETITOR_1, COMPETITOR_2, COMPETITOR_3]

## Page Structure

### H1: [PAGE_TITLE]
Contains the primary keyword. States what the product does and who
it is for in one clear line.

### Hero section (first 150 words)
- One sentence stating what the product is and who it helps
- One sentence with a specific, quantified benefit
- One sentence with social proof (user count, rating, or named customer)
- CTA button

### H2: What is [PRODUCT_NAME]?
40-60 word answer capsule defining the product. Self-contained.
Then 2-3 short paragraphs expanding on the definition with specifics.

### H2: How does [PRODUCT_NAME] work?
Answer capsule, then a numbered list (3-5 steps) showing the user
workflow. Each step: one sentence of action, one sentence of outcome.

### H2: Key Features
Use a table:
| Feature | What It Does | Benefit |
Each row is one feature. 5-8 features total.

### H2: Who is [PRODUCT_NAME] for?
Answer capsule listing 3-4 audience segments. Then a short paragraph
for each segment explaining their specific use case.

### H2: [PRODUCT_NAME] vs [COMPETITOR_1]
Comparison table:
| Capability | [PRODUCT_NAME] | [COMPETITOR_1] |
Include pricing, key features, limitations. Be factual, not salesy.

### H2: Pricing
State pricing clearly. Use a table if multiple tiers exist.
Include what is included in free/trial tier if applicable.

### H2: Frequently Asked Questions
5-8 questions. Same rules as Template 1 FAQ section.

## Writing Rules

Same anti-AI-writing rules as Template 1. Additionally:
- Do not use superlatives without data ("best", "fastest", "#1") unless
  backed by a named benchmark or award
- Every benefit claim must have a specific number or comparison
- Social proof must name real companies or cite real metrics (not
  "thousands of happy customers")
- No pressure tactics or false urgency

## Schema Markup

### WebPage + Product Schema
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "[PAGE_TITLE]",
  "description": "[META_DESCRIPTION]",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".answer-capsule", ".hero-description"]
  }
}
```

### FAQPage Schema (for FAQ section)
Same as Template 1.

### Organization Schema (if homepage or main product page)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[COMPANY_NAME]",
  "url": "[SITE_URL]",
  "logo": "[LOGO_URL]",
  "description": "[COMPANY_DESCRIPTION]",
  "sameAs": ["[TWITTER]", "[LINKEDIN]", "[GITHUB]"]
}
```

## Meta Tags

- **Title**: [50-60 chars, "[PRODUCT_NAME]: [Primary Benefit] | [Brand]"]
- **Description**: [150-160 chars, includes keyword, quantified benefit, CTA]

## Validation Checklist

- [ ] H1 contains primary keyword and states what the product does
- [ ] First 150 words include product definition, quantified benefit, social proof
- [ ] Every H2 has a 40-60 word answer capsule
- [ ] Features presented in a table (not prose)
- [ ] Comparison table with at least one competitor
- [ ] Pricing stated clearly
- [ ] No unsupported superlatives
- [ ] FAQ section with 5-8 self-contained answers
- [ ] No em dashes or AI-tell words
- [ ] WebPage schema included
- [ ] FAQPage schema included
- [ ] Meta title and description within character limits
```

---

## Template 3: Glossary / Definition Page

Use when: creating single-term definition pages, often for programmatic SEO at scale (`/glossary/[term]/`). Optimized for "What is X?" queries that AI systems frequently answer.

```markdown
---
description: "Create SEO + GEO optimized glossary page: What is [TERM]?"
agent: "agent"
tools: ["editFiles", "codebase", "search"]
---

# Create Glossary Page: [TERM]

You are a technical writer and SEO specialist. You create definition
pages that become the go-to source for AI systems answering "What is
[TERM]?" queries. Your definitions get quoted by ChatGPT, Perplexity,
and Google AI Overviews.

## Content Brief

- **Target query**: "What is [TERM]?" / "[TERM] definition" / "[TERM] meaning"
- **Search intent**: informational (definitional)
- **Target audience**: [AUDIENCE -- e.g., developers learning the concept, marketers evaluating tools]
- **Primary keyword**: [TERM]
- **Secondary keywords**: [TERM] definition, [TERM] meaning, [TERM] explained, [RELATED_TERM_1], [RELATED_TERM_2]
- **Word count**: 800-1,500 words
- **Domain context**: [YOUR_INDUSTRY -- how does this term relate to your product/expertise?]

## Page Structure

### H1: What is [TERM]?

### Definition capsule (first paragraph, 40-60 words)
"[TERM] is [category/class it belongs to] that [what it does or means].
[One key characteristic or distinguishing trait]. [One sourced fact or
statistic about its relevance]."

This paragraph MUST be self-contained. AI systems will quote it verbatim.

### H2: How does [TERM] work?
Answer capsule, then 3-5 short paragraphs or a numbered process.
Include a concrete example.

### H2: Why does [TERM] matter?
Answer capsule with a statistic. Then 2-3 paragraphs explaining
importance with sourced data.

### H2: [TERM] vs [RELATED_TERM]
Comparison table:
| Aspect | [TERM] | [RELATED_TERM] |
3-5 rows comparing key differences.

### H2: Examples of [TERM]
2-4 real-world examples with names and specifics. Use a bullet list.

### H2: How to [use/implement/apply] [TERM]
Numbered steps (3-6). Each step is actionable and specific.

### H2: Frequently Asked Questions
3-5 questions about [TERM]. Short, self-contained answers.

## Writing Rules

Same anti-AI-writing rules as Template 1. Additionally:
- The definition paragraph is the single most important element on the
  page. Spend extra effort making it precise, quotable, and complete
- Use the "X is Y that Z" definition structure (entity, category, differentiator)
- Include the term's full name on first use if it's an acronym
- Do not assume the reader knows related terminology -- define or link it

## Schema Markup

### DefinedTerm Schema
```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "name": "[TERM]",
  "description": "[DEFINITION_CAPSULE]",
  "inDefinedTermSet": {
    "@type": "DefinedTermSet",
    "name": "[YOUR_SITE] Glossary"
  }
}
```

### FAQPage Schema
Same as Template 1.

### BreadcrumbList Schema
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "[SITE_URL]"},
    {"@type": "ListItem", "position": 2, "name": "Glossary", "item": "[SITE_URL]/glossary/"},
    {"@type": "ListItem", "position": 3, "name": "[TERM]"}
  ]
}
```

## Programmatic SEO Batch Pattern

When generating glossary pages at scale, replace `[TERM]` with each
item from this list and generate one page per term:

Terms: [TERM_1, TERM_2, TERM_3, ...]

Each page follows the same structure above. Vary the examples and
comparison terms to avoid duplicate content signals.

## Meta Tags

- **Title**: "What is [TERM]? Definition, Examples & Guide | [BRAND]" (50-60 chars)
- **Description**: "[TERM] is [short definition]. Learn how it works, why it matters, and how to use it." (150-160 chars)

## Validation Checklist

- [ ] Definition capsule is 40-60 words, self-contained, uses "X is Y that Z" structure
- [ ] Primary keyword appears in H1, first paragraph, and at least 2 H2s
- [ ] Comparison table with at least one related term
- [ ] 2-3 sourced statistics
- [ ] Real-world examples with specific names
- [ ] FAQ section with 3-5 self-contained answers
- [ ] No em dashes or AI-tell words
- [ ] DefinedTerm schema included
- [ ] BreadcrumbList schema included
- [ ] Meta title and description within character limits
```

---

## Template 4: Comparison Page

Use when: creating "X vs Y" comparison content. These pages are heavily cited by AI systems when users ask "Which is better, X or Y?" or "What's the difference between X and Y?"

```markdown
---
description: "Create SEO + GEO optimized comparison: [PRODUCT_A] vs [PRODUCT_B]"
agent: "agent"
tools: ["editFiles", "codebase", "search", "fetch"]
---

# Create Comparison Page: [PRODUCT_A] vs [PRODUCT_B]

You are a product analyst with SEO and GEO expertise. You write
comparison pages that AI systems cite when users ask "What's the
difference between X and Y?" or "Which is better, X or Y?"

Your comparisons are factual, structured, and fair. They use tables,
specific data points, and clear verdicts. They are not marketing copy
disguised as a comparison.

## Content Brief

- **Target query**: "[PRODUCT_A] vs [PRODUCT_B]" / "[PRODUCT_A] or [PRODUCT_B]"
- **Search intent**: commercial investigation
- **Target audience**: [WHO -- e.g., engineering managers choosing a CI/CD tool]
- **Primary keyword**: [PRODUCT_A] vs [PRODUCT_B]
- **Secondary keywords**: [PRODUCT_A] alternative, [PRODUCT_B] alternative, [PRODUCT_A] comparison, best [CATEGORY]
- **Word count**: 1,500-2,500 words
- **Your product** (if applicable): [YOUR_PRODUCT -- if you're one of the compared products, be transparent about it]

## Page Structure

### H1: [PRODUCT_A] vs [PRODUCT_B]: [Specific Differentiator in YYYY]
Example: "Notion vs Confluence: Which Wiki Tool Is Better for Remote Teams in 2026?"

### TL;DR / Summary box (first 150 words)
A 3-4 sentence verdict. State who should choose Product A and who
should choose Product B. Be specific about the deciding factors.
This will be the most-quoted section by AI systems.

### H2: Quick Comparison
Full comparison table:
| Feature | [PRODUCT_A] | [PRODUCT_B] |
Include: pricing, free tier, key features (5-8 rows), ideal user,
limitations. Use checkmarks, specific numbers, or short phrases.

### H2: What is [PRODUCT_A]?
40-60 word answer capsule. Then 2-3 paragraphs covering the product's
core functionality, target audience, and market position.

### H2: What is [PRODUCT_B]?
Same structure as above.

### H2: [Feature Category 1] Comparison
(e.g., "Ease of Use", "Pricing", "Integrations", "Performance")
Answer capsule naming the winner for this category with one reason.
Then detailed comparison with data, screenshots, or benchmarks.

### H2: [Feature Category 2] Comparison
Repeat for 3-5 key comparison dimensions.

### H2: When to Choose [PRODUCT_A]
Bullet list of 3-5 specific scenarios where Product A is the better choice.
Each bullet starts with a situation, not a feature.

### H2: When to Choose [PRODUCT_B]
Same structure.

### H2: Alternatives to Both
Table with 3-4 alternatives:
| Alternative | Best For | Starting Price |

### H2: Frequently Asked Questions
5-8 questions. Include "Is [PRODUCT_A] better than [PRODUCT_B]?"
and "What is the cheapest alternative to [PRODUCT_A]?"

## Writing Rules

Same anti-AI-writing rules as Template 1. Additionally:
- If your company makes one of the compared products, state this
  transparently in the opening section
- Every claim about a product's capability must be verifiable
  (link to the product's docs, pricing page, or a third-party review)
- Do not say "both are great options" without specifics
- Use actual pricing numbers, not "affordable" or "premium"
- Date all pricing and feature data -- include "(as of [MONTH YEAR])"

## Schema Markup

### Article Schema (with comparison indication)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[PRODUCT_A] vs [PRODUCT_B]: [SUBTITLE]",
  "author": {
    "@type": "Person",
    "name": "[AUTHOR_NAME]",
    "jobTitle": "[AUTHOR_TITLE]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "description": "[META_DESCRIPTION]",
  "about": [
    {"@type": "Thing", "name": "[PRODUCT_A]"},
    {"@type": "Thing", "name": "[PRODUCT_B]"}
  ],
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".tldr", ".answer-capsule"]
  }
}
```

### FAQPage Schema
Same as Template 1.

## Meta Tags

- **Title**: "[PRODUCT_A] vs [PRODUCT_B]: [Key Difference] ([YEAR]) | [BRAND]" (50-60 chars)
- **Description**: "Compare [PRODUCT_A] and [PRODUCT_B] side by side. [Key differentiator]. See pricing, features, and which is best for [audience]." (150-160 chars)

## Validation Checklist

- [ ] TL;DR in first 150 words with a clear verdict and specific reasoning
- [ ] Full comparison table with pricing, features, and limitations
- [ ] Each product defined in a 40-60 word answer capsule
- [ ] 3-5 feature category sections with per-category verdicts
- [ ] "When to Choose" sections with scenario-based bullets
- [ ] Alternatives table included
- [ ] All pricing and feature claims dated "(as of Month Year)"
- [ ] If biased (own product compared), disclosed transparently
- [ ] No em dashes or AI-tell words
- [ ] Article schema with `about` entities included
- [ ] FAQPage schema included
- [ ] Meta title and description within character limits
```

---

## Template 5: FAQ / Resource Page

Use when: creating a comprehensive Q&A page for a topic area. Ideal for pages targeting long-tail "how to" and "what is" queries. These pages have the highest AI citation rate when structured correctly.

```markdown
---
description: "Create SEO + GEO optimized FAQ page: [TOPIC] FAQ"
agent: "agent"
tools: ["editFiles", "codebase", "search"]
---

# Create FAQ Page: [TOPIC]

You are an information architect and SEO specialist. You create FAQ
pages that become authoritative reference points for AI systems.
When ChatGPT, Perplexity, or Google AI Overviews answer questions
about [TOPIC], your page is the source they cite.

## Content Brief

- **Target topic**: [TOPIC]
- **Target queries**: [QUERY_1, QUERY_2, QUERY_3, ... -- list 10-20 questions people search for]
- **Search intent**: informational
- **Target audience**: [WHO -- role, experience level, what they need to accomplish]
- **Primary keyword**: [TOPIC]
- **Secondary keywords**: [KEYWORD_2, KEYWORD_3]
- **Question sources**: [Google "People Also Ask", forums, support tickets, keyword tools]

## Pre-Writing Analysis

1. **Question clustering**: Group the target queries into 4-6 thematic
   categories. Each category becomes an H2 section.
2. **Priority ranking**: Rank questions by search volume and citation
   potential. High-volume "What is" and "How to" questions go first.
3. **Source mapping**: For each question, identify 1-2 authoritative
   sources you will cite in the answer.

## Page Structure

### H1: [TOPIC]: Frequently Asked Questions

### Introduction (first 150 words)
State what this page covers, who it is for, and how many questions
it answers. Include one key statistic about the topic.

### H2: [Category 1 Name] (e.g., "Getting Started")

#### H3: [Question 1]?
Answer: 2-4 sentences. First sentence directly answers the question.
Include one statistic or source. Self-contained.

#### H3: [Question 2]?
Same format.

(Repeat for 3-5 questions per category)

### H2: [Category 2 Name]
(Repeat pattern for 4-6 categories total)

### H2: Summary Table
| Question | Short Answer |
One row per question. Short answer is 1 sentence -- the absolute
minimum someone needs. This table is highly extractable by AI.

## Writing Rules

Same anti-AI-writing rules as Template 1. Additionally:
- Every answer must start with a direct statement, never with
  "Great question!" or "It depends on..."
- Answers should be 2-4 sentences. If an answer needs more, it should
  be its own article page (link to it instead)
- Include the question's keywords naturally in the answer
- Cross-link related questions within answers where relevant

## Schema Markup

### FAQPage Schema (critical -- this is the primary schema)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[QUESTION_TEXT]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[ANSWER_TEXT]"
      }
    }
  ]
}
```

Include ALL questions from the page in the schema, not just a subset.

### WebPage Schema with Speakable
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "[TOPIC] FAQ",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".faq-answer", "h1"]
  }
}
```

## Meta Tags

- **Title**: "[TOPIC] FAQ: [X] Questions Answered ([YEAR]) | [BRAND]" (50-60 chars)
- **Description**: "Get answers to the most common [TOPIC] questions. Covers [subtopic 1], [subtopic 2], and more." (150-160 chars)

## Validation Checklist

- [ ] 15-30 questions organized into 4-6 categories
- [ ] Every answer starts with a direct statement
- [ ] Every answer is 2-4 sentences and self-contained
- [ ] At least 50% of answers include a sourced statistic or named reference
- [ ] Summary table at the bottom with one-sentence answers
- [ ] FAQPage schema includes ALL questions (not a subset)
- [ ] No em dashes or AI-tell words
- [ ] No "It depends" or "Great question!" openers
- [ ] Cross-links between related questions
- [ ] Meta title and description within character limits
```

---

## Template 6: Location / Persona Page

Use when: creating localized pages (`/[service]/[city]/`) or audience-specific pages (`/for/[audience]/`). Designed for programmatic SEO at scale. Each page must feel unique despite sharing a template.

```markdown
---
description: "Create SEO + GEO optimized [location/persona] page: [SERVICE] in [LOCATION] / [SERVICE] for [AUDIENCE]"
agent: "agent"
tools: ["editFiles", "codebase", "search", "fetch"]
---

# Create [Location/Persona] Page: [SERVICE] [in LOCATION / for AUDIENCE]

You are a local SEO and content specialist. You create location-
or audience-specific pages that rank for "[service] in [city]" or
"[product] for [audience]" queries. Each page must contain unique,
locally relevant (or audience-relevant) information -- not just
the same page with a different city name swapped in.

## Content Brief

- **Target query**: "[SERVICE] in [LOCATION]" or "[PRODUCT] for [AUDIENCE]"
- **Search intent**: [commercial / local / informational]
- **Primary keyword**: [SERVICE] [LOCATION] or [PRODUCT] for [AUDIENCE]
- **Secondary keywords**: best [SERVICE] [LOCATION], [SERVICE] near [LOCATION], [SERVICE] [LOCATION] pricing, [AUDIENCE] [PRODUCT]
- **Unique local/audience data**: [WHAT_MAKES_THIS_PAGE_DIFFERENT -- local stats, regulations, demographics, audience-specific pain points]

## Page Structure

### H1: [SERVICE] in [LOCATION] / [PRODUCT] for [AUDIENCE]
Contains the full target keyword.

### Opening paragraph (first 150 words)
State what the service/product is and why it matters specifically in
this location or for this audience. Include a location-specific or
audience-specific data point in the first sentence.

### H2: Why [LOCATION/AUDIENCE] needs [SERVICE/PRODUCT]
Answer capsule with a locally relevant statistic or audience-specific
pain point. Then 2-3 paragraphs with unique, specific information.

NOT acceptable: "Houston is a big city, so you need good SEO."
Acceptable: "Houston has 14,200 businesses competing for 'plumber near
me' searches, with an average CPC of $47 (Google Ads, 2026)."

### H2: How [SERVICE/PRODUCT] works [in LOCATION / for AUDIENCE]
Answer capsule. Then explain any location-specific or audience-specific
differences in how the service/product works.

### H2: [SERVICE] Pricing [in LOCATION / for AUDIENCE]
Table with pricing tiers. Include location-specific pricing if available.

### H2: What to Look for in a [SERVICE] Provider [in LOCATION / for AUDIENCE]
Numbered list of 5-7 criteria. Each criterion has one sentence of
explanation with a locally or audience-relevant detail.

### H2: Frequently Asked Questions
5-8 questions specific to the location or audience.
Example: "How long does [SERVICE] take in [LOCATION]?"

## Programmatic SEO Batch Pattern

When generating pages at scale, replace `[LOCATION]` or `[AUDIENCE]`
with each item from this list:

Locations: [CITY_1, CITY_2, CITY_3, ...]
OR
Audiences: [AUDIENCE_1, AUDIENCE_2, AUDIENCE_3, ...]

For each page, you MUST include at least 3 unique data points specific
to that location or audience. Do not generate pages that differ only
in the location/audience name -- each page needs unique substance.

## Writing Rules

Same anti-AI-writing rules as Template 1. Additionally:
- Every page must have at least 3 data points unique to the specific
  location or audience (not just the same content with a name swap)
- If local data is unavailable, acknowledge it and provide the closest
  available regional data with a note
- Include a local/audience-specific example or case study when possible
- Do not fabricate local statistics or testimonials

## Schema Markup

### LocalBusiness Schema (for location pages)
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[COMPANY_NAME] - [LOCATION]",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "[CITY]",
    "addressRegion": "[STATE]",
    "addressCountry": "[COUNTRY]"
  },
  "url": "[PAGE_URL]",
  "areaServed": {
    "@type": "City",
    "name": "[CITY]"
  }
}
```

### Service Schema (for persona pages)
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "[SERVICE] for [AUDIENCE]",
  "provider": {
    "@type": "Organization",
    "name": "[COMPANY_NAME]"
  },
  "audience": {
    "@type": "Audience",
    "audienceType": "[AUDIENCE]"
  },
  "description": "[SERVICE_DESCRIPTION_FOR_AUDIENCE]"
}
```

### FAQPage Schema
Same as Template 1.

### BreadcrumbList Schema
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "[SITE_URL]"},
    {"@type": "ListItem", "position": 2, "name": "[SERVICE]", "item": "[SITE_URL]/[SERVICE_SLUG]/"},
    {"@type": "ListItem", "position": 3, "name": "[LOCATION/AUDIENCE]"}
  ]
}
```

## Meta Tags

- **Title**: "[SERVICE] in [LOCATION]: [Key Benefit] | [BRAND]" (50-60 chars)
- **Description**: "[SERVICE] in [LOCATION]. [Unique local detail]. [CTA]." (150-160 chars)

## Validation Checklist

- [ ] H1 contains full target keyword ([SERVICE] + [LOCATION/AUDIENCE])
- [ ] First 150 words include a location/audience-specific data point
- [ ] At least 3 unique data points specific to this location/audience
- [ ] No pages that are just name-swapped copies of each other
- [ ] Pricing information included (with location-specific data if available)
- [ ] FAQ section with location/audience-specific questions
- [ ] No em dashes or AI-tell words
- [ ] LocalBusiness or Service schema included
- [ ] BreadcrumbList schema included
- [ ] FAQPage schema included
- [ ] Meta title and description within character limits
```

---

## Combining Templates

When an audit reveals multiple content gaps across different page types, generate one prompt per page. Do not combine different page types into a single prompt -- each page type has its own structure and schema requirements.

For batch generation (programmatic SEO), use a single prompt with the batch pattern from Template 3 or Template 6, instructing the agent to generate one page per item in the list.

**Example combining flow:**

1. Audit finds: "No glossary section" + "No comparison pages" + "Blog has thin content"
2. Generate: Template 3 prompt for glossary terms, Template 4 prompt for top comparison, Template 1 prompt for the blog rewrite
3. User runs each prompt separately in their AI agent
