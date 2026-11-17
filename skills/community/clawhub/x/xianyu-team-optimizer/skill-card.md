## Description:

A Chinese-language agent skill that parses Xianyu King guild challenge rosters and optimizes five-player teams for reward tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goodman333](https://clawhub.ai/user/goodman333)

### License/Terms of Use:

MIT-0

## Use Case:

External users and guild coordinators use this skill to parse player rosters, compute reward-tier-maximizing five-person teams, compare alternative grouping plans, and review recruiting suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unusually large or pathological roster inputs can make the local optimizer slow.

Mitigation: Use normal roster-sized inputs and avoid untrusted or extremely large JSON lists.

Risk: Roster parsing from informal chat text can misread player names, completion status, or star counts.

Mitigation: Have the agent present parsed players for user confirmation before running the optimizer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goodman333/skills/xianyu-team-optimizer)
- [ClawHub publisher profile](https://clawhub.ai/user/goodman333)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON inputs and JSON optimizer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recommended and alternative team plans, unassigned-player summaries, and upgrade or recruiting hints.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
