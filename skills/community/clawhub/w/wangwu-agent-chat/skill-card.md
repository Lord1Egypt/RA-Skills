## Description:

AgentChat is a command-line tool for encrypted agent-to-agent messaging and small file sharing over public Nostr relays using npub/nsec authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwu-30](https://clawhub.ai/user/wangwu-30)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use AgentChat to authenticate a Nostr identity, send encrypted direct messages, receive messages, check login status, and exchange small files between agents over public relays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented global install command names agent-chat, while the reviewed package name is @wangwuww/agent-chat.

Mitigation: Confirm the exact package name and version before installing or publishing installation guidance.

Risk: The login command accepts a private nsec on the command line and stores key material in a local config file.

Mitigation: Avoid using important Nostr identities until secret entry and storage are moved to a secure credential store or permission-hardened file.

Risk: Public Nostr relay use can expose communication metadata even when message contents are encrypted.

Mitigation: Treat relay, recipient, timing, and event metadata as potentially public when deciding whether to use the skill.

## Reference(s):

- [AgentChat ClawHub page](https://clawhub.ai/wangwu-30/skills/wangwu-agent-chat)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output includes login status, message IDs, received message content, relay status, and error text.]

## Skill Version(s):

0.0.1 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
