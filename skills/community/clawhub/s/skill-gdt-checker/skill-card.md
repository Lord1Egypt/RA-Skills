## Description:

Checks GD&T annotation completeness and compliance on mechanical drawings, using ASME Y14.5 and GB geometric tolerancing knowledge to generate checklists and issue lists for missing annotations, datum-system errors, and symbol misuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Design, manufacturing, quality, and dimensional engineers use this skill to review GD&T annotations before drawing release, supplier drawing review, drawing conversion, or first-article inspection. It produces a practical review checklist and issue list, while leaving final design authority, measurement validation, and company-standard interpretation to responsible engineers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GD&T review guidance may be incomplete or unsuitable as final design authority for a specific product, drawing standard, or company practice.

Mitigation: Review the skill output against the applicable ASME, GB, customer, and company standards before release or inspection planning.

Risk: The skill reviews annotation-level completeness and compliance, not CAD geometry, tolerance-stack behavior, or physical measurement results.

Mitigation: Use CAD, tolerance analysis, fixture planning, and CMM or other inspection processes for geometric validation and measurement decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-gdt-checker)
- [Server-resolved GitHub source](https://github.com/duding-engicool/skill-gdt-checker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown checklist and issue report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May mark missing functional requirements, datum definitions, or standard-specific details as pending confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
