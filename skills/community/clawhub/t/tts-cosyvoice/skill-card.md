## Description: <br>
Converts text to speech through Microsoft Edge TTS voices without an API key, supporting 100+ voices across 50+ languages including Chinese and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate speech audio, optionally with SRT subtitles, from supplied text or text files using Microsoft Edge TTS voices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Microsoft's online TTS service. <br>
Mitigation: Do not use this skill for secrets, credentials, private documents, regulated data, or confidential transcripts unless that processing is acceptable. <br>
Risk: Optional README examples describe model download commands and trust_remote_code usage outside the Edge TTS workflow. <br>
Mitigation: Review optional commands before running them and avoid executing model-download or trust_remote_code examples unless they are required and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/tts-cosyvoice) <br>
- [Publisher profile](https://clawhub.ai/user/vincentlau2046-sudo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples; generated artifacts are MP3 audio files and optional SRT subtitle files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the edge-tts Python package, and an internet connection to reach the online TTS service.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
