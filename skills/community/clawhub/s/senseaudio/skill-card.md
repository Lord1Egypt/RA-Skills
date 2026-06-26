## Description: <br>
Sense Audio guides developers through SenseAudio Open Platform API integration for TTS, ASR, realtime agents, video generation, storyboard workflows, and voice clone usage constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, debug, and harden SenseAudio API integrations, including request construction, protocol selection, response parsing, and production error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated examples can send text, prompts, audio, images, or video to SenseAudio services. <br>
Mitigation: Only submit content the user is allowed and comfortable to send to SenseAudio, and disclose external processing expectations when adding integration guidance. <br>
Risk: API keys or realtime tokens could be exposed if examples hardcode credentials or log full authorization values. <br>
Mitigation: Use environment variables or a secret manager for API keys, avoid logging bearer tokens, and redact short-lived realtime credentials in diagnostic output. <br>


## Reference(s): <br>
- [Sense Audio ClawHub release](https://clawhub.ai/scikkk/senseaudio) <br>
- [Realtime Agent Reference](references/agent.md) <br>
- [ASR Reference](references/asr.md) <br>
- [TTS Reference](references/tts.md) <br>
- [Video and Storyboard Reference](references/video.md) <br>
- [Voice and Cloning Reference](references/voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline request examples, code blocks, and implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoint choices, minimal requests, production-ready examples, error handling notes, and model-specific constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
