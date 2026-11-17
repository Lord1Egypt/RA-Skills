## Description:

Fetches real-time FOREX news and market data from Yahoo Finance for major currency pairs (EUR/USD, GBP/USD, USD/JPY, etc.). Analyzes sentiment and provides trading context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nazimboudeffa](https://clawhub.ai/user/nazimboudeffa)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to fetch Yahoo Finance data for supported major FOREX pairs, summarize current rates and recent headlines, and interpret keyword-based sentiment as trading context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BUY/SELL/HOLD labels for FOREX pairs may be mistaken for personalized financial advice.

Mitigation: Treat recommendations as informational sentiment signals only and require independent financial analysis before any trading decision.

Risk: Yahoo Finance data, headlines, and keyword-based sentiment may be delayed, unavailable, incomplete, or missing market context.

Mitigation: Cross-check rates, timestamps, headlines, and market drivers with authoritative financial sources before relying on the output.

Risk: The skill installs yfinance>=0.2.40 without an upper pin and makes outbound Yahoo Finance requests.

Mitigation: Run it only where outbound Yahoo Finance access and review of dependency versions are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nazimboudeffa/skills/yahoo-finance-forex)
- [API Examples](references/api-examples.md)
- [FOREX Pairs Reference](references/forex-pairs.md)
- [Sentiment Analysis Guide](references/sentiment-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports one selected major FOREX pair per script run and a news limit from 1 to 50.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
