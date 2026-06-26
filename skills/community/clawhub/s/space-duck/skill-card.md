## Description: <br>
Space Duck connects an agent to the Space Duck identity network for pairing, status, trust-tier checks, peck connections, messaging, listeners, workspace bridge operations, and Mission Control navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askegor](https://clawhub.ai/user/askegor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to pair an agent with a Space Duck identity, manage peck connections, send and receive network messages, inspect status and permissions, and operate optional local listeners or workspace bridge services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because the skill can enable persistent local listeners, remote-control actions, and workspace file exposure. <br>
Mitigation: Install only when those capabilities are intended; review listener, tunnel, service, and workspace bridge setup before enabling them. <br>
Risk: The Beak Key authorizes Space Duck agent actions and is stored on the local machine. <br>
Mitigation: Protect the key, keep the config file private, avoid pasting secrets into chat, and rotate the key if it may have been exposed. <br>
Risk: Publicly exposed listeners or workspace bridge endpoints could increase local process and file-access risk. <br>
Mitigation: Prefer private or authenticated exposure, avoid unauthenticated public listeners, and verify HMAC/TLS and tunnel configuration before use. <br>
Risk: Autonomous responder and snapshot or sync behavior may operate beyond the operator's intended scope. <br>
Mitigation: Disable autonomous responder, workspace snapshot, or sync behavior unless needed, and use strict consent for remote Telegram control actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/askegor/skills/space-duck) <br>
- [Space Duck API Reference](artifact/references/api.md) <br>
- [Capability Grants](artifact/references/grants.md) <br>
- [Space Duck Scripts](artifact/scripts/README.md) <br>
- [BYOB Workspace Bridge](artifact/scripts/WORKSPACE_BRIDGE_README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented instructions with shell command invocations, JSON responses, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start or configure local listener, Telegram, update, diagnostic, peck, and workspace bridge workflows when explicitly invoked by the user.] <br>

## Skill Version(s): <br>
0.4.14 (source: server release evidence, changelog released 2026-06-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
