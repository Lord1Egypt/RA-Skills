## Description:

Research companies with VeilStrat AI adoption and buying signals. Use for B2B prospecting, account research, AI hiring, funding, technology adoption, hiring velocity, company dossiers, and signal-based sales targeting. Supports the VeilStrat API and public directory previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kprojectship](https://clawhub.ai/user/kprojectship)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and research teams can use this skill to identify companies showing AI adoption or buying signals and prepare evidence-based account shortlists. It supports public previews and authenticated API research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API research sends queries and company IDs to VeilStrat, and successful calls use the account's API quotas; authenticated service behavior was not tested.

Mitigation: Avoid sending sensitive query details, request only the records needed, review the service documentation, and store VEILSTRAT_API_KEY in the host's secret settings.

## Reference(s):

- [VeilStrat product homepage](https://www.veilstrat.com/)
- [VeilStrat API overview](https://www.veilstrat.com/developers)
- [VeilStrat API documentation](https://app.veilstrat.com/docs/api)
- [API and public research guide](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown company research summaries and account shortlists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates observed company signals from fit assessments; identifies public previews as incomplete and marks unavailable signal dates or sources.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
