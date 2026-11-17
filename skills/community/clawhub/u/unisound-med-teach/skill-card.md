## Description:

Generates clinical teaching case responses from question text or structured input by calling a configurable internal medical LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical education teams use this skill to pass de-identified case prompts to a medical model and receive structured teaching-case responses for learning objectives, differential points, and ethical boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical teaching prompts and API credentials can be sent to a configured model endpoint.

Mitigation: Use only trusted --api-url values, provide scoped API keys, and submit de-identified teaching prompts.

Risk: Generated outputs may contain sensitive prompt or case details when written to shared or backed-up storage.

Mitigation: Avoid real patient identifiers and restrict --output destinations and file access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-teach)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Default medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON by default; plain answer text with --text-only; NDJSON for batches.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write UTF-8 output files; dry-run returns parsed question metadata without calling the model.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
