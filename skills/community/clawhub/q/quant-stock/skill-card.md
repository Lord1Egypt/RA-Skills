## Description: <br>
AI量化选股系统 - 基于多维度评分模型的A股选股分析工具。扫描新能源、电力、半导体、医药、AI、机器人、军工、贵金属等行业，输出每日量化选股报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rix-zhang](https://clawhub.ai/user/rix-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agent operators use this skill to run A-share quantitative stock screening across selected industries and generate a daily ranked report with stock scores, positive signal tags, and a sector summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled scripts can automatically send reports and failure notifications to hardcoded Feishu/OpenClaw chat targets. <br>
Mitigation: Review, replace, or remove embedded chat IDs and messaging targets before running the skill. <br>
Risk: The cron installer can create persistent scheduled execution, and the server evidence flags a missing update_hot.sh reference and schedule mismatch for review. <br>
Mitigation: Inspect scripts/install_cron.sh before use, confirm the intended schedule, and fix or remove missing script references before installing cron jobs. <br>
Risk: Generated stock rankings can be incomplete or misleading if market, news, or stock-pool data is stale or unavailable. <br>
Mitigation: Treat reports as research inputs, verify data sources and outputs independently, and avoid using the report as sole investment advice. <br>


## Reference(s): <br>
- [Quant Stock on ClawHub](https://clawhub.ai/rix-zhang/quant-stock) <br>
- [Scoring Rules](references/RULES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown-style daily stock report with setup and scheduling commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write daily_report.txt and send the report through configured Feishu/OpenClaw targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
