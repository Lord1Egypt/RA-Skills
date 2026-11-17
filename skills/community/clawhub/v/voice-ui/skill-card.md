## Description:

Self-evolving voice assistant UI. Talk to your AI, ask it to improve itself, and watch the code update in real-time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yukihamada](https://clawhub.ai/user/yukihamada)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to run a local browser-based voice assistant that transcribes speech, calls an OpenClaw agent, reads responses aloud, and can request UI or code changes through voice commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local server and OpenClaw integration expose agent, file, Git, credential, and browser capabilities without adequate scoping or user control.

Mitigation: Install only in an isolated test workspace with no sensitive files or credentials, keep port 8765 on localhost, authenticate and constrain /api/chat, and require explicit review before code or Git changes.

Risk: The browser client can receive the OpenAI API key and call external transcription, chat, and speech APIs directly.

Mitigation: Remove browser API-key exposure and proxy external API calls through a constrained server-side path with appropriate authentication and secret handling.

Risk: Self-modifying UI requests can lead to automatic broad Git staging and commits.

Mitigation: Disable automatic git add -A commits and require human review of file diffs before committing changes.

Risk: Static file serving and chat rendering may expose path-handling or content-injection issues.

Mitigation: Fix static file path validation and replace innerHTML rendering with safe text rendering or sanitized markup.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenAI](https://openai.com)
- [Anthropic](https://anthropic.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks; runtime chat responses may trigger local code and Git changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses voice transcription, speech synthesis, and a local OpenClaw agent workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
