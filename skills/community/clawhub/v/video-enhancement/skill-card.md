## Description:

AI Video Enhancement - Upscale video resolution, denoise, sharpen. Supports local files and YouTube/Bilibili URLs. HD/4K upscaling with real-time progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alouhaou](https://clawhub.ai/user/alouhaou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to enhance short videos from local files or supported video URLs through the Verging video enhancement service. It helps prepare API calls, local trimming commands, upload steps, job polling, and optional result download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local command execution and installation steps may run external tools or downloaded code.

Mitigation: Review before installing, avoid elevated privileges, and prefer a pinned or verified install source.

Risk: Videos are uploaded to Verging and external storage for processing.

Mitigation: Process only media you have rights to share and avoid sensitive local media.

Risk: Untrusted URLs or trim values can influence local downloader and ffmpeg command behavior.

Mitigation: Use trusted video URLs and validate start and end values before running commands.

Risk: API keys may be exposed through command history, logs, or shared output.

Mitigation: Use VERGING_API_KEY from the environment and do not publish or paste credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alouhaou/skills/video-enhancement)
- [Verging Website](https://verging.ai)
- [Verging API Docs](https://verging.ai/docs/api)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline bash commands, API request examples, status summaries, and optional downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use yt-dlp, ffmpeg, ffprobe, curl, VERGING_API_KEY, and external upload, storage, and processing services.]

## Skill Version(s):

1.2.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
