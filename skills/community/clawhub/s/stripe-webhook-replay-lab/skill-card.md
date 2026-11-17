## Description:

Replay signed Stripe webhook payloads to a local or staging endpoint for idempotency and retry debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to replay signed Stripe webhook events against local or staging endpoints and check idempotency, retry handling, status codes, and latency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Stripe webhook secret while generating signed webhook replay requests.

Mitigation: Use test webhook secrets and non-production payloads, and avoid running the skill on shared or privileged hosts.

Risk: Webhook replay can mutate customer, payment, subscription, or account state if pointed at a production endpoint.

Mitigation: Point the skill at local or staging endpoints unless the target system has been reviewed for safe replay behavior.

Risk: Temporary response files are written during replay attempts.

Mitigation: Review the script before installation and run it in an environment where temporary files do not expose sensitive response data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/stripe-webhook-replay-lab)
- [ClawHub publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The replay script prints event id and type, per-attempt HTTP status and latency, and a pass/fail summary.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
