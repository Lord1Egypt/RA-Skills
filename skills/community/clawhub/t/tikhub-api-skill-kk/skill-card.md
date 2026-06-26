## Description: <br>
Guides an agent through TikHub MCP and fallback Python SDK workflows for collecting multi-platform social video data, download links, comments, user information, and transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kk-kingkong](https://clawhub.ai/user/kk-kingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to query TikHub-backed MCP tools and optional Python helpers for Douyin, TikTok, Bilibili, YouTube, Xiaohongshu, Weibo, and Kuaishou content workflows. It is intended for retrieving video metadata, comments, user data, download URLs, captions, and transcript outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill implicitly uses a local TikHub API key and can call paid TikHub endpoints. <br>
Mitigation: Use a dedicated TikHub API key, monitor paid usage and balance, and avoid exposing local environment files or credentials. <br>
Risk: The Python fallback can run background shell commands for ffmpeg and Whisper processing. <br>
Mitigation: Prefer the MCP workflow when available, run fallback scripts only on trusted filenames and directories, and review generated shell activity before use. <br>
Risk: Fallback dependencies and transcription tooling may change behavior or introduce supply-chain risk. <br>
Mitigation: Pin or review Python dependencies before installing them in production or shared environments. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kk-kingkong/tikhub-api-skill-kk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell and Python snippets, API call examples, and JSON or text file outputs from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded media, extracted audio, transcript text files, comments JSON, user-video JSON, and pipeline result JSON when the Python fallback scripts are used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
