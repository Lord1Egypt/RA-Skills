## Description:

Mokshya agent-wallet guides agents through public REST API and TEE signing troubleshooting for wallets.mokshya.io, GKE deployment, create/sign HTTP flows, rate limits, and inconsistent agent_id lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evilboyajay](https://clawhub.ai/user/evilboyajay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to debug Mokshya wallet API behavior, TEE signing flows, agent_id ownership mismatches, and GKE/Postgres deployment configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive wallet materials or deployment secrets could be exposed while following troubleshooting steps.

Mitigation: Treat key_share, transaction data, HMAC secrets, database URLs, and TEE master keys as sensitive, and avoid pasting or committing them.

Risk: Signing guidance could be applied to unauthorized endpoints or accounts.

Mitigation: Use create and sign flows only against endpoints and accounts you are authorized to operate.

Risk: Multi-replica API deployments without persistent database configuration can return inconsistent wallet ownership data.

Mitigation: Configure DATABASE_URL with Postgres before running more than one API replica.

## Reference(s):

- [Mokshya agent TEE wallet repository](https://github.com/mokshyaprotocol/agent-tee-wallet)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands, configuration names, and API route examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; does not install code or run hidden actions.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter: 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
