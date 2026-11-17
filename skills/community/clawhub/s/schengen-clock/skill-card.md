## Description:

Tracks short-stay Schengen travel days, forecasts remaining allowance, checks proposed trips, and prepares an itinerary statement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Travelers and travel-planning assistants use this skill to record Schengen visits, estimate remaining days under the rolling 90/180-day rule, check future trips, and prepare a travel summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculated allowances may not reflect individual immigration circumstances or current rules.

Mitigation: Treat results as an arithmetic aid, not legal advice; verify dates and eligibility against official guidance before travel.

Risk: The traps command may flag planned future stays too conservatively.

Mitigation: Review flagged plans and verify the underlying dates and allowance independently before changing travel plans.

Risk: Stored travel history may reveal sensitive personal movements.

Mitigation: Keep the local stay registry private and share itinerary statements only when needed.

## Reference(s):

- [Schengen Clock release on ClawHub](https://clawhub.ai/voronindenis5/skills/schengen-clock)
- [Schengen 90/180 rule explained](references/rule-explained.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Files]

**Output Format:** [Plain text reports and itinerary letter; local JSON stay registry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline processing; entry and exit dates both count as presence days.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
