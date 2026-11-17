## Description:

Use the Scrapfly CLI (`scrapfly`) to scrape web pages, capture screenshots, extract structured data with AI, crawl sites, and drive a cloud browser over CDP from a shell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapfly](https://clawhub.ai/user/scrapfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to operate Scrapfly's CLI for web scraping, screenshots, AI extraction, crawling, browser automation, account alerting, scheduling, and MCP tool serving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent browser sessions and authenticated automation can expose account state when reused across tasks.

Mitigation: Isolate browser sessions per task and close sessions when done.

Risk: API keys, LLM provider credentials, and webhook destinations can leak through prompts, logs, or uncontrolled delivery endpoints.

Mitigation: Keep API keys out of prompts and logs, and configure webhooks only to destinations you control.

Risk: Mutable CLI installs can change behavior after review.

Mitigation: Use a pinned and verified Scrapfly CLI release before using real accounts, authenticated browser sessions, webhooks, schedules, or the BYOP connector.

## Reference(s):

- [Scrapfly Documentation](https://scrapfly.io/docs)
- [Scrapfly SDKs](https://scrapfly.io/docs/sdk)
- [Scrapfly CLI Source and Examples](https://github.com/scrapfly/scrapfly-cli)
- [Scrapfly CLI Releases](https://github.com/scrapfly/scrapfly-cli/releases)
- [ClawHub Skill Page](https://clawhub.ai/scrapfly/skills/scrapfly-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI commands generally return JSON envelopes on stdout, while binary artifacts require an output file or directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
