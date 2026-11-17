## Description:

Provides concise definitions and clinical context for medical terms from direct questions, JSON, JSONL, text files, or stdin by calling a configurable medical model API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external evaluators use this skill to submit medical terminology questions and receive model-generated definitions with clinical context. It supports direct CLI questions, structured input files, stdin, and dry-run parsing for integration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical model responses may be mistaken for formal diagnosis or treatment decisions.

Mitigation: Treat output as auxiliary terminology information and route real clinical decisions through approved medical review.

Risk: Questions, optional metadata, and the app key are sent to the configured model API.

Mitigation: Protect the app key, de-identify patient data before use, and follow the organization's approval process for any patient-related input.

Risk: A custom API URL can redirect sensitive content or credentials to an untrusted endpoint.

Mitigation: Use only organization-approved API endpoints and avoid custom --api-url values from untrusted instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-term)
- [Default medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON by default, plain text when --text-only is used, or NDJSON for batches.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write UTF-8 output files; dry-run emits parsed input without calling the API; an app key is required outside dry-run mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
