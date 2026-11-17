## Description:

Turns a scrape, dataset, or endpoint into a priced API that can be published, metered, and called through SettleMesh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[structureintelligence](https://clawhub.ai/user/structureintelligence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data publishers use this skill to deploy dataset-serving endpoints, publish priced API manifests, verify charge readiness, and guide callers through quoted, metered requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help publish user data as a public paid API without a required pre-publication safety check.

Mitigation: Confirm the exact app and routes that will become public, review the dataset before publication, and verify how to disable the endpoint.

Risk: Published datasets may expose secrets, personal data, confidential material, or licensed content.

Mitigation: Review dataset contents and licensing before deployment, and remove sensitive or unauthorized data before publishing.

Risk: The workflow uses authenticated SettleMesh access through SETTLE_API_KEY.

Mitigation: Use a scoped API key, verify the settlemesh CLI source and version, and revoke credentials if exposure or misuse is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/structureintelligence/skills/sell-live-dataset)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the settlemesh CLI and SETTLE_API_KEY; guides authenticated network calls to publish and meter paid APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
