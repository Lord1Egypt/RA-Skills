## Description:

Use this skill as an entry point to discover, select, and fetch specific integration parameters for all supported AI music generation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isdyh01](https://clawhub.ai/user/isdyh01)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to discover supported ShortAPI music generation models, fetch model-specific schemas, construct valid requests, and poll for generated music results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, job requests, and status queries are sent to ShortAPI using SHORTAPI_KEY.

Mitigation: Use this skill only when ShortAPI is an intended service provider, keep SHORTAPI_KEY in the environment, and avoid exposing credentials in prompts, callbacks, or generated payloads.

Risk: Generated media URLs may be rendered inline in environments with strict content or HTML policies.

Mitigation: Review result URLs before inline rendering and allow only authorized shortapi.ai or known CDN domains with sanitized media tags.

Risk: Asynchronous music generation jobs can lead to excessive polling if not bounded.

Mitigation: Stop background polling after five minutes and notify the user if the job has not completed.

## Reference(s):

- [ShortAPI homepage](https://shortapi.ai)
- [ClawHub skill page](https://clawhub.ai/isdyh01/skills/shortapi-ai-music-generation)
- [ShortAPI job creation endpoint](https://api.shortapi.ai/api/v1/job/create)
- [ShortAPI model skill document endpoint](https://shortapi.ai/api/skill/suno/suno-v5/generate)
- [ShortAPI job query endpoint](https://api.shortapi.ai/api/v1/job/query?id=$JOB_ID)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHORTAPI_KEY and uses bounded polling for asynchronous music generation jobs.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
