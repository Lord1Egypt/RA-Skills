## Description: <br>
Check stock prices using yfinance library. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rupprath](https://clawhub.ai/user/rupprath) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to check public stock and ETF ticker prices from Yahoo Finance without configuring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on outbound Yahoo Finance/yfinance traffic and may fail in air-gapped or restricted environments. <br>
Mitigation: Install yfinance from a trusted source and run the skill only where outbound access to Yahoo Finance/yfinance is allowed. <br>
Risk: Ticker data may be unavailable or incomplete for invalid symbols or less common securities. <br>
Mitigation: Handle error output and verify important financial data against an authoritative source before making decisions. <br>


## Reference(s): <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [ClawHub skill page](https://clawhub.ai/rupprath/stock-price-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text stock quote summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ticker symbol, price, price change, percent change, volume, average volume, and related market data when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
