## Description:

Generate narration for silent screen-recording videos by extracting key frames, writing a presentation-style voiceover script, synthesizing speech with Microsoft Edge neural TTS, and merging the audio onto the original video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanzhang-oss](https://clawhub.ai/user/ryanzhang-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and technical presenters use this skill to turn silent demo or screen-recording videos into narrated walkthroughs with a companion voiceover script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled TTS step has a command/code injection risk.

Mitigation: Review and fix the TTS script before use, and only run it with trusted local inputs in a controlled environment.

Risk: Narration text is sent to an external TTS service.

Mitigation: Avoid using sensitive screen-recording content or narration text unless external disclosure is acceptable.

Risk: Generated outputs may overwrite files when output paths collide.

Mitigation: Use a dedicated output directory and avoid paths where silent overwrite would matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanzhang-oss/skills/video-auto-narration)
- [ClawHub publisher profile](https://clawhub.ai/user/ryanzhang-oss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown voiceover script, shell command guidance, generated audio files, and a narrated video file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a narrated video and a companion timestamped voiceover script; timing should be checked against the input video duration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
