## Description:

Turn new AI names or unstructured AI market signals into a keyword priority table, screening related generic terms for relevance, novelty, estimated demand, and momentum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyansen](https://clawhub.ai/user/zhuyansen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and product teams can use this skill to assess which generic search terms related to new AI models, products, or repositories merit a page or tool. It summarizes relevance, novelty, estimated search demand, and momentum in a prioritize, watch, or skip table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword lookups use external providers with the user's API credentials and can incur charges.

Mitigation: Review configured sources and approve the cost estimate before running paid queries.

Risk: A clean scanner result does not establish the external package's runtime safety.

Mitigation: Verify the pinned package release before running it.

## Reference(s):

- [Example configuration for new-term-radar](https://github.com/zhuyansen/new-term-radar/blob/v0.6.0/config.example.json)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown keyword priority table with concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search volume and trend readings are estimates.]

## Skill Version(s):

0.6.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
