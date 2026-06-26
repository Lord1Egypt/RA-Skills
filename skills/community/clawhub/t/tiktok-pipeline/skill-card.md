## Description: <br>
This skill helps agents use TikHub APIs to fetch Douyin, TikTok, and Bilibili data, download videos, extract audio, and transcribe Douyin videos with Whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kk-kingkong](https://clawhub.ai/user/Kk-kingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creator-operations agents use this skill to automate TikHub-backed collection of video metadata, comments, user video lists, video downloads, audio extraction, and transcript generation. It is intended for workflows where the operator has a TikHub API key and authorization to collect or process the target content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CPU/background Whisper path can launch an unsafe shell command from user-controlled paths. <br>
Mitigation: Prefer the mlx-whisper path or synchronous transcription path, and avoid the CPU/background path until command execution is fixed or file paths are tightly controlled. <br>
Risk: The skill requires a TikHub API key and supports paid download endpoints. <br>
Mitigation: Use an isolated environment, limit API-key exposure, avoid putting keys in shell history, monitor account balance, and confirm paid endpoint use before batch downloads. <br>
Risk: Profile, follower, video, and comment collection can involve third-party data and platform policy obligations. <br>
Mitigation: Collect only authorized data, keep batch limits narrow, and review legal, privacy, and platform terms before using profile, follower, or comment workflows. <br>
Risk: Bulk API calls can hit rate limits or produce partial results. <br>
Mitigation: Use delays between requests, cap batch sizes, check returned statuses, and retry only when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kk-kingkong/tiktok-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/Kk-kingkong) <br>
- [TikHub API documentation](https://api.tikhub.io/docs) <br>
- [TikHub user console](https://user.tikhub.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, JSON result files, downloaded media files, WAV audio files, and transcript text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TikHub API key, network access to TikHub endpoints, ffmpeg for audio extraction, and Whisper or mlx-whisper for transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
