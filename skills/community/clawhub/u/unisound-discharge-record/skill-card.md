## Description: <br>
Generates a structured discharge record from inpatient medical records using an internal medical language model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical operations teams and healthcare developers use this skill to turn de-identified inpatient record content into a standardized seven-section discharge summary for clinician review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical-record content is sent to a remote model endpoint. <br>
Mitigation: Use only de-identified records in an approved clinical environment, and confirm that the configured model endpoint is authorized for the data. <br>
Risk: Authentication keys can be exposed through command-line use or shell history. <br>
Mitigation: Protect the app key according to local secret-handling policy and avoid entering real credentials in shared shells or logs. <br>
Risk: Prepared text or generated outputs can be saved locally when optional output flags are used. <br>
Mitigation: Save patient-related prepared text or outputs only when retention is intentional, policy-covered, and access-controlled. <br>
Risk: Generated discharge summaries may be incomplete or clinically incorrect. <br>
Mitigation: Require review and approval by a licensed clinician before using generated text in patient care, billing, transfer, or archival workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-discharge-record) <br>
- [Unisound publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Hivoice chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json] <br>
**Output Format:** [UTF-8 discharge-summary text with optional saved JSON or text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated record is organized into seven standard sections: chief complaint, admission status, admission diagnosis, treatment course, discharge diagnosis, discharge status, and discharge instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
