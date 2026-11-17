## Description:

Checks outpatient medical-record history text for missing blood pressure or blood glucose control information and returns whether the record has no defect or has a defect with a reason.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical quality-control teams and developers can use this skill to review de-identified outpatient medical-record text for a specific past-medical-history rule: whether hypertension or diabetes history lacks blood pressure or blood glucose control details. Results are assistive and require clinician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical record text is sent to the configured remote MaaS provider.

Mitigation: Use only de-identified records and install only after organizational approval for sending medical-record text to that provider.

Risk: Prepared medical-record text can be saved locally when the save-prepared option is used.

Mitigation: Do not use save-prepared with real patient records unless the output directory is secured and retention is planned.

Risk: Quality-control results may be incomplete or incorrect for clinical use.

Mitigation: Treat results as assistive and require review by a qualified clinician.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-pmh-missing-bp-glucose)
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [UTF-8 text result with no-defect or defect status and optional reason]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts UTF-8 outpatient record text directly or via prepared pdf, doc, docx, xls, xlsx, csv, txt, or json input; requires an appkey for the configured MaaS provider.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
