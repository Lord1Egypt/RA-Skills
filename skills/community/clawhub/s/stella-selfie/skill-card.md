## Description:

Generate persona-consistent selfies and third-person photos with OpenClaw native image generation; deliver to the current conversation or return image bytes to a same-host plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tower1229](https://clawhub.ai/user/tower1229)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw agents use this skill to create persona-consistent selfies and third-person photos from a user's scene or camera request, delivering an image to the current conversation or returning image bytes to a same-host plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected avatar images are sent to the configured image provider; provider charges and retention practices apply.

Mitigation: Use only images and scene details you are comfortable sharing, and review the configured provider's terms and retention practices.

Risk: Local avatar access can expose personal images if authorized directories are broader than needed.

Mitigation: Keep authorized directories narrow, provide only intended avatar images, and retain the default reference count.

Risk: Reference-file cleanup may report an incomplete cleanup diagnostic.

Mitigation: Review and follow any cleanup diagnostic returned by the skill.

## Reference(s):

- [Timeline integration](references/timeline-integration.md)
- [Plugin integration](references/plugin-integration.md)
- [OpenClaw image generation](https://docs.openclaw.ai/tools/image-generation)
- [OpenClaw plugin runtime image generation](https://docs.openclaw.ai/plugins/sdk-runtime/media#api-runtime-imagegeneration)
- [ClawHub skill page](https://clawhub.ai/tower1229/skills/stella-selfie)

## Skill Output:

**Output Type(s):** [Images, Guidance]

**Output Format:** [A generated image delivered in the conversation or returned as image bytes to a same-host plugin]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One image per request; persona-consistent selfie or third-person photo]

## Skill Version(s):

2.1.0 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
