## Description: <br>
基于技术形态筛选A股股票池，支持VCP、RPS强势股、创新高、高股息等多种形态，并可按涨跌幅、动量、强度等维度排序。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query DaxiAPI stock-pattern data, screen China A-share candidates by technical patterns and secondary filters, and produce a structured screening report with risk notes and a disclaimer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a DaxiAPI token that may be tied to a paid account. <br>
Mitigation: Store the token in a secure environment variable or protected config file, avoid exposing it in chat, screenshots, or shell history, and rotate it if disclosed. <br>
Risk: The skill invokes the `daxiapi-cli` npm package to fetch market data. <br>
Mitigation: Install and run it only in environments where DaxiAPI and the package are trusted. <br>
Risk: Technical-pattern screening can produce misleading investment conclusions if treated as financial advice. <br>
Mitigation: Keep the report's risk notes and disclaimer, avoid absolute predictions, and review results before making investment decisions. <br>


## Reference(s): <br>
- [CLI 命令参考](references/cli-commands.md) <br>
- [形态类型说明](references/pattern-types.md) <br>
- [Token 配置指南](references/token-setup.md) <br>
- [DaxiAPI](https://daxiapi.com) <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-screener) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs stock-screening summaries, ranked tables, risk notes, and a non-investment-advice disclaimer.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
