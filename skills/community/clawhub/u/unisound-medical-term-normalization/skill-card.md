## Description:

Normalizes colloquial medical record text into standardized clinical record wording using an internal medical LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical operations teams use this skill to convert de-identified outpatient or inpatient notes from colloquial Chinese into standardized clinical record text for archiving, quality review, reimbursement, and research data preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical records and the API key can be sent to any configured endpoint.

Mitigation: Use only de-identified records, keep credentials separate, and allow only approved HTTPS endpoints for the --base setting.

Risk: Plaintext medical data can appear in stdout, output files, saved prepared text, backups, or logs.

Mitigation: Treat generated outputs and logs as sensitive medical data, restrict file paths and access, and apply retention controls.

Risk: Standardized records may be mistaken for clinical judgment.

Mitigation: Require review by licensed clinical staff before using the normalized text in regulated or patient-facing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-medical-term-normalization)
- [Configured medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [UTF-8 normalized medical record text, with optional JSON or text file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires de-identified input records and a Bearer appkey for the configured medical LLM endpoint.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
