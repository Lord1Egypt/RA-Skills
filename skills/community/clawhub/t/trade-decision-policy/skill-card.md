## Description:

Use when stock research, valuation, portfolio analytics, and risk outputs must be converted into structured Vietnam equity recommendation labels, target weights, invalidation rules, and approval-gated action drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External users and portfolio decision agents use this skill as a final decision-policy layer for Vietnam listed equities. It converts research, valuation, risk, and compliance inputs into approval-gated recommendation drafts rather than executable trade orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence investment decisions if users rely on incomplete or stale financial, liquidity, or portfolio data.

Mitigation: Verify financial inputs before use; cap confidence at Medium when critical financial statements, liquidity data, or portfolio weights are missing.

Risk: A recommendation draft could be mistaken for an executable trade order.

Mitigation: Keep requires_user_confirmation set to true, broker_execution_allowed set to false, and broker execution in a separate approval workflow.

Risk: Insufficient evidence could lead to an unjustified active portfolio change.

Mitigation: Return HOLD when evidence is insufficient and require explicit risk, valuation, compliance, or thesis-invalidation reasoning for TRIM or EXIT decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teahann/skills/trade-decision-policy)
- [ClawHub Publisher Profile](https://clawhub.ai/user/teahann)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Structured decision object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes recommendation label, current and target weights, maximum weight, confidence, rationale, invalidation condition, risk and compliance status, data gaps, user-confirmation requirement, and broker-execution flag.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
