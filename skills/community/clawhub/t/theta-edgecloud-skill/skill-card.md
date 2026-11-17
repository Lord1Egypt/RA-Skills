## Description:

Helps agents discover Theta EdgeCloud services, run on-demand inference, and manage GPU, RAG, video, and game-character resources with approval gates and cost checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeuslabsllc](https://clawhub.ai/user/zeuslabsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover Theta EdgeCloud services, run AI inference, and administer approved GPU, RAG, video, and game-character workflows while checking pricing and billing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resource changes and inference can incur charges or disrupt running services.

Mitigation: Use least-privilege keys and provider quotas, rehearse with dry-run, check prices, and get explicit approval before each billable or destructive action.

Risk: Prompts, files, character messages, outputs, and presigned URLs may contain private data.

Mitigation: Treat these inputs and outputs as private and share only data authorized for Theta processing.

Risk: Dry-run can still make authenticated read requests, and a confirmation flag cannot itself establish user consent.

Mitigation: Use dry-run only as a rehearsal, and obtain the user's approval before setting confirmation for a live action.

## Reference(s):

- [Theta EdgeCloud](https://www.thetaedgecloud.com)
- [Capability map](references/capabilities.md)
- [Security scope](references/security.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model outputs, resource status and cost details; secret-bearing values are redacted.]

## Skill Version(s):

0.2.0 (source: server-resolved release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
