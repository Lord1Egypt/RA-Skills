## Description: <br>
Bridges the WristClaw watch and OpenClaw agent by recognizing pairing payloads, registering the native WristClaw OpenClaw channel after explicit user confirmation, and keeping replies concise for the watch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salam](https://clawhub.ai/user/salam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to pair an Apple Watch through WristClaw with an OpenClaw agent, then receive concise text, audio, and small-image replies for watch-originated requests. It also guides safe pairing, channel registration, reply formatting, local watch actions, and revocation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates an ongoing smartwatch control channel to the agent. <br>
Mitigation: Require explicit confirmation before pairing, approve only payloads from a trusted account, bind the watch public key, and remove the channel when access is no longer wanted. <br>
Risk: The external plugin, relay, or fallback installer could be inappropriate for a user's trust boundary. <br>
Mitigation: Prefer the npm install path, inspect any fetched shell installer before execution, and use only relays the user trusts. <br>
Risk: Watch-originated requests can touch sensitive or destructive agent capabilities. <br>
Mitigation: Require explicit confirmation for destructive actions, limit sensitive reads to user-requested scope, and avoid live location lookups unless the request needs them. <br>


## Reference(s): <br>
- [WristClaw homepage](https://wristclaw.app) <br>
- [ClawHub skill listing](https://clawhub.ai/salam/wristclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent replies on the watch are intended to be short plain text, with optional audio and small image delivery through the WristClaw channel.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
