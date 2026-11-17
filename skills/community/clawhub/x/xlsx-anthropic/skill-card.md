## Description:

Use this skill when a spreadsheet file is the primary input or output, including creating, reading, editing, fixing, converting, formatting, charting, or cleaning .xlsx, .xlsm, .csv, and .tsv files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Proprietary Anthropic Terms of Service

## Use Case:

Developers and spreadsheet-focused agents use this skill to produce or modify spreadsheet deliverables with formulas, formatting, data cleanup, and recalculation checks. It is suited for workbook creation, spreadsheet repair, tabular data cleanup, and financial model formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes under-disclosed Word and PowerPoint document-processing code in addition to spreadsheet workflows.

Mitigation: Review the bundled Office helpers and remove DOCX/PPTX functionality before using the skill on sensitive documents.

Risk: The LibreOffice recalculation workflow modifies the LibreOffice profile and includes runtime setup that may be inappropriate for sensitive environments.

Mitigation: Use the skill in a contained workspace and review the LibreOffice setup and LD_PRELOAD shim before installation.

Risk: Processing untrusted Office files can expose the agent environment to unsafe document content or unexpected parser behavior.

Mitigation: Avoid untrusted Office files or handle them only in an isolated workspace with review before opening or recalculating them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell snippets; spreadsheet files as deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recalculation helper returns JSON status and error summaries for spreadsheet formulas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
