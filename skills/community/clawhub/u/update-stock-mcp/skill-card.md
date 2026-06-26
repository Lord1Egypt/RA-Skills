## Description: <br>
Update Stock MCP runs a stdio MCP server that manages a local A-share DuckDB database, including database creation, full or incremental stock-data updates, and stock-price queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mifochen](https://clawhub.ai/user/mifochen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to configure an UpdateStock MCP server, create or update a local DuckDB database for A-share market data, and query adjusted or unadjusted stock price records. <br>

### Deployment Geography for Use: <br>
Global; the data scope is focused on A-share market data. <br>

## Known Risks and Mitigations: <br>
Risk: Create and update tools make persistent local changes to DuckDB database files and full updates may run for a long time. <br>
Mitigation: Use a dedicated DB_path, confirm before running create or update tools, and schedule full updates during idle periods. <br>
Risk: The Tushare API token may be stored in API_tushare.txt or passed as a tool parameter. <br>
Mitigation: Keep API_tushare.txt private, avoid committing or syncing it, and prefer a token with only the access needed for this workflow. <br>
Risk: Update operations may contact Tushare or Baostock and depend on provider availability, account points, and network access. <br>
Mitigation: Install only when provider access is expected, and choose the full or easy update path based on the available Tushare points. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mifochen/update-stock-mcp) <br>
- [Tushare registration](https://tushare.pro/register) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API Calls, Text] <br>
**Output Format:** [Markdown instructions with shell snippets, MCP tool-call examples, and JSON-compatible tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The MCP tools can create and update local DuckDB files, read a local Tushare token file, contact Tushare or Baostock providers, and return stock records or status strings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact documentation labels the skill content as v1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
