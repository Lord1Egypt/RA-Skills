## Description: <br>
Check wallet balances, token holdings, wallet addresses, profile details, and transaction history across supported EVM chains and Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Wallet users and agents acting for them use this skill to inspect authenticated wallet balances, token holdings, profile details, wallet addresses, and recent account activity across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated wallet queries can expose sensitive wallet addresses, balances, profile details, token holdings, and transaction history. <br>
Mitigation: Ask for scoped results when possible, and avoid showing full addresses, balances, profile details, or transaction history in shared or recorded chats unless disclosure is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and wallet data returned by fdx commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated fdx wallet session; supports optional chain, account address, limit, and offset parameters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
