## Description: <br>
Monitors configured A-share stocks and funds, analyzes technical indicators and holdings, and sends scheduled stock reports to Feishu or Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliwenjing](https://clawhub.ai/user/wuliwenjing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual investors, analysts, and automation-focused users use this skill to monitor configured China A-share stocks and funds, track holdings, and receive scheduled technical-analysis summaries through messaging channels. <br>

### Deployment Geography for Use: <br>
Global, with default China market data sources and Asia/Shanghai scheduling assumptions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create recurring background jobs through launchd or cron. <br>
Mitigation: Review installed launchd or cron entries after setup and remove or disable schedules that are not intended. <br>
Risk: Configured watchlists, holdings, and messaging credentials may be sent to Feishu or Telegram when push channels are enabled. <br>
Mitigation: Use dedicated low-privilege bot credentials and verify the configured recipients before enabling scheduled pushes. <br>
Risk: Health-check helper behavior may expose messaging secrets in command output. <br>
Mitigation: Redact secrets before running health-check scripts or sharing their output. <br>
Risk: The setup-sleep helper can change system-wide macOS power settings. <br>
Mitigation: Run the sleep setup script only when the power-setting changes are intentional and reversible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuliwenjing/stocks-quant-assistant) <br>
- [Feishu developer console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style reports, console text, shell commands, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send reports to configured Feishu or Telegram channels and write local logs/state files.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata and artifact skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
