## Description: <br>
Tushare Cli provides command-line access to Tushare finance data for stock basics, financial indicators, daily market data, and financial news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alsoforever](https://clawhub.ai/user/alsoforever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query Tushare financial data from an agent-accessible CLI after configuring a TUSHARE_TOKEN. It supports quick lookup of stock profile data, financial indicators, daily price data, and recent finance news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TUSHARE_TOKEN for external API access. <br>
Mitigation: Keep the token private and configure it only in trusted execution environments. <br>
Risk: Tushare API quota, access limits, or dependency behavior can affect query results. <br>
Mitigation: Review or pin the tushare Python dependency and expect upstream quota or access restrictions to apply. <br>


## Reference(s): <br>
- [Tushare Pro](https://tushare.pro) <br>
- [ClawHub Skill Page](https://clawhub.ai/alsoforever/tushare-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/alsoforever) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the tushare Python package, and a TUSHARE_TOKEN environment variable for API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
