## Description:

Scans embodied AI agent configurations at the edge and returns a compliance report for CPAA-related identity, address-domain, temperature-lock, and hardware-lock checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check an embodied AI agent configuration before deployment and receive a structured pass/fail compliance report. The result should be treated as advisory unless paired with independent hardware-state and safety validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be mistaken for an authoritative physical actuator safety gate.

Mitigation: Use it as an advisory helper unless independent schema validation, trusted hardware-state checks, complete identity and address verification, and supervised shutdown procedures are also in place.

Risk: Under-scoped validation can create false confidence about real-world actuator safety.

Mitigation: Require a separate safety review before wiring its pass/fail result to actuator startup or shutdown decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/taohuayuan-cpaa-core)
- [Publisher profile](https://clawhub.ai/user/spacesq)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [Structured JSON compliance report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes individual check results, a compliance score, and a final certification or rejection status.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-06-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
