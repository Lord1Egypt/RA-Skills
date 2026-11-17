## Description:

Query CJ Dropshipping API v2.0 to source products and fetch details for catalog building.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

External developers and ecommerce operators use this skill to search CJ Dropshipping products, refresh CJ access tokens, and produce normalized product JSON for catalog-building workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CJ API credentials and refreshed access tokens are stored in a local configuration file.

Mitigation: Use only a trusted cj-api.json, keep it out of source control and shared workspaces, and rotate the CJ API key or token if exposure is possible.

Risk: The configured API base URL affects where CJ credentials and product requests are sent.

Mitigation: Keep baseUrl fixed to the official CJ API endpoint before using real CJ credentials.

## Reference(s):

- [CJ Dropshipping API v2.0](https://developers.cjdropshipping.com/api2.0/v1)
- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-dropshipping-sourcing)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON files, Guidance]

**Output Format:** [Markdown guidance with bash commands and normalized JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CJ API configuration file containing credentials and token expiry data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
