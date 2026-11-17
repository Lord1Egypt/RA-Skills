## Description:

Generate video using SkillBoss API Hub (video generation, auto-routed via /v1/pilot).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate short MP4 video clips from text prompts, optionally with up to three reference images, through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to SkillBoss API Hub.

Mitigation: Use non-sensitive prompts and images, and provide SKILLBOSS_API_KEY only in environments where that disclosure is acceptable.

Risk: The downloader trusts an API-returned video URL and does not enforce download size limits.

Mitigation: Run the skill in a contained workspace, choose the output path carefully, and review downloaded media before further use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-video)
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca)
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1)

## Skill Output:

**Output Type(s):** [shell commands, files, text]

**Output Format:** [MP4 video file plus console text including a MEDIA path line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and SKILLBOSS_API_KEY; supports prompt, duration, aspect ratio, optional model hint, and up to three input images.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
