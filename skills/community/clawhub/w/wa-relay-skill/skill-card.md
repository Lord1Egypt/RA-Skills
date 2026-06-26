## Description: <br>
WhatsApp message relay for OpenClaw v0.2.0 that routes third-party DMs to a relay agent, forwards them to the main agent with sessions_send, and supports direct number allowlists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zarruk](https://clawhub.ai/user/zarruk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to route WhatsApp messages from non-allowlisted senders through a relay agent so the main agent can notify the owner and suggest a response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup copies main-agent model-provider credentials into the relay agent. <br>
Mitigation: Use a separate least-privilege auth profile for the relay and rotate or remove copied credentials if the relay is uninstalled. <br>
Risk: Setup temporarily patches OpenClaw internals and modifies the main agent SOUL.md. <br>
Mitigation: Back up SOUL.md and gateway configuration first, review generated changes before applying them, and restore backups or update OpenClaw when the upstream fix is available. <br>
Risk: The relay can receive WhatsApp messages from non-allowlisted senders. <br>
Mitigation: Review generated bindings before applying them and keep direct-number allowlists narrow. <br>


## Reference(s): <br>
- [Wa Relay setup guide](references/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON/YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create relay workspace files, append main-agent SOUL.md guidance, and emit gateway routing configuration for review before application.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
