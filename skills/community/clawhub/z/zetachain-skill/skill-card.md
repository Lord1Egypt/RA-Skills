## Description: <br>
ZetaChain skill for querying omnichain assets, tracking CCTX cross-chain transactions, generating zEVM deployment guidance, and indexing technical documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mango-ice-cat](https://clawhub.ai/user/mango-ice-cat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect ZetaChain-related wallet balances, track cross-chain transaction status, and produce development guidance for zEVM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make live RPC requests to public blockchain endpoints and return balance, gas, or transaction-status data that can be incomplete, delayed, or endpoint-dependent. <br>
Mitigation: Use explicit trusted RPC or Alchemy endpoints for reliability and treat balance, gas, and transaction analysis as informational rather than financial advice. <br>
Risk: Users may be tempted to provide sensitive wallet material while investigating addresses or transactions. <br>
Mitigation: Do not enter wallet private keys or seed phrases; use public wallet addresses and transaction hashes only. <br>


## Reference(s): <br>
- [ZetaChain RPC endpoint](https://zetachain.rpc.thirdweb.com) <br>
- [ZetaChain BlockPI RPC endpoint](https://zetachain-evm.blockpi.network/v1/rpc/public) <br>
- [ZetaChain BlockPI LCD endpoint](https://zetachain.blockpi.network/lcd/v1/public) <br>
- [ClawHub skill page](https://clawhub.ai/mango-ice-cat/zetachain-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make live read-only RPC requests to public blockchain endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
