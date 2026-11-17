## Description:

Interact with X.com (Twitter) via Tavily web search and extraction to search tweets, extract content from linked URLs, and monitor accounts and topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-wzw](https://clawhub.ai/user/0x-wzw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search X.com content through Tavily, inspect linked pages, and gather social context for account, topic, or thread research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and linked-page URLs may be sent to Tavily.

Mitigation: Use the skill only for content you are comfortable processing through Tavily, and avoid submitting sensitive or private URLs or queries.

Risk: Putting a live Tavily API key directly in a command-line URL can expose it through shell history, logs, or shared terminal output.

Mitigation: Configure the API key through a secret store, environment variable, or other mcporter-supported protected mechanism, and rotate any key that may have been exposed.

## Reference(s):

- [X Interact ClawHub release](https://clawhub.ai/0x-wzw/skills/x-interact)
- [Tavily](https://tavily.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tavily API key and mcporter-compatible MCP tool access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
