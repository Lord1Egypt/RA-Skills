## Description: <br>
Text-to-speech conversion using node-edge-tts for generating audio from text with multiple voices, languages, speed adjustment, pitch control, and subtitle generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17854566382](https://clawhub.ai/user/17854566382) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert requested text into spoken audio, optionally choosing voice, language, speed, pitch, output format, and subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text may be sent to an external Microsoft Edge TTS service. <br>
Mitigation: Review the text for private, confidential, regulated, or credential-like content before conversion and get clear user intent for synthesis. <br>
Risk: The skill may filter TTS trigger words before synthesis, changing the text that is spoken. <br>
Mitigation: Confirm the final text to be synthesized when exact wording matters. <br>
Risk: Generated audio files may be written to temporary storage and are not automatically deleted by the bundled script. <br>
Mitigation: Delete generated files after delivery or configure an explicit output path with appropriate retention controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/17854566382/tts-1) <br>
- [node-edge-tts reference](references/node_edge_tts_guide.md) <br>
- [Voice testing page](https://tts.travisvn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [MP3 audio files, MEDIA paths, optional JSON subtitles, and Markdown guidance with shell and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable voice, language, rate, pitch, volume, output path, proxy, timeout, and subtitle generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package metadata reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
