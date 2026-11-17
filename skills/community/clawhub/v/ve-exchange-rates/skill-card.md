## Description:

Get Venezuelan exchange rates - BCV official rate, Binance P2P USDT average, and the gap between them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jehg814](https://clawhub.ai/user/jehg814)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current Venezuelan exchange-rate information, including the BCV official rate, Binance P2P USDT averages, and the gap between official and parallel rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live web requests to BCV, Binance P2P, and a fallback exchange-rate API.

Mitigation: Use it only where those external requests are acceptable and disclose that the rates come from live public sources.

Risk: Exchange-rate outputs are market data that can fluctuate or become stale.

Mitigation: Check the reported source and BCV date warning, rerun for current data, and independently verify rates before making financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jehg814/skills/ve-exchange-rates)
- [BCV exchange-rate source](https://www.bcv.org.ve/)
- [Binance P2P exchange-rate endpoint](https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search)
- [ExchangeRate API fallback endpoint](https://api.exchangerate-api.com/v4/latest/USD)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Console text that can be summarized as Markdown for user-facing replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live source labels, BCV Fecha Valor when available, date mismatch warnings, P2P buy/sell/average rates, gap percentage, and a 100 USD conversion example.]

## Skill Version(s):

1.0.7 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
