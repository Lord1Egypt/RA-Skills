## Description:

Stock Push schedules A-share market, holdings, and next-day watchlist notifications through OpenClaw and WeChat using Eastmoney quote data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maizhenn](https://clawhub.ai/user/maizhenn)

### License/Terms of Use:

MIT-0

## Use Case:

External users who monitor A-share holdings use this skill to receive scheduled pre-market, close-of-day, and next-day attention messages. Operators can configure holdings, recipient details, cron schedules, and troubleshooting steps for an OpenClaw-based notification setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer configures root-level cron jobs and log rotation files on the host.

Mitigation: Review the installer before use, prefer least-privilege scheduling where possible, and remove /etc/cron.d/stock-monitor and /etc/logrotate.d/stock-monitor after testing.

Risk: Stock information may be sent to a hardcoded WeChat recipient if the scripts are installed without editing.

Mitigation: Replace the recipient identifier and holdings with user-owned values before enabling scheduled sends; keep recipient settings in a safer local configuration when adapting the skill.

Risk: The installer can unpack or install a skill archive without independent authenticity checks.

Mitigation: Verify any skill archive by expected hash or signature before installation.

## Reference(s):

- [Stock Push on ClawHub](https://clawhub.ai/maizhenn/skills/stock-push)
- [Publisher profile](https://clawhub.ai/user/maizhenn)
- [Field verification](references/field-verification.md)
- [Change history](references/history.md)
- [Troubleshooting](references/troubleshooting.md)
- [Eastmoney quote endpoint](https://push2.eastmoney.com/api/qt/stock/get)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain-text notification messages with Markdown and shell command setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled cron execution for pre-market, close-of-day, and next-day watchlist messages; requires user-specific recipient and holdings configuration.]

## Skill Version(s):

1.0.2 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
