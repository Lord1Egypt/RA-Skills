## Description:

虾皮A股选股器 helps agents screen A-share stocks by technical patterns such as VCP, RPS, new highs, high dividends, and multi-condition filters, then summarize findings in a structured Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query DAXIAPI stock-pattern data, apply secondary filters, and produce concise A-share screening analysis for technical, momentum, trend, and value-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm CLI through latest-version commands.

Mitigation: Use a pinned, reviewed DAXIAPI CLI version and execute it in a restricted environment.

Risk: DAXIAPI token setup examples can expose tokens in shell history, source code, config files, or agent logs.

Mitigation: Avoid entering real tokens directly in command lines or source code, do not print token config files into logs, and rotate any token that may have been exposed.

Risk: Stock-screening output may be mistaken for financial advice or may rely on stale market data.

Mitigation: Include the data date, source command, risk notes, and a clear disclaimer that generated analysis is for reference only and not investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-screener)
- [DAXIAPI](https://daxiapi.com)
- [CLI command reference](references/cli-commands.md)
- [Token setup guide](references/token-setup.md)
- [Pattern type reference](references/pattern-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and tabular stock-screening analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should include data date, source command, key metrics, risk notes, and a disclaimer that the analysis is not investment advice.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
