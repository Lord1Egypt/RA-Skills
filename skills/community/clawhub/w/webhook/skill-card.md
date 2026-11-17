## Description:

Implement secure webhook receivers and senders with proper verification and reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement webhook receivers and senders with signature verification, replay prevention, idempotent handling, retry behavior, delivery tracking, and operational safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook logging guidance may expose sensitive URLs, payloads, response bodies, or secrets during errors and delivery tracking.

Mitigation: Redact sensitive fields, URLs, and bodies in logs; capture raw payloads or response bodies only in short-lived, access-controlled debug workflows.

Risk: Outbound webhook delivery can introduce SSRF exposure when destination URLs or redirects are not tightly controlled.

Mitigation: Add SSRF protections for outbound destinations, disable redirects or validate them tightly, enforce HTTPS certificate validation, and bound response sizes.

Risk: The security scan verdict is suspicious, so production use without review may preserve unsafe or incomplete guidance.

Mitigation: Review and amend the guidance before relying on it for production webhook code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/webhook)
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation advice and checklists for webhook security, reliability, event design, and delivery operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
