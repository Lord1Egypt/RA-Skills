## Description:

Walletconnect Agent helps agents connect to Web3 dApps through WalletConnect v2 and sign wallet requests such as transactions, messages, typed data, NFT mints, DAO votes, and Basename registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to give an agent WalletConnect access to Web3 dApps and automate wallet actions on supported EVM chains. It is intended for dedicated, low-value wallets where the operator accepts the risk of automated signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated WalletConnect signing can approve transactions, token approvals, typed-data signatures, and other wallet actions with irreversible financial impact.

Mitigation: Use only a dedicated, low-value wallet, keep primary or funded wallets out of scope, and treat every signature or transaction as irreversible.

Risk: Default auto-approve mode gives connected dApps broad transaction authority without strong user confirmation or transaction validation.

Mitigation: Use --interactive for any new or untrusted dApp, review displayed transaction details, and verify the dApp origin and WalletConnect URI before pairing.

Risk: Private keys can be exposed through shell history, process listings, logs, or accidental repository commits.

Mitigation: Provide PRIVATE_KEY only through environment variables, do not pass private keys as command arguments, and keep audit logs and environment handling restricted.

Risk: Raw eth_sign can sign arbitrary data and is commonly abused in phishing flows.

Mitigation: Keep eth_sign blocked by default and enable --allow-eth-sign only for a clearly understood, necessary use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daaab/skills/walletconnect-agent)
- [Publisher profile](https://clawhub.ai/user/daaab)
- [Base Names](https://www.base.org/names)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript command examples and runtime console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local audit log files under the user's home directory during execution.]

## Skill Version(s):

1.6.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
