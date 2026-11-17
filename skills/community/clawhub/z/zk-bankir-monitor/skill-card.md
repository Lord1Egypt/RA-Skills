## Description:

Monitor a ZK-Bankir sovereign banking treasury via API - health checks, balance queries, decision ledger tracking, and hash-chain verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1beekeeper](https://clawhub.ai/user/1beekeeper)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check ZK-Bankir server health, treasury balances, recent decisions, and local hash-chain integrity from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill contradicts read-only claims by documenting a state-changing decision creation request over unauthenticated plain HTTP.

Mitigation: Use against an isolated local development server only, or remove the decision-creation example before deployment. Require HTTPS, authentication, and explicit confirmation for any state-changing request.

Risk: The skill queries treasury, admin, and decision endpoints that may expose sensitive operational data when used against a remote server.

Mitigation: Limit endpoint access to trusted networks and authorized users, avoid remote production monitoring until authentication is enabled, and review outputs before sharing them.

Risk: Premium webhook alerts could disclose treasury or decision status to third-party destinations.

Mitigation: Restrict webhook destinations, avoid sending secrets or private treasury details, and document what fields are included in alerts.

## Reference(s):

- [ZK-Bankir repository](https://gitlab.com/1Beekeeper/zk-bankir)
- [ZK-Bankir documentation](https://gitlab.com/1Beekeeper/zk-bankir/-/tree/main/docs)
- [De 10 Gebuden doctrine](https://gitlab.com/1Beekeeper/zk-bankir/-/blob/main/docs/02-doctrine.md)
- [ClawHub skill page](https://clawhub.ai/1beekeeper/skills/zk-bankir-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only API query results, status summaries, troubleshooting guidance, and local verification commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
