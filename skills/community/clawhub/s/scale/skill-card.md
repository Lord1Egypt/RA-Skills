## Description:

Scale systems, software architecture, and companies with bottleneck mapping, staged leverage plans, and risk-aware execution loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, engineering leaders, operators, and company builders use this skill to diagnose scaling bottlenecks in systems, software architecture, teams, and go-to-market capacity. It helps turn those diagnoses into staged leverage plans with measurable objectives, guardrails, and rollback criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local scaling memory under ~/scale/ could retain sensitive company, architecture, bottleneck, guardrail, or escalation context if the user records it there.

Mitigation: Do not store secrets, credentials, payment data, or sensitive identifiers; review or delete ~/scale/ when durable scaling memory is not desired.

Risk: Planning recommendations for systems, architecture, teams, or go-to-market capacity could be incomplete or mismatched to the user's real constraints.

Mitigation: Validate recommendations against current metrics and domain expertise, use staged tests with guardrails and rollback criteria, and require explicit user approval before executing changes.

## Reference(s):

- [Scale Frameworks on ClawHub](https://clawhub.ai/ivangdavila/skills/scale)
- [Scale Frameworks Homepage](https://clawic.com/skills/scale)
- [Setup - Scale Frameworks](artifact/setup.md)
- [Scale Diagnostic](artifact/scale-diagnostic.md)
- [System Scale Framework](artifact/system-scale-framework.md)
- [Architecture Scale Framework](artifact/architecture-scale-framework.md)
- [Company Scale Framework](artifact/company-scale-framework.md)
- [Execution Cadence](artifact/execution-cadence.md)
- [Memory Template - Scale Frameworks](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with diagnostics, checklists, staged plans, scorecards, and memory templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning-focused output; may use local memory under ~/scale/ and requires explicit user approval before applying technical or organizational changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
