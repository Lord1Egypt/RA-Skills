## Description:

网页抓取引擎 helps agents plan and generate web scraping workflows with Firecrawl, Playwright, and Crawl4AI for search, page extraction, batch crawling, browser interaction, and data export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation teams use this skill to design web scraping and browser automation workflows for competitive analysis, price monitoring, lead generation, market research, content collection, and structured extraction. It is best suited to authorized, batch-oriented collection from websites where target terms, robots.txt, and data handling requirements can be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags under-scoped guidance around login tokens, proxy rotation, and stealth scraping.

Mitigation: Use the skill only for authorized targets, avoid private or login-protected data unless explicitly permitted, and do not use stealth or proxy rotation to bypass site restrictions.

Risk: Generated scraping scripts may run code, write files, upload data, or use API keys and cookies.

Mitigation: Review generated scripts before execution, store keys and tokens only in environment variables, redact sensitive output, and run commands in an appropriate sandbox.

Risk: Web scraping can violate target site terms, robots.txt, copyright, or privacy expectations.

Mitigation: Confirm authorization for each target site, respect rate limits and robots.txt, and define data minimization and retention rules before collecting data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-scraper-engine)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with code blocks, shell commands, configuration notes, and structured data examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scraping scripts, JSON schemas, CSV or JSON export plans, troubleshooting steps, and compliance checks.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
