## Description:

Generate AI videos on the SeaArt platform from text prompts or image URLs using supported video models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxwzh](https://clawhub.ai/user/foxwzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request text-to-video or image-to-video generation through SeaArt and receive the generated video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token-checking guidance can print the password-equivalent SeaArt session token into logs.

Mitigation: Check whether the token is configured without echoing or otherwise printing SEAART_TOKEN, and keep the SeaArt cookie private.

Risk: Prompts, image URLs, and the SeaArt token cookie are sent to seaart.ai.

Mitigation: Use the skill only when the user trusts SeaArt with the creative content and understands the token is used as an authentication cookie.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foxwzh/skills/seaart-video)
- [SeaArt platform](https://www.seaart.ai)
- [Text-to-video endpoint](https://www.seaart.ai/api/v1/task/v2/video/text-to-video)
- [Image-to-video endpoint](https://www.seaart.ai/api/v1/task/v2/video/img-to-video)
- [Batch progress endpoint](https://www.seaart.ai/api/v1/task/batch-progress)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and a generated video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SeaArt session token and sends prompts, image URLs, and the token cookie to seaart.ai while polling for completion.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
