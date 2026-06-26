## Description: <br>
Interprets basic lab-report and ECG text, identifies abnormal indicators, explains clinical significance, flags critical values, and returns structured JSON plus a natural-language summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Primary-care and community clinicians use this skill as clinical decision support for reviewing lab reports and ECG descriptions. It helps summarize abnormal findings and follow-up suggestions, while leaving diagnosis and treatment decisions to licensed clinicians. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive lab-report contents are sent to a configured remote API, and the security evidence notes that code does not perform de-identification despite privacy claims. <br>
Mitigation: Remove names, IDs, phone numbers, addresses, and other identifiers before use, verify the provider and base URL, and use the output only as clinical decision support. <br>
Risk: Generated clinical interpretations may be incomplete or misleading if report text, reference ranges, or patient context are missing. <br>
Mitigation: Have a licensed clinician review the JSON findings, urgency flags, and follow-up suggestions before relying on them for patient care. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-lab-report-interpret) <br>
- [Configured remote model API](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON followed by a natural-language summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the interpreted report to a file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
