## Description: <br>
Generates a structured pre-market A-share market briefing from daxiapi market structure, turnover, style rotation, sector strength, limit-up/limit-down, and hot-rank data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-analysis agents use this skill before A-share trading sessions to gather prior-close market data and produce a concise Markdown briefing on market structure, themes, activity, and risks. The output is informational context and is not personalized trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a daxiapi token configured locally. <br>
Mitigation: Install only if the daxiapi CLI/npm package is trusted, store tokens outside screenshots and synced dotfiles, and avoid exposing tokens in shell history. <br>
Risk: Generated market briefings may be mistaken for personalized trading advice. <br>
Mitigation: Treat the briefing as prior-close informational context only and keep the disclaimer that it does not constitute investment advice. <br>
Risk: Premarket data can be stale, missing on non-trading days, or delayed for fields such as the fear-greed index. <br>
Mitigation: Check data dates and apply the skill's quality checks before relying on the briefing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-premarket-briefing) <br>
- [daxiapi.com](https://daxiapi.com) <br>
- [CLI 命令参考](artifact/references/cli-commands.md) <br>
- [Token 配置指南](artifact/references/token-setup.md) <br>
- [字段说明和名词解释](artifact/references/field-descriptions.md) <br>
- [API 参考文档](artifact/references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with inline shell commands for data retrieval and a fixed six-section report structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses prior-close market data, includes concrete metric checks and an informational financial-risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
