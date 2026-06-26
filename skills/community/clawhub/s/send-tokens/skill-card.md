## Description: <br>
Send or transfer tokens to any address on any supported chain (EVM or Solana). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare and execute token transfers from an authenticated wallet on supported EVM chains or Solana. It guides the agent to check authentication and balance, confirm transfer details with the human, run the transfer command, and report the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain token transfers are irreversible if the recipient address, chain, token, or amount is wrong. <br>
Mitigation: Personally confirm the recipient address, chain, token, and amount before executing any transfer. <br>
Risk: An authenticated wallet may expose funds to unintended transfers if the local CLI or wallet setup is not trusted. <br>
Mitigation: Verify the fdx CLI and wallet setup yourself and keep only appropriate funds available. <br>
Risk: A transfer can fail or create confusion when the wallet has insufficient funds for the token amount or network fees. <br>
Mitigation: Check wallet authentication and balance before sending, including enough native token for applicable fees. <br>


## Reference(s): <br>
- [Send Tokens on ClawHub](https://clawhub.ai/rachidjarray-hk-qa-fdt/send-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate irreversible blockchain token transfers after human confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
