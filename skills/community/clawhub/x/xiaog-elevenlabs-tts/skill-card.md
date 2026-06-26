## Description: <br>
Set up, test, benchmark, and use ElevenLabs text-to-speech as an independent TTS skill, including HTTP streaming, WebSocket streaming guidance, voice listing, model/output-format selection, latency tuning, and safe ELEVENLABS_API_KEY handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure ElevenLabs text-to-speech workflows, list voices, generate streaming audio samples, benchmark latency, select models and output formats, and keep API keys out of files and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to ElevenLabs. <br>
Mitigation: Use the skill only for text your ElevenLabs account and data-handling requirements allow; avoid confidential or regulated text unless that use is approved. <br>
Risk: The skill requires a sensitive ELEVENLABS_API_KEY. <br>
Mitigation: Keep the key in the environment, do not write it into files, commits, logs, or screenshots, and verify key presence without printing it. <br>
Risk: Live synthesis can fail because of missing, revoked, restricted, or account-limited credentials. <br>
Mitigation: Treat missing credentials or blocked synthesis as a live API limitation, report it clearly, and validate docs or scripts locally when live calls cannot run. <br>


## Reference(s): <br>
- [ElevenLabs TTS API Reference](references/elevenlabs-api.md) <br>
- [ElevenLabs API](https://api.elevenlabs.io) <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/xiaog-elevenlabs-tts) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jerryxn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline bash commands, Python script usage, and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save audio files and JSON benchmark summaries when scripts are executed with an ElevenLabs API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
