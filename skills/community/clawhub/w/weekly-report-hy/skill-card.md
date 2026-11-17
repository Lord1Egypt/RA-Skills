## Description:

Generates structured, polished Chinese weekly reports from rough work notes while preserving the facts supplied by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users who draft Chinese weekly work reports use this skill to turn rough notes into categorized, professionally worded report text. It is intended for rewriting and structuring user-provided work items without adding unsupported facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may preserve customer names, amounts, internal project names, or personal data from the user's notes.

Mitigation: Ask for redaction before generation when needed and review the report before sharing it.

Risk: Professional polishing can make ambiguous notes appear more complete than the source supports.

Mitigation: Compare the final report against the original notes and remove any wording that implies unverified facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptocxf/skills/weekly-report-hy)
- [Publisher profile](https://clawhub.ai/user/cryptocxf)
- [NPM package](https://www.npmjs.com/package/weekly-report-hy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese weekly report text with bracketed section headings and numbered work items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves sensitive details unless the user asks for redaction.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
