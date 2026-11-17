## Description:

Xiaohongshu Auto Poster helps an agent generate Xiaohongshu post copy from a topic and publish it through a locally configured Xiaohongshu MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmin1113](https://clawhub.ai/user/jmin1113)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, small businesses, and technically capable operators use this skill to draft Xiaohongshu posts, apply content templates, check account status, and publish through a local MCP service after reviewing the generated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external local Xiaohongshu MCP binary that can act on an authenticated social account.

Mitigation: Use the service only when needed, install it only from trusted upstream sources, and verify the binary where possible.

Risk: Generated content may be published before the user notices factual, brand, or platform-policy issues.

Mitigation: Prefer the copy-only preview flow and require human review before any publish action.

Risk: Optional auto-start can keep the local posting service running persistently.

Mitigation: Avoid enabling LaunchAgent auto-start unless required, stop the service when not actively posting, and monitor local service access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jmin1113/skills/xiaohongshu-auto-poster)
- [Xiaohongshu MCP releases](https://github.com/xpzouying/xiaohongshu-mcp/releases)
- [Setup guide](artifact/references/setup.md)
- [Content templates](artifact/references/content-templates.md)
- [Xiaohongshu operations guide](artifact/references/运营知识.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Chinese post copy, command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a local Xiaohongshu MCP service to publish content when configured and authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata, README changelog, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
