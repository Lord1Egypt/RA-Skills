## Description: <br>
XPR DeFi provides XPR Network tools for Metal X market data and trading, AMM swaps, OTC escrow, yield farming, liquidity management, and multisig proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and XPR Network operators use this skill to inspect DeFi markets and, with configured account credentials and explicit confirmation where implemented, submit trades, swaps, liquidity, farming, OTC escrow, and multisig actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an XPR private key to sign real on-chain financial transactions. <br>
Mitigation: Use a dedicated low-value account or least-privilege permission and review every proposed action before setting confirmed=true. <br>
Risk: Multisig tools provide broad administrative authority beyond narrow DeFi helper behavior. <br>
Mitigation: Treat multisig proposal and approval flows as privileged operations that require explicit operator intent and human review before execution. <br>
Risk: Security evidence reports one write action without the advertised confirmation gate; artifact behavior identifies msig_cancel as callable without confirmed=true. <br>
Mitigation: Patch or disable that action before production use, or restrict access so proposal cancellations cannot be triggered without an independent human approval step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulgnz/xpr-defi) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/paulgnz) <br>
- [Metal X mainnet API](https://dex.api.mainnet.metalx.com) <br>
- [Metal X testnet API](https://dex.api.testnet.metalx.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Structured JSON tool responses with market data, transaction previews, errors, and transaction IDs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require XPR account credentials; most advertised write tools require confirmed=true, but security evidence flags one write action without the advertised confirmation gate.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata; artifact skill.json reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
