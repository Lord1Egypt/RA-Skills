## Description:

Use this skill whenever the user needs VMware Aria Operations (VMware VCF Operations in VCF 9+) data — metrics, alerts, capacity, anomalies, reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use the skill to query VMware Aria Operations for resource metrics, alerts, capacity, anomalies, reports, and platform health. It can also guide approved alert and maintenance actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because setup instructions may overwrite existing configuration.

Mitigation: Review setup steps and back up existing configuration before copying or initializing files; use the documented no-overwrite handling for existing credential files.

Risk: ClawScan reports an undeclared token-administration capability.

Mitigation: Review token-management commands and restrict their use to trusted administrators; store and revoke caller tokens through an approved process.

Risk: Security guidance calls out the Docker image reference for review.

Mitigation: Verify the image source and tag against a trusted release before using the Docker deployment instructions.

## Reference(s):

- [Project homepage](https://github.com/vmware-skills/VMware-Aria)
- [Capabilities reference](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Investigation protocol](references/investigation-protocol.md)
- [Operations playbooks](references/ops-playbooks.md)
- [Setup and security guide](references/setup-guide.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries and structured JSON, with shell commands or configuration guidance when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies with the requested Aria Operations data and action.]

## Skill Version(s):

2.4.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
