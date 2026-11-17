## Description:

Aggregates SMZDM shopping-deal information for deal searches, hot deals, possible bug-price finds, and historical-low style summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[275254cl-hash](https://clawhub.ai/user/275254cl-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to search and summarize SMZDM shopping deals by keyword or category. The skill is intended for savings-oriented shopping workflows, but users should treat deal availability, pricing, and bug-price labels as unverified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deal results may be inaccurate, stale, or simulated without a clear label.

Mitigation: Verify prices, merchants, coupon terms, and availability on the linked shopping or deal page before making purchase decisions.

Risk: The skill description overstates live monitoring and bug-price detection relative to the evidence.

Mitigation: Present outputs as shopping leads rather than confirmed live alerts, and review the tool behavior before using it for automated notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/275254cl-hash/skills/smzdm-deals)
- [SMZDM website](https://www.smzdm.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text summaries with deal titles, prices, merchants, timestamps, popularity, and links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 10 deals per search path in the bundled tool; mock fallback results may be shown when live requests fail.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
