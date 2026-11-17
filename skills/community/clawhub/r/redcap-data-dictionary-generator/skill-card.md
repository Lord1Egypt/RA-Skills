## Description:

Generates REDCap-compatible CSV data dictionaries from clinical trial CRF, protocol, questionnaire, or survey documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenlcj](https://clawhub.ai/user/kenlcj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical data teams use this skill to convert study CRFs, protocols, questionnaires, and survey forms into REDCap data dictionary CSV files for import and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate document conversion capability or produce REDCap CSV fields that do not faithfully match clinical source documents.

Mitigation: Use it only for local, user-approved CSV generation and manually validate generated data dictionaries against the original source document before import.

Risk: Clinical-derived CSV output could expose sensitive study or patient-related information if sent through Feishu or logged during processing.

Mitigation: Avoid Feishu sending unless recipient and data handling are explicitly approved, restrict log access, and run processing in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenlcj/skills/redcap-data-dictionary-generator)
- [OpenClaw homepage metadata](https://clawhub.ai/kenlcj/redcap-data-dictionary-generator)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and Python-generated REDCap CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated CSV output should be manually validated against the source document before REDCap import.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
