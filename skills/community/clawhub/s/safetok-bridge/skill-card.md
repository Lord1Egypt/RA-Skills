## Description: <br>
Connect safeTok Nostr DMs to your OpenClaw agent. Use OpenClaw with Claude OAuth — no Anthropic API key needed. Communicate via safeTok NIP-44 encrypted DMs from your phone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ductapecode](https://clawhub.ai/user/ductapecode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect safeTok encrypted Nostr DMs to an OpenClaw agent session, allowing mobile DM conversations with an agent through a local bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private DM content may appear in bridge logs during normal operation. <br>
Mitigation: Run the bridge in a private environment, avoid centralized logs for bridge output, and redact or disable logs before handling sensitive conversations. <br>
Risk: The documented sender allowlist advice is not implemented in this version, so untrusted senders may be able to drive the connected agent. <br>
Mitigation: Use a dedicated bot key, limit gateway token privileges where possible, expose the bot only to trusted contacts, and treat allowlist controls as unavailable until implemented. <br>
Risk: The bridge needs OpenClaw gateway write access and a safeTok bot private key. <br>
Mitigation: Store credentials in an environment-specific secret manager, rotate them if exposed, and avoid reusing the bot key or gateway token for other services. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ductapecode/skills/safetok-bridge) <br>
- [safeTok](https://safetok.me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown setup guidance with bash snippets and text replies carried through encrypted Nostr DMs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running OpenClaw gateway, a gateway token, a safeTok bot private key, Node.js 22 or newer, and @noble/curves.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
