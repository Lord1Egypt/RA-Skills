## Description: <br>
Guides developers through creating and configuring an Aptos TypeScript SDK client with AptosConfig, network selection, endpoint overrides, singleton use, and Bun compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building Aptos applications use this skill to set up a reusable @aptos-labs/ts-sdk client, choose the right Aptos network, configure custom endpoints, and avoid common client setup mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying examples with mainnet settings, custom endpoints, or added transaction code can affect real assets or route requests through unintended services. <br>
Mitigation: Default to testnet during development, review network and endpoint environment variables before deployment, and inspect any transaction code added around the configured client. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iskysun96/ts-sdk-client) <br>
- [Aptos SDK source references](src/api/aptos.ts, src/api/aptosConfig.ts) <br>
- [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md) <br>
- [Related skill: ts-sdk-account](../ts-sdk-account/SKILL.md) <br>
- [Related skill: ts-sdk-transactions](../ts-sdk-transactions/SKILL.md) <br>
- [Related skill: ts-sdk-wallet-adapter](../ts-sdk-wallet-adapter/SKILL.md) <br>
- [Related skill: use-ts-sdk](../use-ts-sdk/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no code is installed or executed by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
