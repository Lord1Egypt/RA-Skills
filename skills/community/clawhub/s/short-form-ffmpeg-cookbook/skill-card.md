## Description:

Provides tested FFmpeg commands for turning footage into vertical short-form videos with captions, trims, joins, and music ducking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers can use the cookbook to prepare short-form videos for Reels, TikTok, and Shorts by cropping footage, adding captions, trimming or joining clips, and mixing music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unpinned package commands.

Mitigation: Review package sources and versions before running installation commands.

Risk: The remote media-processing option may share media or URLs with a third party.

Mitigation: Use the local FFmpeg recipes for sensitive media, or confirm that sharing the media or URL with the remote service is acceptable before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vargai/skills/short-form-ffmpeg-cookbook)
- [Listed skill homepage](https://github.com/vargHQ/skills/tree/main/short-form-ffmpeg-cookbook)
- [Burn captions with FFmpeg](https://skills.varg.ai/burn-captions-with-ffmpeg/)
- [Crop video to vertical with FFmpeg](https://skills.varg.ai/crop-a-video-to-vertical-with-ffmpeg/)
- [Trim and join video clips with FFmpeg](https://skills.varg.ai/trim-and-join-video-clips-with-ffmpeg/)
- [Add music to a video with FFmpeg](https://skills.varg.ai/add-music-to-a-video-with-ffmpeg/)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown cookbook with inline Bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use video files and may also use subtitle files or music tracks; executing them produces video files.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
