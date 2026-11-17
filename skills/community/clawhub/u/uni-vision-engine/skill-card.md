## Description:

Automated high-quality video generation (text-to-video, image-to-video) via a local jimeng-api Docker service. Features native OpenClaw image interception, allowing users to send images directly in chat to generate videos without any UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahuamld](https://clawhub.ai/user/jiahuamld)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to generate short videos from text prompts or chat-provided images through a local jimeng-api service. The skill guides an agent to submit prompts and local image files, monitor generation, and return status or an MP4 result link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable session token is embedded in the artifact.

Mitigation: Remove the embedded token, rotate the affected credential, and require credentials from a protected source before use.

Risk: The skill installs an npm package during normal execution.

Mitigation: Package and pin required dependencies ahead of time instead of installing them at runtime.

Risk: The skill gives broad automatic image-handling instructions for chat-provided images.

Mitigation: Require explicit user confirmation before saving or sending each chat image to the Jimeng service, and avoid use with private images until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiahuamld/skills/uni-vision-engine)
- [ClawHub publisher profile](https://clawhub.ai/user/jiahuamld)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and generated video task responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, service status messages, and MP4 links returned by the local jimeng-api service.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
