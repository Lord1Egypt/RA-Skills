## Description: <br>
Downloads Douyin videos, extracts audio, runs local speech-to-text, and outputs a transcript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengzi53](https://clawhub.ai/user/mengzi53) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when a user provides a Douyin link and asks to transcribe speech, extract captions, or produce video text. It automates video URL resolution, media download, audio extraction, local ASR, transcript output, and optional Feishu upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow builds shell commands from user-supplied Douyin links and output paths, creating local command-execution risk. <br>
Mitigation: Use only trusted Douyin links and controlled output paths, and run the skill in a least-privileged or isolated environment. <br>
Risk: The workflow submits the Douyin URL to hellotik.app, downloads media from resolved CDN URLs, and can optionally interact with Feishu destinations. <br>
Mitigation: Treat it as a networked workflow; avoid sensitive media, and enable Feishu upload only after confirming the intended tenant, folder token, and knowledge base space. <br>
Risk: Downloaded video and extracted audio remain on disk unless cleanup is requested. <br>
Mitigation: Use a safe temporary output directory and request cleanup after transcription when local media retention is not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mengzi53/xiaofei-ziyong-douyin-transcribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Terminal transcript text plus a local transcript.txt file, with optional Feishu upload status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local command-line tools and network access; downloaded video and audio files remain in the output directory unless cleanup is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
