## Description:

Redcap Crf Generator converts clinical trial CRF, protocol, questionnaire, or survey documents into REDCap data dictionary CSV files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenlcj](https://clawhub.ai/user/kenlcj)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical data managers, researchers, and agents working with allowed CRF, protocol, questionnaire, or survey documents use this skill to create REDCap import-ready data dictionary CSVs. It helps identify forms, sections, field types, validation rules, branching logic, calculated fields, file upload fields, and REDCap-compatible variable names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical data or generated CSVs could be shared through Feishu without explicit recipient, consent, or privacy controls.

Mitigation: Use local-only CSV output by default, process only documents the user is allowed to handle, and send files through Feishu only after recipient and approval are explicit.

Risk: Generated CSVs may contain sensitive fields or content that is unsafe to open directly in spreadsheet software or import into REDCap.

Mitigation: Inspect generated CSVs before spreadsheet use or REDCap import, and confirm identifier fields, validation rules, and branching logic against the source CRF.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenlcj/skills/redcap-crf-generator)
- [OpenClaw metadata homepage](https://clawhub.ai/skills/redcap-crf-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python commands and REDCap-compatible CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated CSV data dictionaries should be reviewed before opening in spreadsheet software or importing into REDCap.]

## Skill Version(s):

1.3.0 (source: server release metadata; bundled OpenClaw metadata says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
