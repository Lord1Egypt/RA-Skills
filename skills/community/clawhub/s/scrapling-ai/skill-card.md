## Description:

Use Scrapling to scrape websites with adaptive parsing, Cloudflare bypass, MCP support, dynamic content handling, anti-bot detection, and clean HTML/JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanpaidashi](https://clawhub.ai/user/nanpaidashi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scrape static or dynamic web pages, extract structured HTML or JSON, and configure Scrapling CLI or MCP workflows for sites they are allowed to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent access to a general-purpose web scraping tool with network access.

Mitigation: Use it only for sites the user is allowed to access, and avoid internal or localhost URLs unless that access is intended.

Risk: Anti-bot and Cloudflare bypass behavior can be sensitive in production workflows.

Mitigation: Confirm the target site's authorization, terms, and rate limits before using bypass features.

Risk: Headers, credentials, or other sensitive values could be exposed through scraping commands.

Mitigation: Do not pass sensitive headers or credentials unless strictly required and approved for the target site.

Risk: The skill depends on installing and executing the third-party Scrapling package and can start an MCP server.

Mitigation: Pin or review the Scrapling package before installation where possible, and enable MCP access only in trusted agent environments.

Risk: Scraped pages and files originate from remote sites and may contain untrusted content.

Mitigation: Treat scraped output as untrusted remote content and review it before using it in downstream workflows.

## Reference(s):

- [Scrapling AI ClawHub skill page](https://clawhub.ai/nanpaidashi/skills/scrapling-ai)
- [nanpaidashi publisher profile](https://clawhub.ai/user/nanpaidashi)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown, Code]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of scraped HTML, JSON, or text files through Scrapling CLI commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
