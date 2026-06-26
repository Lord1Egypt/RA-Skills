## Description: <br>
Build non-custodial wallets where end users retain control of their private keys via Circle's user-controlled wallets SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Circle user-controlled wallet flows for wallet creation, authentication, balance checks, and user-approved token transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet API keys, user tokens, or encryption keys could be exposed if copied into frontend code, logs, or browser-readable storage. <br>
Mitigation: Keep CIRCLE_API_KEY server-side, avoid logging secrets, and replace localStorage or script-readable cookie storage with production-grade secure storage such as httpOnly cookies. <br>
Risk: Incorrect or automated transfer execution can cause loss of funds, especially on mainnet. <br>
Mitigation: Default to testnets during development, validate destination, amount, network, and token values, and require explicit user confirmation before executing transfers. <br>
Risk: Using unpinned dependencies may introduce unreviewed SDK behavior changes. <br>
Mitigation: Pin package versions for production builds and review SDK release notes during upgrades. <br>


## Reference(s): <br>
- [Circle Developer Docs](https://developers.circle.com/llms.txt) <br>
- [Circle Wallet Account Types](https://developers.circle.com/wallets/account-types) <br>
- [Creating User-Controlled Wallets with PIN](references/create-wallet-pin.md) <br>
- [Creating User-Controlled Wallets with Social Login](references/create-wallet-social-login.md) <br>
- [Creating User-Controlled Wallets with Email OTP](references/create-wallet-email-otp.md) <br>
- [Sending Transactions from User-Controlled Wallets](references/send-transaction.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, bash, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes implementation guidance for backend and frontend wallet flows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
