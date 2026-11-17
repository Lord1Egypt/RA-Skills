## Description:

volc-vision uses Volcengine ARK vision models to describe images, answer visual questions, and analyze local files, image URLs, or base64 image inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[big-dust](https://clawhub.ai/user/big-dust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user needs image understanding, visual question answering, or concise image analysis from a local image path, remote image URL, or base64 image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected local images, remote image URLs, base64 image data, and prompts to Volcengine ARK.

Mitigation: Use it only with images and prompts approved for external processing, and avoid sensitive screenshots, documents, IDs, and internal imagery.

Risk: The skill can fetch arbitrary image URLs without explicit URL allowlisting or private-network blocking.

Mitigation: Review URLs before use and avoid untrusted or internal URLs until allowlisting, private-network blocking, redirect limits, size limits, and timeouts are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/big-dust/skills/volc-vision)
- [Publisher profile](https://clawhub.ai/user/big-dust)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown returned from the vision API, with command-line usage and environment configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and ARK_API_KEY; VISION_MODEL can override the default model selection.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
