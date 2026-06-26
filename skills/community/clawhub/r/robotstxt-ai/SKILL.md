---
name: robots-ai
description: Analyze and generate robots.txt files with AI crawler awareness. Detect which AI bots (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) are blocked or allowed on any website.
---

# robots-ai

Analyze, audit, and generate robots.txt files with full awareness of 20+ AI crawlers.

## Capabilities

- **Analyze** any website's robots.txt to see which AI bots are blocked/allowed
- **Generate** a robots.txt with toggleable AI bot blocking
- **Audit** existing robots.txt for completeness and issues
- **List** all known AI crawlers with their user-agents, companies, and documentation links

## AI Bots Database

You know about these AI crawlers and their user-agents:

| Bot | User-Agent | Company | Type |
|-----|-----------|---------|------|
| GPTBot | GPTBot | OpenAI | AI Crawler |
| ChatGPT-User | ChatGPT-User | OpenAI | AI Search |
| OAI-SearchBot | OAI-SearchBot | OpenAI | AI Search |
| ClaudeBot | ClaudeBot | Anthropic | AI Crawler |
| anthropic-ai | anthropic-ai | Anthropic | AI Crawler |
| Google-Extended | Google-Extended | Google | AI Crawler |
| PerplexityBot | PerplexityBot | Perplexity | AI Search |
| CCBot | CCBot | Common Crawl | AI Crawler |
| Bytespider | Bytespider | ByteDance | AI Crawler |
| Diffbot | Diffbot | Diffbot | AI Crawler |
| cohere-ai | cohere-ai | Cohere | AI Crawler |
| Amazonbot | Amazonbot | Amazon | AI Crawler |
| Meta-ExternalAgent | Meta-ExternalAgent | Meta | AI Crawler |
| Meta-ExternalFetcher | Meta-ExternalFetcher | Meta | AI Crawler |
| Applebot-Extended | Applebot-Extended | Apple | AI Crawler |
| YouBot | YouBot | You.com | AI Search |
| Timpibot | Timpibot | Timpi | AI Crawler |
| img2dataset | img2dataset | Open Source | AI Crawler |

## Important Notes

- **Google-Extended** controls Gemini training access but does NOT affect Google Search indexing
- **Blocking Googlebot** removes the site from Google Search entirely — never do this unless explicitly asked
- **CCBot** feeds Common Crawl, which is used by many AI companies for training data
- **Bytespider** (ByteDance) and **Timpibot** are commonly blocked by default due to aggressive crawling

## How to Analyze

When asked to analyze a robots.txt:
1. Fetch the robots.txt from the URL (append /robots.txt if not included)
2. Parse all User-agent directives and their Allow/Disallow rules
3. Check each AI bot against the rules
4. Report: which bots are blocked, which are allowed, and any issues found
5. Suggest improvements if relevant

## How to Generate

When asked to generate a robots.txt:
1. Ask which AI bots to block (or accept "block all AI" / "allow all AI")
2. Ask for sitemap URL(s)
3. Ask for any custom rules (e.g., Disallow: /admin/)
4. Generate clean robots.txt with comments explaining each section
5. Always include `User-agent: *` with `Allow: /` as the default
6. Group blocked AI bots together with comments
7. Add sitemap directives at the end

## Output Format

Always format the generated robots.txt in a code block with syntax highlighting. Add comments explaining what each section does. Example:

```
# Allow all crawlers by default
User-agent: *
Allow: /

# Block AI training crawlers
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

# Sitemap
Sitemap: https://example.com/sitemap.xml
```
