## Description:

Control Suno.com through an OpenClaw managed browser session to enter lyrics, style, and title details, create songs, and play generated tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstatemovingimages-cmyk](https://clawhub.ai/user/upstatemovingimages-cmyk)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to have an agent operate a logged-in Suno browser session for AI music generation workflows. It is intended for entering prompts and song metadata, starting generation, and reviewing playback in the managed browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates in a logged-in Suno managed browser session and may click Create using the user's account.

Mitigation: Install only for users who want agent control of their Suno session, and confirm generation actions before spending account credits or quota.

Risk: Generated songs may contain unwanted, incorrect, or unsuitable content before publication.

Mitigation: Review generated songs before publishing or sharing them.

## Reference(s):

- [ClawHub Skill Page: Suno Automation](https://clawhub.ai/upstatemovingimages-cmyk/skills/suno-automation)
- [Suno Create](https://suno.com/create)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline browser and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running OpenClaw managed browser profile with an authenticated Suno session; element references should be refreshed with browser snapshots before actions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
