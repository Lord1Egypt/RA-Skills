## Description:

Analyzes close-up pet eye photos or videos for visible redness, tearing, and cloudiness, then returns a structured screening report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, boarding staff, and veterinary teams can use the skill to screen pet eye images or videos for visible changes and review prior reports. Its findings are visual alerts and do not replace a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious for credential and identity behavior beyond the advertised analysis; its assessment was partial because a local reference was missing.

Mitigation: Avoid installation until the credential destination, account creation and storage, media processing disclosure, and export-only behavior are clarified.

## Reference(s):

- [API interface notes](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured JSON analysis reports and Markdown report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include anomaly alerts, suggestions, and report links; not a veterinary diagnosis.]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
