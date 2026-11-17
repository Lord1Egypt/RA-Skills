## Description:

Generates targeted rework or repair disposition plans for nonconforming products based on objective defect information and customer requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, process, customer quality, MRB, and manufacturing teams use this skill to turn specific nonconformance evidence and customer acceptance requirements into controlled rework, repair, or scrap disposition guidance. It is intended for batch- or item-specific planning, not generic SOP generation or replacement of authorized MRB/customer approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated local reports may contain customer, product, and quality details.

Mitigation: Confirm the output location before generation and handle report files according to the user's confidentiality and retention requirements.

Risk: The artifact references a report-building helper that may write files locally.

Mitigation: Run only trusted, reviewed helper scripts from the installed skill package or approved local tooling, and check for existing files before writing reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-rework-repair-plan)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-rework-repair-plan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured text and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires objective nonconformance information and customer requirements before generating a disposition plan.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
