## Description: <br>
Place and claim decentralized sports bets on-chain via Pinwin and Azuro, including game discovery, odds selection, EIP-712 signing, and Polygon transaction submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skinnynoizze](https://clawhub.ai/user/skinnynoizze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to browse sports markets, place Polygon USDT bets through Pinwin and Azuro, monitor bet status, and claim winnings. It is intended for explicit, user-confirmed betting actions using a dedicated wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real wallet credentials and irreversible sports-betting transactions. <br>
Mitigation: Install it only for a dedicated low-balance betting wallet and require explicit confirmation of the amount, selection, odds, contract, and destination before any transaction. <br>
Risk: Transaction safeguards may be weaker in practice than the skill instructions imply. <br>
Mitigation: Avoid unattended execution and do not use automatic confirmation flags; review each generated command and transaction payload before signing. <br>
Risk: A background watcher may continue running after a bet is placed. <br>
Mitigation: Check running processes after betting and stop any watcher that is no longer needed. <br>
Risk: USDT approvals can leave spend allowance after betting is complete. <br>
Mitigation: Revoke or reduce USDT allowances after finishing betting activity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/skinnynoizze/sports-betting) <br>
- [Publisher profile](https://clawhub.ai/user/skinnynoizze) <br>
- [Pinwin](https://pinwin.xyz) <br>
- [Polygon transaction explorer](https://polygonscan.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and transaction status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet setup guidance, game and odds summaries, explicit confirmation prompts, transaction hashes, bet status updates, and claim guidance.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
