## Description: <br>
短视频下载器 - 支持抖音、小红书、快手、B站无水印视频下载。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and archivers use this skill to parse a supported short-video share link and download watermark-free video or image media locally. It is intended for one authorized URL at a time and requires a RedFox API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted links and related metadata are sent to RedFox for parsing. <br>
Mitigation: Use only links you are authorized to download and avoid private or token-bearing share URLs. <br>
Risk: The downloader may expose the RedFox API key to media download hosts when fetching returned media files. <br>
Mitigation: Review or fix the downloader before installation so the RedFox API key is not sent to third-party media hosts. <br>
Risk: The release under-explains privacy and rights risks for downloaded media. <br>
Mitigation: Review applicable platform terms, copyright, and privacy requirements before downloading or reusing media. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/video-downloader-redfox) <br>
- [RedFoxHub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk?source=github) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; downloaded media files are written locally as MP4, JPG, or PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY or an equivalent CLI/config-file API key; handles one share URL per run.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
