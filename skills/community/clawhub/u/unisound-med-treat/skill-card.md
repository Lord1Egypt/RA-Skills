## Description:

Creates standardized diagnosis, examination, and treatment guidance frameworks from disease-specific medical question text or structured inputs using an internal medical LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical-workflow integrators use this skill to pass disease-specific case prompts into an internal medical LLM and receive a structured, non-decisional framework for diagnosis, examinations, and treatment principles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical prompts and the provided API key can be sent to a user-configured endpoint.

Mitigation: Use only approved trusted HTTPS endpoints, avoid unnecessary --api-url overrides, and use a dedicated least-privileged API key.

Risk: Raw patient-like input can appear in logs, stdout, or files written through --output.

Mitigation: Do not use real patient identifiers unless the destination service, logs, and output path are approved; de-identify inputs before use.

Risk: Medical model output may be mistaken for a formal clinical decision.

Mitigation: Treat outputs as non-decisional support and require appropriate clinical review before any care-related use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-treat)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON object or NDJSON batch output; optional plain answer text with --text-only]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write UTF-8 JSON or NDJSON to --output; dry-run returns parsed input metadata without calling the model.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
