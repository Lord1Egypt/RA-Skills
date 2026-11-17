## Description:

Use when answering structural code questions in an indexed repo - who calls this, what does this call, what breaks if I change it, what changed between two versions. Reach for it BEFORE grep whenever the question is about relationships between symbols rather than text. Triggers include "who calls", "what uses", "blast radius", "impact of changing", "callers of", "what depends on", and reviewing a diff's structural effect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer structural questions about indexed repositories, including symbol callers and callees, change impact, file relationships, and structural differences between graph snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository indexes are local, persist between refreshes, and may be stale.

Mitigation: Choose repository roots deliberately and refresh or resync the index when freshness matters.

Risk: Optional Brigade receipt export can expose or preserve repository-related evidence according to its settings.

Mitigation: Review the separately installed GraphTrail tooling and Brigade receipt-export settings before using that integration.

## Reference(s):

- [Graphtrail on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-graphtrail)
- [Publisher profile: escoffier-labs](https://clawhub.ai/user/escoffier-labs)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Concise text or Markdown describing code relationships and change impact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the indexed graph; dynamic dispatch, reflection, and metaprogrammed calls may not appear, and indexes may need refreshing.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
