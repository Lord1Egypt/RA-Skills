## Description:

Jimeng AI Image Generator helps agents create images and videos through the Volcengine Jimeng API, with prompt templates for commerce, social, design, and video scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to ask an agent to submit Jimeng text-to-image, video-generation, and task-query jobs with saved files or media URLs. It is suited for marketing, social media, design, and short-video asset generation when Volcengine processing is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated-media requests are sent to Volcengine.

Mitigation: Avoid sensitive prompts or proprietary source material unless Volcengine handling is acceptable for the use case.

Risk: Jimeng AccessKeyId and SecretAccessKey are required for authentication.

Mitigation: Store credentials only in the intended OpenClaw token manager and avoid copying them into prompts, logs, or shared files.

Risk: Generated images may be written to local output paths.

Mitigation: Use explicit output paths in private directories when generated content should not be exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luis1213899/skills/xingxiaolu-jimeng)
- [Prompt template library](references/prompts-templates.md)
- [Prompt template source](https://www.tahou.com/article/203607417559502853)
- [Volcengine Visual API endpoint](https://visual.volcengineapi.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime scripts emit task IDs, media URLs, and saved file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local image files or return media URLs after Volcengine processing.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
