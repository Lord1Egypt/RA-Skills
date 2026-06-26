## Description: <br>
Use when stock research, valuation, portfolio analytics, and risk outputs must be converted into structured Vietnam equity recommendation labels, target weights, invalidation rules, and approval-gated action drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment workflow operators use this skill as a final decision-policy layer for Vietnam listed equities. It converts research, valuation, portfolio risk, and compliance inputs into recommendation labels, target weights, invalidation rules, and approval-gated action drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial outputs may be mistaken for executable orders or standalone investment advice. <br>
Mitigation: Treat outputs as approval-gated drafts, require independent verification, and keep broker execution disabled. <br>
Risk: Missing financial statements, liquidity data, or portfolio weights can reduce decision quality. <br>
Mitigation: Cap confidence at Medium when critical inputs are missing and return HOLD when evidence is insufficient. <br>
Risk: Security guidance notes possible authenticated finance-platform services, cloud storage, dashboards, backtests, or scheduled automations in related workflows. <br>
Mitigation: Review any plan before approving builds or releases and confirm that connected services match the intended finance workflow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Structured decision object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation; broker execution is disabled unless a separate execution policy explicitly enables it.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
