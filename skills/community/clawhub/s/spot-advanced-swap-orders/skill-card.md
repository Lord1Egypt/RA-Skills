## Description: <br>
Use for gasless non-custodial EVM market, limit, TWAP, stop-loss, take-profit, delayed-start swaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eranp-orbs](https://clawhub.ai/user/eranp-orbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare, sign, submit, query, and cancel non-custodial Spot swap orders on supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps prepare and submit live DeFi orders that require wallet approvals and signatures. <br>
Mitigation: Before approving or signing, verify the chain, token addresses, spender or verifying contract, amounts, recipient, deadline, slippage, triggers, and relay URL. <br>
Risk: Signed payloads and typed data can authorize token movement for the exact order. <br>
Mitigation: Avoid storing signed payloads where others can read them, keep retries tied to the exact populated typed data, and do not rebuild an ambiguous submission until its status is resolved. <br>
Risk: Changing output.recipient away from the swapper can send proceeds to another address. <br>
Mitigation: Keep output.recipient equal to the swapper unless the user explicitly confirms a different recipient address. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/eranp-orbs/spot-advanced-swap-orders) <br>
- [Quickstart](references/quickstart.md) <br>
- [Params](references/params.md) <br>
- [Template, Sign, And Submit](references/sign.md) <br>
- [Lifecycle](references/lifecycle.md) <br>
- [Examples](references/examples.md) <br>
- [Common Token Addressbook](assets/token-addressbook.md) <br>
- [RePermit Template](assets/repermit.template.json) <br>
- [Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf) <br>
- [Spot Config](https://github.com/orbs-network/spot/blob/master/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, JavaScript snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces locally populated EIP-712 typed data, relay payload guidance, approval guidance, signing commands, and order lifecycle instructions.] <br>

## Skill Version(s): <br>
2.5.5 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
