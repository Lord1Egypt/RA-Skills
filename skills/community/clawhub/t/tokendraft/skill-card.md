## Description:

TokenDraft helps agents authenticate with a Solana wallet, query and join fantasy crypto tournaments, configure auto-join workflows, and manage auto-draft asset priority rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikzt](https://clawhub.ai/user/nikzt)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to operate TokenDraft fantasy crypto tournament workflows, including wallet authentication, tournament entry, paid buy-in transaction handling, asset ranking, and scheduled auto-join or auto-ranking tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Solana private key can be used to sign server-supplied buy-in transactions.

Mitigation: Use a wallet with limited funds and require decoded transaction review plus explicit approval before any buy-in transaction is signed.

Risk: Recurring auto-join workflows can enter paid tournaments without spending limits.

Mitigation: Avoid paid auto-join unless the user sets clear spend limits and reviews the scheduled workflow before enabling it.

## Reference(s):

- [TokenDraft ClawHub listing](https://clawhub.ai/nikzt/skills/tokendraft)
- [TokenDraft API base URL](https://tokendraft-production.up.railway.app)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash, JavaScript, TypeScript, JSON, and OpenClaw cron command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOLANA_PRIVATE_KEY and may propose authenticated API requests, transaction-signing steps, and scheduled cron workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
