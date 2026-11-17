## Description:

简历-JD匹配度5维度评分技能。输入简历文本和目标JD，自动提取关键词、交叉匹配、5维评分，并生成交互式HTML报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate how well a resume matches a target job description, inspect five scoring dimensions and keyword matches, and generate reports with prioritized improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute injected content when built from untrusted or externally modified score JSON.

Mitigation: Use trusted resume and JD inputs, and avoid opening generated HTML from untrusted score JSON until HTML escaping and CSP protections are fixed.

Risk: Optional web lookup may send job-query data externally.

Mitigation: Do not allow web search or fetch unless the user is comfortable sharing the job-query data with external services.

Risk: Generated report files can contain personal career information.

Mitigation: Treat score JSON, HTML, and Markdown reports as sensitive files and limit storage or sharing accordingly.

## Reference(s):

- [Scoring Rubric](references/scoring-rubric.md)
- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/resume-jd-scorer)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON scoring data plus HTML and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can contain sensitive resume and job-description information.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
