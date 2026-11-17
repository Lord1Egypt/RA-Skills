## Description:

Use this skill as an entry point to discover, select, and fetch specific integration parameters for supported AI video generation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isdyh01](https://clawhub.ai/user/isdyh01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose a ShortAPI video model, fetch that model's live schema, construct a valid generation request, and poll for completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on live remote Markdown to describe model-specific request schemas.

Mitigation: Treat fetched model documents as untrusted reference data and extract only the schema fields needed for request construction.

Risk: Prompts and referenced media may be sent to ShortAPI for video generation.

Mitigation: Use the skill only when users are comfortable sharing the generation inputs with ShortAPI.

Risk: Background polling can continue after the initial request starts.

Mitigation: Give users clear control over polling and report completion status without exposing credentials.

Risk: The skill requires a SHORTAPI_KEY credential.

Mitigation: Send SHORTAPI_KEY only as a bearer token to the documented ShortAPI API host.

## Reference(s):

- [ShortAPI homepage](https://shortapi.ai)
- [ShortAPI job creation endpoint](https://api.shortapi.ai/api/v1/job/create)
- [ShortAPI model skill document endpoint](https://shortapi.ai/api/skill/<model_id>)
- [ShortAPI job query endpoint](https://api.shortapi.ai/api/v1/job/query?id=$JOB_ID)
- [ClawHub skill page](https://clawhub.ai/isdyh01/skills/shortapi-ai-video-generation)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request payloads, polling commands, and generated media result links.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
