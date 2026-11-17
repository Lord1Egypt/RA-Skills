## Description:

股票研究专家研木的Skill - 将DCF和Comps分析结果生成专业券商研报（PDF或Word）

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and finance-focused agents use this skill to turn financial data, DCF valuation outputs, comparable-company analysis, and optional charts into Chinese-language equity research reports in PDF or Word format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated investment ratings or conclusions may be misleading if the supplied valuation data is incomplete or inaccurate.

Mitigation: Review the input data, valuation assumptions, and final investment conclusions before relying on or distributing generated reports.

Risk: Unpinned report-generation dependencies may behave differently across environments.

Mitigation: Install dependencies in an isolated virtual environment and pin fpdf2 and python-docx for repeatable report generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yanmu-report-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/caoling7878-arch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands for generating PDF or Word report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports depend on user-provided financial, DCF, comps, and optional chart inputs.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
