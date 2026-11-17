## Description:

Generate and edit images with Qwen Image through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to create, edit, remix, or transform images with Qwen Image through RunAPI, either as a one-off CLI task or as guidance for SDK integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party RunAPI CLI distributed through a Homebrew tap.

Mitigation: Review the tap and CLI source before installing, and prefer a pinned or otherwise verified CLI version where possible.

Risk: The workflow can submit potentially billable RunAPI jobs under the user's account.

Mitigation: Authenticate with a narrowly scoped RunAPI credential, submit each task once, preserve the task response, and avoid replacement submissions without user authorization.

Risk: Image generation or editing may upload user-provided media to RunAPI.

Mitigation: Provide only media intended for the requested image task and verify every returned deliverable before reporting completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-qwen-image)
- [RunAPI Qwen Image model page](https://runapi.ai/models/qwen-image)
- [RunAPI Qwen Image documentation](https://runapi.ai/models/qwen-image.md)
- [RunAPI Alibaba provider overview](https://runapi.ai/providers/alibaba.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Qwen Image SDK integration](https://github.com/runapi-ai/qwen-image-sdk)
- [Qwen Image edit image operation](https://runapi.ai/models/qwen-image/edit-image.md)
- [Qwen Image remix image operation](https://runapi.ai/models/qwen-image/remix-image.md)
- [Qwen Image text to image operation](https://runapi.ai/models/qwen-image/text-to-image.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce request JSON, task and result handling instructions, SDK integration guidance, and verified downloaded image files when the agent executes the workflow.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
