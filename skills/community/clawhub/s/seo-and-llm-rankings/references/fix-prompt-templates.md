# Fix Prompt Templates

Ready-to-use prompt templates for AI coding agents. Select the relevant template(s), fill in the `[PLACEHOLDERS]` with findings from the audit, and give the combined prompt to your AI coding agent (Cursor, Claude Code, Codex, etc.).

---

## How to Use

1. Run the SEO & GEO audit (URL mode or codebase mode)
2. Identify which categories of fixes are needed
3. Copy the relevant template(s) below
4. Replace `[PLACEHOLDERS]` with actual audit findings
5. Combine into a single prompt if multiple templates apply
6. Paste into your AI coding agent

**Codebase mode tip:** When auditing local files, include exact file paths and line numbers in the placeholders (e.g., `app/layout.tsx line 12` instead of just `homepage`). This makes the prompt directly actionable for the AI agent working on the codebase.

---

## Template 1: Meta Tags Fix

Use when: title, description, OG tags, or Twitter Card tags are missing or incorrect.

```markdown
---
description: "Fix meta tag issues on [DOMAIN]"
agent: "agent"
tools: ["editFiles", "codebase", "search"]
---

# Fix Meta Tag Issues

You are an SEO expert. Fix the following meta tag issues found during an
audit of [DOMAIN].

## Issues Found

[LIST EACH ISSUE, e.g.:]
1. Page [URL]: Title is [CURRENT_LENGTH] chars (should be 50-60). Current: "[CURRENT_TITLE]"
2. Page [URL]: Meta description missing
3. Page [URL]: No Open Graph tags
4. Page [URL]: No Twitter Card tags

## Fix Instructions

For each issue:

### Title Tags
- Must be 50-60 characters
- Must contain the primary keyword near the beginning
- Format: "[Primary Keyword] - [Brand] | [Secondary Keyword]"
- Do not include the brand name if already shown by the search engine

### Meta Descriptions
- Must be 150-160 characters
- Must include primary keyword
- Must have a clear value proposition and call to action
- Write compelling copy that encourages clicks

### Open Graph Tags (add if missing)
```html
<meta property="og:title" content="[Same as title or slightly different]">
<meta property="og:description" content="[Same as meta description]">
<meta property="og:image" content="[Image URL, 1200x630px]">
<meta property="og:url" content="[Canonical URL]">
<meta property="og:type" content="website">
```

### Twitter Card Tags (add if missing)
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[Title]">
<meta name="twitter:description" content="[Description]">
<meta name="twitter:image" content="[Image URL]">
```

## Validation
After fixing, verify each page has all required meta tags by viewing page source.
```

---

## Template 2: Schema Markup Addition

Use when: structured data (JSON-LD) is missing or incomplete.

```markdown
---
description: "Add schema markup to [DOMAIN]"
agent: "agent"
tools: ["editFiles", "codebase", "search"]
---

# Add Schema Markup

You are an SEO and structured data expert. Add JSON-LD schema markup to
[DOMAIN] based on audit findings.

## What's Missing

[LIST WHAT'S NEEDED, e.g.:]
1. Homepage: Missing Organization schema
2. Blog posts: Missing Article schema
3. FAQ section: Missing FAQPage schema (+40% AI visibility)
4. All pages: Missing BreadcrumbList schema
5. All pages: Missing SpeakableSpecification

## Implementation

Add JSON-LD in a `<script type="application/ld+json">` tag. Place it in
the `<head>` or at the end of `<body>`.

### Organization Schema (homepage)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[COMPANY_NAME]",
  "url": "[SITE_URL]",
  "logo": "[LOGO_URL]",
  "description": "[COMPANY_DESCRIPTION]",
  "sameAs": [
    "[TWITTER_URL]",
    "[GITHUB_URL]",
    "[LINKEDIN_URL]"
  ]
}
```

### FAQPage Schema (FAQ sections)
For each question/answer pair already on the page, wrap them in FAQPage schema:
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

### Article Schema (blog posts)
Include author, datePublished, dateModified, publisher, and headline.

### WebPage with SpeakableSpecification
Add to key pages so AI/voice assistants know which content to extract:
```json
{
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".summary", ".faq-answer"]
  }
}
```

## Validation
Test each page at: https://search.google.com/test/rich-results
```

---

## Template 3: robots.txt Fix

Use when: AI crawlers are blocked or robots.txt needs updating.

```markdown
---
description: "Update robots.txt for AI crawler access on [DOMAIN]"
agent: "agent"
tools: ["editFiles", "codebase"]
---

# Fix robots.txt for AI Crawler Access

You are an SEO and AI visibility expert. Update the robots.txt file for
[DOMAIN] to allow AI search engine crawlers.

## Current Problem

[DESCRIBE ISSUE, e.g.:]
- robots.txt blocks GPTBot (ChatGPT cannot cite this site)
- robots.txt has no rules for AI crawlers (they may be blocked by default)
- ClaudeBot is explicitly disallowed

## Required robots.txt Content

Add the following rules to robots.txt. Keep all existing rules for
Googlebot, Bingbot, and other traditional crawlers. Add these AI bot rules:

```
# AI Search Engine Crawlers (allow for citation visibility)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

# Sitemap
Sitemap: [SITEMAP_URL]
```

## Important Notes
- Do NOT remove existing Googlebot/Bingbot Allow rules
- Do NOT add Crawl-delay for AI bots (most don't respect it; use server-side rate limiting instead)
- If using Cloudflare or a WAF, verify AI bot user agents aren't being blocked at the firewall level
```

---

## Template 4: llms.txt Creation

Use when: the site has no llms.txt file (AI discovery file).

```markdown
---
description: "Create llms.txt file for [DOMAIN]"
agent: "agent"
tools: ["editFiles", "codebase"]
---

# Create llms.txt File

You are an AI visibility and SEO expert. Create an llms.txt file for
[DOMAIN] to help AI systems understand the site's purpose and content.

## What is llms.txt?

llms.txt is a plain-text markdown file at the site root that provides
structured context to LLMs. Sites with llms.txt see ~35% increase in
AI search visibility.

## Create the File

Create `llms.txt` in the site root (same directory as robots.txt).
It should be served at `https://[DOMAIN]/llms.txt` with content type
`text/plain; charset=utf-8`.

## Content Template

```markdown
# [COMPANY/PROJECT NAME]

> [1-3 sentence summary: what the company does, who it serves, core value.]

## Contact

- Website: [URL]
- Email: [EMAIL]
- Support: [SUPPORT_EMAIL]

## Services

- [Service 1]: [Brief description]
- [Service 2]: [Brief description]
- [Service 3]: [Brief description]

## What We Do Not Do

- [Exclusion 1]
- [Exclusion 2]

## Key Information

- [Page Name](URL): [What this page covers]
- [Docs](URL): [Description]
- [Pricing](URL): [Description]
- [Blog](URL): [Description]
```

## Requirements
- UTF-8 encoding
- Unix-style line endings (LF)
- Under 50KB
- CommonMark-compatible Markdown
- Must have H1 heading and blockquote summary
- Must have ## Contact section

## Deployment
Ensure your web server/framework serves this file at the root path.
For Next.js: place in `public/llms.txt`.
For WordPress: upload via FTP or use a plugin.
For static sites: place in the root build directory.
```

---

## Template 5: Content Structure Optimization

Use when: content lacks answer-first format, proper headings, or extractable structure.

```markdown
---
description: "Optimize content structure for SEO and AI citation on [DOMAIN]"
agent: "agent"
tools: ["editFiles", "codebase", "search"]
---

# Optimize Content Structure for AI Citations

You are a content optimization expert specializing in GEO (Generative
Engine Optimization). Restructure content on [DOMAIN] to maximize both
traditional search rankings and AI citation likelihood.

## Pages to Optimize

[LIST PAGES AND THEIR ISSUES, e.g.:]
1. [URL]: No answer capsule, headings don't match questions
2. [URL]: Content buried in long introduction
3. [URL]: No FAQ section, no tables for comparisons

## Optimization Rules

### Answer Capsules (highest impact)
After each question-style H2 heading, add a 40-60 word self-contained
answer that makes sense without any surrounding context.

Example:
```html
<h2>What is [Topic]?</h2>
<p>[Topic] is [clear definition in 40-60 words that directly answers
the question, includes one key statistic or fact, and names a source].</p>
```

### Heading Structure
- Single H1 per page with primary keyword
- H2 headings as questions people would ask
- H3 headings for subtopics under each H2
- No heading level skips (H1 > H2 > H3)

### Content Formatting
- Short paragraphs (2-3 sentences max)
- Bullet points for lists of items
- Numbered lists for sequential steps
- Tables for comparison data (AI systems extract these directly)
- Bold key terms on first use

### FAQ Section
Add a FAQ section at the bottom with 5-10 questions. Each answer should:
- Start with a direct answer (not "Well, it depends...")
- Be 2-4 sentences
- Include at least one specific data point or source
- Be self-contained

### Statistics and Citations
- Add sourced statistics: "[Claim] (Source, Year)"
- Include at least 2-3 citations per major section
- Prefer primary sources (research, official docs) over secondary blogs

## Do NOT
- Stuff keywords unnaturally (causes -9% AI visibility)
- Use AI writing cliches (see ai-writing-detection.md)
- Write long introductions before giving the answer
- Use vague claims without data ("many experts believe...")
```

---

## Template 6: E-E-A-T Enhancement

Use when: content lacks author credentials, expertise signals, or trust indicators.

```markdown
---
description: "Add E-E-A-T signals to [DOMAIN]"
agent: "agent"
tools: ["editFiles", "codebase", "search"]
---

# Enhance E-E-A-T Signals

You are an SEO expert focused on E-E-A-T (Experience, Expertise,
Authoritativeness, Trustworthiness). Add trust signals to [DOMAIN].

## What's Missing

[LIST ISSUES, e.g.:]
1. No author bios on blog posts
2. About page lacks company credentials
3. No datePublished/dateModified on content
4. No contact information visible
5. Missing trust indicators (testimonials, certifications)

## Fixes

### Author Bios
Add an author section to each blog post/article:
```html
<div class="author-bio">
  <img src="[AUTHOR_PHOTO]" alt="[AUTHOR_NAME]">
  <div>
    <strong>[AUTHOR_NAME]</strong>
    <p>[JOB_TITLE] at [COMPANY]. [RELEVANT_CREDENTIALS].
    [X] years of experience in [FIELD].</p>
    <a href="[LINKEDIN_URL]">LinkedIn</a>
  </div>
</div>
```

Also add Person schema:
```json
{
  "@type": "Person",
  "name": "[AUTHOR_NAME]",
  "jobTitle": "[JOB_TITLE]",
  "worksFor": {"@type": "Organization", "name": "[COMPANY]"},
  "url": "[AUTHOR_PAGE_URL]"
}
```

### Content Dates
Add visible publish and update dates to all content pages:
```html
<time datetime="2026-03-20">Published: March 20, 2026</time>
<time datetime="2026-03-20">Last updated: March 20, 2026</time>
```

### About Page
Ensure the about page includes:
- Company history and founding date
- Team credentials and expertise
- Mission statement
- Physical address or location
- Contact information

### Trust Signals
- Add customer testimonials with names and companies
- Show certifications, awards, or media mentions
- Include privacy policy and terms of service links in footer
- Display security badges if handling payments

## Validation
- Check that author bios appear on all blog posts
- Verify dates are visible and current
- Test Person schema at: https://search.google.com/test/rich-results
```

---

## Combining Templates

When an audit reveals multiple issue categories, combine the relevant
templates into a single prompt. Structure as:

```markdown
---
description: "Fix SEO and AI visibility issues on [DOMAIN]"
agent: "agent"
tools: ["editFiles", "codebase", "search", "fetch"]
---

# Fix SEO & AI Visibility Issues on [DOMAIN]

You are an SEO and GEO optimization expert. Fix all issues found in
the audit below.

## Issue Category 1: [e.g., Meta Tags]
[Paste relevant section from Template 1]

## Issue Category 2: [e.g., Schema Markup]
[Paste relevant section from Template 2]

## Issue Category 3: [e.g., Content Structure]
[Paste relevant section from Template 5]

## Validation
[Combined validation steps]
```
