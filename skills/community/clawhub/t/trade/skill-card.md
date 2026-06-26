## Description: <br>
Swap or trade tokens on Base network using the Awal CLI, including buying, selling, or converting between USDC, ETH, WETH, and contract-address tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRAG](https://clawhub.ai/user/0xRAG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check authenticated wallet status and prepare token swaps on Base, including custom slippage and optional JSON command output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute real authenticated wallet swaps without a required final confirmation step. <br>
Mitigation: Require explicit final approval before any swap and manually verify the active wallet, Base network, token addresses, amount, expected output, fees, and slippage. <br>
Risk: The skill invokes an unpinned external CLI with `npx awal@latest`. <br>
Mitigation: Prefer a pinned and reviewed version of the Awal CLI before allowing an agent to trade. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xRAG/trade) <br>
- [Publisher profile](https://clawhub.ai/user/0xRAG) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command output may be JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated wallet, sufficient source-token balance, Base network support, token selection, amount selection, and slippage settings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
