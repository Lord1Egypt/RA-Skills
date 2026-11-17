## Description:

Use for read-only Symantec ZTNA site and connector health, applications, access policies, collections, DNS, identities, cloud integrations and audit logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Security and network operations teams use this skill to inspect Symantec ZTNA site and connector health, affected applications, access configuration, DNS, identities, cloud integrations, and bounded audit-log searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign scanner verdict has medium confidence and does not guarantee zero risk.

Mitigation: Check that the skill's purpose and requested access fit your needs before use.

Risk: A health sample may not cover the full tenant, and reported site or application status does not establish end-user connectivity.

Mitigation: Treat samples as partial indicators and separately verify the relevant tenant and end-user paths.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zw008/skills/symantec-ztna-aiops)
- [Publisher profile](https://clawhub.ai/user/zw008)
- [Project homepage](https://github.com/AIops-tools/Symantec-ZTNA-AIops)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Structured status and audit data, summarized as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only operational queries; health samples are partial, and reported site or application status does not prove end-user connectivity.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
