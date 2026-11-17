## Description:

Generates a structured treatment-process summary from medical progress records by calling an internal medical large language model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical documentation teams and developers use this skill to turn de-identified inpatient progress notes, ward rounds, and related records into a coherent treatment-process summary for medical record filing, homepage completion, and case statistics. Generated medical text should be reviewed by a licensed clinician before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive medical records and can send record text plus an API key to a configured model endpoint.

Mitigation: Install only in approved medical-record environments, use de-identified inputs, and keep --base pointed at a trusted HTTPS endpoint.

Risk: Passing reusable credentials on the command line can expose them through process listings, shell history, or logs.

Mitigation: Use short-lived or environment-approved credentials and avoid operational patterns that log command-line arguments.

Risk: The --save-prepared option can retain plaintext intermediate medical text.

Mitigation: Use --save-prepared only when plaintext retention is explicitly approved, and store outputs under the organization's medical-data handling controls.

Risk: Generated treatment summaries may contain omissions or clinically incorrect phrasing.

Mitigation: Require licensed clinician review before using generated text in medical records or downstream clinical workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-treatment-process)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Hivoice medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [UTF-8 treatment-process text, optionally saved as plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts pdf, doc, docx, xls, xlsx, csv, txt, and json inputs; requires an app key for the medical model API; can optionally save preprocessed plaintext for debugging.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
