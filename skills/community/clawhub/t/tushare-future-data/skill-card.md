## Description: <br>
Provides access to 14 supported Tushare Pro futures-data interfaces for contracts, calendars, market data, warehouse receipts, settlement, holdings, indexes, and risk indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaingush](https://clawhub.ai/user/gaingush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and quantitative researchers use this skill to query Chinese futures-market data from Tushare Pro through a bounded set of documented APIs. Users must provide their own Tushare token through an environment variable or request parameter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Tushare API token is required and could be exposed if pasted into prompts or request JSON. <br>
Mitigation: Use a dedicated Tushare token and provide it through TUSHARE_TOKEN or a secret manager where possible. <br>
Risk: Dependency behavior can change when installing unpinned transitive packages. <br>
Mitigation: Pin dependency versions or use a lockfile in controlled environments before installing. <br>
Risk: Returned data can be empty, delayed, or unavailable if the token lacks the required Tushare permissions or the requested date is not a trading day. <br>
Mitigation: Validate contracts and dates with the supported reference interfaces, and confirm Tushare account permissions for restricted or real-time data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaingush/tushare-future-data) <br>
- [Tushare Pro official documentation](https://tushare.pro/document/2) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON objects containing success status, returned data arrays, counts, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid user-provided Tushare token and network access to Tushare Pro.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
