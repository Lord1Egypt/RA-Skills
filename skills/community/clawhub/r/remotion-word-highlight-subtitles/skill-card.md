## Description:

Add word-level highlighted subtitles to local short videos using Whisper word timestamps and Remotion rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x00000003](https://clawhub.ai/user/0x00000003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, video creators, and agent users use this skill to transcribe local short videos, review and correct word-level captions, and render polished Chinese-oriented subtitles with current-word highlighting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow processes local media and writes rendered outputs, so users could choose the wrong input or output location.

Mitigation: Use only video files and output folders selected by the user, and keep the generated video separate from the source file.

Risk: The default Whisper settings are optimized for Chinese-language subtitles and may produce inaccurate captions for other languages.

Mitigation: Change the Whisper language option for non-Chinese videos and complete the transcript QA pass before rendering.

Risk: Missing or mismatched local rendering tools can cause failed renders, lost audio, or duration mismatches.

Mitigation: Verify python3, ffmpeg, ffprobe, whisper, node, npm, and Remotion dependencies, then inspect stills and check final duration and audio with ffprobe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x00000003/skills/remotion-word-highlight-subtitles)
- [Project documentation linked by skill](https://github.com/0x00000003/remotion-word-highlight-subtitles)
- [Word highlight subtitle example image](https://raw.githubusercontent.com/0x00000003/remotion-word-highlight-subtitles/main/assets/effect-word-highlight.jpg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, code snippets, and JSON caption data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Remotion caption JSON and guidance for rendering a local MP4 subtitle output; expects local python3, ffmpeg, ffprobe, whisper, node, and npm.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
