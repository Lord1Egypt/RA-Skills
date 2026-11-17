## Description:

自媒体矩阵管家虾 helps agents monitor multi-account social-media operations, analyze engagement and account health, detect viral or declining accounts, and generate concise daily Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

External social-media operators and content teams use this skill to summarize multi-platform account metrics, detect anomalies such as viral spikes, traffic decline, account risk, or negative sentiment, and prepare daily reports or scheduling suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may expose social-media account metrics, account IDs, operational notes, or account-risk details when shared externally.

Mitigation: Review Markdown reports before sending them to Feishu or group chats, and remove account IDs or sensitive risk notes that unintended recipients should not see.

Risk: CSV data from collaborators or external sources may include sensitive or inaccurate operational data.

Mitigation: Use the skill only with data sources you are comfortable processing, and verify report content before treating it as an operational decision record.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/social-matrix-manager-claw)
- [平台数据指标手册](references/platform-metrics.md)
- [内容分类与标签体系](references/content-taxonomy.md)
- [舆情关键词库](references/sentiment-keywords.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports and concise guidance, with optional shell commands for CSV analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a report file when the bundled analysis script is run with an output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
