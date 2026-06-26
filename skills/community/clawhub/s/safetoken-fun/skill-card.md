## Description: <br>
Discover and use SafeToken.fun, a fair memecoin launchpad on BNB Chain where agents can create tokens without an API key, read contract addresses and ABI from GET /api, and register tokens with POST /api/tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panagot](https://clawhub.ai/user/panagot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, crawlers, and AI agents use this skill to discover SafeToken.fun endpoints, create BNB Chain memecoins, register created tokens, and read token, bonding-curve, holder, and metadata information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create real BNB Chain mainnet memecoins from a funded wallet. <br>
Mitigation: Use only a limited dedicated wallet, verify chain ID 56, contract address, and ABI independently, simulate where possible, and manually approve every wallet transaction. <br>
Risk: Token registration and public launchpad interactions can publish irreversible or public information. <br>
Mitigation: Review token metadata, creator address, burn percent, launchpad address, and registration payload before submitting any transaction or POST request. <br>


## Reference(s): <br>
- [SafeToken.fun](https://safetoken.fun) <br>
- [SafeToken.fun API manifest](https://safetoken.fun/api) <br>
- [SafeToken.fun API docs](https://safetoken.fun/api-docs) <br>
- [ClawHub skill page](https://clawhub.ai/panagot/safetoken-fun) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, API calls] <br>
**Output Format:** [Markdown guidance with endpoint URLs, JSON payload examples, and on-chain transaction steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key required; on-chain token creation requires a funded BNB Chain wallet and manual transaction approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
