## Description: <br>
Guides an agent through purchasing virtual Visa or Mastercard debit cards with USDT on BSC via the x402 protocol, checking card status, and configuring an EVM wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyongm](https://clawhub.ai/user/yuanyongm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to set up an EVM wallet, purchase a prepaid virtual Visa or Mastercard with USDT on BSC, and query order or card status through the AEON CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for and persists a full EVM wallet private key. <br>
Mitigation: Use a new low-balance wallet, never a main wallet, avoid passing private keys in command-line arguments, and confirm local storage permissions before purchases. <br>
Risk: The workflow relies on an external npm CLI that is not pinned and can auto-upgrade. <br>
Mitigation: Review the npm package before installation, disable or avoid automatic upgrades, and require explicit approval before any upgrade or card-purchase command. <br>
Risk: Card creation spends cryptocurrency on BSC and failed transfers to the wrong network can lose funds. <br>
Mitigation: Confirm the card amount with the user, use CLI-reported limits and balance checks, and instruct users to send only BEP-20 USDT on BSC to the displayed wallet address. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyongm/x402-card) <br>
- [Create virtual card workflow](references/create-card.md) <br>
- [Check card status workflow](references/check-status.md) <br>
- [Wallet setup](references/wallet-setup.md) <br>
- [x402 protocol notes](references/x402-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npx; uses EVM_PRIVATE_KEY for wallet configuration; CLI responses may include JSON order, payment, wallet, and card status data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact metadata reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
