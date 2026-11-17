## Description:

Generates designed portfolio-resume images from conversation-supplied resume content by converting the resume and optional style direction into a fixed portfolio-resume image prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn user-provided resume text and optional visual style directions into a tall portfolio-resume image for presentation or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume content can include personal or sensitive information and may be sent to configured external model providers.

Mitigation: Review provider configuration and redact unnecessary personal details before using the skill.

Risk: Plaintext resume material may be written to predictable temporary files without clear cleanup.

Mitigation: Avoid shared or multi-user machines unless temporary-file handling is hardened, and remove temporary outputs after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-image-resume)
- [Fixed portfolio-resume layout prompt](artifact/prompts/resume.md)

## Skill Output:

**Output Type(s):** [text, image]

**Output Format:** [Short text summary with a generated resume image file; verbose mode may include the generated image prompt and timing details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default aspect ratio is 9:16 and default image size is 2k.]

## Skill Version(s):

2026.9.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
