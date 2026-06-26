## Description: <br>
分析A股大小盘风格轮动，通过中证2000与沪深300的相对强弱差值判断风格偏向与切换信号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to produce an A-share large-cap versus small-cap style-rotation report from DaxiAPI market style data. It supports style positioning, trend analysis, and extreme-zone mean-reversion context, but not individual stock, sector, bond, futures, FX, intraday, or automated trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DaxiAPI tokens can be exposed through shared chats, logs, repositories, backups, synced dotfiles, or persistent local CLI configuration. <br>
Mitigation: Trust the DaxiAPI CLI before installation, prefer temporary environment variables where practical, avoid sharing tokens, and delete or rotate any token that may have been exposed. <br>
Risk: The skill depends on an external CLI package and API for market data. <br>
Mitigation: Review the `npx daxiapi-cli@latest` commands before execution and confirm that the configured token and data source are appropriate for the environment. <br>
Risk: Style-rotation analysis may be overinterpreted as investment advice or as a guaranteed prediction. <br>
Mitigation: Keep the report conclusion tied to observed spread, percentile, and trend data, include the artifact's disclaimer, and avoid absolute language about future market moves. <br>
Risk: Data is updated after market close and is not suitable for intraday signals or automated trading. <br>
Mitigation: Use the output as post-close analytical context only and do not present it as real-time trading guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ksky521/xiapi-style-rotation) <br>
- [CLI 命令参考](references/cli-commands.md) <br>
- [Token 配置指南](references/token-setup.md) <br>
- [字段说明和名词解释](references/field-descriptions.md) <br>
- [DaxiAPI](https://daxiapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and structured analysis sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DaxiAPI market style data and should include concrete spread values, percentile context, trend evidence, and a risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
