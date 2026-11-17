## Description:

分析红利类指数投资机会，基于打分算法判断超买超卖状态，并生成包含风险提示的结构化投资分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze dividend index timing opportunities, compare supported dividend indexes, and produce differentiated strategy guidance based on DaxiAPI score, CS, and RSI data. It is intended for informational analysis reports, not personalized financial advice or automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable npm code through daxiapi-cli@latest.

Mitigation: Prefer a pinned, reviewed daxiapi-cli version before execution.

Risk: The skill handles an API token for DaxiAPI access.

Mitigation: Avoid pasting tokens directly into shell commands and verify where the CLI stores credentials.

Risk: The skill can produce concrete investment actions from technical indicators.

Mitigation: Treat outputs as informational analysis, include disclaimers, and require human review before making financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-dividend-analysis)
- [DaxiAPI](https://daxiapi.com)
- [CLI command reference](references/cli-commands.md)
- [Field descriptions](references/field-descriptions.md)
- [Token setup guide](references/token-setup.md)
- [Report template](assets/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and tabular analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DaxiAPI dividend score data and should include risk disclaimers for investment-related output.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
