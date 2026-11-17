## Description:

Checks outpatient medical-record text for hypertension cases where the highest blood pressure value is missing, using a configured HiVoice MaaS medical LLM to return either no defect or a defect with a reason.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical quality-control reviewers and developers use this skill to screen de-identified outpatient EMR text for a specific hypertension documentation rule before clinician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical-record text is transmitted to the configured remote LLM provider.

Mitigation: Use only de-identified records in an environment approved for that provider and endpoint.

Risk: API credentials may be exposed when passed as command-line arguments on shared systems.

Mitigation: Use protected execution environments and avoid command-line credential passing where process inspection is a concern.

Risk: The optional prepared-text debug output can persist sensitive record content.

Mitigation: Do not use --save-prepared with sensitive records unless the output directory is access-controlled and retention is managed.

Risk: Record text may influence LLM behavior and affect quality-control conclusions.

Mitigation: Keep clinician review in the workflow and treat the skill output as an assistive QC signal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-hypertension-missing-bp)
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm)
- [HiVoice MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [UTF-8 plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns '\u65e0\u7f3a\u9677' or '\u6709\u7f3a\u9677' followed by a reason, and writes the same result to the configured output path.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
