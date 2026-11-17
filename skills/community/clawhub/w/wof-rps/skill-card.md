## Description:

Play Rock Paper Scissors on WatchOrFight - on-chain gaming with USDC stakes on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wof-developers](https://clawhub.ai/user/wof-developers)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to play WatchOrFight Rock Paper Scissors matches, stake USDC, manage match state, and check balances or leaderboard results on Base or Base Sepolia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable npm CLI that receives a wallet private key and can stake or approve USDC.

Mitigation: Review the package and source before installing, pin an exact package version when possible, prefer testnet first, and use an isolated signer or dedicated minimally funded game wallet.

Risk: On-chain match actions can spend gas, stake USDC, and approve USDC for the RPSArena contract.

Mitigation: Confirm the selected network, entry fee, balance, and contract interaction scope before running play or match-management commands.

Risk: Commit secrets are stored locally so rounds can be revealed after restart.

Mitigation: Restrict permissions on the local secret file after first use with chmod 600 ~/.wof-rps-secrets.json.

## Reference(s):

- [WatchOrFight homepage](https://watchorfight.com)
- [RPS MCP source listed in metadata](https://github.com/wof-games/rps-mcp)
- [RPSArena contract on Base](https://basescan.org/address/0xd7bee67cc28F983Ac14645D6537489C289cc7e52)
- [Circle faucet for Base Sepolia USDC](https://faucet.circle.com/)
- [ClawHub skill page](https://clawhub.ai/wof-developers/skills/wof-rps)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progress messages are emitted to stderr by the CLI; command success and failure are represented with process exit codes.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
