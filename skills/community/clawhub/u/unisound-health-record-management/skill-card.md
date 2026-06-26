## Description: <br>
Organizes patient-owned health record entries such as profile data, medical history, allergies, surgery history, family history, and medication history into structured summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and patient-facing care workflows use this skill to organize health record inputs and produce a structured record summary. It is for record management and completeness review, not diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive patient records and uploaded document contents are sent to a fixed remote model API. <br>
Mitigation: Use only with informed consent, prefer de-identified data, and confirm retention, deletion, credential handling, and data-use expectations before using real patient data. <br>
Risk: PDF, Office, and image inputs may be processed by broad parsers, converters, or OCR tools. <br>
Mitigation: Avoid untrusted documents unless the runtime isolates file conversion and OCR, and keep optional parser dependencies patched. <br>
Risk: The skill produces health-record summaries and completeness notes in a medical context. <br>
Mitigation: Use outputs as record-management aids only; do not treat them as diagnosis or treatment advice. <br>


## Reference(s): <br>
- [ClawHub listing: unisound-health-record-management](https://clawhub.ai/unisound-llm/unisound-health-record-management) <br>
- [GitEHR patient-owned health record reference](https://gitehr.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls] <br>
**Output Format:** [JSON object containing structured record fields and Markdown narrative text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey bearer token for the remote u1-insuremed endpoint; supports JSON, CSV, Excel, text, PDF, Word, and image inputs when optional parsers are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
