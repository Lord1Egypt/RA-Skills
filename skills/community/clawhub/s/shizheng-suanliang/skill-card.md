## Description:

Estimates municipal pipeline length bands, pipe diameter bands, well counts, road area bands, and pavement material lists from municipal geometry contracts; it does not replace bill-of-quantities preparation or settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Developers and municipal quantity estimators use this skill to turn a municipal geometry contract into planning-level quantity estimates and a reviewable list of missing evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified contract data or guessed coordinate units could make quantity estimates unreliable.

Mitigation: Review the contract-integrity and coordinate-unit checks before installation or use, and confirm the source contract and units from trusted evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lisong2003-lgtm/skills/shizheng-suanliang)
- [Bus contract reference](references/bus-contract.md)
- [Quantity takeoff rules](references/on-demand.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, CSV]

**Output Format:** [JSON, Markdown, and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning estimates use a stated uncertainty band; all quantities are marked non-final, and missing evidence is reported rather than filled with defaults.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact SKILL.md reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
