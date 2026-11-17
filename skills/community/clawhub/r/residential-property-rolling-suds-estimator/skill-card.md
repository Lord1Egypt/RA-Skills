## Description:

Estimate exterior cleaning services for Rolling Suds from a U.S. residential property address using public property information, attached exterior photos, map/listing context, and a fixed pricing rubric for power washing and window cleaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwdearing](https://clawhub.ai/user/mwdearing)

### License/Terms of Use:

MIT-0

## Use Case:

Rolling Suds salespeople use this skill to turn a residential lead number, address, optional exterior photos, and public property context into a practical exterior-cleaning estimate for later review and Workiz entry.

### Deployment Geography for Use:

United States; operationally scoped to residential properties in the St. Louis, Missouri metro area within a 50-mile service radius.

## Known Risks and Mitigations:

Risk: Estimates may be inaccurate when public property data, photos, measurements, materials, or feature counts are incomplete.

Mitigation: State assumptions and confidence, provide conservative low/target/high ranges, and request photos or measurement confirmation when needed.

Risk: Special surfaces or unclear conditions can change pricing after the initial estimate.

Mitigation: Apply the documented minimums and pricing rules, exclude chain-link fence from automatic totals, and flag natural wood, paver/slate, and heavy-condition work for review.

Risk: A salesperson could treat the estimate as final pricing.

Mitigation: Keep the estimate-only disclaimer in the output and require review before entering final pricing into Workiz.

## Reference(s):

- [Pricing Rules](references/pricing-rules.md)
- [Version History](references/version-history.md)
- [Iteration Notes](references/iteration-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/mwdearing/skills/residential-property-rolling-suds-estimator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown estimate with line items, assumptions, confidence, follow-up notes, and an estimate-only disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a lead number before estimating; intended for salesperson review before final pricing or Workiz entry.]

## Skill Version(s):

0.1.9 (source: server release metadata and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
