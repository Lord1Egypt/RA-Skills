## Description: <br>
Swap tokens on Solana via the Jupiter aggregator and check wallet balances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imthatcarlos](https://clawhub.ai/user/imthatcarlos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check Solana wallet balances, fetch Jupiter swap quotes, and prepare token swaps that require explicit confirmation before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet swaps with a Solana keypair and relies on a helper script that was not present in the artifact. <br>
Mitigation: Use only a limited-funds wallet and do not run the signing step unless the exact jupiter-swap.mjs implementation is present from a trusted, reviewed source. <br>
Risk: Incorrect token mints, amounts, slippage, price impact, or minimum received values can cause unintended swaps. <br>
Mitigation: Verify token mints, amounts, slippage, price impact, and minimum received before confirming any transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imthatcarlos/solana-swaps) <br>
- [Publisher profile](https://clawhub.ai/user/imthatcarlos) <br>
- [Jupiter quote API endpoint](https://api.jup.ag/swap/v1/quote) <br>
- [Jupiter swap API endpoint](https://api.jup.ag/swap/v1/swap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires solana, spl-token, curl, jq, node, SOLANA_KEYPAIR_PATH, and a Jupiter API key for authenticated swap requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
