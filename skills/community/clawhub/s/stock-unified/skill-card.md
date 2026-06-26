## Description: <br>
UnifiedStock provides a unified interface for querying Chinese A-share realtime quotes, historical K-lines, sector rankings and constituents, financial data, and sector search across pytdx, Tonghuashun, Eastmoney, akshare, and Sina Finance with automatic source fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to ask an agent for Chinese A-share market data, including live quotes, K-line history, sector rankings, sector constituents, financial summaries, source status checks, and JSON-formatted results for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock codes, sector searches, and status checks to third-party Chinese financial-data services. <br>
Mitigation: Use an isolated Python environment and avoid private watchlists or sensitive research patterns when those queries should not be exposed to external market-data providers. <br>
Risk: Realtime and sector data can be unavailable, delayed, rate-limited, or zero outside normal market hours. <br>
Mitigation: Check source status, review returned source labels and errors, and treat market data as informational rather than authoritative trading advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/stock-unified) <br>
- [Data source reference](references/data_sources.md) <br>
- [Eastmoney datacenter API endpoint](https://datacenter.eastmoney.com/api/data/v1/get) <br>
- [Eastmoney data portal](https://data.eastmoney.com/) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, Python API examples, tabular CLI text, and optional JSON data output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on live third-party market-data services and may include realtime quote fields, K-line records, sector lists, constituent stocks, financial summaries, and source status results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
