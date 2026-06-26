## Description: <br>
Superhero.com social network agent for posting tamperproof content, creating tokens, and trading trending tokens on the aeternity blockchain with optional autonomous scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superhero-com](https://clawhub.ai/user/superhero-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage a Superhero.com wallet workflow: post and read on-chain social content, create bonding-curve tokens, monitor holdings, and buy or sell trending tokens. It supports both manual approval flows and autonomous posting or trading schedules after the user configures risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend AE or trade bonding-curve tokens automatically when autonomous mode is enabled. <br>
Mitigation: Use a dedicated low-balance wallet, start in manual mode, and enable autonomous trading only after setting strict per-trade, position, and exit limits. <br>
Risk: The skill requires AE_PRIVATE_KEY to sign on-chain transactions. <br>
Mitigation: Do not reuse a primary wallet key, avoid loading the key broadly in shell profiles, and keep mnemonics or private keys offline and out of logs. <br>
Risk: Posts, token creation, and trades are public on-chain actions that may be irreversible. <br>
Mitigation: Review content and transaction intent before execution, especially before enabling scheduled posting or trading. <br>
Risk: Generated invite links can contain wallet secrets. <br>
Mitigation: Share invite links only with intended recipients and avoid committing, logging, or reposting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superhero-com/superhero) <br>
- [Superhero API](https://api.superhero.com) <br>
- [aeternity mainnet node](https://mainnet.aeternity.io) <br>
- [Install dependency: @aeternity/aepp-sdk](https://www.npmjs.com/package/@aeternity/aepp-sdk) <br>
- [Install dependency: bignumber.js](https://www.npmjs.com/package/bignumber.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger scripts that return JSON, publish public on-chain content, or submit signed wallet transactions when the user has configured AE_PRIVATE_KEY.] <br>

## Skill Version(s): <br>
1.0.8 (source: evidence.json release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
