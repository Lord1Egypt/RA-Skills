## Description:

把 YouTube 视频变成中文音频播客：NotebookLM Audio Overview 生成、ffmpeg 转码，再上传小宇宙（上传即进入平台审核，通过后自动上线；可用 --hold-upload 在上传前停下）；完成后回推一条结果通知。用户从微信/聊天里发来 YouTube 链接时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[seuwangcy](https://clawhub.ai/user/seuwangcy)

### License/Terms of Use:

MIT

## Use Case:

External users can send a YouTube link to an OpenClaw agent to create a Chinese conversational podcast and upload it to a Xiaoyuzhou program.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports an unauthenticated local file server and unclear upload triggers; its guidance notes that unrelated websites may be able to read files being prepared for upload.

Mitigation: Review the local server exposure and upload triggers before use. Use --hold-upload to inspect generated audio before transfer, and keep public publishing disabled unless explicitly approved.

## Reference(s):

- [ClawHub release](https://clawhub.ai/seuwangcy/skills/yt2podcast)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [opencli package](https://www.npmjs.com/package/@jackwener/opencli)
- [Xiaoyuzhou](https://www.xiaoyuzhoufm.com/)

## Skill Output:

**Output Type(s):** [Audio files, JSON, Text]

**Output Format:** [M4A or WAV audio, JSON job and notification data, and a completion notification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads the generated audio to Xiaoyuzhou; platform review may result in automatic public availability.]

## Skill Version(s):

0.2.4 (source: changelog, released 2026-11-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
