## Description:

Extracts and downloads embedded videos from WeChat official account articles by opening an article page, locating the video player, extracting the video URL, and downloading the file locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenjie0112](https://clawhub.ai/user/wenjie0112)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download videos embedded in trusted WeChat official account articles for offline viewing, archiving, or authorized personal study.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL and output-file handling are broader than expected for strict WeChat-only video downloading.

Mitigation: Use only trusted mp.weixin.qq.com article links and avoid absolute or traversal output paths.

Risk: The downloader may follow redirects or write outside an intended workspace if inputs are not constrained.

Mitigation: Prefer a patched version that restricts allowed hosts, blocks private-network targets and redirects, confines downloads to a dedicated folder, and refuses overwrites by default.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/wenjie0112/skills/wechat-video-downloader)
- [ClawHub Publisher Profile](https://clawhub.ai/user/wenjie0112)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and local download status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write downloaded video files to the current working directory or to a requested output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
