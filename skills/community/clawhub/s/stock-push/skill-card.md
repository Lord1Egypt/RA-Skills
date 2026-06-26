## Description: <br>
Stock Push installs and documents scheduled OpenClaw jobs that fetch A-share market data from Eastmoney and send pre-market, after-close, and next-day WeChat stock alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maizhenn](https://clawhub.ai/user/maizhenn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users who monitor A-share holdings use this skill to install and maintain timed stock-market push jobs. It helps configure WeChat alerts for watchlists, holdings summaries, market-close reviews, and next-day reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer configures root-level cron and logrotate entries. <br>
Mitigation: Review the installer before use, prefer a user-level scheduler or dedicated non-root account where possible, and know how to remove /etc/cron.d/stock-monitor and /etc/logrotate.d/stock-monitor. <br>
Risk: The stock scripts contain a hard-coded WeChat USER_ID and example holdings or watchlists. <br>
Mitigation: Edit all three scripts before deployment so alerts use the intended recipient and portfolio data. <br>
Risk: The Python installer includes a remote-download path for a packaged skill file. <br>
Mitigation: Use a local package or verify the downloaded package before installation. <br>


## Reference(s): <br>
- [Stock Push ClawHub Page](https://clawhub.ai/maizhenn/stock-push) <br>
- [Publisher Profile](https://clawhub.ai/user/maizhenn) <br>
- [Field Verification](references/field-verification.md) <br>
- [History](references/history.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled stock-alert messages through OpenClaw and writes local cron, logrotate, and log files when installed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
