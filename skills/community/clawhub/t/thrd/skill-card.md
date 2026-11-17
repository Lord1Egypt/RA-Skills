## Description:

Provision a dedicated inbox for your AI agent and manage email safely via thrd.email. Includes instant onboarding, inbound polling, reply/send (idempotent + policy-gated), Proof of Reasoning for cold outbound, Human Claiming for verification, and trust/delivery tracking. Does not persist API keys to disk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergiorico1](https://clawhub.ai/user/sergiorico1)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to provision a dedicated THRD email inbox for an AI agent, poll inbound mail, send or reply to messages, manage verification flows, and monitor usage or delivery status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom poll daemon base URL can receive the THRD_API_KEY during email polling.

Mitigation: Use the default api.thrd.email endpoint unless the alternate endpoint has been reviewed and trusted; run the skill in an isolated environment and keep THRD_API_KEY in a secret manager.

Risk: Authenticated email operations can send, reply to, or poll agent inbox content.

Mitigation: Install only when the THRD service is trusted, review outbound actions before use, monitor monthly usage, and rely on the documented Prompt Shield and security acknowledgement flow for high-risk inbound context.

## Reference(s):

- [Thrd API Reference](references/api.md)
- [THRD website](https://thrd.email)
- [ClawHub skill page](https://clawhub.ai/sergiorico1/skills/thrd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and THRD_API_KEY for authenticated email operations; onboarding can emit a redacted API key by default.]

## Skill Version(s):

1.4.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
