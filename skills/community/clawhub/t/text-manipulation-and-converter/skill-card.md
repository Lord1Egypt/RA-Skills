## Description:

Text Manipulation and Converter helps agents clean, transform, convert, sort, deduplicate, wrap, quote, and count text through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external agents use this skill to normalize text, convert naming conventions, format lists, add quotes, wrap or unwrap content, and compute line, word, and character counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text is processed by AgentPMT's remote service.

Mitigation: Do not send secrets, credentials, regulated data, confidential logs, customer records, or proprietary source unless remote processing is approved.

Risk: Optional setup guidance includes unpinned skills.sh commands.

Mitigation: Prefer pinned or trusted installation paths for related setup skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/text-manipulation-and-converter)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/text-manipulation-and-converter)
- [Action Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text, JSON call examples, Markdown guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote tool responses may include original text length, result length, validation warnings, or structured character statistics depending on the action.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
