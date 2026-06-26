## Description: <br>
Reviews outpatient chronic disease materials for diabetes or hypertension from OCR-derived medical records and returns a structured decision with reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Claims and operations reviewers can use this skill to review OCR-derived outpatient chronic disease materials for diabetes or hypertension and produce an initial pass, fail, or needs-more-information decision with a reason. The output is assistance for review workflows and should not be treated as medical diagnosis or standalone clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical text can be sent to the configured remote LLM endpoint and saved locally by default. <br>
Mitigation: Use only with authorization for the records and endpoint; add independent redaction if required, restrict output locations, and apply retention and deletion controls. <br>
Risk: The skill output can influence medical insurance review decisions. <br>
Mitigation: Require qualified human review before acting on pass, fail, or needs-more-information decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-chronic-disease) <br>
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Configured medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Structured JSON review response plus natural-language text summary saved as files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey except in dry-run; supports OCR-array JSON and document inputs normalized through the bundled preprocessing entry point.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
