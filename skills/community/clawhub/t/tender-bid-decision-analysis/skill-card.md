## Description:

基于招中标历史数据，分析具体项目的投标价值、潜在竞争者、报价参考和投标风险，并生成决策报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

投标团队和企业用户可针对具体招标项目评估是否参与、竞争格局、报价区间及废标风险，并获取带依据的决策报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts the Zhiliaobiaoxun service and may create and store a local API key during registration.

Mitigation: Install only if comfortable with service access and local credential storage; review registration and safeguard the API key.

Risk: Shareable reports can contain signed detail-page links that allow recipients to access vendor pages without logging in.

Mitigation: Share reports only with trusted recipients, or remove signed links before wider distribution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liu-jiapeng/skills/tender-bid-decision-analysis)
- [API quick reference](references/api-quick.md)
- [Registration guide](references/auto-register.md)
- [Analysis workflow](references/workflow.md)
- [Report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML files]

**Output Format:** [Structured Markdown decision report and shareable HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a recommendation, supporting data, pricing range, risks, and linked citations; a full report also produces an HTML file.]

## Skill Version(s):

1.0.7 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
