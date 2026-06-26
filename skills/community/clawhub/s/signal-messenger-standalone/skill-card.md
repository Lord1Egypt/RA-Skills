## Description: <br>
Adds Signal messaging for OpenClaw agents through signal-cli, including send and receive workflows, contact roles, voice handling, conversation history, and wake-on-message integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucksus](https://clawhub.ai/user/lucksus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect a standalone OpenClaw bot account to Signal, handle incoming messages, send replies, triage new contacts, and configure wake-on-message behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote Signal messages can wake and steer the agent, and the provided security summary says advertised permission and triage controls are largely advisory rather than enforced. <br>
Mitigation: Use a dedicated Signal bot account, treat every incoming message as untrusted input, and require local confirmation for commands, installs, file or configuration changes, and permission changes requested over Signal. <br>
Risk: The skill stores Signal state, wake tokens, permissions, and conversation logs on disk, which may expose sensitive data if the files are not protected. <br>
Mitigation: Restrict access to the signal-cli data directory, wake token, permissions file, and conversation logs; define retention for plaintext logs or disable logging when conversations may contain sensitive data. <br>


## Reference(s): <br>
- [Signal Contact Permissions](references/permissions.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [signal-cli](https://github.com/AsamK/signal-cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/lucksus/signal-messenger-standalone) <br>
- [Publisher Profile](https://clawhub.ai/user/lucksus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, operating, and troubleshooting guidance for Signal bot messaging workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
