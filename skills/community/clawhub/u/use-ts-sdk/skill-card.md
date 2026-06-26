## Description: <br>
Orchestrates Aptos TypeScript SDK integration for fullstack dApps and routes agents to setup, account, transaction, view, type, and wallet-adapter guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate the Aptos TypeScript SDK into frontend or fullstack dApps, especially when tasks span client setup, account handling, transaction submission, view functions, types, and wallet connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Aptos transaction payloads, addresses, networks, or gas settings may be incorrect for the user's target deployment. <br>
Mitigation: Review payloads, addresses, network selection, and gas settings before signing or submitting transactions. <br>
Risk: Private keys or sensitive account material could be exposed if copied into frontend code, browser-exposed environment variables, committed files, or logs. <br>
Mitigation: Keep private keys server-only, load them from protected server-side environment variables, and exclude them from browser bundles, logs, and source control. <br>


## Reference(s): <br>
- [Aptos TypeScript SDK documentation](https://aptos.dev/build/sdks/ts-sdk) <br>
- [Aptos TypeScript SDK API reference](https://aptos-labs.github.io/aptos-ts-sdk/) <br>
- [Aptos wallet adapter documentation](https://aptos.dev/build/sdks/wallet-adapter/dapp) <br>
- [Aptos TypeScript SDK GitHub repository](https://github.com/aptos-labs/aptos-ts-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript code examples, links, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route the agent to companion Aptos SDK skills when a task needs narrower guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
