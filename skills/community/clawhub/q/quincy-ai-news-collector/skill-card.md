## Description:

Collects AI news from broad public web sources, ranks items by heat, and returns Chinese summaries with original links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather current AI product, research, business, policy, open-source, and community news, then receive a ranked Chinese Markdown digest with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse many external news, newsletter, forum, and social sites.

Mitigation: Review generated links and source domains before acting on or redistributing the digest.

Risk: The skill is designed to output Chinese summaries.

Mitigation: Adapt the output language requirements before deployment if the intended audience needs another language.

## Reference(s):

- [Recommended AI News Sources](references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/quincygunter/skills/quincy-ai-news-collector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown news digest with ranked items, short summaries, source links, and collection metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill targets 15-25 deduplicated news items and records search count, covered dimensions, and update time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
