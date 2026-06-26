## Description: <br>
Transcribe audio and video files to text with speaker detection, timestamps, and format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to transcribe local files, URLs, voice memos, podcasts, interviews, meetings, and lectures, with provider selection based on privacy, diarization, latency, and file length needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files and transcripts can contain sensitive information and may be stored locally under ~/speech-to-text-transcription/. <br>
Mitigation: Install only if local storage of transcription preferences and saved transcripts is acceptable, and save transcripts only when needed. <br>
Risk: Cloud transcription sends audio to OpenAI, AssemblyAI, or Deepgram when those providers are chosen. <br>
Mitigation: Use local Whisper for sensitive recordings and confirm before sending audio to any cloud provider. <br>
Risk: Cloud providers require API keys for optional features. <br>
Mitigation: Keep API keys in environment variables and avoid storing them in skill memory or transcript files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/speech-to-text-transcription) <br>
- [Skill Homepage](https://clawic.com/skills/speech-to-text-transcription) <br>
- [OpenAI Audio Transcriptions Endpoint](https://api.openai.com/v1/audio/transcriptions) <br>
- [AssemblyAI Upload Endpoint](https://api.assemblyai.com/v2/upload) <br>
- [AssemblyAI Transcript Endpoint](https://api.assemblyai.com/v2/transcript) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and transcript outputs such as txt, srt, vtt, json, or md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save transcripts under ~/speech-to-text-transcription/transcripts/ when the user asks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
