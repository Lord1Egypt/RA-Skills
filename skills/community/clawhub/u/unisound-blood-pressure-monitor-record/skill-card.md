## Description: <br>
Records patient blood-pressure measurements, structures systolic pressure, diastolic pressure, heart rate, measurement time, and notes, and returns JSON plus a concise Markdown summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-management workflows use this skill to turn blood-pressure readings from JSON, tables, text, documents, or images into standardized records and a patient-facing summary. It is for record keeping and informational summaries, not diagnosis or a substitute for clinician judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive blood-pressure readings, heart rate, timestamps, and notes are sent to a remote medical model. <br>
Mitigation: Use the skill only with appropriate consent and data-handling approval, and provide only the minimum information needed for the record. <br>
Risk: The generated summary may read like health guidance even though the skill is intended for record keeping. <br>
Mitigation: Treat the Markdown output as informational and non-diagnostic; route medical decisions or abnormal readings to qualified clinical review. <br>
Risk: The required app key is a sensitive credential. <br>
Mitigation: Provide the app key through a secret-management mechanism and avoid storing it in prompts, input files, logs, or source control. <br>
Risk: Document and image preprocessing can extract unrelated sensitive content if broad files are supplied. <br>
Mitigation: Use focused input files containing only the intended blood-pressure record fields and review prepared data before remote submission when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-blood-pressure-monitor-record) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [HealthLog](https://healthlog.dev/) <br>
- [Remote medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, text, files] <br>
**Output Format:** [UTF-8 JSON containing structured blood-pressure records and a Markdown text summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write results to a JSON file or stdout. Requires an app key and remote model access; optional preprocessing supports JSON, CSV/XLS, text, PDF/DOC, and image inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
