## Description:

短视频下载器 — 支持抖音、小红书、快手、视频号、B站、YouTube、Instagram 等主流平台无水印视频下载，开箱即用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, content collectors, operators, and researchers use this skill to parse supported short-video or image-post share links and save watermark-free local copies for editing, backup, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may submit or download content they do not have permission to use.

Mitigation: Use only links and content the user is authorized to download, and review applicable platform terms before use.

Risk: Submitted URLs are sent to redfox.hk for parsing and may expose private or sensitive content links.

Mitigation: Avoid submitting sensitive links and make the redfox.hk dependency clear before use.

Risk: API keys can be exposed through command-line arguments, config files, logs, or output.

Mitigation: Prefer REDFOX_API_KEY, avoid hardcoding or logging keys, and use a revocable key with limited value.

Risk: Credential handling and download boundaries were flagged as review-worthy before installation.

Mitigation: Review the skill before installing and avoid valuable personal API keys until the session header reuse and URL/download validation issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/video-downloader-redfox)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and terminal status text; downloaded MP4, JPG, or PNG files are saved locally by the script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses one supported share link at a time and may require REDFOX_API_KEY for authenticated redfox.hk API access.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
