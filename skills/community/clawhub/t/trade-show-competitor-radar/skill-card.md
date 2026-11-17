## Description:

Structure on-site competitor booth observations into tagged, actionable intelligence notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

External exhibitors, sales teams, product teams, and leadership use this skill during or shortly after trade shows to turn raw competitor booth observations into tagged field-intelligence notes and internal action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs include a mandatory promotional tracking footer unrelated to the user's competitive-intelligence note.

Mitigation: Remove or disable the promotional footer before installing the skill or sharing reports outside the team.

Risk: The workflow can encourage identifying booth visitors for outreach without explicit privacy guardrails.

Mitigation: Use attendee, badge-derived, or contact information only when it was collected lawfully, with appropriate consent, and in line with event rules and company privacy policy.

Risk: Competitive notes may contain overheard, estimated, or inferred claims that are not independently verified.

Mitigation: Preserve evidence tags in summaries and verify sensitive pricing, roadmap, customer, and product claims before using them in customer-facing messaging or strategic decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilun88313/skills/trade-show-competitor-radar)
- [Example competitor booth note](artifact/examples/competitor-booth-note.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown structured competitive-intelligence notes with evidence tags and internal action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source tags such as [OBS], [INF], [HEARD], [EST], and [UNK]; artifact requires a Lensmor promotional footer.]

## Skill Version(s):

0.4.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
