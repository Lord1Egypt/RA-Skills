## Description: <br>
Fetch Chinese stock and futures market data via Tushare API. Supports stock quotes, futures data, company fundamentals, and macroeconomic indicators. Use when the user needs financial data from Chinese markets. Requires TUSHARE_TOKEN environment variable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query Chinese equities, futures, company fundamentals, and macroeconomic indicators through Tushare. It helps agents provide setup guidance and shell commands for retrieving market data when the user has a Tushare API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tushare API token, which should be treated as a secret. <br>
Mitigation: Store TUSHARE_TOKEN in a trusted local environment and avoid pasting the token into chats, logs, or shared files. <br>
Risk: The skill installs and uses third-party Python packages and calls the Tushare service. <br>
Mitigation: Install dependencies in a trusted Python environment and review Tushare account permissions, usage limits, and terms before relying on results. <br>
Risk: The artifact includes a signup link with a registration parameter. <br>
Mitigation: Use the main Tushare site directly if you do not want that registration parameter applied. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/manifoldor/tushare) <br>
- [Tushare Official Site](https://tushare.pro) <br>
- [Tushare Stock API Documentation](https://tushare.pro/document/2?doc_id=14) <br>
- [Tushare Futures API Documentation](https://tushare.pro/document/2?doc_id=134) <br>
- [Stock API Reference](references/stock_api.md) <br>
- [Futures API Reference](references/futures_api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and formatted command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided TUSHARE_TOKEN and Python dependencies for live data retrieval.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
