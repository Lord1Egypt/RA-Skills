## Description: <br>
Yield Farm Payment automates Base Network USDC payments while depositing collateral into Aave V3 so users can recover payment costs from yield over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[altoninelli](https://clawhub.ai/user/altoninelli) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to make immediate USDC payments on Base while depositing collateral into Aave V3 for long-term yield-based payment recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign live wallet transactions and move real USDC from a private-key-backed wallet. <br>
Mitigation: Use a dedicated low-balance wallet, run dry-runs first, and verify the chain, recipient, Aave addresses, total required funds, and fixed 0.2 USDC fee before signing. <br>
Risk: Some execution paths may bypass the safer confirmation flow or report success after partial failure. <br>
Mitigation: Prefer the CLI flow with interactive confirmation, avoid direct execution of scripts/yield-farm-payment.js unless reviewed, and confirm on-chain payment and collateral-deposit results before relying on success output. <br>
Risk: The skill requires a raw PRIVATE_KEY value in local configuration. <br>
Mitigation: Never use a main wallet or high-balance wallet; store only the dedicated wallet key needed for this skill and rotate or empty it after use. <br>


## Reference(s): <br>
- [Aave V3 Addresses - Base Network](references/aave-addresses.md) <br>
- [Aave Protocol](https://aave.com) <br>
- [Base Network](https://base.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/altoninelli/yield-farm-payment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run commands, transaction previews, and risk reminders for wallet-funded execution.] <br>

## Skill Version(s): <br>
1.0.18 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
