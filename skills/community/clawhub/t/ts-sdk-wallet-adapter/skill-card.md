## Description: <br>
Guides React developers through Aptos wallet integration with @aptos-labs/wallet-adapter-react, including provider setup, useWallet(), frontend transaction submission, and wallet connection UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers integrating Aptos wallet connections in React frontends use this skill to configure the wallet adapter provider, call useWallet(), submit transactions through a browser wallet, and avoid private-key handling in frontend code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Adding the Aptos wallet adapter introduces a frontend dependency into the application. <br>
Mitigation: Review and pin the dependency through the app's normal package-management process before release. <br>
Risk: Users could be asked to sign a transaction on the wrong network or without enough context. <br>
Mitigation: Show the intended network and transaction details clearly before wallet signing, and verify the provider network configuration. <br>
Risk: Frontend code that handles raw private keys would expose users to key compromise. <br>
Mitigation: Use the browser wallet adapter for end-user signing and keep private-key generation or custody out of React frontend code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iskysun96/ts-sdk-wallet-adapter) <br>
- [Aptos Wallet Adapter Documentation](https://aptos.dev/build/sdks/wallet-adapter/dapp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, TSX, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes frontend wallet setup patterns, transaction submission guidance, and safety reminders for browser wallet handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
