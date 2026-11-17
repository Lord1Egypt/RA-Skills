## Description:

Scrape web pages using Scrapling with HTTP requests, stealth browsers, JavaScript rendering, browser actions, API response capture, concurrent spiders, and adaptive parsing. Use when asked to scrape, crawl, or extract data from websites; web_fetch fails; the site has anti-bot protections; write Python code to scrape/crawl; or write spiders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d4vinci](https://clawhub.ai/user/d4vinci)

### License/Terms of Use:

BSD 3-Clause

## Use Case:

Developers and engineers use this skill to write Python code and shell commands for fetching, parsing, and crawling websites with Scrapling. It supports static pages, JavaScript-rendered pages, and multi-page crawls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser login files and captured traffic may contain credentials.

Mitigation: Use a dedicated browser context; keep these files private, exclude them from commits and uploads, and remove them when finished.

Risk: Untrusted proxies or scraping requests that change remote data can expose users to avoidable security or operational risks.

Mitigation: Choose trusted proxies and authorize any requests that modify remote data.

Risk: Scraping sites without permission or ignoring their access rules can violate site terms or expose sensitive personal data.

Mitigation: Scrape only authorized content, respect robots.txt and terms of service, and do not scrape personal or sensitive data.

## Reference(s):

- [Scrapling Documentation](https://scrapling.readthedocs.io/en/latest/index.html)
- [ClawHub release page](https://clawhub.ai/d4vinci/skills/scrapling-official)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.5.1 (source: SKILL.md frontmatter; target release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
