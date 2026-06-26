## Description: <br>
盘口变化监控助手，用于实时监控足球、篮球等体育赛事的亚盘、欧赔、大小球盘口变化，并识别异常波动、大额注单信号和机构态度转变。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sports odds analysts, bettors, and risk-control users can use this skill to monitor line movement, compare market changes, detect abnormal odds signals, and generate monitoring reports. Its outputs are for data monitoring and should not be treated as guaranteed betting advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SkillPay billing can charge a USDT balance without clear per-use confirmation. <br>
Mitigation: Require explicit user confirmation before each paid call and configure billing limits before enabling repeated or autonomous runs. <br>
Risk: ODDS_API_KEY and SKILLPAY_USER_ID are sensitive, and the artifact includes a hard-coded billing key. <br>
Mitigation: Use platform-managed secrets, rotate exposed keys, and prefer a release that removes hard-coded billing credentials. <br>
Risk: Continuous monitoring or automated intervals could trigger repeated paid invocations. <br>
Mitigation: Set conservative monitoring intervals, enforce maximum charge counts, and stop monitoring when the intended event window ends. <br>
Risk: Unpinned dependencies may change behavior across installations. <br>
Mitigation: Pin and review dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-odds-monitor-v3) <br>
- [Publisher profile](https://clawhub.ai/user/shenmeng) <br>
- [The Odds API](https://the-odds-api.com/) <br>
- [The Odds API v4 endpoint](https://api.the-odds-api.com/v4) <br>
- [SkillPay billing provider](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text monitoring reports with command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require ODDS_API_KEY and SKILLPAY_USER_ID environment variables, may call external odds and billing services, and may store odds snapshots in SQLite.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact metadata, and package __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
