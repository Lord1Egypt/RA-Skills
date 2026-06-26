## Description: <br>
Transcribe audio files to text via Step ASR streaming API (HTTP SSE), with support for Chinese and English, PCM, WAV, MP3, and OGG/OPUS audio, streaming output, and terminology prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[randzero](https://clawhub.ai/user/randzero) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local audio files through StepFun's ASR service, stream transcript text, save transcripts, or return JSON with usage statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files and optional prompt text are sent to StepFun for transcription under the user's StepFun account. <br>
Mitigation: Use only audio and prompt content that StepFun's terms, consent requirements, and the user's data-handling policy allow. <br>
Risk: The StepFun API key is required for access and could expose the user's account if mishandled. <br>
Mitigation: Keep STEPFUN_API_KEY private and avoid committing it to source files, logs, or shared configuration. <br>


## Reference(s): <br>
- [Step ASR streaming API documentation](https://platform.stepfun.com/docs/zh/api-reference/audio/asr-stream) <br>
- [Step Platform](https://platform.stepfun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcript, optional JSON with usage statistics, and optional saved transcript file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and STEPFUN_API_KEY; sends selected audio and optional prompt text to StepFun for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
