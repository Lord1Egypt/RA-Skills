## Description:

Audio Transcribe helps an agent transcribe meeting, podcast, and interview recordings into structured transcripts with ASR, speaker diarization, optional speaker verification, and optional LLM cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxkane](https://clawhub.ai/user/zxkane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill to convert audio recordings into Markdown transcripts with speaker labels, timestamps, and optional cleanup for meeting notes or podcast/interview review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive audio, transcript excerpts, speaker context, or reference material may be sent to external LLM providers when cleanup is enabled.

Mitigation: Omit --model or use --skip-llm to keep cleanup local, and only provide trusted reference and speaker-context files when LLM cleanup is needed.

Risk: Speaker-gender inference is enabled by default and may create unnecessary demographic processing.

Mitigation: Use --no-detect-gender when demographic inference is not required.

Risk: OpenAI-compatible endpoints and setup commands can change the operational trust boundary.

Mitigation: Review any OPENAI_BASE_URL value and run setup commands in an isolated virtual environment after reviewing privileged and dependency behavior.

## Reference(s):

- [Project homepage](https://github.com/zxkane/audio-transcriber)
- [Pipeline Details](references/pipeline-details.md)
- [Xiaomi MiMo-V2.5-ASR Model Card](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-ASR)
- [ClawHub Skill Page](https://clawhub.ai/zxkane/skills/zxkane-audio-transcriber-funasr)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated transcript output may include Markdown and raw JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription output can include speaker labels, timestamps, hotword-biased ASR results, and optional LLM-cleaned text.]

## Skill Version(s):

1.7.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
