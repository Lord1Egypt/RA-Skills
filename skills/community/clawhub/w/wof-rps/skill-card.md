## Description: <br>
Play Rock Paper Scissors on WatchOrFight — on-chain gaming with USDC stakes on Base <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wof-developers](https://clawhub.ai/user/wof-developers) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to play WatchOrFight Rock Paper Scissors matches on Base, including checking balances, creating or joining matches, playing commit-reveal rounds, and viewing match or leaderboard state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke an external npm CLI with access to a wallet private key and funds for on-chain game transactions. <br>
Mitigation: Use a fresh dedicated game wallet funded only with ETH and USDC you are willing to risk, and prefer a hardware wallet or ephemeral signer where supported. <br>
Risk: Auto-play or match actions can spend funds on Base mainnet if the network and entry fee are not checked. <br>
Mitigation: Confirm mainnet versus testnet, wallet balances, and the entry fee before play; use Base Sepolia for testing. <br>
Risk: Installing or running an unverified package could expose secrets or execute unexpected code. <br>
Mitigation: Verify the npm package and source before installing, and restrict local secret-file permissions after first use. <br>


## Reference(s): <br>
- [WatchOrFight](https://watchorfight.com) <br>
- [RPS MCP CLI source](https://github.com/wof-games/rps-mcp) <br>
- [RPSArena contract](https://basescan.org/address/0xd7bee67cc28F983Ac14645D6537489C289cc7e52) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [CLI commands with JSON stdout, stderr progress messages, and concise setup or recovery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user invocation and a configured game wallet private key; commands return exit code 0 on success and 1 on error.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
