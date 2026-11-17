## Description:

[QwenCloud] Generates videos using Wan models for text-to-video, image-to-video, first+last-frame transitions, reference-based role-play, and VACE video editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creative automation agents use this skill to generate and edit video clips with QwenCloud Wan models. It supports prompt construction, request-field selection, asynchronous task submission, polling, download handling, and media workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be forwarded to configurable QwenCloud-compatible endpoints.

Mitigation: Use the skill only in trusted workspaces, avoid unreviewed workspace .env files, and set QWEN_BASE_URL only for a trusted HTTPS gateway.

Risk: Local media paths can be uploaded to QwenCloud temporary storage or configured OSS storage.

Mitigation: Treat any image, video, or audio path supplied to the skill as an upload and avoid sending sensitive media unless the destination is approved.

Risk: Optional update-check and package-install prompts can introduce unpinned dependency changes.

Mitigation: Decline or carefully review those prompts unless the install target and version are trusted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cuixiaoyang123/skills/qwencloud-video-generation)
- [Qwen video generation official documentation](https://docs.qwencloud.com/developer-guides/getting-started/video-models)
- [QwenCloud model list](https://www.qwencloud.com/models)
- [QwenCloud pricing](https://docs.qwencloud.com/developer-guides/getting-started/pricing)
- [API supplementary guide](references/api-guide.md)
- [Execution guide](references/execution-guide.md)
- [Request fields by mode](references/request-fields.md)
- [Workflow recommendations](references/workflows.md)
- [Task polling guide](references/polling-guide.md)
- [Local media merging guide](references/merge-media.md)
- [Prompt guide](references/prompt-guide.md)
- [Official documentation sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON request bodies, shell commands, and downloaded media or response files when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit asynchronous QwenCloud API tasks, poll task status, upload local media, and save MP4 plus response JSON files under output/qwencloud-video-generation/.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
