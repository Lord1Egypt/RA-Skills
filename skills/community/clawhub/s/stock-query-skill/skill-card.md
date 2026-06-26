## Description: <br>
Queries a stock ticker's past 30 days of daily market data and returns prices, volume, dividends, and stock split information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tf9527666666-spec](https://clawhub.ai/user/tf9527666666-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to request recent daily stock-price data for a ticker and save the resulting market-data table for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external market-data services through yfinance. <br>
Mitigation: Use it only where outbound market-data requests are acceptable. <br>
Risk: Running the script writes a ticker-named CSV file and may overwrite an existing file in the current directory. <br>
Mitigation: Run it from a directory where creating or replacing the output CSV is acceptable. <br>
Risk: The skill depends on yfinance and pandas in the active Python environment. <br>
Mitigation: Install dependencies only in a Python environment you trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tf9527666666-spec/stock-query-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text and CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a ticker-named 30-day CSV file in the current directory when the script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
