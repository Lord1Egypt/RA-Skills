## Description:

Generates structured outpatient initial medical record information from Chinese doctor-patient dialogue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, clinical documentation teams, and healthcare developers can use this skill to convert de-identified Chinese outpatient doctor-patient dialogue into structured initial-record sections for clinician review and downstream parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical dialogue may be sent to a configured API endpoint.

Mitigation: Use only de-identified inputs in an environment approved for medical data and keep the API base URL fixed to a trusted HTTPS endpoint.

Risk: The required bearer key may be exposed if handled in an unsafe runtime or sent to an untrusted endpoint.

Mitigation: Protect the appkey as a secret, restrict where the skill can run, and do not override the API base URL without approval.

Risk: Prepared patient dialogue can be written locally when debug saving is enabled.

Mitigation: Avoid --save-prepared unless a local debug copy is intentionally required and covered by the data-handling policy.

Risk: Generated medical records may contain inaccurate or incomplete clinical information.

Mitigation: Require clinician review before using generated records operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-initial-record)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)
- [Example dialogue input](artifact/example/dialogue.txt)
- [Example JSON input](artifact/example/gen_records.json)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Structured plain text with one medical-record field per line; optionally written to an output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated through a configured chat-completions API using the selected model and may be printed to stdout or written to a provided path.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
