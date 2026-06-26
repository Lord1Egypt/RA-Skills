## Description: <br>
How to read on-chain data in @aptos-labs/ts-sdk using view(), getBalance(), getAccountInfo(), getAccountResources(), getAccountModules(), and getResource(). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query Aptos on-chain data with the TypeScript SDK, including balances, account metadata, resources, modules, and Move view functions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect account addresses, module names, or SDK assumptions can produce misleading blockchain query results. <br>
Mitigation: Verify account addresses, module names, and current SDK behavior before relying on returned on-chain data for important decisions. <br>
Risk: Using JavaScript number values for large Move integers can lose precision. <br>
Mitigation: Use bigint handling for u128 and u256 values, as described by the skill guidance. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/iskysun96/ts-sdk-view-and-query) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/iskysun96) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Aptos SDK query examples and type-handling recommendations] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
