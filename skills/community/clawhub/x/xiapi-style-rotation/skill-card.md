## Description:

分析A股大小盘风格轮动，通过中证2000与沪深300的相对强弱差值判断风格偏向与切换信号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to retrieve DaxiAPI market-style data and generate a concise A-share large-cap versus small-cap rotation report. It supports style-bias assessment, trend review, and extreme-spread risk framing, but not individual stock, sector, bond, or intraday trading analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a mutable npm CLI with @latest.

Mitigation: Use a pinned, reviewed DaxiAPI CLI version before installing or running the command.

Risk: API tokens may be exposed if entered directly on the command line or repeated in logs or chat context.

Mitigation: Prefer environment variables or reviewed local configuration, avoid sharing real token values, and prevent the agent from printing or storing tokens.

Risk: The scanner verdict is suspicious because the skill combines external CLI execution with credential handling.

Mitigation: Review the skill and DaxiAPI CLI source before installation and use it only if the CLI source is trusted.

## Reference(s):

- [CLI 命令参考](references/cli-commands.md)
- [Token 配置指南](references/token-setup.md)
- [字段说明](references/field-descriptions.md)
- [DaxiAPI](https://daxiapi.com)
- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-style-rotation)
- [Publisher profile](https://clawhub.ai/user/ksky521)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market spread values, historical percentiles, trend interpretation, risk disclaimer, and token setup guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
