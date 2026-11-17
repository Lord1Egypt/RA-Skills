## Description:

ScholarPlot AI Academic Figure Generator connects via MCP to generate and edit SCI-standard figures, including line charts, bar charts, heatmaps, neural network architectures, and experimental flowcharts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peizhou](https://clawhub.ai/user/peizhou)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and MCP-compatible agent users use this skill to generate or edit academic figures from natural language prompts, structured chart data, or figure edit instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Figure descriptions, edit instructions, and provided data values are sent to the remote figure.thirdme.com service.

Mitigation: Avoid submitting confidential manuscripts, patient data, proprietary datasets, or unpublished results until the provider's privacy and retention commitments are reviewed.

Risk: The MCP server URL embeds an API key that is tied to subscription usage and quota.

Mitigation: Keep MCP configuration files private, do not share the full configured URL, and rotate the API key if it is exposed in logs or public repositories.

## Reference(s):

- [ScholarPlot MCP Documentation](https://figure.thirdme.com/mcp)
- [ScholarPlot Website](https://figure.thirdme.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with figure URLs, metadata summaries, optional editable figure code, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated figures may be available as 300dpi images or SVG vector output through the remote ScholarPlot service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
