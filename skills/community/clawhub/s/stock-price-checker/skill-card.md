## Description:

Checks stock prices with the yfinance library without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rupprath](https://clawhub.ai/user/rupprath)

### License/Terms of Use:


## Use Case:

Developers and external users can ask an agent to look up stock or ETF symbols and return current Yahoo Finance market data such as price, change, volume, market cap, and 52-week range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell launcher uses a hard-coded script path outside the packaged skill.

Mitigation: Run the packaged stock-price.py directly or update stock-price.sh to resolve stock-price.py relative to its own directory before deployment.

Risk: Market data depends on yfinance and Yahoo Finance availability and may be incomplete for some symbols.

Mitigation: Verify important results against an authoritative market data source before making financial decisions.

Risk: The Python dependency may be resolved from an unexpected environment.

Mitigation: Install and run yfinance in a reviewed Python environment with pinned or otherwise controlled dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rupprath/skills/stock-price-checker)
- [Yahoo Finance](https://finance.yahoo.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status line from the bundled command, with documented JSON fields in the skill reference.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and yfinance; no API key is documented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
