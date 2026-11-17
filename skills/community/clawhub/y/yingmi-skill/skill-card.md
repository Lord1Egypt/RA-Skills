## Description:

Routes fund, strategy, market news, asset allocation, portfolio diagnosis, risk backtesting, charting, and PDF reporting requests to Yingmi/Qieman data tools and remote workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingmi-soc](https://clawhub.ai/user/yingmi-soc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a local entry point for Yingmi/Qieman finance workflows, including fund lookup, strategy analysis, portfolio diagnosis, wealth planning, financial news, charts, HTML reports, and PDF generation. It helps decide when to call MCP tools directly and when to enter remote scenario skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates important behavior to mutable remote sub-skills.

Mitigation: Before acting inside a remote workflow, list available remote skills, enter the server-reported skill name, and read that remote SKILL.md before executing task steps.

Risk: The workflow asks users to install and update the yingmi-skill-cli package, including possible global or sudo installation paths.

Mitigation: Install only from trusted package sources, avoid sudo or global installation where possible, and confirm the CLI version before invoking MCP or remote-skill commands.

Risk: Initialization can involve phone numbers, SMS verification codes, and API keys.

Mitigation: Treat phone numbers, SMS codes, and API keys as sensitive credentials; request them only when required and avoid exposing them in reports or logs.

Risk: Generated HTML reports can load third-party fonts, scripts, or assets.

Mitigation: Open generated reports with external resource loading enabled only when third-party asset and script loading is acceptable for the environment.

Risk: Financial analysis can become misleading if values are estimated or inferred beyond MCP responses.

Mitigation: Use only MCP-returned or user-provided data for quantitative claims, mark missing data explicitly, and avoid interpolating or inventing chart values.

## Reference(s):

- [CLI precheck workflow](references/CLI前置检查.md)
- [HTML report visual template](references/HTML视觉模板.md)
- [MCP data authenticity requirements](references/MCP数据真实性零容忍.md)
- [Demo report HTML template](references/demo-report.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown guidance with inline bash and JSON examples; may direct agents to produce HTML reports, charts, or PDFs through the referenced tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live MCP tool responses and remote scenario-skill instructions; generated finance reports must use tool-returned or user-provided data.]

## Skill Version(s):

0.1.5 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
