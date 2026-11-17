## Description:

Build non-custodial wallets where end users retain control of their private keys using Circle's user-controlled wallets SDK, with support for PIN, email OTP, and social login authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mscandlen3](https://clawhub.ai/user/mscandlen3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to implement Circle user-controlled wallet onboarding and transaction flows where end users authorize sensitive wallet operations. It is suited for applications that need non-custodial wallet creation with PIN, email OTP, or social login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable examples may expose sensitive wallet credentials if copied into production storage patterns.

Mitigation: Keep wallet credentials out of localStorage and JavaScript-readable cookies; use authenticated server-side sessions and httpOnly cookie storage for production flows.

Risk: Transaction examples may leave authorization and transfer controls under-specified.

Mitigation: Validate and authorize destination, amount, network, token, wallet identity, and user identity server-side before creating transfer challenges.

Risk: Mainnet transfers can move real assets if examples are adapted without safeguards.

Mitigation: Default to testnet, require explicit user confirmation before mainnet use, and add warning thresholds for higher-value transfers.

Risk: Dependency and SDK examples may change over time when latest package tags are used.

Mitigation: Pin reviewed dependency versions before production release and retest Circle SDK flows after upgrades.

## Reference(s):

- [Creating User-Controlled Wallets with PIN](references/create-wallet-pin.md)
- [Creating User-Controlled Wallets with Email OTP](references/create-wallet-email-otp.md)
- [Creating User-Controlled Wallets with Social Login](references/create-wallet-social-login.md)
- [Sending Transactions from User-Controlled Wallets](references/send-transaction.md)
- [Circle Developer Docs](https://developers.circle.com/llms.txt)
- [Circle Wallet Account Types](https://developers.circle.com/wallets/account-types)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, TSX, bash, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full-stack backend and frontend implementation steps for Circle user-controlled wallet flows.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
