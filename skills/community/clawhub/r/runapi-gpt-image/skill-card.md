## Description:

Generate and edit images with GPT Image through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to generate or edit image assets with GPT Image through RunAPI, either as a one-off CLI workflow or as SDK-backed application integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, referenced media files, and generated outputs may be sent through RunAPI and may incur account costs.

Mitigation: Install and use the skill only after confirming trust in RunAPI, and review request contents before submitting paid generation or editing tasks.

Risk: Authentication failures or ambiguous login state can lead to incomplete task execution.

Mitigation: Use an environment API key or explicit token import, verify authentication status before submission, and use browser login only by user choice.

Risk: A generated task response may succeed without providing every requested image deliverable.

Mitigation: Validate complete task results, download every requested media output, and confirm each file is non-empty with the expected image MIME type.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-gpt-image)
- [RunAPI GPT Image model overview](https://runapi.ai/models/gpt-image.md)
- [RunAPI OpenAI provider overview](https://runapi.ai/providers/openai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI GPT Image SDK](https://github.com/runapi-ai/gpt-image-sdk)
- [RunAPI publisher profile](https://clawhub.ai/user/runapi-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request examples, SDK integration guidance, and generated image files from RunAPI task responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts, referenced media files, generated outputs, authentication data, and account usage may pass through RunAPI; downloaded image deliverables should be checked for non-empty content and expected image MIME type.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
