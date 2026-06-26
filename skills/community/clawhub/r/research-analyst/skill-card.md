## Description: <br>
Minimal local stock/crypto analysis (5 core scripts bundled). Public APIs only, zero credentials, no subprocess, ClawHub reviewed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenstaff](https://clawhub.ai/user/zhenstaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local stock, crypto, dividend, China market, and portfolio analysis from bundled Python scripts using public market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation can expose the host environment to normal PyPI supply-chain risk. <br>
Mitigation: Install requirements in a virtual environment and avoid using sudo. <br>
Risk: Ticker queries are sent to public market-data providers. <br>
Mitigation: Only query tickers and date ranges you are comfortable exposing to those providers. <br>
Risk: The local portfolios.json file can reveal holdings and cost basis. <br>
Mitigation: Store portfolio data in a protected local state directory and limit access to that file. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/research-analyst) <br>
- [Publisher Profile](https://clawhub.ai/user/zhenstaff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with optional local JSON portfolio data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated locally from public market-data lookups and locally stored portfolio inputs.] <br>

## Skill Version(s): <br>
1.0.54 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
