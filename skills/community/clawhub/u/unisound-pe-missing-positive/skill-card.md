## Description:

Checks outpatient medical records for missing key positive physical-exam findings and returns whether a defect is present with the reason when applicable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical quality-control teams and developers use this skill to review de-identified outpatient records for one medical-record rule: whether physical-exam notes omit major positive findings relevant to selected diagnoses. Results are advisory and require clinician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive medical-record text and a bearer app key to a user-supplied model endpoint.

Mitigation: Run only in a controlled clinical environment with de-identified records, an approved HTTPS endpoint, and a narrowly scoped app key.

Risk: Prepared or result files may contain clinical content if saved to disk.

Mitigation: Protect output directories and avoid --save-prepared unless the destination is authorized for sensitive clinical data.

Risk: The quality-control result is advisory and may be incomplete or incorrect.

Mitigation: Require review by a licensed clinician before using findings in clinical or operational decisions.

Risk: The multi-format entry point depends on shared preprocessing code that must be trusted in the deployment environment.

Mitigation: Install the shared preprocessing directory from a trusted source and scan it before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-pe-missing-positive)
- [HiVoice MaaS OpenAI-compatible chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [UTF-8 plain text result with optional console messages and saved text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs either no defect or defect with a reason; may save prepared text when requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
