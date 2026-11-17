## Description:

After an explicit quote and approval, creates an operations weekly brief for one subscribed Amazon ASIN using product details, snapshots, and review evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and operators use the skill to review one subscribed ASIN's product details, snapshots, and customer reviews in a weekly operations brief. The documented workflow requires a quote and explicit confirmation before a paid run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release exposes broader monitoring controls beyond the weekly ASIN report, including controls that can enable recurring collection.

Mitigation: Restrict use to operations quote/run, and review recurring collection settings before changing them.

Risk: Account credits may be spent without fresh approval under current ARI account settings.

Mitigation: Configure ARI to ask before every charge and require explicit user approval after the quote before any paid run.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/funewa/skills/weekly-asin)
- [ARI CLI and API reference](references/reference.md)
- [Weekly ASIN operations workflow](references/operation-workflow.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown operations brief in the user's language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses available product, snapshot, and review evidence; reports data scope and sample limitations.]

## Skill Version(s):

1.5.3 (source: server release evidence, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
