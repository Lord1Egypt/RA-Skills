## Description: <br>
Self-evolving voice assistant UI. Talk to your AI, ask it to improve itself, and watch the code update in real-time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yukihamada](https://clawhub.ai/user/yukihamada) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to run a local browser voice assistant that transcribes speech, sends prompts to an OpenClaw agent, speaks responses, and can request UI or code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local voice interface can pass spoken prompts to an agent with broad file, Git, and API authority. <br>
Mitigation: Install in an isolated workspace, review diffs before retaining changes, and require explicit confirmation before keeping or committing agent-initiated edits. <br>
Risk: Provider credentials may be exposed through the local browser flow or over permissive local endpoints. <br>
Mitigation: Use a disposable or tightly scoped API key, keep provider keys server-side where possible, restrict CORS and origins, and avoid running the server while visiting untrusted sites. <br>
Risk: Automatic Git commits can preserve unintended or unsafe changes. <br>
Mitigation: Disable automatic commits or gate them behind user approval, then inspect commit contents before pushing or reusing the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yukihamada/voice-ui) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenAI](https://openai.com) <br>
- [Anthropic](https://anthropic.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Voice-driven browser UI with plain-text agent responses, code edits, Git commands, and configuration snippets when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local HTTP endpoints, browser microphone input, OpenAI Whisper/TTS calls, and an OpenClaw voice agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
