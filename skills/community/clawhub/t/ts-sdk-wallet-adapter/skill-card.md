## Description:

Guides React developers through Aptos wallet connection with @aptos-labs/wallet-adapter-react, including provider setup, useWallet, frontend transaction submission, and wallet connection UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Aptos wallet connection in React applications and route end-user transaction signing through browser wallets rather than raw private keys. It provides setup guidance, example TypeScript/React snippets, and common mistake corrections for wallet-adapter usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may approve real blockchain actions generated from frontend transaction payloads.

Mitigation: Review transaction payloads, target network, and user-facing wallet prompts before asking users to sign or submit transactions.

Risk: A project could install or import an unofficial package that imitates the Aptos wallet adapter.

Mitigation: Verify that dependencies use the official @aptos-labs/wallet-adapter-react package and review dependency changes before release.

Risk: Frontend code could expose raw private-key handling if developers bypass the wallet adapter pattern.

Mitigation: Use browser wallet signing through useWallet and keep private-key generation or direct signing out of React frontend components.

## Reference(s):

- [Aptos Wallet Adapter documentation](https://aptos.dev/build/sdks/wallet-adapter/dapp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript/React and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes frontend wallet integration patterns, transaction submission guidance, and common mistake remediation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
