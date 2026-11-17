## Description:

Revenue infrastructure for autonomous AI agents on Base that helps deploy ERC20 tokens with Uniswap V4 liquidity, creator fee sharing, locked liquidity, and direct blockchain calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawd800](https://clawhub.ai/user/clawd800)

### License/Terms of Use:


## Use Case:

External developers and agent builders use this skill to launch and manage Base ERC20 tokens, inspect token information, and claim creator trading fees through command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a wallet private key and can run financial blockchain transactions.

Mitigation: Use a dedicated low-balance wallet and avoid exporting valuable private keys into a broad shell environment.

Risk: The documented npx commands are unpinned and execute external tooling.

Mitigation: Pin and review package versions before execution instead of running unpinned npx commands as written.

Risk: The release evidence flags under-scoped and partly unaudited tooling, including missing shared contract and ABI files.

Mitigation: Verify the shared contract and ABI files, contract addresses, and every transaction target before signing.

Risk: Token swap behavior can create financial exposure if transaction parameters are not reviewed.

Mitigation: Review swap amounts, recipient addresses, and slippage expectations before signing any transaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawd800/skills/token-launcher)
- [PumpClaw website](https://pumpclaw.com)
- [pumpclaw-cli npm package](https://www.npmjs.com/package/pumpclaw-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and TypeScript command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may initiate Base blockchain reads, token deployment transactions, fee claims, and token swaps when run with wallet credentials.]

## Skill Version(s):

2.1.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
