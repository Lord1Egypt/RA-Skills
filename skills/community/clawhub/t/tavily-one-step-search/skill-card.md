## Description:

Adds Tavily-powered real-time web search, page extraction, crawling, and site mapping to OpenClaw, with guided API key setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plabzzxx](https://clawhub.ai/user/plabzzxx)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to run Tavily web searches, extract page content, crawl documentation sites, and map site URLs from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow asks the agent to persistently prefer Tavily for future general web searches.

Mitigation: Add that persistent preference only when the user explicitly wants future general searches routed through Tavily.

Risk: The installation flow clones mutable code from GitHub.

Mitigation: Install from a pinned commit or verified release and review the release before use.

Risk: The skill requires a Tavily API key in the local environment.

Mitigation: Keep the API key in a trusted local environment file and avoid sending the secret through chat.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/plabzzxx/skills/tavily-one-step-search)
- [Tavily](https://tavily.com)
- [Tavily documentation](https://docs.tavily.com)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY in the environment or ~/.openclaw/.env; results may include external web content.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
