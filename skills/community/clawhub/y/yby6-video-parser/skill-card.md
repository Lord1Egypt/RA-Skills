## Description:

Parses short-video and image-gallery share links from major platforms and can extract speech from videos into text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangbuyiya](https://clawhub.ai/user/yangbuyiya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-processing teams use this skill to parse supported social-video URLs, collect metadata such as media links, cover images, titles, and authors, and optionally transcribe video audio into text for subtitles, notes, or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles untrusted URLs and downloaded media.

Mitigation: Run it in a sandboxed environment and only process URLs from trusted sources.

Risk: Audio files are uploaded to SiliconFlow for transcription.

Mitigation: Do not use the transcription workflow for sensitive media unless the upload is approved for the data involved.

Risk: Raw media and extracted audio may remain on disk by default.

Mitigation: Enable automatic cleanup for sensitive videos and review the temporary output directory after use.

Risk: Caller-supplied parse_result data can bypass normal parsing assumptions.

Mitigation: Avoid caller-supplied parse_result values unless they come from a trusted prior parse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangbuyiya/skills/yby6-video-parser)
- [SiliconFlow audio API documentation](https://docs.siliconflow.cn/api-reference/audio)
- [SiliconFlow API key portal](https://siliconflow.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON parse results, Markdown transcription reports, and command/configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription requires a SiliconFlow API key and ffmpeg; media and audio files may be retained locally unless cleanup is enabled.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
