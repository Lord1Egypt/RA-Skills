## Description:

TARDIS helps agents create, lock, verify, list, and export tamper-evident elapsed-time meters for uptime, service hours, event counters, project duration, and equipment runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rm289](https://clawhub.ai/user/rm289)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to track time since, until, or between events with tamper-evident locks, paper codes, witness files, milestone checks, JSON exports, and optional email or webhook notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes networked email and webhook features that can expose event data or send outbound notifications when configured.

Mitigation: Install only when those features are needed, run them from a constrained account, and configure only intended SendGrid, Discord, or OpenClaw destinations.

Risk: The webhook server and tunnel helper can expose a local service to the public internet.

Mitigation: Avoid running the webhook server or tunnel helper on sensitive hosts, and prefer controlled ingress with least-privilege runtime credentials.

Risk: Generic .env loading can make unrelated secrets visible to the skill process.

Mitigation: Do not keep unrelated secrets in generic .env files accessible to the skill; use a dedicated environment for SendGrid and webhook credentials.

Risk: Unsigned SendGrid webhook events can be spoofed if signature verification is not configured.

Mitigation: Enable signed SendGrid webhooks, install the cryptography dependency, and set SENDGRID_WEBHOOK_PUBLIC_KEY with a bounded timestamp age.

Risk: ACTION-prefixed milestone messages can become unsafe if an agent is configured to execute them as instructions.

Mitigation: Keep ACTION handling disabled unless explicitly required, and add approval gates plus allowlist controls before treating milestone messages as executable instructions.

## Reference(s):

- [TARDIS ClawHub listing](https://clawhub.ai/rm289/skills/tardis)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [WHITEPAPER.md](artifact/WHITEPAPER.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local meter state, witness logs, webhook logs, and exported JSON files through the bundled command-line scripts.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
