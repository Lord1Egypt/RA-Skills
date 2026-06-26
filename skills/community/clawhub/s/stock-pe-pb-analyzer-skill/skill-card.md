## Description: <br>
Analyzes historical PE and PB percentile levels for A-share stocks using BaoStock data, accepting stock names or codes and reporting current valuation levels against 1-, 3-, 5-, and 10-year history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyachao](https://clawhub.ai/user/caoyachao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and developers use this skill to query a Chinese A-share by name or code and generate PE/PB percentile reports for valuation reference. The output is financial reference data and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock names or codes submitted for analysis are sent to BaoStock. <br>
Mitigation: Avoid submitting sensitive watchlists or identifiers if that disclosure is not acceptable for the deployment. <br>
Risk: The generated PE/PB report is financial reference data and may be incomplete, delayed, or unsuitable as a sole decision basis. <br>
Mitigation: Treat the report as one input, verify material decisions against authoritative market data, and keep the non-advice disclaimer visible to users. <br>
Risk: The script depends on external Python packages and a live BaoStock service. <br>
Mitigation: Install it in a virtual environment, review or pin dependencies for regular use, and handle BaoStock outages or missing data before relying on outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caoyachao/stock-pe-pb-analyzer-skill) <br>
- [BaoStock data source](http://www.baostock.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Console text report with optional CSV data export and text summary files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports PE-TTM and PB-MRQ percentiles across 1-, 3-, 5-, and 10-year windows when BaoStock data is available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
