## Description: <br>
Tracebit Canaries helps agents deploy and monitor Tracebit honeytoken canaries for credential theft, prompt injection, data exfiltration, and human-supervised incident response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alessandro-brucato-tracebit](https://clawhub.ai/user/alessandro-brucato-tracebit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and agent operators use this skill to set up Tracebit canary credentials, configure recurring alert checks, and follow a human-supervised incident response workflow when a canary is triggered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation may lead an agent to begin account setup, CLI authentication, credential-store changes, or recurring monitoring when the user expected only security advice. <br>
Mitigation: Require explicit user confirmation before setup, account creation, CLI install/auth, canary deployment, heartbeat changes, email access, messaging, and cleanup. <br>
Risk: Canary deployment and incident response touch sensitive areas such as credential stores, email search, messaging, memory files, and temporary credentials. <br>
Mitigation: Keep email access read-only, send notifications only to the user's configured channel, avoid exposing canary or auth token values, and require human approval before reading memory files or rotating canaries. <br>
Risk: Installing the Tracebit CLI introduces a persistent local tool and background daemon. <br>
Mitigation: Install only from official releases with mandatory SHA256 verification, run as the current user, and use the documented removal steps when canaries are no longer needed. <br>


## Reference(s): <br>
- [Tracebit Community](https://community.tracebit.com) <br>
- [Tracebit Canaries on ClawHub](https://clawhub.ai/alessandro-brucato-tracebit/tracebit-canary-honeytokens) <br>
- [Security Compliance](references/security-compliance.md) <br>
- [Incident Response Playbook](references/incident-response-playbook.md) <br>
- [Canary Types](references/canary-types.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [API Reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append heartbeat and incident-response entries only after the required user confirmations described by the skill.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
