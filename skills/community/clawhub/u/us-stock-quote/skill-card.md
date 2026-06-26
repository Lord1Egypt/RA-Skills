## Description: <br>
Fetches real-time US stock and ETF quotes from Yahoo Finance, with crypto-style symbols routed to Binance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wndagg](https://clawhub.ai/user/wndagg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run a Python quote script for common US tickers and ETF symbols, then read price, change, percentage change, and currency output in the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols are sent to Yahoo Finance, and crypto-style symbols are sent to Binance through the configured local proxy. <br>
Mitigation: Run only if that data sharing is acceptable, and review or change the proxy setting before use. <br>
Risk: The script depends on third-party market data services and may fail because of network issues, API changes, or rate limits. <br>
Mitigation: Handle quote lookup failures in the calling workflow and verify important prices against an authoritative source. <br>
Risk: The script requires the Python requests dependency and uses a local proxy on port 7891. <br>
Mitigation: Use a trusted Python environment and confirm the local proxy is expected and trusted before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wndagg/us-stock-quote) <br>
- [Project Homepage](https://github.com/wNDAGG/mimi-scripts) <br>
- [Yahoo Finance Chart API endpoint used by the script](https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d) <br>
- [Binance ticker price endpoint used by the script](https://api.binance.com/api/v3/ticker/price?symbol={symbol}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain terminal text from a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each requested symbol is printed as a separate line; errors are reported inline per symbol.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
