## Description:

Full-featured X/Twitter toolkit for agents that can read, search, post, interact, manage DMs, lists, polls, and trends through cookie-authenticated command-line scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ignsoftwarellc](https://clawhub.ai/user/ignsoftwarellc)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use X-CLI Toolkit to monitor and search X/Twitter content and, when explicitly authorized, perform account actions such as posting, replies, DMs, follows, lists, polls, and scheduling from command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account credentials and cookies can be exposed through agent chat, shell commands, or plaintext configuration.

Mitigation: Do not paste passwords into agent chats or commands; prefer imported cookies with restrictive local permissions and treat cookies.json and config.json as secrets.

Risk: Authenticated commands can post, delete, send DMs, follow, block, mute, manage lists, create polls, or schedule posts with limited safeguards.

Mitigation: Use a dedicated low-risk account and require explicit manual confirmation before any account-changing command.

Risk: Broad account automation may affect private messages or public reputation if misused or compromised.

Mitigation: Avoid using the skill with accounts whose private messages, audience, or public reputation would be costly to lose.

## Reference(s):

- [X-CLI Toolkit on ClawHub](https://clawhub.ai/ignsoftwarellc/skills/x-cli)
- [X-CLI source homepage](https://github.com/ignsoftwarellc/x-cli)
- [twikit Python X/Twitter API wrapper](https://github.com/d60/twikit)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON command output with command-line setup and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >=3.10, twikit, local cookies or credentials, and optional proxy configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
