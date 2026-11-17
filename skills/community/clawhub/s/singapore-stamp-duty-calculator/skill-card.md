## Description:

Use when the user asks how much stamp duty, BSD or ABSD they will pay on a Singapore condo, apartment or other residential property, e.g. as a citizen buying a second home, a PR, a foreigner or a company. Free, no-auth calculator using current IRAS rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External home buyers and advisers use the calculator to estimate BSD and ABSD for a Singapore residential property based on its value, buyer category, and property count. The tier-by-tier breakdown helps them review the estimate before confirming amounts with IRAS.

### Deployment Geography for Use:

Singapore

## Known Risks and Mitigations:

Risk: The calculator sends the property value, buyer category, and property count to an external service; its retention practices are not explained.

Mitigation: Share only those calculation inputs, verify estimates with IRAS, and review any paid follow-up before approving it.

## Reference(s):

- [Stamp duty calculator service](https://finch-agent-catalog.finch-catalog-mcp.workers.dev/mcp)
- [ClawHub skill release](https://clawhub.ai/a0971025732-netizen/skills/singapore-stamp-duty-calculator)

## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [Structured JSON with BSD and ABSD totals, a tier-by-tier BSD breakdown, and notes]

**Output Parameters:** [3 inputs: property value in SGD, buyer category, and residential property count]

**Other Properties Related to Output:** [Estimates only; applicable remissions are not included. Confirm amounts with IRAS. A paid follow-up requires user approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
