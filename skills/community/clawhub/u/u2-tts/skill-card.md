## Description: <br>
Text-to-speech conversion using UniSound's TTS WebSocket API for generating high-quality Chinese Mandarin audio from text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaiccee](https://clawhub.ai/user/aaiccee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to convert Chinese Mandarin text into speech through UniSound's WebSocket TTS service, with configurable voice, format, sample rate, speed, volume, pitch, and brightness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared-looking UniSound credentials appear in the artifact examples and may be copied, leaked, or abused. <br>
Mitigation: Use only your own UniSound credentials, store them in environment variables, rotate any copied sample values, and avoid passing secrets on the command line. <br>
Risk: Text submitted for synthesis is sent to UniSound or the configured WebSocket endpoint for processing. <br>
Mitigation: Do not submit confidential or regulated text unless the deployment policy allows that provider and endpoint to process it. <br>
Risk: The skill depends on external WebSocket connectivity and provider availability. <br>
Mitigation: Review the configured endpoint, install dependencies before use, and handle API, credential, and network failures in workflows that call the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaiccee/u2-tts) <br>
- [UniSound homepage](https://www.unisound.com) <br>
- [UniSound TTS API](https://www.unisound.com/tts-api) <br>
- [websocket-client documentation](https://websocket-client.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash and Python snippets; the included script writes MP3, WAV, or PCM audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, websocket-client, UniSound credentials, network access to the configured WebSocket endpoint, and writes timestamped files under results/.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
