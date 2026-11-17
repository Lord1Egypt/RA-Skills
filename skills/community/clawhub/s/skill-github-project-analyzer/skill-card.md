## Description:

深度分析GitHub项目，输出大白话版项目评估报告；当用户提供GitHub链接或要求分析GitHub项目时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[liderongyao-crypto](https://clawhub.ai/user/liderongyao-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical evaluators use this skill to analyze public GitHub projects and receive a plain-language Chinese Markdown report covering project purpose, audience fit, usability, activity, risks, competitors, and adoption advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the user provides only a project name, the agent may analyze the wrong repository.

Mitigation: Confirm the exact GitHub repository before starting the analysis.

Risk: Project popularity, activity, issue status, and comparisons can become stale or incomplete.

Mitigation: Use current public GitHub and web sources, and verify important decisions against the official repository and documentation.

Risk: The generated report is based on public lookup and document review rather than executing the target project.

Mitigation: Treat installation, testing, and performance sections as evidence-based analysis, then run a hands-on demo before adoption.

## Reference(s):

- [GitHub 项目深度分析 - 详细框架参考](artifact/references/analysis-framework.md)
- [ClawHub skill page](https://clawhub.ai/liderongyao-crypto/skills/skill-github-project-analyzer)

## Skill Output:

**Output Type(s):** [guidance, markdown, analysis]

**Output Format:** [Markdown report in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves a project-specific analysis report under ./GitHub项目分析/ when file output is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
