## Description:

Computes French fixed-rate mortgage monthly payments, insurance cost, total interest, and amortization schedules through Vestafolio's simulator API after collecting the loan amount, annual rate, duration, and insurance rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate French mortgage payments, total borrowing cost, insurance cost, and month-by-month amortization for a fixed-rate loan. It is suited to payment, loan-cost, amortization-table, and borrower-insurance cost questions after the user consents to sending the required parameters to Vestafolio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personalized mortgage calculations transmit loan parameters to Vestafolio's external service.

Mitigation: Before transmission, the agent must explain the API use, summarize the exact fields and values, obtain the user's approval, and omit unrelated personal identifiers.

Risk: Mortgage estimates may be mistaken for a binding loan offer or financial advice.

Mitigation: The agent should state that results are estimates, not financial advice, and note that fees such as dossier, guarantee, and other TAEG components are not modeled.

Risk: Network or API failures could lead to unsupported calculations.

Mitigation: If schema retrieval, execution, or API response validation fails, the agent should say the calculation could not be completed and avoid inventing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-credit-immobilier)
- [Vestafolio credit immobilier API schema](https://www.vestafolio.com/api/tools/v1/credit-immobilier)
- [Vestafolio credit immobilier simulator](https://www.vestafolio.com/simulateurs/credit-immobilier)

## Skill Output:

**Output Type(s):** [guidance, API Calls, shell commands, markdown]

**Output Format:** [Markdown with calculated figures, assumptions, limits, and optional amortization table details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must be grounded in Vestafolio API results; if execution or network access is unavailable, the agent should not invent a result.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
