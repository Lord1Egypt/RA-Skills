## Description:

ToB销售丢单复盘助手。输入行业/规模/阶段/竞品/关键事件，使用原创销售经验规则引擎输出根因分析、风险信号和改进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[william202404](https://clawhub.ai/user/william202404)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sales teams use this skill to review ToB sales losses from deal context such as industry, account size, sales stage, competitor, and key events. It produces Chinese-language root-cause analysis, risk signals, and practical next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated win/loss analysis may be misleading if treated as a definitive customer truth.

Mitigation: Use the output as advisory input and validate conclusions against customer interviews and deal evidence.

Risk: User-entered deal notes may include sensitive customer details.

Mitigation: Avoid entering sensitive customer details unless local processing is acceptable; redact or generalize customer identifiers before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/william202404/skills/tob-win-loss-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Chinese Markdown report, with optional JSON debug output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline rule-engine output; advisory sales review, not a substitute for customer interviews.]

## Skill Version(s):

2.0.2 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
