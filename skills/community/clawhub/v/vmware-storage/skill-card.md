## Description:

Use this skill whenever the user needs to manage VMware storage — datastores, iSCSI targets, and vSAN clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to inspect VMware datastores, iSCSI, vSAN, and Fibre Channel storage, and to make approved storage configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles per-target VMware credentials, and insecurely stored passwords could be exposed.

Mitigation: Keep passwords in the documented .env file with owner-only permissions (chmod 600); avoid placing secrets in configuration files or agent-visible output.

Risk: The doctor --skip-auth option bypasses connectivity and authentication checks.

Mitigation: Run the full doctor check before relying on the configured target's authentication status; treat a skipped check as unverified.

Risk: Removing an iSCSI target can make backing LUNs and datastores inaccessible.

Mitigation: Inspect affected paths and blast radius, confirm the target is unused, and proceed only after explicit user approval.

## Reference(s):

- [VMware Storage project homepage](https://github.com/vmware-skills/VMware-Storage)
- [Setup guide](references/setup-guide.md)
- [CLI reference](references/cli-reference.md)
- [Capabilities](references/capabilities.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Structured tool results and human-readable text or Markdown; CLI examples use shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the configured VMware target and account privileges.]

## Skill Version(s):

2.6.2 (source: server-resolved release metadata, skill installation instructions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
