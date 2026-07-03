## Description: <br>
定时检索白名单科技公司的近 24 小时热点，生成带来源 URL 的中文纯文字短文，并发送到配置的推送渠道。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuewuya20180928](https://clawhub.ai/user/yuewuya20180928) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users configure this skill to have an agent search whitelisted technology companies on a schedule, summarize recent items in Chinese, and send plain-text updates to channels such as WeChat, Telegram, Slack, or email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring outbound delivery can send generated news summaries to external messaging services or the wrong recipient. <br>
Mitigation: Set the recipient, delivery channel, and account ID explicitly before enabling the cron job, and remove or replace any fallback recipient values. <br>
Risk: The skill depends on search API keys and local bot credentials, and its troubleshooting steps include credential reset operations. <br>
Mitigation: Keep API keys and bot tokens in local secret stores, avoid printing secrets from configuration files, and back up account files before following reset instructions. <br>
Risk: Generated news summaries may be inaccurate if the agent uses facts outside the search result content. <br>
Mitigation: Keep the source-URL requirement, whitelist restriction, and content-only summarization rules enabled, and review outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuewuya20180928/redian-jiansuo-baochuwen) <br>
- [Cron Job 配置详解](artifact/references/cron-config.md) <br>
- [完整 Prompt模板](artifact/references/prompt.md) <br>
- [配置变量完整定义](artifact/references/variables.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese plain-text messages, Markdown instructions, shell commands, and cron configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is three short Chinese articles of about 400 characters each, with source URLs and a delivery report; model, search provider, whitelist, article count, schedule, and delivery channel are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
