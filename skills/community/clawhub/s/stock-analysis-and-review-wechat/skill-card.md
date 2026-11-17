## Description:

Provides a Chinese-language workflow for stock market review, portfolio profit and loss checks, position-building evaluation, financial-news review, scheduled OpenClaw tasks, and WeChat report delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cavillie-crypto](https://clawhub.ai/user/cavillie-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal investors use this skill to produce daily stock-review reports, monitor holdings, evaluate buy or sell conditions, and send concise reports through WeChat. Developers can also use the included scripts and references as examples for Tencent/Sina market data retrieval, portfolio-report formatting, OpenClaw cron scheduling, and WeChat delivery setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring OpenClaw cron tasks may repeatedly process portfolio data and send reports after the user no longer needs monitoring.

Mitigation: Confirm each task name, schedule, target agent, and report cadence before enabling automation; prefer one-time reports unless recurring monitoring is intentional, and remove stale tasks.

Risk: Reports may be sent to the wrong WeChat recipient or account if delivery fields are misconfigured.

Mitigation: Verify the WeChat recipient, account ID, plugin authorization, and delivery mode before enabling scheduled delivery or sending a report.

Risk: Automated reviews may update memory with stale or incorrect portfolio state.

Mitigation: Review memory-write behavior and validate holdings, prices, and alert thresholds before allowing the workflow to update persistent notes.

Risk: Stock review output can be mistaken for investment advice.

Mitigation: Treat the generated analysis as decision-support material only and require human review before trading or portfolio changes.

## Reference(s):

- [Position Building Reference](references/position_building.md)
- [Stock Review Technical Guide](references/technical_guide.md)
- [WeChat Push Integration Guide](references/wechat_push.md)
- [Tencent Finance API](https://qt.gtimg.cn/)
- [Sina Finance API](https://hq.sinajs.cn/)
- [Eastmoney](https://www.eastmoney.com/)
- [OpenClaw Cron Documentation](https://docs.openclaw.ai/cron)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON examples, Python code, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include market data, portfolio calculations, cron task commands, WeChat delivery configuration, and investment-risk reminders.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
