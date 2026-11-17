## Description:

Check stock prices using yfinance library. No API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check a single public stock or ETF ticker through Yahoo Finance via yfinance and receive current price, change, volume, and range information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested ticker symbols are sent to Yahoo Finance through yfinance.

Mitigation: Use the skill only when sharing the requested ticker symbol with Yahoo Finance is acceptable.

Risk: Stock quote output can become privacy-sensitive when combined with names, account numbers, portfolio holdings, or personal financial amounts.

Mitigation: Present quote data without correlating it with personal identifiers or personal portfolio context.

Risk: Sending quote output to external endpoints can leak financial context outside the local environment.

Mitigation: Keep output local and do not pipe stock price results to network-transmitting commands or webhooks.

Risk: Bypassing the documented workflow can remove the skill's intended error handling and guardrails.

Mitigation: Use only the documented `python3 stock-price.py SYMBOL` pattern with a single valid ticker.

## Reference(s):

- [Yahoo Finance](https://finance.yahoo.com)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/stock-price-checker)
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/stock-price-checker-hardened)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs the documented single-ticker command pattern and returns formatted quote data or an error message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
