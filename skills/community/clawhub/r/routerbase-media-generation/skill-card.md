## Description:

Build image, video, and audio generation workflows on RouterBase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenlee123](https://clawhub.ai/user/zenlee123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to design RouterBase media generation workflows, choose image, video, audio, and speech endpoints, handle synchronous and asynchronous responses, and produce integration guidance with request examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source image URLs, callback URLs, and task metadata may be sent to or handled around RouterBase as part of media generation.

Mitigation: Send only data appropriate for the user's rights and product policy, and verify current RouterBase model, retention, and cost behavior before production use.

Risk: API keys, private media URLs, or user data could be exposed through logs or examples.

Mitigation: Keep the RouterBase API key in environment variables and avoid logging secrets, private media URLs, or sensitive user data.

Risk: Generated media can expire before the application stores it.

Mitigation: Download and persist generated media on the application side before the documented retention window ends.

Risk: Model IDs and media parameters can be model-dependent or stale.

Mitigation: Verify model IDs against the live catalog when credentials are available and validate requested parameters against the selected model before use.

## Reference(s):

- [RouterBase Media Generation Notes](references/routerbase-media.md)
- [RouterBase documentation](https://docs.routerbase.com)
- [RouterBase image API reference](https://docs.routerbase.com/api-reference/images)
- [RouterBase overview](https://docs.routerbase.com/overview)
- [ClawHub skill page](https://clawhub.ai/zenlee123/skills/routerbase-media-generation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, JavaScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint selection, model ID validation notes, sync or async handling, storage and retention guidance, and minimal request examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
