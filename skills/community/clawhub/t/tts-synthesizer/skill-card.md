## Description: <br>
Converts text to speech with Microsoft edge-tts or an OpenAI-compatible TTS API, including OGG/Opus output for Feishu voice messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to synthesize spoken audio from text, choose voices and speech settings, and produce files suitable for Feishu voice messages or general playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis may be sent to Microsoft edge-tts or to the configured OpenAI-compatible API endpoint. <br>
Mitigation: Avoid synthesizing secrets or confidential text, and use only trusted TTS endpoints for sensitive workflows. <br>
Risk: API mode requires sensitive credentials. <br>
Mitigation: Keep API keys scoped, provide them through trusted configuration, and rotate them if exposed. <br>
Risk: Generated audio files are saved in the OpenClaw workspace output directory by default. <br>
Mitigation: Choose explicit output paths when needed and review generated audio files before sharing or sending them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moroiser/tts-synthesizer) <br>
- [Publisher profile](https://clawhub.ai/user/moroiser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated audio files are OGG/Opus or MP3 depending on the script and engine.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call online TTS services and may write generated audio files under the OpenClaw workspace output directory unless another output path is provided.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
