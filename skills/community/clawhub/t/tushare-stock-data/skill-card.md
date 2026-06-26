## Description: <br>
Provides A-share stock basic data from Tushare by stock code with a configurable result limit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghjkkkkkklkk](https://clawhub.ai/user/ghjkkkkkklkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve A-share stock basic records from Tushare during agent workflows, optionally filtering by stock code and limiting returned rows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds and uses an undisclosed Tushare API token for stock-data queries. <br>
Mitigation: Prefer a version that removes and rotates the exposed token and requires a user-provided credential through configuration or environment variables. <br>
Risk: The skill depends on external Tushare network access that is not documented in the artifact. <br>
Mitigation: Review and document Tushare network access before installation, especially in environments with data-access or egress controls. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON] <br>
**Output Format:** [JSON object with status, count, and stock data records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns records from Tushare stock_basic using the requested stock code and row limit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
