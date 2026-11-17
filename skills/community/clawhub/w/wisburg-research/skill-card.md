## Description:

Retrieves and summarizes Wisburg financial research, company reports, earnings-call notes, and market updates through the Wisburg CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weaxs](https://clawhub.ai/user/weaxs)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and analysts use this skill to search Wisburg's financial reports, company research, earnings-call notes, news feeds, and market summaries by keyword or date, then receive concise findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to retry permission-denied or sandbox-blocked commands through a generic request path without approval.

Mitigation: Treat permission denials and sandbox blocks as final; retry through the generic request path only after explicit user approval.

Risk: Financial research queries are sent to Wisburg.

Mitigation: Avoid sending confidential research topics or sensitive information unless the user accepts this data sharing.

## Reference(s):

- [Wisburg Research on ClawHub](https://clawhub.ai/weaxs/skills/wisburg-research)
- [Wisburg CLI repository (skill homepage; not verified skill provenance)](https://github.com/Weaxs/wisburg-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown summaries with optional CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes retrieved titles, publication dates, and findings instead of returning raw JSON by default.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
