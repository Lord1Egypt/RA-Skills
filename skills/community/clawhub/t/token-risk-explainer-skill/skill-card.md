## Description:

Explain crypto token risk in plain Chinese and English from Binance Web3 token audit and market metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2663629531](https://clawhub.ai/user/2663629531)

### License/Terms of Use:


## Use Case:

External users, community managers, content operators, and developers use this skill to explain contract-level token risk, compare tokens, triage watchlists, and draft neutral community warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal explain, compare, and watchlist runs can trigger live SkillPay billing calls.

Mitigation: Use skip-billing or noop billing mode unless billing is intentionally enabled, and keep SKILLPAY_* settings in trusted deployment configuration.

Risk: Token audit or market data may be unavailable or incomplete, so a low-risk result can be misunderstood as a safety guarantee.

Mitigation: Treat results as current-snapshot triage, keep manual review in the loop, and do not present low risk as safe or as investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2663629531/skills/token-risk-explainer-skill)
- [Binance Web3](https://web3.binance.com)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON reports with bilingual plain-text summaries and alert drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk scores, factor explanations, comparison or watchlist rankings, billing status, and disclaimer text.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
