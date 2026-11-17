## Description:

Alerts chronic-care users to abnormal patient indicators by checking caller-provided thresholds and generating explanatory follow-up guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Patients, care teams, and developers can use this skill to process chronic-disease indicator records, flag values outside configured thresholds, and produce a structured alert plus patient-facing guidance. It is an alerting aid, not a diagnostic or treatment-planning system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical indicator data is sent to an external model service.

Mitigation: Use the skill only where users are allowed to send this data to the listed provider; require consent and minimize or redact inputs for patient-facing use.

Risk: The fallback shared preprocessor can run unreviewed local code.

Mitigation: Remove the fallback or pin it to trusted, reviewed code before installation or deployment.

Risk: Local document and OCR processing can expand the file-processing attack surface.

Mitigation: Run document and OCR tools in a sandbox with restricted file access.

Risk: Generated medical text may be incorrect or exceed the skill's alerting boundary.

Mitigation: Validate generated medical text against approved rules and keep use limited to alerts rather than diagnosis or treatment planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-abnormal-indicator-alert)
- [Open Wearables](https://openwearables.io/)
- [Hivoice medical chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [UTF-8 JSON containing structured alert data and Markdown natural-language analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires caller-provided thresholds and an appkey; the skill does not include built-in medical thresholds.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
