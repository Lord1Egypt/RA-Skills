## Description: <br>
Nostr P2P messaging gateway for AI agents. Send and receive E2E encrypted messages via the Nostr protocol. Enables your agent to be reachable from Sigil Messenger, Damus, and any Nostr client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmanchu](https://clawhub.ai/user/lmanchu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent a Nostr identity, receive encrypted direct messages from Nostr clients, and route replies through an agent bridge. It is intended for agent messaging workflows that need peer-to-peer client access through Sigil, Damus, Primal, or compatible Nostr clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge stores a long-lived Nostr messaging key for the agent. <br>
Mitigation: Protect ~/.sigil key files with strict local permissions and use Sigil key encryption or passphrase protection where available. <br>
Risk: Remote messages can be forwarded to the configured agent or tools. <br>
Mitigation: Keep personal mode and allowlists enabled, review the access-control file before use, and avoid public service mode unless broad access is intended. <br>
Risk: Hermes mode has broader routing and execution risk according to the security guidance. <br>
Mitigation: Avoid Hermes mode until message routing uses safer argument-array execution and a narrower capability set. <br>
Risk: Gateway mode shares decrypted conversations and sender metadata with the configured gateway service. <br>
Mitigation: Use only trusted gateway endpoints and treat gateway logs and storage as sensitive conversation data. <br>


## Reference(s): <br>
- [Sigil GitHub](https://github.com/lmanchu/sigil) <br>
- [Sigil Landing Page](https://lmanchu.github.io/sigil/) <br>
- [Agent Registry](https://github.com/lmanchu/sigil#agent-registry-kind31990) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Sigil key and access-control files when bridge commands are run.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
