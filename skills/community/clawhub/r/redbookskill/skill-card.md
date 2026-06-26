## Description: <br>
定时采集小红书果茶/咖啡/健康饮品近24小时低粉爆款热点，生成HTML选题报告推送至飞书，每日9点自动运行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuheng0330](https://clawhub.ai/user/yuheng0330) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to monitor recent Xiaohongshu drink-topic trends, generate a mobile-friendly HTML topic report, and send it to a Feishu group for daily content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Feishu webhook could be exposed or reused outside the intended group. <br>
Mitigation: Use a private Feishu group and a dedicated webhook, and rotate the webhook if it is exposed. <br>
Risk: The scheduled workflow could send reports at an unintended time or to an unintended audience. <br>
Mitigation: Confirm the cron expression, timezone, and Feishu group before enabling automatic delivery. <br>
Risk: Generated reports could include sensitive account or operational data if such data is included in inputs or configuration. <br>
Mitigation: Avoid putting sensitive data in prompts, configuration, report fields, or Feishu messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuheng0330/redbookskill) <br>
- [Volcengine](https://www.volcengine.com/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, html, configuration, guidance] <br>
**Output Format:** [HTML report with Feishu message preview and attachment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scheduled daily run by cron expression; requires FEISHU_WEBHOOK configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
