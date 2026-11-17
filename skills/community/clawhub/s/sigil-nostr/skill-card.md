## Description:

Nostr P2P messaging gateway for AI agents. Send and receive E2E encrypted messages via the Nostr protocol. Enables your agent to be reachable from Sigil Messenger, Damus, and any Nostr client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmanchu](https://clawhub.ai/user/lmanchu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make an AI agent reachable over Nostr encrypted direct messages from Sigil Messenger, Damus, Primal, Amethyst, or another Nostr client. It provides setup guidance and a bridge script for routing messages between Nostr and OpenClaw, Hermes, or a custom agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill overstates its working bridge behavior.

Mitigation: Review the bridge behavior before deployment and use the Rust bridge recommended by the skill for live operation.

Risk: The security evidence identifies under-scoped handling for private keys stored under ~/.sigil.

Mitigation: Protect private key files with restrictive permissions or encryption and avoid sharing agent identities beyond the intended access model.

Risk: The install instructions use a mutable Git source for the Sigil CLI.

Mitigation: Install a pinned and reviewed Sigil CLI version before using the skill in a production or customer-facing environment.

Risk: The security evidence flags a dormant unsafe Hermes command path when remote messages are routed into Hermes.

Mitigation: Do not connect the Node Hermes route to remote messages unless shell command construction is replaced and the receiving agent tools are narrowly scoped.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lmanchu/skills/sigil-nostr)
- [Sigil GitHub Repository](https://github.com/lmanchu/sigil)
- [Sigil Landing Page](https://lmanchu.github.io/sigil/)
- [Sigil Agent Registry](https://github.com/lmanchu/sigil#agent-registry-kind31990)
- [Sigil Messenger on App Store](https://apps.apple.com/app/sigil-messenger/id6761321150)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command, JSON configuration, and JavaScript bridge examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and local bridge behavior for agent messaging over Nostr.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
