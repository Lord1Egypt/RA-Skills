## Description: <br>
Receive external webhooks and callbacks in real time by exposing a local HTTP endpoint via an aitun tunnel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to receive GitHub webhooks, payment notifications, OAuth callbacks, form submissions, and other third-party HTTP callbacks while working from a local environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full webhook headers and bodies can expose OAuth secrets, payment data, or personal data in logs. <br>
Mitigation: Redact sensitive fields, limit log retention, and avoid full request logging for OAuth, payment, production, or personal-data webhooks. <br>
Risk: Remote install scripts can execute code outside the package manager review path. <br>
Mitigation: Install aitun with pip or uv from a trusted package source and verify the package before use. <br>
Risk: A public tunnel can expose a local webhook handler to untrusted traffic. <br>
Mitigation: Use the skill for controlled webhook testing unless the handler adds request verification, authentication, and response hardening. <br>


## Reference(s): <br>
- [AiTun homepage](https://aitun.cc) <br>
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/webhook-receiver) <br>
- [ClawHub package link](https://clawhub.ai/ctz168/webhook-receiver) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent through installing aitun, starting a local webhook handler, exposing it through a tunnel, registering callback URLs, processing requests, and cleaning up processes.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
