## Description: <br>
An MCP server that interfaces with VCF SDDC Manager to retrieve and analyze LCM upgrade pre-check results, providing instant remediation steps for failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasture-rohit](https://clawhub.ai/user/kasture-rohit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
VCF administrators and infrastructure engineers use this skill to query the latest SDDC Manager LCM pre-check results and summarize failures, warnings, and remediation guidance before an upgrade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an SDDC Manager API token to retrieve upgrade pre-check data. <br>
Mitigation: Use a minimally scoped read-only token where possible and do not store it in shared configuration or source control. <br>
Risk: TLS certificate verification is disabled when connecting to SDDC Manager. <br>
Mitigation: Review before installing in production and change the server to verify TLS with the VCF CA bundle. <br>
Risk: Runtime dependencies are unpinned. <br>
Mitigation: Pin dependencies before production deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text remediation summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SDDCMANAGER_HOST and SDDCMANAGER_API_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
