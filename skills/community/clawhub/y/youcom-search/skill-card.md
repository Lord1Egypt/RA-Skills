## Description:

you.com web search, deep research, and content extraction for OpenClaw; basic search is free, while research and extraction require a paid API key and send queries or URLs to You.com and ydc-index.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crabsticksalad](https://clawhub.ai/user/crabsticksalad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to perform You.com web searches, request paid deep research with citations, or extract content from specific URLs when those queries and URLs are appropriate to send to external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and submitted URLs are transmitted to You.com and ydc-index.io.

Mitigation: Do not use the skill with secrets, private or internal URLs, regulated data, sensitive repository content, or other information that should not be sent to those services.

Risk: Research and extraction calls require a paid You.com API key.

Mitigation: Confirm paid research or extraction calls with the user before use and configure YOUCOM_API_KEY only when those endpoints are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crabsticksalad/skills/youcom-search)
- [Publisher profile](https://clawhub.ai/user/crabsticksalad)
- [you.com API Reference](references/api.md)
- [you.com API keys](https://you.com/platform/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON results and Markdown/text guidance with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Basic search needs no API key; research and extraction require YOUCOM_API_KEY and should be confirmed before paid calls.]

## Skill Version(s):

0.1.5 (source: frontmatter, _meta.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
