## Description:

Fetches live and historical Yahoo Finance stock data, with IDX ticker handling for Indonesia stocks and endpoints for prices, OHLCV history, fundamentals, dividends, and splits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[temmyraharjo](https://clawhub.ai/user/temmyraharjo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to answer stock-market questions by querying a local REST service for current prices, historical OHLCV data, fundamentals, dividends, and stock splits. It is especially oriented toward Indonesia Stock Exchange tickers, where bare symbols are resolved to .JK by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start or document an unauthenticated FastAPI market-data service bound to all network interfaces.

Mitigation: Bind the service to 127.0.0.1 for local use, do not expose port 8000 publicly without authentication and rate limits, and avoid --reload for normal operation.

Risk: The README includes optional persistent systemd deployment guidance for the local service.

Mitigation: Treat persistent deployment instructions as optional and harden the service separately before using them outside a trusted local environment.

## Reference(s):

- [ClawHub Yfinance skill page](https://clawhub.ai/temmyraharjo/skills/yfinance)
- [OpenAPI connector specification](artifact/openapi.json)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown guidance with curl commands and JSON or formatted text returned by the local API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be grounded in the API result; stock prices should not be guessed or fabricated.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
