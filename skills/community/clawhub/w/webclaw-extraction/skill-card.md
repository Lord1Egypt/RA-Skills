## Description:

Web extraction for LLMs and agents. Scrape, crawl, map, search, extract, summarize, diff, monitor, and research any URL into clean Markdown, text, or JSON, including pages that block bots or render with JavaScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmassi](https://clawhub.ai/user/0xmassi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use webclaw to retrieve, crawl, search, monitor, summarize, and structure web content for agent workflows when basic web fetching is unreliable or insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud API calls and cloud fallback can transmit target URLs, page contents, research prompts, and monitor or webhook details to WebClaw.

Mitigation: Use only for data you are comfortable sending to the remote service, and avoid confidential, regulated, or private-network targets.

Risk: Backend-discovery and bot-protection examples could be misused against third-party systems.

Mitigation: Run endpoint discovery, bypass-oriented extraction, research, and monitoring only on systems where you have explicit authorization.

Risk: The MCP install path is unpinned in the release metadata.

Mitigation: Prefer a pinned install source or reviewed package version before deploying the MCP component.

## Reference(s):

- [WebClaw homepage](https://webclaw.io)
- [WebClaw API base](https://api.webclaw.io/v1/)
- [ClawHub skill page](https://clawhub.ai/0xmassi/skills/webclaw-extraction)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown, plain text, JSON, and command guidance for web extraction workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require WEBCLAW_API_KEY for cloud API calls; direct API and cloud fallback send requested URLs and extraction prompts to WebClaw.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
