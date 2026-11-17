## Description:

Interact with LOAN Protocol on XPR Network to supply assets, borrow against collateral, redeem, repay loans, and claim LOAN token rewards on mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect LOAN Protocol markets and positions, estimate APY or TVL, and prepare lending, borrowing, repayment, redemption, collateral, and reward-claim actions on XPR Network mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign XPR Network mainnet financial transactions using local account credentials.

Mitigation: Install only in trusted agent environments, require explicit review before setting confirmed=true, and prefer a limited blockchain permission rather than a broad active key.

Risk: Supplying, borrowing, redeeming, withdrawing collateral, repaying, and claiming rewards affect real mainnet assets.

Mitigation: Review market, amount, account, permission, and transaction details before confirmation; keep borrowing well below collateral limits to reduce liquidation risk.

Risk: Account lookups and market statistics rely on external RPC and API services.

Mitigation: Treat external data as service-dependent, verify important financial figures against trusted sources, and account for availability or data freshness limits.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/paulgnz/skills/xpr-lending)
- [XPR mainnet RPC endpoint](https://xpr-mainnet-rpc.saltant.io)
- [Metal X loan stats API](https://identity.api.prod.metalx.com/v1/loan/stats)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown or JSON-like tool results with transaction details, market data, position summaries, APY or TVL data, and confirmation prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require confirmed=true and use local XPR account credentials when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
