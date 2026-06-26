## Description: <br>
Trade prediction markets on WatchOrFight - on-chain oracle-settled markets with USDC stakes on Base L2 (Ethereum). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wof-developers](https://clawhub.ai/user/wof-developers) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to enter, monitor, and advance WatchOrFight prediction markets for ETH, BTC, and SOL using USDC stakes on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external npm CLI uses a raw wallet private key and can sign irreversible USDC transactions. <br>
Mitigation: Use a fresh, dedicated wallet funded only with small amounts of ETH and USDC, and prefer testnet before mainnet. <br>
Risk: Contract or package substitution could route transactions through unexpected code or addresses. <br>
Mitigation: Verify the npm package and on-chain contract addresses independently before funding or executing trades. <br>
Risk: Stored commit-reveal secrets in ~/.wof-predict/secrets.json may expose active market positions if the file is mishandled. <br>
Mitigation: Protect the secrets file during active markets and remove it when it is no longer needed. <br>


## Reference(s): <br>
- [WatchOrFight](https://watchorfight.com) <br>
- [PredictionArena contract](https://basescan.org/address/0xA62bE1092aE3ef2dF062B9Abef52D390dF955174) <br>
- [ERC-8004 registry](https://8004scan.io) <br>
- [Circle faucet](https://faucet.circle.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON command output with progress messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return exit code 0 on success and 1 on error.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
