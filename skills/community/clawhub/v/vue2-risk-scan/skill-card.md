## Description:

Skill 用于自动扫描 Vue2 项目的潜在风险，覆盖依赖安全、Webpack 配置风险和 Babel 配置问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gfrxf](https://clawhub.ai/user/gfrxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run lightweight checks on Vue2 projects during local development, CI review, or agent-assisted diagnosis. It helps identify dependency security issues, Webpack configuration risks, and Babel configuration problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan is a lightweight helper and may miss issues that a full Vue2 security audit or CI security program would catch.

Mitigation: Review the results manually and pair the skill with broader dependency, configuration, and CI security tooling before using findings for release decisions.

Risk: The dependency check may run npm audit against the npm registry.

Mitigation: Run the skill in an environment where registry access is expected and where local package data can be reviewed safely.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gfrxf/skills/vue2-risk-scan)
- [Publisher profile](https://clawhub.ai/user/gfrxf)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with shell command examples and scan findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports high and medium risk counts from dependency, Webpack, and Babel checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
