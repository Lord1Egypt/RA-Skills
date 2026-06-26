## Description: <br>
Interact with the Rhaios staging REST API for DeFi yield operations, including vault discovery, preparation, setup when needed, signing, and execution with a pluggable signer backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xTimepunk](https://clawhub.ai/user/0xTimepunk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work through Rhaios staging DeFi yield workflows: discover vaults, prepare deposits, redeems, or rebalances, inspect proposed actions, and execute them after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and submit wallet actions for Rhaios staging yield operations. <br>
Mitigation: Use only a wallet intended for this staging flow, prefer an isolated ownerless Privy wallet or test private key, keep dryRun enabled until the prepared action is inspected, and set confirm="yes" only after verifying the vault, amount, chain, and wallet address. <br>
Risk: Signer credentials and Privy app secrets are sensitive. <br>
Mitigation: Store credentials in the environment or a secret manager, do not print them in logs or chat, and avoid reusing production wallet credentials for staging tests. <br>
Risk: A deposit, redeem, or rebalance can target the wrong vault or amount if the request is not reviewed. <br>
Mitigation: Run vault discovery first, present ranked options to the user, pass the chosen vaultId explicitly, and keep max amount and gas controls in place for live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xTimepunk/rhaios-staging) <br>
- [Rhaios staging API](https://api.staging.rhaios.com) <br>
- [Rhaios staging fork status](https://api.staging.rhaios.com/v1/testing/fork-status) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON examples; runtime command output is structured text and JSON status from Rhaios staging API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 22+ or Bun 1.0+ and signer environment variables; live execution should use explicit confirmation.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
