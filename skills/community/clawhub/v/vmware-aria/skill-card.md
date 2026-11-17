## Description:

Helps agents query VMware Aria Operations and VCF Operations for infrastructure metrics, alerts, capacity, anomalies, reports, and platform health, with a limited set of auditable operational actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

VMware administrators and platform engineers use the skill to investigate Aria Operations health and alerts, review infrastructure performance and capacity, and generate reports. It also supports limited alert, alert-definition, report, and resource-maintenance changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports that setup guidance may overwrite existing configuration without warning.

Mitigation: Back up and inspect existing configuration before installation or initialization, and confirm the setup behavior for the target paths before proceeding.

Risk: ClawScan reports authentication-token management capability outside the stated monitoring purpose.

Mitigation: Review token-related operations before use and restrict them to an authorized environment with least-privilege access; avoid token management unless it is explicitly required.

Risk: The security review was partial and noted unresolved references.

Mitigation: Review unresolved references and the skill's source files before installation; follow the scanner's recommendation to defer installation until the concerns are resolved.

## Reference(s):

- [Project homepage](https://github.com/vmware-skills/VMware-Aria)
- [Setup and security guide](references/setup-guide.md)
- [Capabilities reference](references/capabilities.md)
- [Investigation protocol](references/investigation-protocol.md)
- [Operations playbooks](references/ops-playbooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance, Operational recommendations]

**Output Format:** [Structured text and JSON results, Markdown summaries, and shell commands or configuration guidance when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the configured Aria Operations targets and available APIs; write operations are audit-logged.]

## Skill Version(s):

2.4.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
