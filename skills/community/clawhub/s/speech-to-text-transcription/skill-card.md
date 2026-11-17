## Description:

Transcribe audio and video files to text with speaker detection, timestamps, and format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent transcribe local files, URLs, voice memos, podcasts, interviews, meetings, and lectures. It guides provider selection, audio preprocessing, speaker diarization, timestamped transcript formats, and optional transcript saving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio may be uploaded to cloud transcription providers when the user chooses OpenAI, AssemblyAI, or Deepgram.

Mitigation: Use local Whisper for sensitive recordings and confirm cloud provider use before any upload.

Risk: Saved preferences and transcripts may remain under ~/speech-to-text-transcription/.

Mitigation: Save transcripts only when requested, auto-clean temporary files after successful transcription, and review or delete the directory when retention is not desired.

Risk: Unpinned dependencies or misplaced API keys can increase operational exposure.

Mitigation: Use a virtual environment with pinned dependencies and keep provider API keys in environment variables.

Risk: Large audio or video files can cause timeouts or memory pressure if uploaded or processed as one file.

Mitigation: Split long or large files into chunks with ffmpeg, process each chunk, and merge transcripts with timestamps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/speech-to-text-transcription)
- [Skill Homepage](https://clawic.com/skills/speech-to-text-transcription)
- [OpenAI Audio Transcriptions Endpoint](https://api.openai.com/v1/audio/transcriptions)
- [AssemblyAI Upload Endpoint](https://api.assemblyai.com/v2/upload)
- [AssemblyAI Transcript Endpoint](https://api.assemblyai.com/v2/transcript)
- [Deepgram API Endpoint](https://api.deepgram.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and transcript format options such as .txt, .srt, .vtt, .json, and .md.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local transcript files and temporary audio chunks when the agent follows the skill.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
