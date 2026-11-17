## Description:

Generate AI videos, images, voiceovers, music, captions, and multi-scene MP4 renders through the varg service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to generate images, video, voice, and music from prompts or reference media, then assemble those assets into composed videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions request broadly scoped skill updates.

Mitigation: Review the update scope and limit changes to this skill before running an update.

Risk: Setup can save the VARG_API_KEY in credential or project files beyond its original location.

Mitigation: Choose where the key may be saved and protect any credential files that contain it.

Risk: Prompts, reference media, and speech text are sent to remote generation services, and generation consumes credits.

Mitigation: Avoid sending sensitive material and check expected credit use before generating.

## Reference(s):

- [Varg](https://varg.ai)
- [Varg API dashboard](https://varg.ai/dashboard/api)
- [Varg model catalog](https://varg.ai/models/llms.txt)
- [ClawHub skill release](https://clawhub.ai/vargai/skills/varg-ai)

## Skill Output:

**Output Type(s):** [Video, Images, Audio, Code, Shell commands, Guidance]

**Output Format:** [Generated media files, including MP4 video, and TypeScript/TSX or API request text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model, duration, quality, and credit use vary by request.]

## Skill Version(s):

2.0.13 (source: target metadata and server release evidence; artifact frontmatter reports 2.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
