## Description:

Generates complete story videos from images, text descriptions, or mixed inputs, with optional duration and style settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeng-austin](https://clawhub.ai/user/zeng-austin)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to turn one or more images, a written story idea, or a combination of both into a finished short video with generated script, subject reference image, key frames, video segments, instrumental background music, and final assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and can overwrite generated media under output/.

Mitigation: Run it in a workspace where output/ can be replaced, or back up and rename existing output media before execution.

Risk: The skill uses FFmpeg for local video assembly and may attempt installation if FFmpeg is unavailable.

Mitigation: Confirm FFmpeg installation steps before proceeding and review generated FFmpeg commands before execution.

## Reference(s):

- [Story Video Generator ClawHub page](https://clawhub.ai/zeng-austin/skills/story-video-generator)
- [Background Music Generation](references/bgm-generation.md)
- [Frame Generation](references/frame-generation.md)
- [Image Script Generation](references/image-script-generation.md)
- [Subject Reference Generation](references/subject-reference.md)
- [Text Script Generation](references/text-script-generation.md)
- [Video Generation](references/video-generation.md)
- [Video Merge](references/video-merge.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON snippets, XML-style asset delivery tags, shell commands, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces story_script.json, subject_reference.png, frame images, video segments, bgm.mp3, and final_video.mp4 under output/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
