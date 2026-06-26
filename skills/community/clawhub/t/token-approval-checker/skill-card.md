## Description: <br>
Checks ERC20 and ERC721 wallet token approvals, identifies unlimited or high-risk authorizations, and provides revoke-oriented guidance for supported blockchain explorers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liusanhong](https://clawhub.ai/user/liusanhong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External wallet users and crypto operators use this skill to review token approval exposure, identify unlimited or risky approvals, and decide whether to revoke allowances. The skill includes paid SkillPay usage at 0.001 USDT per call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports an exposed billing API key. <br>
Mitigation: Remove or rotate the exposed key before using the skill with real billing. <br>
Risk: The security evidence reports under-scoped paid billing behavior. <br>
Mitigation: Require explicit billing consent and confirm the SkillPay charge flow before each paid use. <br>
Risk: Wallet approval checks and revocation flows can affect real assets. <br>
Mitigation: Use trusted revoke tools and verify every wallet transaction before signing. <br>
Risk: The approval-checking behavior is not fully clarified in the security guidance. <br>
Mitigation: Review the generated approval report against trusted blockchain explorer data before acting on high-risk findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liusanhong/token-approval-checker) <br>
- [Publisher profile](https://clawhub.ai/user/liusanhong) <br>
- [Etherscan Token Approval Checker](https://etherscan.io/tokenapprovalchecker) <br>
- [BscScan Token Approval Checker](https://bscscan.com/tokenapprovalchecker) <br>
- [PolygonScan Token Approval Checker](https://polygonscan.com/tokenapprovalchecker) <br>
- [Revoke.cash](https://revoke.cash) <br>
- [Unrekt](https://app.unrekt.net) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with tables and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet-approval risk levels, revoke tool links, and billing-flow examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
