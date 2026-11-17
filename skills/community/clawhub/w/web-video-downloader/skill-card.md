## Description:

Web Video Downloader guides agents through detecting direct MP4, M3U8/HLS, segmented MP4, and blob-backed video sources from webpages and downloading or merging them into complete MP4 files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieliuzhu888](https://clawhub.ai/user/xieliuzhu888)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to inspect pages with embedded video, choose an appropriate download strategy, capture network media URLs when needed, and run curl, CDP, and FFmpeg workflows to produce MP4 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDP capture can collect browser request headers, including cookies or other sensitive session data.

Mitigation: Run capture only in a dedicated browser profile or while signed out of sensitive accounts, treat /tmp/captured_video_urls.json as secret, and delete it after use.

Risk: Downloader and merge scripts may fetch and execute an FFmpeg binary from the internet when FFmpeg is not already installed.

Mitigation: Install and verify FFmpeg from a trusted source before running the scripts so they use the trusted local binary.

Risk: Download and merge commands can overwrite user-selected output files.

Mitigation: Choose output paths deliberately and review existing files before executing generated commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xieliuzhu888/skills/web-video-downloader)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with bash, JavaScript, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may write MP4 outputs and /tmp/captured_video_urls.json when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
