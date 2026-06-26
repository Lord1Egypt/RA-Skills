## Description: <br>
Helps personal investors review A-share, Hong Kong, and U.S. stock holdings, fetch market data, calculate portfolio profit and loss, format review reports, configure scheduled OpenClaw tasks, and prepare WeChat delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cavillie-crypto](https://clawhub.ai/user/cavillie-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal investors use this skill to generate daily post-market portfolio reviews, assess buy or add-position conditions, summarize market context, and send concise reports through WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process private portfolio details and send recurring reports to WeChat. <br>
Mitigation: Confirm report contents, destination account, and WeChat delivery configuration with harmless test messages before enabling automation. <br>
Risk: Scheduled market reports may keep running after they are no longer needed. <br>
Mitigation: Review cron schedules regularly and remove automated tasks when reports are no longer required. <br>
Risk: Stock analysis output may be incomplete, stale, or unsuitable as investment advice. <br>
Mitigation: Treat generated reviews as decision support only and verify market data, assumptions, and trade decisions independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cavillie-crypto/stock-analysis-and-review-wechat) <br>
- [Position building guide](references/position_building.md) <br>
- [Technical guide](references/technical_guide.md) <br>
- [WeChat push guide](references/wechat_push.md) <br>
- [Tencent Finance quote API](https://qt.gtimg.cn/) <br>
- [Sina Finance quote API](https://hq.sinajs.cn/) <br>
- [OpenClaw cron documentation](https://docs.openclaw.ai/cron) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON configuration, Python helper output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include scheduled task setup, WeChat-friendly report formatting, and portfolio review guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
