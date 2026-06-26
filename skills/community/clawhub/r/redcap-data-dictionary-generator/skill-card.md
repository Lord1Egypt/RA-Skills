## Description: <br>
Converts clinical trial CRF, protocol, questionnaire, and survey documents into REDCap-compatible data dictionary CSV output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenlcj](https://clawhub.ai/user/kenlcj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to transform uploaded clinical-study forms, protocols, questionnaires, or survey documents into REDCap data dictionary CSV files for import and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated clinical-study CSV output may be sent through Feishu without a clearly documented recipient, consent process, or privacy control. <br>
Mitigation: Use Feishu delivery only when the workflow intentionally requires it; confirm the recipient or channel and authorization before sharing clinical, patient-related, or institutional documents. <br>
Risk: Clinical or patient-related source documents may contain sensitive identifiers or institutional data. <br>
Mitigation: Prefer local CSV output when sharing is not required, and review generated fields and identifier markings before importing or distributing the data dictionary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenlcj/redcap-data-dictionary-generator) <br>
- [Publisher profile](https://clawhub.ai/user/kenlcj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and REDCap data dictionary CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated CSV files, REDCap field metadata, validation choices, branching logic, and previews of parsed document content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
