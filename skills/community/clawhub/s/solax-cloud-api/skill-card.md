## Description: <br>
Fetch inverter summary data from the Solax Cloud API using the npm package solax-cloud-api when the user provides or has configured a Solax tokenId and inverter serial number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AllMightySauron](https://clawhub.ai/user/AllMightySauron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to retrieve current Solax inverter summary data as JSON for dashboards, monitoring, or energy automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Solax API token and inverter serial number to retrieve energy summary data. <br>
Mitigation: Prefer environment variables over CLI arguments, do not hardcode credentials, and keep the token redacted from logs. <br>
Risk: The inverter serial number and returned energy summary may be sensitive operational data. <br>
Mitigation: Treat the serial number and JSON output as private and share them only with intended dashboards or automation systems. <br>
Risk: The skill depends on the npm package solax-cloud-api. <br>
Mitigation: Review or pin the dependency before use and install it only in the skill scripts directory. <br>


## Reference(s): <br>
- [SolaxSummary typing reference](references/solax-summary.d.ts) <br>
- [ClawHub skill page](https://clawhub.ai/AllMightySauron/solax-cloud-api) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON object printed to stdout, with setup and command guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Solax tokenId and inverter serial number; failures return structured error JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
