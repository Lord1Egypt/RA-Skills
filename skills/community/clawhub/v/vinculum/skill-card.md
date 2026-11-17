## Description:

Shared consciousness between Clawdbot instances. Links multiple bots into a collective, sharing memories, activities, and decisions in real-time over local network using Gun.js P2P sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and teams use Vinculum to link multiple Clawdbot instances into a shared local-network collective for synchronized memories, activity updates, decisions, relay management, and peer status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared memories, activity, decisions, messages, filenames, and status may be readable or modifiable by anyone who can reach the relay or access relay storage/config.

Mitigation: Use only on trusted private networks, restrict relay access with localhost, VPN, or firewall rules, and avoid sharing secrets or sensitive data.

Risk: The skill claims encryption, but the authoritative security summary says it uses an unauthenticated plaintext relay.

Mitigation: Do not rely on the advertised encryption for sensitive workflows; wait for real client-side encryption and peer authentication before sensitive use.

Risk: Pairing and relay access are not sufficient access controls for untrusted networks.

Mitigation: Treat pairing codes as sensitive, share them only through secure channels, monitor connected peers, and keep relay endpoints off public networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/koba42corp/skills/vinculum)
- [Publisher profile](https://clawhub.ai/user/koba42corp)
- [Declared project homepage](https://github.com/koba42/clawdbot-vinculum)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown command responses with inline command examples, status summaries, relay information, activity lists, decision lists, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and npm; typical operation uses a local Gun.js relay on port 8765 and local configuration under the user's Clawdbot config directory.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
