## Description: <br>
Build crypto wallets using Circle Modular Wallets SDK with passkey authentication, gasless transactions, and extensible module architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Circle Modular Wallet smart accounts with WebAuthn passkeys, sponsored user operations, batch transactions, and BIP-39-based passkey recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet code can move real assets or perform account recovery actions if used on mainnet. <br>
Mitigation: Default to testnets and require explicit user review of destination, amount, network, token, and recovery action before execution. <br>
Risk: Client keys, passkey credentials, and recovery phrases can expose accounts if hardcoded, logged, committed, or stored insecurely. <br>
Mitigation: Use environment variables or a secrets manager, keep recovery phrases outside the repository, and replace localStorage examples with production-grade protected storage. <br>
Risk: Incorrect chain support or transport URL configuration can produce failed or unintended wallet operations. <br>
Mitigation: Use only supported EVM chains and append the required chain-specific path segment to the Circle modular transport URL. <br>


## Reference(s): <br>
- [Circle Smart Account with Passkey Authentication](references/circle-smart-account.md) <br>
- [Passkey Recovery for Circle Smart Accounts](references/passkey-recovery.md) <br>
- [Circle Developer Docs](https://developers.circle.com/llms.txt) <br>
- [Circle Modular Wallet Console Setup](https://developers.circle.com/wallets/modular/console-setup) <br>
- [Circle Wallet Account Types](https://developers.circle.com/wallets/account-types) <br>
- [Circle Smart Account Example](https://github.com/circlefin/modularwallets-web-sdk/blob/master/examples/circle-smart-account/index.tsx) <br>
- [Circle Passkey Recovery Example](https://github.com/circlefin/modularwallets-web-sdk/blob/master/examples/passkey-recovery/index.tsx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include security warnings and explicit confirmation steps before mainnet transfers or recovery actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
