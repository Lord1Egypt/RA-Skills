## Description:

Searches financial market data, securities, listed-company fundamentals, prices, candlesticks, disclosure files, financial news, A-share data, Hong Kong stocks, and global tickers using yfinance, mootdx, API scripts, or browser-use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve and cross-check structured finance data, market history, company fundamentals, filings, and financial news for securities across global, Hong Kong, U.S., and China A-share markets. Outputs should preserve ticker, market, date range, metric definitions, and source URLs, and should not be presented as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial data, news, and filings can be incomplete, stale, rate-limited, or inconsistent across sources.

Mitigation: Cross-check important results against public source pages, keep ticker, market, date range, metric definitions, and source URLs in the response, and avoid presenting retrieved data as investment advice.

Risk: Dependencies and remote data downloads can affect the local Python environment or write files under the selected download directory.

Mitigation: Install dependencies in a virtual environment or container, consider pinning dependency versions, and run download commands only in workspaces where saving remote financial data under the chosen --downdir path is acceptable.

Risk: API keys, tokens, or cookies could be exposed if placed in committed files, logs, reports, or skill payloads.

Mitigation: Load credentials from environment variables or explicit CLI arguments at runtime, and do not include real secrets in committed files, logs, reports, or payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-search-finance)
- [Publisher profile](https://clawhub.ai/user/sensenova-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled finance_search.py script emits JSON for supported yfinance and mootdx commands.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
