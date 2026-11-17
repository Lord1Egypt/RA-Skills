## Description:

Use this skill as an entry point to discover, select, and fetch specific integration parameters for all supported AI image generation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isdyh01](https://clawhub.ai/user/isdyh01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover ShortAPI image-generation models, fetch model-specific parameter schemas, and construct authenticated generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated external requests can send prompts or image inputs to ShortAPI and may incur generation costs.

Mitigation: Use the skill only for explicit generation jobs, protect SHORTAPI_KEY, and review request payloads before submission.

Risk: Background polling is mandated without clear limits or fresh user control.

Mitigation: Run the skill in an agent environment with visible cancellation or timeout controls and avoid silent indefinite polling.

Risk: Model schemas vary, so guessed parameters can produce invalid requests or unintended behavior.

Mitigation: Fetch the model-specific skill document before constructing each request and include only documented parameters.

## Reference(s):

- [ShortAPI Homepage](https://shortapi.ai)
- [ShortAPI Skill Page](https://clawhub.ai/isdyh01/skills/shortapi-ai-image-generation)
- [ShortAPI Image Generation Job API](https://api.shortapi.ai/api/v1/job/create)
- [ShortAPI Model Skill Document Endpoint](https://shortapi.ai/api/skill/<model_id>)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHORTAPI_KEY and may produce image result URLs after polling the ShortAPI job API.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
