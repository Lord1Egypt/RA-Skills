## Description: <br>
盘口变化监控助手 - 实时监控足球、篮球等体育赛事的亚盘、欧赔、大小球盘口变化。检测异常波动、大额注单信号、机构态度转变。支持多平台对比、历史趋势分析、自动预警通知。当用户需要监控盘口变化、追踪赔率走势、发现投注机会时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to monitor sports betting odds and line movements, compare bookmaker changes, and generate alerts or reports for market volatility. It is intended as a data-monitoring aid, not as a substitute for human judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evidence security summary reports direct billing code that can charge a user identifier through an external payment service without a clear per-run approval flow. <br>
Mitigation: Install only if the publisher and billing provider are trusted, review billing terms before use, and control or sandbox SkillPay-related environment variables and network access. <br>
Risk: The skill can transmit a SkillPay user identifier to an external billing service and may incur USDT charges. <br>
Mitigation: Keep SkillPay user configuration unset unless paid use is intended, and run the skill in an environment where outbound billing calls can be reviewed or blocked. <br>
Risk: Odds movement reports and detected market signals may be incomplete or misleading if source data is unavailable, delayed, or interpreted without broader context. <br>
Mitigation: Treat outputs as monitoring signals only, verify data sources independently, and require human review before making betting or financial decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shenmeng/shenmeng-odds-monitor-2025) <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/text monitoring reports with console alerts, shell commands, and JSON or SQLite-backed odds data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live monitoring requires an odds API key; billing behavior may depend on SkillPay-related environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release.version, artifact _meta.json and config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
