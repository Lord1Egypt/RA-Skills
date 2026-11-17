## Description:

Fetch real-time stock quotes via Quodd API. Get current prices, daily high/low, and after-hours data for US equities. Use when the user asks for stock prices, quotes, market data, or ticker information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaney64](https://clawhub.ai/user/khaney64)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve current US equity quote data from Quodd, including daily high, low, close, and after-hours values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quodd credentials are sent to Quodd and a short-lived API token can be stored in a local plaintext cache.

Mitigation: Use this skill only on trusted systems, set credentials through environment variables, use --no-cache on shared systems, and tighten permissions on ~/.openclaw/credentials where token caching is enabled.

## Reference(s):

- [Quodd Stock and ETF Data](https://www.quodd.com/stock-and-etf-data)
- [ClawHub Quodd Skill Page](https://clawhub.ai/khaney64/skills/quodd)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text table or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus QUODD_USERNAME and QUODD_PASSWORD environment variables; authentication tokens may be cached locally for up to 20 hours unless --no-cache is used.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
