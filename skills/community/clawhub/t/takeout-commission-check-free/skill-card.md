## Description:

A free deterministic check for Chinese food delivery platform monthly statements, covering commission, merchant-borne delivery fee, activity subsidy and merchant net payout, with every finding citing the source line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant operators and staff use this skill after receiving monthly Meituan, Ele.me, or Douyin Takeout statements to re-check commission, merchant-paid delivery fees, merchant-paid activity subsidies, merchant net payout, totals, duplicate rows, and missing fields before settlement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported billing text can contain sensitive merchant financial information.

Mitigation: Run the local checker only in an environment where providing the billing export to a local Node.js script is acceptable.

Risk: The free version is limited to the listed arithmetic and structural checks and does not verify contract-specific commission rates, order-level details, refunds, or platform disputes.

Mitigation: Use the output as a line-cited arithmetic review, and confirm platform contracts, special settlement rules, and dispute decisions separately.

Risk: Missing or unrecognized headers prevent reliable conclusions.

Mitigation: Provide a tab-delimited statement with recognizable headers for merchant, platform, period, settlement base, commission rate, commission, merchant-paid delivery fee, merchant-paid subsidy, and merchant net payout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/takeout-commission-check-free)

## Skill Output:

**Output Type(s):** [analysis, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js against user-provided exported billing text; no API key or network access is described.]

## Skill Version(s):

1.0.42 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
