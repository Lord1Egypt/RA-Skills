## Description:

Generate animated pixel art sprites from any image using AI. Send a photo, get a 16-frame animated GIF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awlevin](https://clawhub.ai/user/awlevin)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn a source image into a looping pixel-art sprite animation, with selectable animation styles such as idle, wave, bounce, and dance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned external package, so behavior can change after review.

Mitigation: Review the `sprite-animator` package, pin a known version where possible, and run it in an isolated environment.

Risk: Input images and prompts are processed through Gemini using `GEMINI_API_KEY`.

Mitigation: Avoid sensitive personal, confidential, or proprietary images unless that external processing is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/awlevin/skills/sprite-animator)
- [Publisher Profile](https://clawhub.ai/user/awlevin)
- [Source Link Listed in Skill Artifact](https://github.com/Olafs-World/sprite-animator)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown with inline bash commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides creation of a 16-frame animated GIF and can optionally retain the source sprite sheet and extracted frame PNG files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
