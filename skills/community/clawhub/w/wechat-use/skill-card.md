## Description:

Wechat Use helps agents on macOS send WeChat messages, query local contacts and chat history, stream new messages, and connect through local HTTP or gRPC surfaces.

This skill is for research and development only.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically capable end users use this skill for personal or research automation of their own macOS WeChat account, including sending messages, retrieving chat context, exporting history, and wiring local message streams into agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party native tool with broad access to local WeChat database keys, chat history, contacts, media, sending, and background processes.

Mitigation: Install only after reviewing the source and required permissions; treat cached WeChat key material like a password and keep it out of commits, logs, and chat transcripts.

Risk: Installer and update flows can use curl-to-bash or unpinned release paths.

Mitigation: Verify the project source and release artifact before installation or upgrade, and avoid unpinned update paths unless the source can be independently checked.

Risk: The local bridge can expose private message data and message-sending capabilities, especially if tunneled or bound for remote access.

Mitigation: Keep the bridge local by default; when remote access is required, require strong bearer authentication and network controls before exposing it.

Risk: Automating WeChat may violate Tencent policies or applicable messaging laws and can lead to account suspension, bans, or downstream misuse.

Mitigation: Use only for the user's own account and personal or research workflows, avoid spam or third-party account automation, and confirm local legal and platform-policy compliance before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/wechat-use)
- [Server-resolved GitHub source](https://github.com/leeguooooo/wechat-use)
- [SSE payload schema](https://github.com/leeguooooo/wechat-use/blob/main/wx/schema/sse-payload-v1.10.28.schema.json)
- [AI agent integration notes](https://github.com/leeguooooo/wechat-use#%E6%8E%A5-ai-agent)
- [Release history](https://github.com/leeguooooo/wechat-use/releases)
- [Issue tracker](https://github.com/leeguooooo/wechat-use/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/YAML parsing notes, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct agents to invoke local WeChat CLI or bridge commands that can access private WeChat data and send messages.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.12.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
