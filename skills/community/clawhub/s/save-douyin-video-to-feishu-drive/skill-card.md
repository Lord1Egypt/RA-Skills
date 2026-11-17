## Description:

Parses a Douyin share link or video page URL to obtain downloadable video URLs, title, and description, with options to download the video locally or upload it to Feishu Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuaner](https://clawhub.ai/user/kuaner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to process Douyin URLs, extract video metadata and playable download URLs, and optionally save the resulting video to local storage or Feishu Drive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app secrets, tenant tokens, or bearer credentials could be exposed if stored in TOOLS.md, source files, chat, logs, or command history.

Mitigation: Keep credentials in environment variables or a secret manager, avoid persisting them in workspace files, and rotate any token that may have been exposed.

Risk: The Feishu integration can access Drive resources beyond the intended folder if granted broad permissions.

Mitigation: Grant only the minimum Feishu Drive permissions needed, share only the target folder with the app, and verify folder access before use.

Risk: Local download mode writes video files to disk and could overwrite or place files in an unintended location.

Mitigation: Confirm the destination path before downloading and prefer a controlled temporary or project-specific output directory.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/kuaner/save-douyin-video-to-feishu-drive/tree/main/skills/save-douyin-video-to-feishu-drive)
- [ClawHub skill page](https://clawhub.ai/kuaner/skills/save-douyin-video-to-feishu-drive)
- [Feishu Drive app permissions documentation](https://open.feishu.cn/document/faq/trouble-shooting/how-to-add-permissions-to-app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with bash commands and structured result fields such as title, desc, video_urls, feishu_url, and download_path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Feishu app credentials, a Feishu Drive folder token, and a Douyin Referer header when downloading direct video URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
