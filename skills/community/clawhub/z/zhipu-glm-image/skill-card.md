## Description:

Zhipu GLM Image helps an agent use a logged-in image.z.ai web session to check availability, open login when needed, generate images from prompts, and download the results locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangm199](https://clawhub.ai/user/huangm199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route image generation prompts through an existing image.z.ai browser login and save generated PNG images locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses and stores browser login cookies for a debug-enabled image.z.ai session.

Mitigation: Use a dedicated browser profile for image.z.ai, treat ~/.zhipu_image_session.json as sensitive, and delete or rotate the session when the skill is no longer needed.

Risk: The network monitor can observe requests from a debug-enabled browser session.

Mitigation: Run monitoring only for image.z.ai review work and avoid browsing unrelated sites from the monitored profile during capture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangm199/skills/zhipu-glm-image)
- [image.z.ai](https://image.z.ai/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [JSON status messages, shell commands, and downloaded PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser session cookies stored in ~/.zhipu_image_session.json and writes images to a captures directory by default.]

## Skill Version(s):

1.0.1 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
