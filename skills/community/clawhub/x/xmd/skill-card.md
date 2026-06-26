## Description: <br>
Interact with Metal Dollar (XMD) stablecoin to mint, redeem, check supply, collateral reserves, and oracle prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect XMD treasury state, collateral reserves, balances, supply, and oracle prices, and to perform confirmed XMD mint or redeem transactions on XPR Network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write tools can sign real XPR Network transactions that move assets. <br>
Mitigation: Use read-only tools by default; enable mint or redeem only when needed and require users to verify the amount, collateral symbol, and confirmed=true flag before execution. <br>
Risk: Private-key environment variables are used for write operations but are not declared in the manifest requirements. <br>
Mitigation: Provision a dedicated least-privileged XPR permission for this skill and avoid broad active-key access. <br>
Risk: Mint and redeem outcomes depend on collateral limits, treasury pause state, and oracle pricing. <br>
Mitigation: Check treasury config, collateral status, reserves, and oracle price before initiating a transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulgnz/xmd) <br>
- [Publisher profile](https://clawhub.ai/user/paulgnz) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON tool responses with status messages, XMD analytics, and transaction identifiers for write operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only tools return XMD and collateral state; write tools require confirmed=true and can sign real blockchain transactions.] <br>

## Skill Version(s): <br>
0.2.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
