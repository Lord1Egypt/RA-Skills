## Description: <br>
Set up Stalwart Mail Server on a new VPS via Dokploy, with default outbound delivery through Resend SMTP relay for environments where direct SMTP port 25 egress is blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a self-hosted Stalwart mail server on Dokploy and route outbound mail through Resend when direct SMTP egress is blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resend API keys, mailbox passwords, Dokploy admin access, and SSH credentials may be exposed during setup. <br>
Mitigation: Use protected secret storage, avoid placing credentials in chat logs, tickets, screenshots, shell history, or repositories, and rotate any credential that may have been exposed. <br>
Risk: DNS, TLS, port, or relay misconfiguration can prevent inbound or outbound mail delivery. <br>
Mitigation: Run the documented preflight checks and verification checklist before relying on the mail server. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/stalwart-dokploy-resend-relay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied domain, VPS SSH access, Dokploy access, and a Resend API key.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
