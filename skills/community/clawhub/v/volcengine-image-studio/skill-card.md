## Description:

Practical image generation workflow for Volcengine/ARK-compatible APIs for poster creation, text-to-image, reference-image generation, local image upload, multi-image runs, and automatic result downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to generate and download images through a configured Volcengine/ARK-compatible image endpoint, including prompt-only, reference-image, and multi-image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured endpoints receive API keys, prompts, and any supplied reference images.

Mitigation: Use only trusted HTTPS Volcengine/ARK-compatible endpoints and avoid confidential prompts or sensitive local images.

Risk: Failed runs can print request details that may include encoded reference images or sensitive prompt content.

Mitigation: Redact logs before sharing them and avoid publishing failure output from runs that used private inputs.

Risk: Automatic downloads can write remote image results to local folders with limited controls.

Mitigation: Disable automatic downloads or set a controlled download directory when handling untrusted prompts or endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinhuadeng/skills/volcengine-image-studio)
- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated image file paths or URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger API calls, create local image files, download remote image URLs, and open a local download folder when configured.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
