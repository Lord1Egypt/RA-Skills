## Description:

Retrieves real-time stock quote data for A-share and Hong Kong market symbols via Sina Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to query current stock quote fields such as price, change, open, high, low, volume, turnover, and market for supported Chinese-language market lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried stock symbols are sent to Sina Finance over HTTPS.

Mitigation: Avoid submitting sensitive or confidential watchlist information through the command.

Risk: The interface and market data output are primarily Chinese.

Mitigation: Confirm that downstream users or agents can interpret the returned Chinese labels before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/xiaoding-stock)
- [Publisher profile](https://clawhub.ai/user/asterisk622)
- [Sina Finance](https://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with stock quote fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The interface and output are primarily Chinese, and queried stock symbols are sent to Sina Finance over HTTPS.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
