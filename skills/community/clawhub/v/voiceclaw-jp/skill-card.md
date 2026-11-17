## Description:

voiceclaw provides a voice conversation interface for OpenClaw with wake word detection, streaming LLM responses, and VOICEVOX text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kentoku24](https://clawhub.ai/user/kentoku24)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to add a browser-based spoken interface for local OpenClaw agents. It supports configurable wake words, browser speech recognition, streaming chat responses, and sentence-level speech playback through VOICEVOX.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local service can expose OpenClaw access if port 8788 is made reachable without authentication or TLS.

Mitigation: Keep the service bound to 127.0.0.1; add authentication and TLS before using HOST=0.0.0.0 or exposing the service remotely.

Risk: Configured OpenClaw or VOICEVOX endpoints may receive spoken commands and conversation history.

Mitigation: Use trusted local backends and avoid pointing OPENCLAW_GATEWAY_URL or VOICEVOX_URL at untrusted remote services.

Risk: The service may use an automatically discovered OpenClaw gateway token.

Mitigation: Prefer an explicit least-privilege OpenClaw token for this voice assistant and review token access before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kentoku24/skills/voiceclaw-jp)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [VOICEVOX](https://voicevox.hiroshiba.jp/)
- [Architecture](docs/architecture.md)
- [OSS wake word research](docs/research/oss-scan-2026-03-01.md)
- [Android wake word feasibility](docs/research/android-feasibility-2026-03-01.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration details, and Node.js/browser code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup guidance and a voice UI/server implementation that relays speech-derived prompts to OpenClaw and returns spoken responses.]

## Skill Version(s):

0.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
