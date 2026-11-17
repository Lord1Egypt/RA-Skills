## Description:

Use this skill when a veterinarian, vet technician, or resident needs to build a patient-specific draft anesthesia plan with weight-based dose ranges, monitoring and recovery protocols, an emergency-drug worksheet, and an equipment checklist for licensed-veterinarian review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Veterinary teams use this skill to gather case details and draft anesthesia planning material for scheduled or emergency procedures. It structures protocol modifications, dose ranges, monitoring, recovery, emergency-drug worksheets, and equipment checks for attending veterinarian review and sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports high-stakes veterinary anesthesia planning and may produce incorrect or incomplete clinical guidance if case facts, formularies, or dose references are wrong.

Mitigation: Require the attending veterinarian to verify every dose and source against the practice formulary, review the complete draft, and sign before any drug is drawn or administered.

Risk: Clinical case details may contain sensitive patient or owner information.

Mitigation: Provide only the minimum necessary clinical details and avoid owner PII unless essential.

Risk: Using an estimated or historical body weight can make calculated doses unsafe.

Mitigation: Use the current measured day-of-procedure weight before finalizing any dose; otherwise keep dose calculations marked for recalculation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/veterinary-anesthesia-plan)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft anesthesia plan with tables, checklists, evidence matrix, unresolved questions, and sign-off block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Every plan is labeled as a draft for licensed veterinarian review before administration.]

## Skill Version(s):

0.1.1 (source: server release metadata and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
