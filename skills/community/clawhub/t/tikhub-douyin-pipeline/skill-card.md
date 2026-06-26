## Description: <br>
TikHub API 多平台数据爬取工具，支持抖音/TikTok/B站等；用于爬取视频或评论、获取用户信息或粉丝列表、批量下载无水印视频、将抖音链接转写为文字，以及调用 TikHub API。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kk-kingkong](https://clawhub.ai/user/kk-kingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to collect TikHub-backed Douyin, TikTok, Bilibili, and related platform data, download video assets, collect comments or user metadata, and produce transcripts from downloaded media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TikHub API key and can make paid TikHub calls. <br>
Mitigation: Use a limited API key, monitor account balance, and rotate the key if it is exposed. <br>
Risk: The skill can download platform media and collect comments, followers, and user data. <br>
Mitigation: Collect only content and personal data that the operator is authorized to access and use. <br>
Risk: The security review identified an unsafe background transcription command in the CPU Whisper path. <br>
Mitigation: Prefer the mlx-whisper path or avoid the CPU background path until the shell command is fixed and reviewed. <br>


## Reference(s): <br>
- [TikHub API documentation](https://api.tikhub.io/docs) <br>
- [ClawHub release page](https://clawhub.ai/kk-kingkong/tikhub-douyin-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, JSON files, downloaded media files, extracted audio files, and transcript text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate external API calls, paid TikHub endpoints, file downloads, ffmpeg audio extraction, and Whisper transcription workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
