## Description:

Firecrawl CLI for web scraping, crawling, and search, with support for extracting web content as clean Markdown and summarizing URLs or files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilianglin100-sketch](https://clawhub.ai/user/weilianglin100-sketch)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and researchers use this skill to search, scrape, crawl, map, and summarize web content for research, documentation extraction, market analysis, competitor monitoring, and news review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends target URLs and extracted content to external services such as Firecrawl and, for summarization workflows, AI providers or Apify.

Mitigation: Use it only for material approved for those services, and avoid confidential, internal, regulated, or proprietary content unless policy permits it.

Risk: The documented batch command pattern can execute shell commands over untrusted URL lists.

Mitigation: Review URL lists before batch execution, avoid running the xargs/sh example on untrusted input, and prefer constrained, quoted command construction.

Risk: Installation and authentication examples can encourage global installs and shell-profile API key storage.

Mitigation: Prefer pinned or local installs, avoid sudo npm install, and store API keys in a proper secret manager.

## Reference(s):

- [Web Researcher Mini ClawHub Page](https://clawhub.ai/weilianglin100-sketch/skills/web-researcher-mini)
- [Summarize CLI](https://summarize.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can direct agents to write scraped, searched, crawled, mapped, or summarized web content to local output files.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
