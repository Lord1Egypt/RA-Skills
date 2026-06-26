## Description: <br>
Detect scam tokens on Solana before you trade. Checks ticker patterns, token age, and known scam mints. Read-only - no wallet signing required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ammkode](https://clawhub.ai/user/ammkode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to perform read-only heuristic checks on Solana token mints before trading or integrating a token workflow. It can validate mint addresses, flag suspicious ticker patterns, check configurable blacklists, and estimate token age through Solana RPC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic checks can miss scam tokens or incorrectly flag legitimate tokens. <br>
Mitigation: Use results as one signal only and review independent token, liquidity, contract, and issuer information before trading. <br>
Risk: The skill exposes a liquidity configuration value but evidence says it does not verify liquidity. <br>
Mitigation: Do not treat the returned safety result as a liquidity assessment; verify liquidity with a separate trusted source. <br>
Risk: Public Solana RPC use may reveal IP addresses and query patterns. <br>
Mitigation: Use a trusted private RPC endpoint through RPC_URL when query privacy matters. <br>
Risk: User-added blacklist entries can affect later checks in the same running process. <br>
Mitigation: Review custom blacklist additions and reset process state when switching users or workflows. <br>
Risk: Wallet keys are not required for this read-only skill. <br>
Mitigation: Do not provide wallet keys, seed phrases, Telegram IDs, or trade history when using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ammkode/solana-scam-detector) <br>
- [Publisher profile](https://clawhub.ai/user/ammkode) <br>
- [Solana public RPC endpoint](https://api.mainnet-beta.solana.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and structured token-safety result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only heuristic safety results such as safe status, issue list, and applied configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
