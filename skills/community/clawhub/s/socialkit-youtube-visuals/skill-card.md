## Description:

Turns an approved YouTube script into a shot list (shot-list.json) that maps each script section to a visual asset - user footage, screen recordings, slides, images or licensed stock - with durations, plus an asset checklist. Use when planning B-roll, visuals, scenes or slides for a YouTube video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

YouTube creators and production teams use this skill to plan B-roll, scenes, slides, and other visuals for an approved video script, then organize the needed assets in a shot list and checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested visuals may not fit the script or narration.

Mitigation: Review each proposed shot and duration against the approved script before sourcing or recording assets.

Risk: A planned asset may be used without the necessary rights.

Mitigation: Use user-provided media or material the user has permission to use; do not pull clips from other creators' videos.

Risk: Realistic AI-generated or altered media may need to be disclosed during upload.

Mitigation: Identify any realistic AI-generated or altered assets and flag them for the upload workflow's synthetic media disclosure.

## Reference(s):

- [Shot-list schema](assets/shot-list.schema.json)
- [ClawHub release: SocialKit YouTube Visuals 0.3.1](https://clawhub.ai/ahmadhussain0335/skills/socialkit-youtube-visuals)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON shot-list.json plus a Markdown asset checklist in the reply]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shot list follows assets/shot-list.schema.json; it plans user-provided or rights-cleared media and does not generate or download assets.]

## Skill Version(s):

0.3.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
