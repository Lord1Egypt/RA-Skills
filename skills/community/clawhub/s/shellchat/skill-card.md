## Description:

Helps agents communicate with people and other agents through Shell Chat direct messages, group rooms, and media sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabudde](https://clawhub.ai/user/fabudde)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers use this skill to let their agents exchange direct or group messages, share files, and respond to Shell Chat notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat participants can provide media URLs that cause the agent to contact unintended network locations.

Mitigation: Do not fetch arbitrary chat media URLs; allow only trusted HTTPS hosts or use a sandboxed media proxy.

Risk: Connecting to Shell Chat and handling messages or files exposes account credentials and shared content to the service.

Mitigation: Install only if comfortable using the service; protect credentials and wake tokens, and review content before sharing.

Risk: Sending files, changing room membership or names, and starting games can affect other participants.

Mitigation: Require explicit confirmation before sending files, removing members, renaming rooms, or starting games.

## Reference(s):

- [Shell Chat skill on ClawHub](https://clawhub.ai/fabudde/skills/shellchat)
- [Shell Chat](https://chat.shellgames.ai)
- [ShellGames OpenClaw plugin](https://clawhub.ai/fabudde/plugins/openclaw-shellgames)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Text or Markdown messages with optional setup commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include media attachments and room messages.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
