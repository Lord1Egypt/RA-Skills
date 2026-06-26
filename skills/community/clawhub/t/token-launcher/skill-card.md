## Description: <br>
Revenue infrastructure for autonomous AI agents on Base. Deploy ERC20 tokens with Uniswap V4 liquidity, with trading fees to the creator, locked liquidity, and direct blockchain calls through CLI, MCP, or smart contract workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawd800](https://clawhub.ai/user/clawd800) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use Pumpclaw to create, inspect, trade, and manage Base ERC20 tokens with Uniswap V4 liquidity and creator fee flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign irreversible Base transactions using BASE_PRIVATE_KEY. <br>
Mitigation: Use a fresh wallet with minimal funds and require manual confirmation before create, claim, buy, sell, metadata update, or swap operations. <br>
Risk: Private keys can be exposed through shared shells, logs, or unsafe environment handling. <br>
Mitigation: Avoid shared terminals and logs for BASE_PRIVATE_KEY, and clear the environment after use. <br>
Risk: Runtime contract and ABI dependencies are referenced outside the artifact and were not fully reviewed in the release evidence. <br>
Mitigation: Review the shared contract and ABI files before allowing an agent to execute transaction-signing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawd800/token-launcher) <br>
- [Pumpclaw website](https://pumpclaw.com) <br>
- [pumpclaw-cli npm package](https://www.npmjs.com/package/pumpclaw-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and transaction-result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce blockchain transaction hashes, token addresses, token metadata, balances, and fee information.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and evidence.json release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
