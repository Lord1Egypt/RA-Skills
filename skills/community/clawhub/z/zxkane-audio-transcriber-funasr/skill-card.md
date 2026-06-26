## Description: <br>
Transcribes meeting, podcast, and interview audio into structured transcripts with ASR, speaker diarization, optional hotword biasing, and optional LLM cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxkane](https://clawhub.ai/user/zxkane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prepare and run local audio transcription workflows for meetings, podcasts, and interviews, including speaker labeling and transcript cleanup when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recordings, transcripts, speaker context, and reference files can contain sensitive personal or business information. <br>
Mitigation: Use local-only transcription for sensitive recordings by omitting --model, and keep supporting files limited to the minimum needed for accuracy. <br>
Risk: Optional LLM cleanup or speaker-verification workflows can send transcript excerpts and context to cloud LLM providers. <br>
Mitigation: Enable cloud LLM features only after confirming the provider is approved for the data; otherwise use --skip-llm or omit --model. <br>
Risk: Speaker gender inference runs by default and may be unnecessary for many transcripts. <br>
Mitigation: Use --no-detect-gender unless gender labels are explicitly needed and appropriate for the use case. <br>
Risk: Speaker diarization can merge or swap similar speakers, especially in multi-speaker or podcast recordings. <br>
Mitigation: Provide the expected speaker count and speaker context, then review or verify speaker labels before relying on the transcript. <br>


## Reference(s): <br>
- [Audio Transcribe homepage](https://github.com/zxkane/audio-transcriber) <br>
- [Pipeline details](references/pipeline-details.md) <br>
- [MiMo-V2.5-ASR model card](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-ASR) <br>
- [ClawHub skill page](https://clawhub.ai/zxkane/zxkane-audio-transcriber-funasr) <br>
- [Publisher profile](https://clawhub.ai/user/zxkane) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown transcripts, raw transcript JSON, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The main workflow writes a final transcript Markdown file and a raw transcript JSON file; optional helper workflows produce setup commands and speaker-verification guidance.] <br>

## Skill Version(s): <br>
1.7.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
