## Description:

Sih.AI Photo Changer helps agents edit or generate images from a source image and a natural-language prompt using the Sih.AI image API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to transform an input image with prompts for background, outfit, face, style, or beauty edits. The skill returns API JSON and generated image URLs for downstream use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user-selected images and prompts to an under-disclosed third-party endpoint.

Mitigation: Use only images and prompts suitable for the remote provider; avoid sensitive photos and confidential documents.

Risk: The bundled script contains an exposed bearer token.

Mitigation: Treat the token as exposed, rotate it before trusted use, and replace hardcoded credentials with managed secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3273283/skills/sih-ai-photo-changer)
- [Publisher profile](https://clawhub.ai/user/a3273283)
- [Sih.AI image generation endpoint](https://api.vwu.ai/v1/images/generations/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and API JSON responses containing generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image URLs are documented as valid for 24 hours; local images are base64-encoded before upload.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
