## Description: <br>
Downloads Xiaohongshu video content, extracts audio, transcribes speech through Poe/Gemini, and guides the agent to produce a detailed Chinese summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HViktorTsoi](https://clawhub.ai/user/HViktorTsoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Xiaohongshu video links by downloading media, transcribing audio, and producing a detailed Chinese content summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded video/audio and extracted speech are stored locally. <br>
Mitigation: Run only on content you are permitted to process and remove the work directory when the files are no longer needed. <br>
Risk: Audio chunks are uploaded to Poe/Gemini using the user's Poe API key. <br>
Mitigation: Avoid private, confidential, copyrighted, or legally sensitive videos unless that third-party processing is acceptable, and protect POE_API_KEY as a credential. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HViktorTsoi/xhs-video-analyzer) <br>
- [Xiaohongshu](https://www.xiaohongshu.com/) <br>
- [Poe API Endpoint](https://api.poe.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with shell commands and generated transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local video, audio, transcript, and chunk files in a working directory; requires POE_API_KEY for cloud transcription.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
