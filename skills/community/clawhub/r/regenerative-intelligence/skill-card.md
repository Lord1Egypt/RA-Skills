## Description:

Use when designing, reviewing, or operating memory, recall, and pattern-stewardship systems for agentic AI where harm reduction, non-identifiability, consent-scoped recall, and energy restraint are required; this is a specification of invariants, not a runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otherpowers](https://clawhub.ai/user/otherpowers)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and operators use this skill to specify or audit memory and recall systems against non-identifiability, consent scope, honest refusal, energy restraint, and pattern-stewardship requirements. It supports design review and conformance planning rather than installing or running a memory service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readers may mistake the bundle for an implemented memory system or deployed security control.

Mitigation: Treat it as a design checklist only; review any implementation's actual storage, deletion, audit, identity-vault, and user-consent controls before relying on conformance.

Risk: An implementation could claim conformance without test evidence.

Mitigation: Use the bundled conformance checklist and publish criterion-level results, including any unmet criteria and the numeric defaults in force.

Risk: Memory-governance implementations can introduce identity, surveillance, or hidden-storage risk if core controls are omitted.

Mitigation: Require non-identifiability, no behavioral telemetry, Trust Vault separation for execution-only identity, aggregate-only audit, and plainly announced boundaries before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/otherpowers/skills/regenerative-intelligence)
- [Publisher profile](https://clawhub.ai/user/otherpowers)
- [README](artifact/README.md)
- [Skill specification](artifact/SKILL.md)
- [Conformance checklist](artifact/conformance-checklist.md)
- [Threat model](artifact/threat-model.md)
- [Metadata schema](artifact/metadata-schema.md)
- [Energy accounting](artifact/energy-accounting.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance, specifications, schemas, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no code execution, API calls, credentials, or persistent storage.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact status says 1.1.0 specification draft)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
