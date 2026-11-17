## Description:

财报可视化分析 helps agents analyze financial report data and generate structured visual outputs such as SVG mini charts, radar charts, and multi-format reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance teams can use this skill to analyze financial report content, extract key financial indicators, and produce chart-oriented report outputs. It is intended for financial analysis, reporting, statistical insight, and visualization workflows rather than real-time stream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses read and exec authority for financial data analysis workflows.

Mitigation: Review proposed commands before execution and install only when the agent should have that authority for the target workspace.

Risk: The skill may use API-keyed financial data sources and sensitive financial inputs.

Mitigation: Configure API keys through controlled environment variables and avoid providing confidential internal financial data unless the external data flow has been approved.

Risk: Security claims in the artifact are not fully supported by the security summary, which marks the release suspicious.

Mitigation: Treat security and performance claims as unverified until reviewed, and follow the server security guidance before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/report-viz-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown and JSON-style structured results, with possible chart or report file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe SVG mini charts, radar charts, PDF or Word report outputs, and API-key configuration steps.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact/SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
