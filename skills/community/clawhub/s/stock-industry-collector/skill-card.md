## Description: <br>
收集A股某行业全部上市公司资料，包括代码、名称、交易所、行业、财务数据（ROE、毛利率、净利率、资产负债率、现金流、增长率）、控股股东及持股比例 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wtjjacobj](https://clawhub.ai/user/wtjjacobj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to collect Chinese A-share industry constituents, financial metrics, shareholder information, and daily market data for industry-level stock research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on unpinned Python packages. <br>
Mitigation: Pin and review baostock, akshare, and pandas versions before deploying in a controlled environment. <br>
Risk: The skill makes outbound requests to public Chinese stock-data services and executes local curl calls. <br>
Mitigation: Run only in an environment where those outbound requests and local curl execution are permitted and monitored. <br>
Risk: Collected fields may be incomplete or differ from the documentation. <br>
Mitigation: Verify collected financial and shareholder fields against trusted sources before relying on them for investment analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wtjjacobj/stock-industry-collector) <br>
- [Eastmoney market data endpoint used by the artifact](https://push2.eastmoney.com/api/qt/stock/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python objects and tabular stock data suitable for DataFrame or spreadsheet workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a stock list and count; optional price collection adds current market data fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
