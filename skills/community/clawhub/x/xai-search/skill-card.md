## Description:

Search X/Twitter and the web in real-time using xAI's Grok API with agentic search tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aydencook03](https://clawhub.ai/user/aydencook03)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search the web and X/Twitter through xAI's Grok API for current information, sentiment, and research queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to xAI/Grok and may include sensitive user-provided content.

Mitigation: Avoid confidential, regulated, or secret content in queries unless organizational policy allows use of xAI/Grok for that data.

Risk: The helper script depends on an XAI_API_KEY environment variable and the xai-sdk package.

Mitigation: Use a virtual environment and install a pinned, reviewed xai-sdk version; manage XAI_API_KEY as a secret.

## Reference(s):

- [xAI Documentation](https://docs.x.ai/docs/)
- [xAI Chat Completions API](https://api.x.ai/v1/chat/completions)
- [ClawHub xAI Search Skill](https://clawhub.ai/aydencook03/skills/xai-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text search responses with optional source URLs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY and may call xAI/Grok web_search or x_search tools.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
