## Description:

Helps agents answer currency exchange-rate questions using rates returned by the disclosed zqpay service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greenteawater](https://clawhub.ai/user/greenteawater)

### License/Terms of Use:

MIT-0

## Use Case:

People asking an agent about currency exchange rates can request a currency pair or a single currency, which defaults to a CNY comparison. The agent reports available rates and their effective time rather than providing transaction terms or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Currency-code queries are sent to the disclosed zqpay service.

Mitigation: Confirm that sending requested currency pairs to that service is acceptable before use.

Risk: An example maps a CNY/USD request to USD/AUD, which could produce an incorrect currency pair.

Mitigation: Correct the example and check requested and returned currency codes before presenting a rate.

Risk: Exchange rates can be stale or incomplete and do not establish trading or banking terms.

Mitigation: Display the available rate timestamp and treat results as informational, not a sole basis for financial decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/greenteawater/skills/zqpay-rate)
- [Exchange-rate query endpoint](https://aipaytest.zqpay.com/zl-core-rate-crawler/api/rates/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Exchange-rate guidance]

**Output Format:** [Markdown response with exchange rates, currency codes, and available timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags inverted conversions and unavailable rates; rates are informational.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
