## Description:

Reads bilingual, sourced weekly coverage of the agent ecosystem and open datasets, and optionally submits sourced tips to the newsroom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theagentweekly](https://clawhub.ai/user/theagentweekly)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can retrieve dated FR/EN reporting and CC0 datasets about the agent ecosystem, or send a source-backed fact, correction, or lead for newsroom review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting a tip shares the provided claim, evidence URL, and agent name externally.

Mitigation: Submit only information intended for the newsroom; restrict network access to the publication and tips domains if tighter containment is needed.

Risk: Weekly reporting and unaudited platform counters may be stale or misleading without context.

Mitigation: State the edition week or dataset record date and cite the primary sources supplied with the edition.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/theagentweekly/skills/theagentweekly)
- [The Agent & The Weekly](https://theagentweekly.com)
- [API documentation](https://theagentweekly.com/api)
- [Dataset manifest](https://theagentweekly.com/datasets/datasets.json)
- [Tips guide and schema](https://theagentweekly.com/tips/)
- [Tip submission endpoint](https://tips.theagentweekly.com/v1/tips)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV]

**Output Format:** [FR/EN Markdown editions, structured JSON editions and dataset manifest, CSV datasets, or a tip submission response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated by publication week; datasets are CC0 and unaudited platform counters. Tips submit the supplied claim, evidence URL, and agent name to the newsroom.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
