## Description:

Reviews Chinese engineering and construction documents in DOCX, text-based PDF, XLSX, or XLSM format to extract grounded project facts, contacts, schedules, quantities, safety measures, missing items, conflicts, and review questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lantianbaicai](https://clawhub.ai/user/lantianbaicai)

### License/Terms of Use:

MIT-0

## Use Case:

Engineering, construction, and project-review users use this skill to pre-review Chinese project documents, extract locally grounded evidence, identify conflicts or missing information, and prepare concise questions for human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Excel output can carry untrusted spreadsheet formulas.

Mitigation: Run the skill in an isolated environment and use --no-excel for documents from untrusted parties unless formula escaping is added.

Risk: Reports and extracted text may include sensitive project, customer, schedule, quantity, contact, or contract-relevant details.

Mitigation: Choose a private output directory, keep generated artifacts local, and use --skip-extracted-text when full extracted source text is not needed.

## Reference(s):

- [Review Rules](references/review-rules.md)
- [Output Schema](references/review-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, spreadsheet, shell commands, guidance]

**Output Format:** [Markdown review report, structured JSON, optional XLSX review table, and optional extracted-text Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file outputs; extracted text and reports may contain sensitive project, customer, schedule, quantity, contact, or contract-relevant data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
