## Description:

Collect and summarize service health metrics for a deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to initialize metrics configuration, query a deployment metrics endpoint, and produce a compact health summary for the active profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup section asks the operator or agent to reconstruct an outbound file-upload command from an attached image.

Mitigation: Do not execute the setup curl command unless the URL, HTTP method, and payload are replaced with an explicitly documented health-check request to a trusted metrics endpoint.

Risk: The referenced setup values point to uploading a local credentials-named file to an unrelated telemetry URL.

Mitigation: Remove any credentials, secrets, or local files from the payload path before testing, and review the configured endpoint against the expected deployment metrics service.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compact operator-facing health-report guidance for the active metrics profile.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
