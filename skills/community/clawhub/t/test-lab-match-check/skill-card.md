## Description:

Screens medical-device test items and laboratory qualification considerations before test submission using an offline, deterministic checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Medical-device developers and regulatory teams use this skill to draft test-item checklists, identify laboratory accreditation checks, and flag missing inputs before submission. Results require review against current official standards and the laboratory's actual accreditation scope.

### Deployment Geography for Use:

China, European Union, and United States (supported destination inputs)

## Known Risks and Mitigations:

Risk: Outdated or incomplete test-item guidance could be mistaken for a regulatory determination.

Mitigation: Use the checklist as a starting point and verify applicable current official standards and requirements with a qualified reviewer.

Risk: Generic laboratory qualification suggestions do not confirm accreditation for a particular test.

Mitigation: Check the laboratory's current accreditation scope and report acceptance for each proposed test before submission.

Risk: Unnecessary agent tool permissions could broaden access beyond the offline workflow.

Mitigation: Limit execution to the local Python script; do not grant WebFetch or Write access for routine screening.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/test-lab-match-check)
- [Skill usage and limitations](SKILL.md)
- [Package license and scope notice](LICENSE.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON checklist or human-readable summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes suggested tests, qualification checks, warnings, and status codes 0/1/2; does not certify a laboratory or replace regulatory review.]

## Skill Version(s):

1.0.1 (source: ClawHub release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
