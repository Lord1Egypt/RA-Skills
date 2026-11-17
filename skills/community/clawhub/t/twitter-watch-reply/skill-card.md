## Description:

Monitors specified Twitter/X accounts through the 6551 API, filters new posts, and helps an agent draft reply candidates for user-approved browser-based replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yugulugulu](https://clawhub.ai/user/yugulugulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social operators use this skill to monitor selected X/Twitter accounts, generate concise reply drafts, and keep a deduplicated pending/replied state while preserving a manual approval step before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A helper can execute a spoofed local script when rendering alert text from an untrusted working directory.

Mitigation: Avoid or patch render_alert_text.py until it resolves render_alert.py relative to its installed skill directory, and run commands only from a trusted workspace.

Risk: The workflow relies on sensitive 6551 token access and a logged-in X browser session.

Mitigation: Use a scoped 6551 token, keep credentials out of skill files and chats, and enable notifications only for channels and targets you control.

Risk: Generated replies could be posted publicly through the user's social account.

Mitigation: Keep the documented semi-automatic confirmation step for every public reply and verify the selected reply before posting.

## Reference(s):

- [README](README.md)
- [Configuration Example](references/config-example.json)
- [Host Adapter Reference](references/host-adapter.md)
- [Reply Generation Guide](references/reply-generation.md)
- [6551 MCP Token Setup](https://6551.io/mcp)
- [6551 API Base](https://ai.6551.io)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON alert payloads, plain-text alert summaries, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reply candidates are intended for human confirmation before browser-based posting.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
