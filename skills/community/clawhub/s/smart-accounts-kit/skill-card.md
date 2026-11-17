## Description:

Provides developer guidance for using MetaMask Smart Accounts Kit to build ERC-4337 dApps with smart accounts, user operations, signer configuration, gas abstraction, delegations, advanced permissions, Viem integrations, and related signer frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayushbherwani1998](https://clawhub.ai/user/ayushbherwani1998)

### License/Terms of Use:


## Use Case:

Developers building Web3 dApps use this skill to get implementation guidance, code examples, and configuration steps for MetaMask smart accounts, delegation workflows, gasless transactions, and ERC-7715 advanced permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can authorize automated blockchain transactions if copied into real applications.

Mitigation: Use testnets first and verify chain IDs, addresses, calldata, limits, and expiry values before using production accounts or mainnet assets.

Risk: Transaction and permission examples may move tokens, spend gas or sponsored gas, deploy contracts, or enable recurring automated actions until expiry or revocation.

Mitigation: Use secure signer custody, avoid plaintext production private keys, apply restrictive caveats and time limits, and monitor or revoke delegated permissions.

## Reference(s):

- [MetaMask Smart Accounts Kit documentation](https://docs.metamask.io/smart-accounts-kit)
- [Smart Accounts Reference](references/smart-accounts.md)
- [Delegations Reference](references/delegations.md)
- [Advanced Permissions Reference](references/advanced-permissions.md)
- [MetaMask Smart Accounts Kit 0.3.0 changelog](https://docs.metamask.io/smart-accounts-kit/changelog/0.3.0/)
- [ERC-7715 specification](https://eips.ethereum.org/EIPS/eip-7715)
- [ERC-7710 specification](https://eips.ethereum.org/EIPS/eip-7710)
- [MetaMask Flask](https://metamask.io/flask)
- [Swiss-Knife calldata decoder](https://calldata.swiss-knife.xyz/decoder)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include blockchain transaction, permission, signer, contract address, and troubleshooting guidance.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
