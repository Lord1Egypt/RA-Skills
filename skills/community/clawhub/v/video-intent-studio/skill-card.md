## Description:

Guide staged text-to-video generation from a rough user idea to ranked video type options, parameter tuning, prompt preview, and final Volcengine Ark video generation via bundled helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxxxxxxxxxxxxxxxxxx20gex](https://clawhub.ai/user/xxxxxxxxxxxxxxxxxxx20gex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a rough video idea into ranked video directions, adjustable generation parameters, a transparent prompt preview, and a confirmed Ark video generation request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can send the Ark API key and final prompt to a configurable task endpoint.

Mitigation: Leave ARK_VIDEO_TASKS_URL unset unless the endpoint is trusted and verified, and use a limited-scope Ark key with quota controls or rotation.

Risk: Final prompts are sent to Volcengine Ark during generation.

Mitigation: Review the prompt preview before confirmation and avoid submitting sensitive or confidential content.

Risk: API keys could be exposed through shared logs, files, or command history.

Mitigation: Prefer environment variables for credentials and avoid placing Ark keys in prompts, shared files, or copied command output.

## Reference(s):

- [Usage Guide](references/usage-guide.md)
- [Video Types](references/video-types.md)
- [Volcengine Ark video task endpoint](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files, guidance]

**Output Format:** [Markdown guidance with JSON script outputs and an optional MP4 video file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow keeps prompt previews visible and requires explicit user confirmation before generation.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
