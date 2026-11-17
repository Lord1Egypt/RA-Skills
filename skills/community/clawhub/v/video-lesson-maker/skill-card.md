## Description:

Turns source documents into a series of educational videos with whiteboard animation, narrated audio, and synchronized subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8288hit](https://clawhub.ai/user/8288hit)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and content creators use this skill to break down course materials or articles into short lessons and produce narrated whiteboard videos with synchronized subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration text is sent to a cloud text-to-speech service.

Mitigation: Do not submit confidential or sensitive scripts without approval for cloud processing.

Risk: Media processing may overwrite local outputs.

Mitigation: Run the workflow in a dedicated project directory and keep copies of original assets.

Risk: The workflow includes a watermark-removal step.

Mitigation: Remove watermarks only from assets you are authorized to modify.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/8288hit/skills/video-lesson-maker)
- [Theme refinement](references/theme-refinement.md)
- [Production pipeline](references/pipeline.md)
- [Subtitle guidelines](references/srt-guidelines.md)
- [Annotation schema](references/annotation-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files]

**Output Format:** [Lesson plans, scripts, SRT subtitles, JSON timing plans, and rendered MP4 videos]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Narration and burnt-in subtitles are timed to the rendered scenes.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, manifest, and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
