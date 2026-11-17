## Description:

Context-aware recommendations. Learns preferences, researches options, anticipates expectations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to make context-aware recommendations by collecting preference signals, researching viable options, ranking candidates, and presenting concise recommendations with tradeoffs and confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs broad searches of stored personal context and conversation history before making recommendations.

Mitigation: Use it only where the user has consented to personal-context lookup, or run with memory access disabled until explicit confirmation is added.

Risk: The skill asks agents to remember inferred preferences after each recommendation.

Mitigation: Confirm long-term preference updates with the user and avoid storing sensitive or one-off contextual details as durable preferences.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/recommend)
- [Recommendation Categories](categories.md)
- [Where to Find User Context](sources.md)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown recommendations with preference signals, candidate shortlist, ranking rationale, tradeoffs, and confidence notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include targeted clarification questions when available context is insufficient.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
