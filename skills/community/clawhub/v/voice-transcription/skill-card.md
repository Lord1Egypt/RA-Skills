## Description: <br>
Transcribes user-selected audio files to text through SiliconFlow speech-to-text models, with support for multiple languages and dialect-oriented recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datou3456](https://clawhub.ai/user/datou3456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert audio recordings such as conversations, meetings, or dialect speech into text. It is useful when an agent needs to transcribe a provided audio file and optionally save plain text or JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to SiliconFlow for transcription. <br>
Mitigation: Use only when SiliconFlow's privacy and retention terms are acceptable for the recording, and avoid confidential, regulated, or highly personal audio unless approved. <br>
Risk: The skill requires a sensitive SiliconFlow API key. <br>
Mitigation: Keep the SILICONFLOW_API_KEY private, prefer environment-variable configuration, and do not paste credentials into shared logs or transcripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/datou3456/voice-transcription) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON transcription results with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SiliconFlow API key and uploads selected audio files to SiliconFlow for transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
