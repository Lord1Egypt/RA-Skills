## Description:

Use the ScrapingBee CLI to retrieve web pages, search results, crawls, and structured data from websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapingbee-integrations](https://clawhub.ai/user/scrapingbee-integrations)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the skill to read and search websites, crawl sites, and collect structured web data through ScrapingBee.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs, queries, prompts, cookies, and headers may contain sensitive information sent to ScrapingBee.

Mitigation: Use public or approved inputs and protect the stored API key.

Risk: Large crawls, batches, recurring jobs, and shell hooks can incur costs or perform unintended actions.

Mitigation: Bound crawl size and spending, and deliberately authorize recurring jobs and shell hooks.

Risk: The external CLI code was not included, and the optional pipeline-agent file is missing.

Mitigation: Review the CLI and inspect any replacement pipeline-agent file before copying it into a project.

## Reference(s):

- [ScrapingBee CLI ClawHub release](https://clawhub.ai/scrapingbee-integrations/skills/scrapingbee-cli)
- [Scraping and extraction guide](reference/scrape/overview.md)
- [Crawling guide](reference/crawl/overview.md)
- [Batch processing guide](reference/batch/overview.md)
- [Security and safety guidance](rules/security.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Files, Shell commands, Configuration instructions]

**Output Format:** [Text, JSON, Markdown, and optional saved files such as HTML, CSV, or screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be filtered, extracted, batched, crawled, or saved to files.]

## Skill Version(s):

1.6.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
