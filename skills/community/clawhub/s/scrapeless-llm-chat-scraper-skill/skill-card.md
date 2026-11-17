## Description:

Scrape AI chat conversations from ChatGPT, Gemini, Perplexity, Copilot, Google AI Mode, and Grok.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapelesshq](https://clawhub.ai/user/scrapelesshq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI labs, and enterprise teams use this skill to collect structured responses, citations, links, and model metadata from multiple consumer LLM chat services for AI search monitoring, benchmarking, brand intelligence, and workflow automation.

### Deployment Geography for Use:

Global; some model scrapers document Japan (JP) and Taiwan (TW) restrictions.

## Known Risks and Mitigations:

Risk: Prompts and scraper results are sent through Scrapeless, which may be inappropriate for secrets, regulated data, private customer information, or confidential prompts.

Mitigation: Avoid sending sensitive data through the skill and review data-handling requirements before use.

Risk: X_API_TOKEN is required for authentication and could be exposed if environment files or command output are mishandled.

Mitigation: Treat X_API_TOKEN as a secret, keep .env files out of source control, and avoid exposing token-bearing environments in shared terminals or CI logs.

Risk: The artifact uses broad dependency version ranges rather than pinned dependencies or a lockfile.

Mitigation: Pin dependencies or add a reviewed lockfile before deploying in controlled or production environments.

Risk: Prompt content may appear in local or centralized logs during task creation.

Mitigation: Remove or reduce prompt-content logging before use in shared terminals, CI, or centralized logging systems.

## Reference(s):

- [Scrapeless Homepage](https://www.scrapeless.com)
- [Scrapeless LLM Scraper Documentation](https://docs.scrapeless.com/en/llm-chat-scraper/quickstart/introduction/)
- [Scrapeless ChatGPT Scraper Documentation](https://docs.scrapeless.com/en/llm-chat-scraper/scrapers/chatgpt/)
- [Scrapeless Universal Scraping API Documentation](https://docs.scrapeless.com/en/universal-scraping-api/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [JSON responses containing model-specific text or Markdown, citations, links, search results, and task metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X_API_TOKEN. Supports country, web-search, mode, polling interval, and retry options; task results are documented as available for 12 hours.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
