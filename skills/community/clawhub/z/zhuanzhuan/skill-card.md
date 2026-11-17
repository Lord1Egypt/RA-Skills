## Description:

Zhuanzhuan Assistant helps users buy and sell second-hand goods, search listings, check market prices and trends, estimate resale value from descriptions or images, and access order or logistics pages after connecting the Zhuanzhuan MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuanzhuan-tech](https://clawhub.ai/user/zhuanzhuan-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find second-hand products, compare prices, estimate resale value, route image-based valuation requests, and return concise purchase or recycling guidance through Zhuanzhuan services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security evidence reports a suspicious updater path that can replace local skill instructions from an unsigned remote ZIP while hiding technical details from the user.

Mitigation: Avoid automatic upgrades unless the publisher provides a signed or checksum-pinned release; inspect the downloaded ZIP and SKILL.md before replacing local skill files.

Risk: The skill requires a Zhuanzhuan MCP token for service access and may upload product images supplied by the user for valuation workflows.

Mitigation: Install only when comfortable configuring the MCP token and uploading the intended product images; keep tokens out of replies, logs, and plain-text documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuanzhuan-tech/skills/zhuanzhuan)
- [Publisher profile](https://clawhub.ai/user/zhuanzhuan-tech)
- [Zhuanzhuan MCP setup](https://open.zhuanzhuan.com/mcp?copymcp=1)
- [Zhuanzhuan skill update package](https://sf3329.zhuanstatic.com/2szbuN0pkHL/zhuanzhuan.zip)
- [MCP setup guide](guides/mcp-setup.md)
- [Image upload guide](guides/image-upload.md)
- [Detail display guide](guides/detail-display.md)
- [Skill upgrade guide](guides/skill-upgrade.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text, markdown tables, optional HTML widget fragments, shell commands, and JSON-style configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product, price, valuation, order, logistics, and image-recognition results depend on a configured Zhuanzhuan MCP connection and user-provided inputs.]

## Skill Version(s):

1.5.5 (source: server release evidence; artifact frontmatter reports 1.5.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
