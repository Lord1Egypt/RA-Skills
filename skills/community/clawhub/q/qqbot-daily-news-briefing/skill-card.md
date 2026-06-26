## Description: <br>
Generates automated daily technology and finance news briefings with AI commentary and delivers them through QQBot, Telegram, or Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[propn](https://clawhub.ai/user/propn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and news-monitoring users can use this skill to schedule recurring news aggregation, generate Markdown briefings, and send summaries to configured messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delivery scripts can send generated reports to a hard-coded QQ recipient if defaults are not changed. <br>
Mitigation: Inspect the delivery scripts, replace the QQ target with the intended recipient, and run a manual test delivery before enabling cron. <br>
Risk: API keys and outbound delivery settings may be exposed or misrouted if placed in broad shell profiles or passed to unreviewed helpers. <br>
Mitigation: Use a dedicated, permission-restricted config file or secret manager for API keys, and verify any external Baidu search helper before providing credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/propn/qqbot-daily-news-briefing) <br>
- [Configuration guide](references/CONFIGURATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing files with shell command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled briefing content and delivery commands; review target recipients, cron entries, and credential handling before unattended use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
