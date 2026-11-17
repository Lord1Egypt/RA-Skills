## Description:

Create vertical three-beat debunk videos with timed English captions for a "you think X, actually Y, but Z" structure using WeryAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent users use this skill to turn a topic or X/Y/Z brief into a short vertical debunk video plan, submit it to WeryAI after explicit confirmation, and retrieve the generated video link or error details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses paid WeryAI generation jobs and requires a WeryAI API key.

Mitigation: Review the full prompt and parameter table before confirming any submit or wait action, and use an isolated or short-lived API key where practical.

Risk: Local image paths may be read and uploaded to WeryAI if used for image-to-video inputs.

Mitigation: Prefer public HTTPS image URLs, and approve local file paths only after checking the exact file and accepting the upload.

## Reference(s):

- [WeryAI Video API](resources/WERYAI_VIDEO_API.md)
- [Skill page](https://clawhub.ai/zoucdr/skills/think-x-actually-y-video-gen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, parameter tables, JSON command payloads, shell commands, and Markdown video links or error summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, explicit approval before paid submit or wait actions, and public HTTPS image URLs for normal image-to-video use.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
