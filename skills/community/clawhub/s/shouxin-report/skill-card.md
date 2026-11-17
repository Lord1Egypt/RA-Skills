## Description:

Guides agents through a fixed-template small-business bank credit investigation report workflow, from material intake and extraction to drafting, financial analysis, examiner-style review, final audit, and revision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jieszs](https://clawhub.ai/user/jieszs)

### License/Terms of Use:

MIT-0

## Use Case:

Bank credit-report teams and their agents use this skill to prepare, review, and revise fixed-template small-business credit investigation reports while preserving Excel structure and separating customer supplement requests from report content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive borrower financial materials.

Mitigation: Use approved data-handling controls, limit inputs to the active matter, and review outputs against source materials before sharing or filing.

Risk: The skill includes continuous-update guidance that could modify an installed skill from project experience.

Mitigation: Remove or gate skill updates so changes require explicit human review and cannot persist customer-derived details.

Risk: Fixed Excel templates can be damaged if formulas, merged cells, headings, or disclosure blocks are changed.

Mitigation: Keep a separate template-skeleton check and formula-retention check before final write-back.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jieszs/skills/shouxin-report)
- [Publisher profile](https://clawhub.ai/user/jieszs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown or workbook-ready report content with structured extraction tables, checklist text, and review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce an updated report draft or final workbook copy, a separate customer supplement checklist, structured extraction results, and a repair plan before final write-back.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
