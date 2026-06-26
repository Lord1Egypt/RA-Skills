## Description: <br>
Web3 development using MetaMask Smart Accounts Kit. Use when the user wants to build dApps with ERC-4337 smart accounts, send user operations, batch transactions, configure signers (EOA, passkey, multisig), implement gas abstraction with paymasters, create delegations, or request advanced permissions (ERC-7715). Supports Viem integration, multiple signer types (Dynamic, Web3Auth, Wagmi), gasless transactions, and the Delegation Framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AyushBherwani1998](https://clawhub.ai/user/AyushBherwani1998) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to build dApps with MetaMask smart accounts, ERC-4337 user operations, gas abstraction, signer configuration, delegations, and ERC-7715 advanced permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated wallet automation can expose private keys or grant broader spending authority than intended if examples are copied directly into production. <br>
Mitigation: Use testnets first, never paste or commit real private keys, prefer wallet-managed signing or KMS/HSM-backed secrets for production, and limit delegations by amount, target, redeemer, call count, and expiry. <br>
Risk: Users may approve delegated transactions without fully understanding the resulting authority. <br>
Mitigation: Require clear consent, keep permission scopes narrow, and provide revocation controls for delegated access. <br>


## Reference(s): <br>
- [MetaMask Smart Accounts Kit Documentation](https://docs.metamask.io/smart-accounts-kit) <br>
- [Smart Accounts Reference](references/smart-accounts.md) <br>
- [Delegations Reference](references/delegations.md) <br>
- [Advanced Permissions Reference](references/advanced-permissions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples should be reviewed before use with wallets, keys, or live networks.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
