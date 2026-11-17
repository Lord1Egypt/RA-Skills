## Description:

Scout Anti-Crawl v3 helps agents fetch web pages and WeChat search results through a layered fallback strategy for static pages, browser-rendered pages, anti-bot challenges, proxy-backed cloud scraping, and AI-assisted extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garisonli](https://clawhub.ai/user/garisonli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to fetch difficult web content, extract readable text, save fetched output, and search WeChat articles when standard HTTP retrieval is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs, search terms, and fetched page content may be sent through a local proxy and third-party scraping or search services.

Mitigation: Avoid private, internal, signed, token-bearing, or regulated URLs unless proxy and cloud fallback behavior is explicitly disabled or controlled.

Risk: The artifact includes an embedded Olostep API credential.

Mitigation: Remove or rotate the embedded credential before use and supply credentials through an approved secret-management path.

Risk: The skill is designed to bypass anti-crawl controls and may be inappropriate for unauthorized targets.

Mitigation: Use only on targets where crawling is authorized and review site, contractual, and policy restrictions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/garisonli/skills/scout-anti-crawl)
- [Olostep](https://olostep.com)
- [Scrapling](https://github.com/D4Vinci/Scrapling)
- [Firecrawl](https://github.com/firecrawl/firecrawl)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands]

**Output Format:** [Plain text, Markdown, JSON-like dictionaries, or saved HTML/text files depending on command options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May truncate extracted text in CLI output and may use local proxy or third-party cloud scraping fallbacks.]

## Skill Version(s):

3.0.0 (source: frontmatter, skill.json, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
