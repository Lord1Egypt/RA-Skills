## Description: <br>
Interact with LOAN Protocol on XPR Network to supply assets, borrow against collateral, redeem, repay loans, and claim LOAN token rewards on mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query LOAN Protocol markets and user positions, then prepare confirmed XPR Network lending actions such as supplying, borrowing, repaying, redeeming, withdrawing collateral, and claiming rewards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign real XPR mainnet lending transactions using private-key environment variables. <br>
Mitigation: Install only when the publisher and runtime are trusted, use a dedicated or limited-permission XPR account when possible, and do not provide XPR_PRIVATE_KEY or XPR_ACCOUNT unless signing is intended. <br>
Risk: Borrowing, redeeming, or withdrawing collateral can increase liquidation risk or create financial loss. <br>
Mitigation: Verify every market, token, amount, borrower, collateral position, utilization level, and liquidation buffer before setting confirmed=true. <br>
Risk: The manifest does not declare the private-key environment variables needed for write operations. <br>
Mitigation: Review runtime configuration before use and treat any request for XPR_PRIVATE_KEY, XPR_ACCOUNT, or XPR_PERMISSION as sensitive signing setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulgnz/xpr-lending) <br>
- [XPR mainnet RPC endpoint](https://xpr-mainnet-rpc.saltant.io) <br>
- [Metal X LOAN stats API](https://identity.api.prod.metalx.com/v1/loan/stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API Calls, guidance] <br>
**Output Format:** [Structured tool responses with transaction details, market data, balances, APY/TVL values, warnings, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require confirmed=true and XPR signing credentials; read-only tools query mainnet RPC and Metal X API data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
