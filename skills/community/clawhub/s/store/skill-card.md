## Description:

Manage a physical store of any kind with opening routines, inventory control, staffing, cash discipline, merchandising, and weekly reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators, managers, and agents supporting brick-and-mortar retail locations use this skill to manage opening and closing routines, inventory accuracy, staffing decisions, merchandising, cash discipline, incidents, and weekly KPI reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local store-operation notes in ~/store/ could contain sensitive payroll, payment card, customer, or employee information if users enter it.

Mitigation: Ask for confirmation before file creation and avoid putting payroll records, payment card data, private customer details, or sensitive employee records into store notes.

Risk: Broad activation could surface store-operation guidance when the user only wants help on explicit request.

Mitigation: Narrow the activation preference during setup if support should engage only when explicitly requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/store)
- [Skill homepage](https://clawic.com/skills/store)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain-language operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown notes under ~/store/ only after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
