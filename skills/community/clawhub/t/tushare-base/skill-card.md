## Description: <br>
Fetch Chinese stock and futures market data from the Tushare API, including stock quotes, futures data, company fundamentals, and macroeconomic indicators; requires a user-provided TUSHARE_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WdBlink](https://clawhub.ai/user/WdBlink) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and financial data analysts use this skill to retrieve Chinese stock, futures, company, money-flow, and macroeconomic data through Tushare-backed shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Tushare API token may be exposed if pasted into shared chats, command history, or logs. <br>
Mitigation: Use a dedicated Tushare token where possible, store it in TUSHARE_TOKEN, and avoid sharing token values in prompts, logs, or screenshots. <br>
Risk: Installing Python dependencies globally can affect the user's broader Python environment. <br>
Mitigation: Install tushare and pandas in a virtual environment or another isolated Python environment before running the helper script. <br>
Risk: Some Tushare endpoints may return no data or require account permissions beyond a basic token. <br>
Mitigation: Confirm the requested symbol format, date range, and Tushare account permissions before treating missing data as a market-data result. <br>


## Reference(s): <br>
- [Tushare Base on ClawHub](https://clawhub.ai/WdBlink/tushare-base) <br>
- [Tushare Stock API Reference](references/stock_api.md) <br>
- [Tushare Futures API Reference](references/futures_api.md) <br>
- [Tushare Website](https://tushare.pro) <br>
- [Tushare Stock Interface Documentation](https://tushare.pro/document/2?doc_id=14) <br>
- [Tushare Futures Interface Documentation](https://tushare.pro/document/2?doc_id=134) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Python helper that prints tabular market data and JSON-style records from Tushare API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
