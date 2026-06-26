## Description: <br>
Provides a patient-facing post-operative rehabilitation function self-assessment workflow based on survey and questionnaire inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can collect post-operative rehabilitation questionnaire responses, calculate basic scores, and generate a Markdown interpretation through an external medical model. The skill is limited to self-reported assessment support and is not a diagnosis or substitute for professional evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health assessment data may be sent to an external model provider without clear disclosure, consent, retention, or deletion controls. <br>
Mitigation: Use only with explicit user disclosure and consent; document what fields and files are transmitted; prefer sandboxed or local processing for sensitive health data and define retention and deletion handling. <br>
Risk: Broad document, spreadsheet, text, and image inputs can contain unintended patient or regulated data. <br>
Mitigation: Limit accepted files to the minimum necessary, review prepared JSON before API calls, and avoid uploading regulated patient data unless appropriate governance controls are in place. <br>
Risk: The skill requires a sensitive appkey bearer token for model access. <br>
Mitigation: Use a scoped credential, keep it out of source files and logs, rotate it regularly, and revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [ResearchKit surveys/questionnaires reference](https://github.com/ResearchKit/ResearchKit) <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-function-self-assessment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [UTF-8 JSON containing structured assessment data and Markdown natural-language interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey bearer token; supports JSON plus document, table, text, and image inputs through preprocessing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
