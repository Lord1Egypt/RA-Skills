## Description:

Fetch inverter summary data from the Solax Cloud API using the npm package solax-cloud-api when a Solax tokenId and inverter serial number are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allmightysauron](https://clawhub.ai/user/allmightysauron)

### License/Terms of Use:


## Use Case:

Developers and automation maintainers use this skill to fetch current Solax inverter summary data as JSON for dashboards, monitoring, or energy automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Solax tokenId and inverter serial number and sends them to the Solax Cloud API through the solax-cloud-api package.

Mitigation: Treat the token as a secret, prefer environment variables or a secret manager, avoid hardcoding credentials, and run the script in a limited environment.

Risk: The artifact does not include a package-lock.json, so npm install may resolve dependency changes over time.

Mitigation: Review dependency changes and add or review a lockfile before production deployment.

Risk: Solax summary fields can vary with the installed package version and API response.

Mitigation: Validate downstream dashboards or automation against observed JSON output before relying on specific fields.

## Reference(s):

- [SolaxSummary typing reference](references/solax-summary.d.ts)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Solax tokenId and inverter serial number; successful runs print one JSON summary object, while failures return structured error JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
