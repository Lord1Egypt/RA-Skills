## Description:

Guides an authorized operator through setting up a low-balance wallet and managing approved Verdikta bounties and mutual wagers on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nigelon11](https://clawhub.ai/user/nigelon11)

### License/Terms of Use:

MIT-0

## Use Case:

External wallet operators use this skill to configure an authorized Verdikta account, create and submit bounty work, resolve eligible claims, and manage mutual wagers on Base or Base Sepolia. Financial actions use an operator-reviewed spending policy and require approval for the specific action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release security findings flag inaccurate password-storage assurances and misleading preflight results.

Mitigation: Resolve these defects before using real funds, and do not rely on preflight output alone as proof that an action is safe.

Risk: The skill signs irreversible hot-wallet transactions, and spending limits reset for each process.

Mitigation: Use a fresh low-balance wallet, review every transaction, and keep spending limits tight for each run.

Risk: A password file is readable by processes running as the same user.

Mitigation: Prefer a protected secret store; if using a password file, restrict its permissions and avoid running untrusted processes under the same account.

Risk: Signed recovery files can broadcast the exact approved transaction.

Mitigation: Keep signed recovery files private.

Risk: Work-order steps run the separate verdikta-discover package and its dependencies in the signing process.

Mitigation: Review that package separately and protect it from untrusted replacement before enabling work orders.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nigelon11/skills/verdikta-bounties-onboarding)
- [Operator setup and custody](artifact/references/onboarding.md)
- [Commission configuration and spending policy](artifact/references/commission.md)
- [Security and owner withdrawals](artifact/references/security.md)
- [Mutual wagers](artifact/references/wagers.md)
- [Agent API endpoints](artifact/references/api_endpoints.md)
- [Verdikta Bounties mainnet service](https://bounties.verdikta.org)
- [Verdikta Bounties testnet service](https://bounties-testnet.verdikta.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Text guidance, shell commands, and JSON configuration or state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transaction actions are scoped to owner-approved terms and an operator-defined spending policy.]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
