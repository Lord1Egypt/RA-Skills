## Description: <br>
Transcribes audio or video into same-language timestamped SRT subtitles, routing Chinese audio to Volcano ASR and other supported languages to OpenAI Whisper with custom cue assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, localization teams, and agents working with audio or video use this skill to produce source-language SRT subtitles before translation, dubbing, or burn-in workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio or video content may be sent to external transcription providers during processing. <br>
Mitigation: Ask the user to confirm before sending confidential, private, or regulated media to external services. <br>
Risk: The workflow depends on sensitive provider credentials such as local transcription API keys. <br>
Mitigation: Configure only the required provider key in a dedicated environment file and avoid exposing credentials in prompts, logs, or generated files. <br>
Risk: Automatic transcription and cue assembly can produce recognition, punctuation, timing, or repeated-text errors. <br>
Mitigation: Review the generated SRT for sequential numbering, non-overlapping timestamps, readable cue lengths, and repeated phrases before using it downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-transcribing-audio) <br>
- [OpenAI audio transcriptions endpoint](https://api.openai.com/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python snippets for producing SRT subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces source-language .srt subtitle files with timestamped, punctuation-bounded cues after agent execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
