## Description:

Connect safeTok Nostr DMs to your OpenClaw agent. Use OpenClaw with Claude OAuth — no Anthropic API key needed. Communicate via safeTok NIP-44 encrypted DMs from your phone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ductapecode](https://clawhub.ai/user/ductapecode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to run a bridge that forwards safeTok NIP-44 encrypted Nostr DMs into a dedicated OpenClaw session and returns encrypted assistant replies through Nostr relays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge exposes a dedicated OpenClaw session to messages arriving through public Nostr relays with weak access controls.

Mitigation: Use a separate minimally privileged gateway token and bot key, and restrict allowed senders before use.

Risk: Sensitive plaintext DM content may be logged by the bridge process.

Mitigation: Remove plaintext logging and route runtime logs to protected storage before production use.

Risk: The gateway or dependency setup may be unsafe for production if left with broad network exposure or unpinned dependencies.

Mitigation: Keep the gateway loopback-only unless remote access is deliberately secured, and pin dependencies with a lockfile before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ductapecode/skills/safetok-bridge)
- [safeTok](https://safetok.me)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown instructions with bash and JavaScript snippets plus Node.js bridge files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22 or newer, an OpenClaw gateway token, a safeTok/Nostr private key, and relay configuration.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
