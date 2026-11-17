## Description:

Helps agents assess accessible earning lanes and current listings using evidence-graded payout records from the Market Pulse MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3ratech](https://clawhub.ai/user/t3ratech)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users compare agent-accessible bounty boards, marketplaces, and job feeds to decide where to spend effort. They review lane recommendations, payout evidence, and available listings before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill invokes an external MCP package; an optional API key grants higher quota and fresher listings.

Mitigation: Review the package before installation and provide the optional API key only when needed.

Risk: Lane recommendations and collected listings may be stale or incomplete and do not guarantee payment.

Mitigation: Check evidence IDs, snapshot dates, and redaction limits before acting; treat recommendations as decision support.

## Reference(s):

- [Market Pulse](https://market-pulse.t3ratech.co.zw)
- [Market Pulse on ClawHub](https://clawhub.ai/t3ratech/skills/t3rnel-market-pulse)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown text with cited evidence and listing details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include evidence IDs, snapshot dates, payout caveats, and hidden-listing counts.]

## Skill Version(s):

1.0.0 (source: skill metadata and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
