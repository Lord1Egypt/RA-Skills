## Description:

Helps agents remove embedded subtitles from videos and repair the affected frames using Qinghu's video-edit service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and localization teams remove hardcoded subtitles before reusing or translating footage and receive a link to the processed video.

### Deployment Geography for Use:

China (Qinghu domestic service)

## Known Risks and Mitigations:

Risk: The agent may install or upgrade qhkit and Node tooling.

Mitigation: Review installation commands before execution and approve changes to the environment.

Risk: Selected video files may be uploaded to the Qinghu service for processing.

Mitigation: Avoid submitting sensitive footage unless the service is acceptable for that content.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-video-subtitle-remove)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance, Video links]

**Output Format:** [Markdown with command snippets and a processed-video URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task status and credits charged when available.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
