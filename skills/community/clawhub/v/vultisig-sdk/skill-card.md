## Description:

Use this skill when an agent needs to create crypto wallets, send transactions, swap tokens, check balances, or perform on-chain operations across 36+ blockchains using threshold signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realpaaao](https://clawhub.ai/user/realpaaao)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to guide agents through Vultisig SDK wallet creation, balance queries, token sends, swaps, vault import/export, and transaction lifecycle tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may execute crypto transactions autonomously, including transfers and swaps that are irreversible.

Mitigation: Use explicit transaction limits, recipient verification, and human approval for meaningful value before signing or broadcasting.

Risk: Vault passwords, vault backups, and seedphrases are sensitive and can lead to loss or compromise if mishandled.

Mitigation: Keep secrets out of logs and plaintext storage, use strict handling rules, and start with test wallets or low-value accounts.

Risk: Fast Vault flows can default to VultiServer co-signing without human approval.

Mitigation: Use Secure Vault or a policy-gated Fast Vault setup for high-value, treasury, or compliance-sensitive activity.

Risk: SDK version drift can change wallet or transaction behavior.

Mitigation: Pin and audit SDK versions before deployment.

## Reference(s):

- [Vultisig SDK Repository](https://github.com/vultisig/vultisig-sdk)
- [SDK Users Guide](https://github.com/vultisig/vultisig-sdk/blob/main/docs/SDK-USERS-GUIDE.md)
- [Agent Integration Guide](https://github.com/vultisig/vultisig-sdk/blob/main/docs/agent.md)
- [Architecture](https://github.com/vultisig/vultisig-sdk/blob/main/docs/architecture/ARCHITECTURE.md)
- [Security & Technology](https://docs.vultisig.com/security-and-technology/security-technology)
- [Fast Vault Docs](https://docs.vultisig.com/infrastructure/what-is-vultisigner/how-does-vultisigner-work)
- [ClawHub Skill Page](https://clawhub.ai/realpaaao/skills/vultisig-sdk)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes transaction, wallet, swap, vault backup, and seedphrase handling procedures.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
