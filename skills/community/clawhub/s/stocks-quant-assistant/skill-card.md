## Description:

Stocks Quant Assistant monitors configured China A-share stocks and funds, analyzes technical indicators, tracks positions, and produces scheduled market reports for console, Feishu, or Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliwenjing](https://clawhub.ai/user/wuliwenjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance-focused agent users can configure stock and fund watchlists, generate technical-indicator summaries, track positions, and deliver recurring market-monitoring reports. The reports are informational monitoring output and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health-check behavior can expose Feishu messaging credentials if real credentials are used before the scripts are fixed.

Mitigation: Review and patch artifact/scripts/health-check.sh to redact app_secret and other tokens before using real credentials; start with console output or test credentials.

Risk: Setup behavior can create persistent launchd or cron scheduled execution that sends market reports to configured recipients.

Mitigation: Review scheduled-job definitions before installation, install in an isolated environment, and remove launchd or cron entries when recurring pushes are no longer intended.

Risk: Privileged launchctl and setup-sleep power-setting guidance can change host behavior beyond report generation.

Mitigation: Avoid sudo launchctl and setup-sleep guidance unless explicitly required and reviewed by the operator.

Risk: Unpinned dependency installation can change runtime behavior across installs.

Mitigation: Use a virtual environment and pin dependencies before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuliwenjing/skills/stocks-quant-assistant)
- [Publisher profile](https://clawhub.ai/user/wuliwenjing)
- [Feishu Open Platform app setup](https://open.feishu.cn/app)
- [Artifact usage guide](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown market report with YAML configuration examples and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print to console or send reports to configured Feishu or Telegram recipients; setup paths can create local logs, state files, and scheduled jobs.]

## Skill Version(s):

3.1.0 (source: server release, artifact/skill.yml, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
