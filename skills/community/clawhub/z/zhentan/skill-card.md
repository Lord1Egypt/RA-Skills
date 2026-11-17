## Description:

Zhentan is an onchain security agent and Safe co-signer that monitors pending multisig transactions, screens them against behavioral patterns and security data, and helps approve, reject, analyze, or queue transactions and invoices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koshikraj](https://clawhub.ai/user/koshikraj)

### License/Terms of Use:

MIT-0

## Use Case:

External Safe owners and operators use Zhentan to monitor multisig activity, request risk analysis, approve or reject flagged transactions, manage screening rules, and queue invoices for payment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route high-impact wallet co-signing, approvals, and invoice flows through a remote API.

Mitigation: Use it only with Safes, funds, and invoices you are comfortable routing through Zhentan's remote API, and confirm that backend authorization, audit logging, and transaction simulation meet your requirements.

Risk: AGENT_SECRET is a powerful credential for calls made by this skill.

Mitigation: Store AGENT_SECRET securely, limit access to trusted agent runtimes, rotate it when exposure is suspected, and avoid logging it in command output.

Risk: Approvals, screening changes, and rule or threshold updates can affect irreversible onchain activity.

Mitigation: Confirm irreversible approvals and security-configuration changes out of band, and add stronger confirmation controls before allowing casual chat commands to disable screening or change thresholds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/koshikraj/skills/zhentan)
- [Zhentan API](https://api.zhentan.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl commands and JSON API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and AGENT_SECRET; reports transaction status, transaction hashes, risk scores, rule state, and invoice status from the remote API.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
