## Description:

Production-ready Volcengine/ARK video generation for prompt-to-video, image-to-video, and draft-video refinement, including job submission, polling, payload inspection, and result downloads with Seedance-compatible models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to run real Volcengine/ARK video generation workflows from prompts, reference images, or draft videos, then inspect task payloads and retrieve generated video outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits prompts and selected media to a remote video API.

Mitigation: Use only prompts and media intended for upload, and configure trusted HTTPS Volcengine/ARK endpoints before running tasks.

Risk: Broad endpoint and API key fallbacks can send requests to an unintended compatible endpoint.

Mitigation: Prefer VOLCENGINE_VIDEO_ENDPOINT or ARK_BASE_URL and VOLCENGINE_API_KEY or ARK_API_KEY; avoid OPENAI_* fallbacks for this skill.

Risk: Generated outputs may be downloaded automatically to the local filesystem.

Mitigation: Disable automatic downloads or set a controlled download directory when local file placement needs review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jinhuadeng/skills/volcengine-video-studio)
- [API notes](references/api-notes.md)
- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON task results, and local file paths for downloaded videos when enabled.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit prompts and selected media to remote Volcengine/ARK endpoints, poll task status, print raw JSON payloads for debugging, and save generated media locally.]

## Skill Version(s):

0.1.4 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
