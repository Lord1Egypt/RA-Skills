## Description:

Wallet authorization management tool for checking ERC20/ERC721 token approval risks, identifying unlimited approvals and high-risk authorizations, and guiding users toward revocation options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liusanhong](https://clawhub.ai/user/liusanhong)

### License/Terms of Use:


## Use Case:

External users use this skill to review wallet token approvals, identify risky unlimited or high-risk authorizations, and find supported tools for revoking unnecessary approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a billing API key and describes charging users through an external service.

Mitigation: Review billing behavior before installation, avoid sharing unnecessary user identifiers, and confirm any charge or payment link before acting on it.

Risk: Revocation examples can lead users to submit on-chain transactions.

Mitigation: Only run revoke code or use revoke tools when the wallet owner intentionally wants to change token approvals and understands gas costs.

Risk: Approval risk labels may be incomplete or misleading if token, spender, liquidity, or contract-verification data is stale.

Mitigation: Verify high-impact findings against chain explorers or trusted approval tools before revoking important permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liusanhong/skills/token-approval-checker)
- [Publisher Profile](https://clawhub.ai/user/liusanhong)
- [Etherscan Token Approval Checker](https://etherscan.io/tokenapprovalchecker)
- [BscScan Token Approval Checker](https://bscscan.com/tokenapprovalchecker)
- [PolygonScan Token Approval Checker](https://polygonscan.com/tokenapprovalchecker)
- [Revoke.cash](https://revoke.cash)
- [Unrekt](https://app.unrekt.net)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with risk summaries, reference links, and optional JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet approval risk levels, revocation guidance, billing disclosures, and transaction-related cautions.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
