## Description:

US stock valuation model skill (English-first + 中文) based on financial report data that applies explicit rules for ROE, debt ratio, free cash flow conversion, and moat assessment, then outputs an A/B/C/D investment rating with reasons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:


## Use Case:

External users and investment-analysis agents use this skill to evaluate US stock financial report data against a fixed value-investing framework. It produces a bilingual rating and rule-by-rule explanation for buy, watch, or avoid decisions and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the A/B/C/D rating as financial advice or as a complete investment decision.

Mitigation: Present the rating as a rule-based analysis aid and require human review before acting on buy, watch, avoid, or position-sizing conclusions.

Risk: Incorrect or stale financial inputs can produce misleading rule results and ratings.

Mitigation: Verify the company financial data, dates, and moat scores before relying on the generated JSON or Markdown output.

Risk: The deterministic framework may omit market, legal, tax, liquidity, portfolio, or company-specific risks outside the encoded rules.

Mitigation: Use the output alongside broader due diligence and document any additional risks that are not captured by the fixed framework.

## Reference(s):

- [US Value Investing Framework - Extended Guide](references/framework-guide.md)
- [Input Template](references/input-template.json)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands]

**Output Format:** [JSON result file and Markdown report with English-first bilingual text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs a deterministic A/B/C/D rating, pass count, English reasons, Chinese summary, and per-rule results from user-provided company financial JSON.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
