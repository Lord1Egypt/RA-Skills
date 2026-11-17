## Description:

This skill uses the configured turing-shikuan-mcp to identify a product image's category, brand, series, and short summary, while excluding authenticity, genuineness, quality, and value judgments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turingsenseai](https://clawhub.ai/user/turingsenseai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure and invoke turing-shikuan-mcp for product-image classification from an accessible image URL. It returns category, brand, series, and a concise product summary in Chinese, and it explicitly avoids authentication or quality assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow configures a third-party MCP endpoint and may install the mcporter npm package.

Mitigation: Confirm trust in the Turing MCP endpoint and mcporter package before setup; use normal user privileges and pin mcporter if tighter supply-chain control is required.

Risk: API credentials are required for MCP setup and could be exposed if written into repository files or committed.

Mitigation: Provide credentials through environment variables or client configuration, and avoid committing real API keys or secrets.

Risk: Product-image classification can be mistaken for authenticity, quality, or value assessment.

Mitigation: Use the skill only for category, brand, series, and summary extraction, and keep the stated disclaimer that results are not authentication conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turingsenseai/skills/turingsenseai-classify-skill)
- [turing-shikuan-mcp endpoint](https://turing-mcp-server-test.turingsenseai.com/mcp)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured Chinese result fields and optional shell or JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid image URL and configured MCP credentials; missing or empty MCP-returned fields are labeled rather than inferred.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
