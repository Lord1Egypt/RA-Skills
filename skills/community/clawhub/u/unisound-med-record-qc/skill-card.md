## Description:

Supports medical record entity extraction, chart content quality control, clinical pathway quality control, and radiology report text quality control through a configurable medical LLM call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and healthcare system integrators use this skill to submit medical-record or medical-report prompts and receive quality-control conclusions or structured extraction results for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted medical records or reports may leave the local machine when the model endpoint is called.

Mitigation: Install only where operators understand this data flow, de-identify real patient data first, and follow approved healthcare data-handling procedures.

Risk: The configurable API URL can direct medical text and credentials to an unintended destination.

Mitigation: Use a trusted HTTPS endpoint and avoid overriding --api-url unless the endpoint and credential scope are approved.

Risk: The app key used for model access is sensitive.

Mitigation: Treat the app key as a secret and provide it only in controlled execution environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-record-qc)
- [Default model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object by default; optional plain text answer with --text-only; batch output uses NDJSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task metadata, source input details, model name, record index, and model answer text.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
