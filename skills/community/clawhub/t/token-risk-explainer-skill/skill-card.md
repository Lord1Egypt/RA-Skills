## Description: <br>
Explain crypto token risk in plain Chinese and English from Binance Web3 token audit and market metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2663629531](https://clawhub.ai/user/2663629531) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, community managers, and content operators use this skill to turn token audit and market metadata into contract-level risk scores, bilingual explanations, token comparisons, watchlist triage, and community warning drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal analysis commands can trigger third-party SkillPay charges without a clear per-run confirmation step. <br>
Mitigation: Confirm the price and billing owner before use, require explicit approval for billable runs, or pass --skip-billing for non-billable runs. <br>
Risk: Billing sends a user_ref and uses SKILLPAY_APIKEY for charge requests. <br>
Mitigation: Keep SKILLPAY_APIKEY in environment secrets, verify who controls it, and avoid sending sensitive user identifiers as user_ref. <br>
Risk: Token queries are sent to Binance Web3 or a configured replacement endpoint. <br>
Mitigation: Only submit contract or symbol queries that are acceptable to share with the configured token-data provider. <br>
Risk: LOW risk output does not mean a token is safe or suitable for investment. <br>
Mitigation: Treat results as research support, keep manual review in the loop, and do not present the output as investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2663629531/token-risk-explainer-skill) <br>
- [Binance Web3 service endpoint](https://web3.binance.com) <br>
- [SkillPay service endpoint](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON reports with bilingual plain-language summaries and draft community copy] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk score, risk level, risk factors, continue-research guidance, audit hits, links, billing status, and a disclaimer.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
