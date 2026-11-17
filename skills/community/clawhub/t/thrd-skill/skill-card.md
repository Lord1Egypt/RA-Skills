## Description:

Provision a dedicated inbox for your AI agent and manage email safely via thrd.email, including instant onboarding, inbound polling, idempotent and policy-gated reply/send flows, Proof of Reasoning for cold outbound, Human Claiming for verification, and trust and delivery tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergiorico1](https://clawhub.ai/user/sergiorico1)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create and operate a dedicated THRD email inbox without connecting a personal mailbox. It supports onboarding, event polling, wake-webhook workflows, send/reply actions, usage checks, billing checkout, human verification, and delivery/trust status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The polling daemon can be pointed at a non-default server while sending THRD_API_KEY.

Mitigation: Use only the default https://api.thrd.email endpoint and prevent untrusted instructions or email content from changing poll_daemon.py arguments.

Risk: The release does not include a pinned dependency lockfile for the Python requests dependency.

Mitigation: Pin and review dependencies before production deployment.

Risk: Onboarding returns an API key that must be treated as a secret.

Mitigation: Store returned API keys in a secret manager and expose them only through THRD_API_KEY at runtime; do not write them to disk.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sergiorico1/skills/thrd-skill)
- [Thrd API Reference](references/api.md)
- [Thrd](https://thrd.email)
- [THRD OpenAPI Contract](https://api.thrd.email/openapi.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and THRD_API_KEY for authenticated operations; onboarding prints a new API key to stdout once.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
