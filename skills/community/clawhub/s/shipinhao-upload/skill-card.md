## Description:

Use EasyPost to fill in or publish short videos on WeChat Channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gybin02](https://clawhub.ai/user/gybin02)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and social media operators can prepare or publish short videos to WeChat Channels through their currently signed-in Chrome session, including a title, description, media, and optional vertical cover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The active WeChat account or selected video and text may be unintended during a live upload.

Mitigation: Use a trusted EasyPost installation, confirm which account Chrome is signed into, and review the video, cover, title, and description before publishing.

Risk: The supplied documentation does not verify the external CLI's behavior or its claimed title validation.

Mitigation: Check the installed CLI's title constraints and review its response rather than relying on the documentation's validation claim alone.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gybin02/skills/shipinhao-upload)
- [Publisher profile (gybin02)](https://clawhub.ai/user/gybin02)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON payload supplied to the EasyPost CLI, with shell command examples and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For short videos; titles are limited to 16 characters and allow only Chinese characters, English letters, digits, and spaces. Descriptions may include hashtags; covers may be vertical 9:16 images.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
