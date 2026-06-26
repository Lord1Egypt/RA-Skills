## Description: <br>
Voice conversation interface for OpenClaw using wake word detection, streaming LLM responses, and text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kentoku24](https://clawhub.ai/user/kentoku24) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up a browser-based voice interface that listens for a wake word, sends spoken commands to OpenClaw, and returns streamed speech through VOICEVOX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser microphone capture and speech transcripts may include sensitive spoken information. <br>
Mitigation: Use the skill only in an environment where microphone access is expected, avoid speaking sensitive information until logging and retention behavior is reviewed, and confirm browser microphone permissions before use. <br>
Risk: The local server processes conversation content and forwards requests to the local OpenClaw gateway. <br>
Mitigation: Review where transcripts and responses flow before use, keep the server bound to localhost unless remote access is deliberately configured, and verify any HTTPS or reverse proxy setup. <br>
Risk: The skill can auto-detect and use a local OpenClaw gateway token. <br>
Mitigation: Prefer a scoped token, keep tokens outside the repository, and confirm the OpenClaw gateway token source before starting the server. <br>


## Reference(s): <br>
- [voiceclaw architecture](docs/architecture.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [VOICEVOX](https://voicevox.hiroshiba.jp/) <br>
- [Android wake word feasibility notes](docs/research/android-feasibility-2026-03-01.md) <br>
- [Wake word and voice assistant OSS research notes](docs/research/oss-scan-2026-03-01.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include localhost service URLs, environment variable settings, and browser setup guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
