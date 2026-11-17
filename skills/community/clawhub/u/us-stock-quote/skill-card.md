## Description:

Stock Tools fetches real-time market quotes for US stocks and ETFs through Yahoo Finance and can also query cryptocurrency prices through Binance for crypto-formatted symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wndagg](https://clawhub.ai/user/wndagg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request current quote data for common US stocks and ETFs from an agent workflow or command-line helper. Users should account for the local proxy requirement and the additional Binance crypto path described in security evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker symbols are sent through a local proxy to Yahoo Finance and, for crypto-formatted inputs, to Binance.

Mitigation: Use only when that routing is acceptable, document the proxy requirement for users, and avoid submitting sensitive or private ticker lists.

Risk: The user-facing description understates Binance crypto support and external data-source behavior.

Mitigation: Document or disable the Binance path before relying on the skill in a fully scoped release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wndagg/skills/us-stock-quote)
- [Yahoo Finance chart endpoint](https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d)
- [Binance ticker price endpoint](https://api.binance.com/api/v3/ticker/price?symbol={symbol})

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote output includes symbol, price, percentage change for equities and ETFs, and price for crypto symbols when supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
