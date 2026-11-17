## Description:

Real-time cryptocurrency price lookup from Upbit (Korean KRW exchange). Use when user asks for Korean crypto prices, Upbit prices, domestic cryptocurrency rates, or market ticker in Korean won (KRW). Supports all coins listed on Upbit exchange.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkjsays](https://clawhub.ai/user/lkjsays)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up Upbit KRW cryptocurrency market prices and present ticker data with price changes, ranges, volume, and 52-week context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on live public market data from Upbit, so returned prices can be unavailable, delayed, or change quickly.

Mitigation: Treat results as market information at lookup time and verify important values against Upbit before making financial decisions.

Risk: Invalid or unsupported market codes return no ticker records.

Mitigation: Use the KRW-{SYMBOL} format, keep symbols uppercase, and tell the user when a requested coin is not listed on Upbit.

## Reference(s):

- [ClawHub Upbit Skill](https://clawhub.ai/lkjsays/skills/upbit)
- [Upbit ticker API example](https://api.upbit.com/v1/ticker?markets=KRW-BTC)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and formatted market summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public API responses and Korean won market metrics such as current price, daily change, 24-hour volume, day range, and 52-week range.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
