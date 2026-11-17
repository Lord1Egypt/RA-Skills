## Description:

Supports read-only investigation of on-premises Symantec EDR appliances, incidents, events, entities, threat feeds, policy lists, and sandbox results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and EDR operators use this skill to inspect on-premises Symantec EDR appliances and review incidents, events, entities, threat feeds, policy lists, and sandbox results. Treat missing, partial, and unverified responses as unknown when drawing conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing, partial, or unverified appliance responses could be mistaken for a healthy state or zero findings.

Mitigation: Treat those responses as unknown and check the verification status before drawing conclusions.

Risk: Installing a skill from an untrusted source may not suit the intended environment, even when the reported scan is clean.

Mitigation: Review the publisher and confirm the skill fits your use case before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zw008/skills/symantec-edr-aiops)
- [Project homepage (Clawdis metadata)](https://github.com/AIops-tools/Symantec-EDR-AIops)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text summaries and structured EDR response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only investigation; results depend on the appliance response and its verification status.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
