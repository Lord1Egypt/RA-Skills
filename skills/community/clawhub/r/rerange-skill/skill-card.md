## Description: <br>
Build, preview, monitor, rerange, close, and risk-check non-custodial Rerange liquid orders using @rerange/wagmi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rerange](https://clawhub.ai/user/rerange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, wallet-connected assistants, portfolio agents, treasury agents, and autonomous resolvers use this skill to discover Rerange deployments, build and preview liquid orders, monitor order state, run permissionless reranges, manage scoped vault delegation, compose bounded strategies, and perform preflight safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto order automation can create financial loss through bad approvals, Permit2 signatures, vault delegation, close, call, multicall, resolver automation, market movement, gas cost, or unsupported deployment choices. <br>
Mitigation: Use the skill only in a wallet-aware environment, prefer canonical Rerange deployments and trusted RPC providers, run preview and simulation checks, and review every transaction or automation policy before execution. <br>
Risk: Private keys, seed phrases, or broad signing authority could compromise user assets if shared with an agent or untrusted runtime. <br>
Mitigation: Keep signing in a wallet or trusted runtime, never provide private keys or seed phrases, and avoid granting withdrawal authority to autonomous agents. <br>


## Reference(s): <br>
- [Rerange homepage](https://rerange.xyz) <br>
- [Rerange skill page](https://clawhub.ai/rerange/rerange-skill) <br>
- [Protocol deployments](https://github.com/rerange-xyz/info/tree/main/protocol/deployments) <br>
- [Protocol ABIs](https://github.com/rerange-xyz/info/tree/main/protocol/abi) <br>
- [Protocol interfaces](https://github.com/rerange-xyz/info/tree/main/protocol/interfaces) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and Node.js helper command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes unsigned transaction intent guidance and read-only helper outputs; signing remains in a wallet or trusted runtime.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
