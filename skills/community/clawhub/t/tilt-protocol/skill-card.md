## Description: <br>
Create and manage tokenized stock investment funds on Tilt Protocol (Robinhood L2). Self-custodied — you own your wallet, your keys, and your vaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rontoTech](https://clawhub.ai/user/rontoTech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to create and manage self-custodied tokenized stock funds on Tilt Protocol, including wallet setup, vault creation, portfolio allocation, rebalancing, and investor-facing strategy updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent wallet, trading, approval, and public-posting authority for testnet DeFi fund management. <br>
Mitigation: Use an isolated testnet setup with a disposable wallet, require explicit approval before vault creation, approvals, trades, or public posts, and do not reuse valuable private keys. <br>
Risk: Remote skill updates and changing contract or endpoint details can alter the instructions an agent follows. <br>
Mitigation: Review any fetched skill update before following it, verify the chain ID and contract addresses, and prefer bounded approvals where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rontoTech/tilt-protocol) <br>
- [Tilt Protocol homepage](https://tiltprotocol.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network and shell access; uses Foundry cast, curl, jq, and a TILT_PRIVATE_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and claw.json/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
