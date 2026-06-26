## Description: <br>
Generates structured initial outpatient medical record content from Chinese doctor-patient dialogue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare developers and clinical operations teams use this skill to convert de-identified Chinese consultation transcripts or supported input files into structured initial-visit record fields for clinician review and downstream systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical dialogue may contain sensitive patient information and is sent to the configured LLM endpoint. <br>
Mitigation: Use only authorized medical dialogue, de-identify patient text before processing, and use only approved base endpoints. <br>
Risk: The app key grants access to the configured LLM service. <br>
Mitigation: Protect the app key and avoid exposing it in logs, shared commands, or committed files. <br>
Risk: Prepared data or generated records can be written to local files when output options are used. <br>
Mitigation: Avoid save-prepared or file outputs unless local storage of medical records is permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-initial-record) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Example dialogue JSON](artifact/example/gen_records.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Structured plain text with optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an app key for the configured LLM service; supported inputs include text, JSON, PDF, document, spreadsheet, and CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
