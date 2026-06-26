## Description: <br>
Provides real-time and historical A-share stock data from multiple free sources including mootdx, Sina, Tencent, Eastmoney, and Tushare. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[same1317](https://clawhub.ai/user/same1317) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve and compare A-share real-time quotes, historical K-line data, and selected financial data from multiple public data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data can be incomplete, delayed, unavailable, or inconsistent across public data sources. <br>
Mitigation: Compare results across supported sources and verify important values against an authoritative market data provider before making financial or operational decisions. <br>
Risk: Some data sources are documented as unstable, backup-only, or dependent on local package installation. <br>
Mitigation: Use mootdx or Sina as the primary path when available, keep dependencies installed, and handle endpoint failures with retries or fallback sources. <br>


## Reference(s): <br>
- [Stock-A ClawHub release](https://clawhub.ai/same1317/stock-a) <br>
- [same1317 publisher profile](https://clawhub.ai/user/same1317) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-like stock data examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on live third-party market data endpoints and local Python package availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
